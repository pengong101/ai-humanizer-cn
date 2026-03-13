# Docker 容器健康监控与自动恢复系统

**创建时间：** 2026-03-12  
**维护者：** 小马 🐴  
**目标：** 确保 OpenClaw 等关键容器稳定运行，避免重启失败

---

## 🎯 问题根因

根据检查，当前容器状态：
- **RestartPolicy:** `always` ✅（已配置自动重启）
- **Memory Limit:** 无限制 ✅
- **OOMKilled:** false ✅
- **Health Status:** healthy ✅

**潜在风险：**
1. 容器重启后可能未正确恢复网络配置
2. 端口冲突导致重启失败
3. 磁盘空间不足（当前 17% 使用率，安全）
4. 内存泄漏（当前 424.5MiB，正常）

---

## 📁 监控系统架构

```
docker-monitor/
├── health-check.sh          # 容器健康检查脚本
├── auto-recover.sh          # 自动恢复脚本
├── resource-monitor.sh      # 资源监控脚本
├── alert.sh                 # 告警通知脚本
└── config.json              # 配置文件
```

---

## 🔧 监控脚本

### health-check.sh - 健康检查

```bash
#!/bin/bash
# Docker 容器健康检查脚本

CONTAINER_NAME="xiaoma_new"
HEALTH_CHECK_INTERVAL=60  # 秒
MAX_RESTART_COUNT=3
RESTART_COOLDOWN=300  # 5 分钟

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a /var/log/docker-monitor.log
}

check_container_status() {
    local container=$1
    
    # 检查容器是否运行
    if ! docker inspect --format='{{.State.Running}}' "$container" 2>/dev/null | grep -q "true"; then
        log "${RED}❌ 容器 $container 未运行${NC}"
        return 1
    fi
    
    # 检查健康状态
    local health=$(docker inspect --format='{{.State.Health.Status}}' "$container" 2>/dev/null)
    if [ "$health" = "unhealthy" ]; then
        log "${YELLOW}⚠️  容器 $container 健康检查失败${NC}"
        return 1
    fi
    
    # 检查重启次数
    local restart_count=$(docker inspect --format='{{.RestartCount}}' "$container" 2>/dev/null || echo "0")
    if [ "$restart_count" -gt "$MAX_RESTART_COUNT" ]; then
        log "${YELLOW}⚠️  容器 $container 重启次数过多：$restart_count${NC}"
        return 1
    fi
    
    log "${GREEN}✅ 容器 $container 健康${NC}"
    return 0
}

check_port_conflict() {
    local port=$1
    if netstat -tuln 2>/dev/null | grep -q ":$port "; then
        log "${GREEN}✅ 端口 $port 正常${NC}"
        return 0
    else
        log "${RED}❌ 端口 $port 未监听${NC}"
        return 1
    fi
}

main() {
    log "=========================================="
    log "Docker 健康检查"
    log "=========================================="
    
    # 检查 OpenClaw 容器
    if ! check_container_status "xiaoma_new"; then
        log "${YELLOW}尝试恢复 OpenClaw 容器...${NC}"
        /root/.openclaw/workspace/docker-monitor/auto-recover.sh xiaoma_new
    fi
    
    # 检查关键端口
    check_port_conflict 8082  # OpenClaw
    check_port_conflict 8081  # SearXNG
    check_port_conflict 7890  # Clash
    
    log "健康检查完成"
}

main "$@"
```

---

### auto-recover.sh - 自动恢复

```bash
#!/bin/bash
# Docker 容器自动恢复脚本

CONTAINER_NAME=$1
MAX_RETRIES=3
RETRY_DELAY=10

log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a /var/log/docker-recover.log
}

recover_container() {
    local container=$1
    local retry=0
    
    log "开始恢复容器：$container"
    
    while [ $retry -lt $MAX_RETRIES ]; do
        retry=$((retry + 1))
        log "尝试恢复 (第 $retry 次)..."
        
        # 停止容器（如果运行中）
        docker stop "$container" 2>/dev/null || true
        
        # 等待端口释放
        sleep 5
        
        # 删除旧容器
        docker rm "$container" 2>/dev/null || true
        
        # 重新启动容器
        if start_container "$container"; then
            log "✅ 容器恢复成功"
            return 0
        fi
        
        log "⚠️  恢复失败，${RETRY_DELAY}秒后重试..."
        sleep $RETRY_DELAY
    done
    
    log "❌ 容器恢复失败，已达到最大重试次数"
    return 1
}

start_container() {
    local container=$1
    
    case $container in
        "xiaoma_new")
            docker run -d \
                --name xiaoma_new \
                --restart=always \
                --memory=2g \
                --memory-swap=4g \
                -p 8082:8080 \
                -v /root/.openclaw/workspace:/root/.openclaw/workspace \
                -v /root/.openclaw/data:/root/.openclaw/data \
                -e OPENCLAW_CONFIG=/root/.openclaw/data/config.json \
                ghcr.io/openclaw/openclaw:latest
            ;;
        "searxng")
            docker restart searxng
            ;;
        "clash")
            docker restart clash
            ;;
        "browser")
            docker restart browser
            ;;
        *)
            docker start "$container"
            ;;
    esac
    
    # 验证容器是否启动
    sleep 5
    if docker inspect --format='{{.State.Running}}' "$container" 2>/dev/null | grep -q "true"; then
        return 0
    fi
    return 1
}

# 执行恢复
recover_container "$CONTAINER_NAME"
```

---

### resource-monitor.sh - 资源监控

