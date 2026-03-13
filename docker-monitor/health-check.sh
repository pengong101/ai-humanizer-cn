#!/bin/bash
# Docker 容器健康检查脚本
# 功能：每 5 分钟检查容器健康状态，异常时自动触发恢复

set -e

# 配置
CONTAINER_NAME="xiaoma_new"
HEALTH_CHECK_INTERVAL=60
MAX_RESTART_COUNT=5
RESTART_COOLDOWN=300
LOG_FILE="/var/log/docker-monitor.log"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 日志函数
log() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "${timestamp} [${level}] ${message}" | tee -a "$LOG_FILE"
}

log_info() { log "INFO" "${GREEN}$1${NC}"; }
log_warn() { log "WARN" "${YELLOW}$1${NC}"; }
log_error() { log "ERROR" "${RED}$1${NC}"; }

# 检查容器状态
check_container_status() {
    local container=$1
    
    # 检查容器是否存在
    if ! docker inspect "$container" &>/dev/null; then
        log_error "❌ 容器 $container 不存在"
        return 1
    fi
    
    # 检查容器是否运行
    local running=$(docker inspect --format='{{.State.Running}}' "$container" 2>/dev/null)
    if [ "$running" != "true" ]; then
        log_error "❌ 容器 $container 未运行"
        return 1
    fi
    
    # 检查健康状态（如果有健康检查）
    local health=$(docker inspect --format='{{.State.Health.Status}}' "$container" 2>/dev/null)
    if [ "$health" = "unhealthy" ]; then
        log_warn "⚠️  容器 $container 健康检查失败"
        return 1
    fi
    
    # 检查重启次数
    local restart_count=$(docker inspect --format='{{.RestartCount}}' "$container" 2>/dev/null || echo "0")
    if [ "$restart_count" -gt "$MAX_RESTART_COUNT" ]; then
        log_warn "⚠️  容器 $container 重启次数过多：$restart_count"
        return 1
    fi
    
    log_info "✅ 容器 $container 健康 (重启次数：$restart_count)"
    return 0
}

# 检查端口监听
check_port() {
    local port=$1
    local service=$2
    
    # 使用多种方法检查端口
    if ss -tuln 2>/dev/null | grep -qE ":$port[[:space:]]" || \
       netstat -tuln 2>/dev/null | grep -qE ":$port[[:space:]]" || \
       docker ps --format '{{.Ports}}' | grep -q ":$port->"; then
        log_info "✅ 端口 $port ($service) 正常监听"
        return 0
    else
        log_error "❌ 端口 $port ($service) 未监听"
        return 1
    fi
}

# 检查容器资源使用
check_resources() {
    local container=$1
    
    # 获取内存使用率
    local mem_usage=$(docker stats --no-stream --format "{{.MemPerc}}" "$container" 2>/dev/null | tr -d '%')
    if [ -n "$mem_usage" ]; then
        if (( $(echo "$mem_usage > 80" | bc -l 2>/dev/null || echo 0) )); then
            log_warn "⚠️  容器 $container 内存使用率过高：${mem_usage}%"
            return 1
        fi
        log_info "✅ 容器 $container 内存使用率：${mem_usage}%"
    fi
    
    return 0
}

# 触发恢复
trigger_recovery() {
    local container=$1
    local reason=$2
    
    log_warn "🔄 触发容器恢复：$container (原因：$reason)"
    
    # 调用恢复脚本
    if [ -x "/root/.openclaw/workspace/docker-monitor/auto-recover.sh" ]; then
        /root/.openclaw/workspace/docker-monitor/auto-recover.sh "$container" "$reason"
    else
        log_error "❌ 恢复脚本不存在或不可执行"
        return 1
    fi
}

# 主函数
main() {
    log_info "=========================================="
    log_info "Docker 健康检查开始"
    log_info "=========================================="
    
    local health_issues=0
    
    # 检查 OpenClaw 容器
    if ! check_container_status "$CONTAINER_NAME"; then
        health_issues=$((health_issues + 1))
        trigger_recovery "$CONTAINER_NAME" "container_unhealthy"
    fi
    
    # 检查资源使用
    if ! check_resources "$CONTAINER_NAME"; then
        health_issues=$((health_issues + 1))
    fi
    
    # 检查关键端口
    check_port 8082 "OpenClaw" || health_issues=$((health_issues + 1))
    check_port 8081 "SearXNG" || health_issues=$((health_issues + 1))
    check_port 7890 "Clash" || health_issues=$((health_issues + 1))
    
    # 总结
    log_info "=========================================="
    if [ $health_issues -eq 0 ]; then
        log_info "✅ 健康检查通过，无问题"
    else
        log_warn "⚠️  发现 $health_issues 个问题，已处理"
    fi
    log_info "=========================================="
}

main "$@"