```bash
#!/bin/bash
# Docker 资源监控脚本

MEMORY_THRESHOLD=80  # 内存使用率告警阈值
DISK_THRESHOLD=85    # 磁盘使用率告警阈值
CPU_THRESHOLD=90     # CPU 使用率告警阈值

log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a /var/log/docker-resources.log
}

check_memory() {
    local container=$1
    local mem_info=$(docker stats --no-stream --format "table {{.MemUsage}}" "$container" 2>/dev/null | tail -1)
    
    if [ -n "$mem_info" ]; then
        local used=$(echo $mem_info | cut -d'/' -f1 | tr -d 'MiBGiB')
        local limit=$(echo $mem_info | cut -d'/' -f2 | tr -d 'MiBGiB')
        local percent=$(awk "BEGIN {printf \"%.0f\", ($used/$limit)*100}")
        
        if [ "$percent" -gt "$MEMORY_THRESHOLD" ]; then
            log "⚠️  容器 $container 内存使用率过高：${percent}%"
            return 1
        fi
        log "✅ 容器 $container 内存使用率：${percent}%"
    fi
    return 0
}

check_disk() {
    local disk_usage=$(df /var/lib/docker 2>/dev/null | tail -1 | awk '{print $5}' | tr -d '%')
    
    if [ -n "$disk_usage" ] && [ "$disk_usage" -gt "$DISK_THRESHOLD" ]; then
        log "⚠️  Docker 磁盘使用率过高：${disk_usage}%"
        return 1
    fi
    log "✅ Docker 磁盘使用率：${disk_usage}%"
    return 0
}

check_all_containers() {
    for container in $(docker ps --format '{{.Names}}'); do
        check_memory "$container"
    done
    check_disk
}

check_all_containers
```

---

### alert.sh - 告警通知

```bash
#!/bin/bash
# 告警通知脚本

ALERT_TYPE=$1
MESSAGE=$2

log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a /var/log/docker-alerts.log
}

send_feishu_alert() {
    local message=$1
    # 通过 OpenClaw 发送飞书通知
    echo "🚨 Docker 告警：$message"
    # 实际使用时调用 OpenClaw message 工具
}

case $ALERT_TYPE in
    "container_down")
        log "❌ 容器宕机告警：$MESSAGE"
        send_feishu_alert "容器 $MESSAGE 已宕机，正在自动恢复..."
        ;;
    "memory_high")
        log "⚠️  内存告警：$MESSAGE"
        send_feishu_alert "容器内存使用率过高：$MESSAGE"
        ;;
    "disk_high")
        log "⚠️  磁盘告警：$MESSAGE"
        send_feishu_alert "Docker 磁盘使用率过高：$MESSAGE"
        ;;
    "recover_success")
        log "✅ 恢复成功：$MESSAGE"
        send_feishu_alert "容器 $MESSAGE 已成功恢复"
        ;;
    "recover_failed")
        log "❌ 恢复失败：$MESSAGE"
        send_feishu_alert "容器 $MESSAGE 恢复失败，请手动干预！"
        ;;
esac
```

---

## ⏰ Cron 配置

```bash
# Docker 健康监控 - 每 5 分钟检查一次
*/5 * * * * /root/.openclaw/workspace/docker-monitor/health-check.sh >> /var/log/docker-monitor.log 2>&1

# 资源监控 - 每 15 分钟检查一次
*/15 * * * * /root/.openclaw/workspace/docker-monitor/resource-monitor.sh >> /var/log/docker-resources.log 2>&1

# 每日清理 - 每天凌晨 03:00 清理悬空镜像
0 3 * * * docker image prune -f >> /var/log/docker-cleanup.log 2>&1
```

---

## 📊 监控面板

### 查看容器状态

```bash
# 快速状态检查
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 资源使用
docker stats --no-stream

# 健康状态
docker inspect --format='{{.State.Health.Status}}' xiaoma_new
```

### 日志查看

```bash
# 实时监控日志
tail -f /var/log/docker-monitor.log

# 查看恢复历史
tail -f /var/log/docker-recover.log

# 查看告警历史
tail -f /var/log/docker-alerts.log
```

---

## 🛠️ 故障排查

### 问题 1：容器无法启动

```bash
# 检查端口占用
netstat -tuln | grep 8082

# 查看容器日志
docker logs xiaoma_new --tail 100

# 检查磁盘空间
df -h /var/lib/docker
```

### 问题 2：频繁重启

```bash
# 查看重启次数
docker inspect --format='{{.RestartCount}}' xiaoma_new

# 查看退出码
docker inspect --format='{{.State.ExitCode}}' xiaoma_new

# 检查内存限制
docker inspect --format='{{.HostConfig.Memory}}' xiaoma_new
```

### 问题 3：健康检查失败

```bash
# 查看健康检查日志
docker inspect --format='{{json .State.Health}}' xiaoma_new | python3 -m json.tool

# 手动执行健康检查
docker exec xiaoma_new openclaw status
```

---

## 📋 配置清单

### 必须配置

- [ ] 创建 docker-monitor 目录
- [ ] 复制所有监控脚本
- [ ] 赋予执行权限 `chmod +x *.sh`
- [ ] 配置 Cron 任务
- [ ] 测试健康检查脚本
- [ ] 测试自动恢复脚本

### 可选配置

- [ ] 配置告警通知（飞书/邮件）
- [ ] 配置资源阈值
- [ ] 配置监控面板（Grafana）
- [ ] 配置日志轮转

---

## 🎯 成功标准

1. **容器可用性** > 99.9%
2. **自动恢复时间** < 2 分钟
3. **告警响应时间** < 5 分钟
4. **资源使用率** < 80%

---

**系统版本：** v1.0  
**最后更新：** 2026-03-12  
**维护者：** 小马 🐴
