# 🌐 Clash 自主控制功能

**版本：** v1.0  
**功能：** 自动检测网络，智能开关 Clash  
**状态：** ✅ 部署完成

---

## 🎯 功能说明

### 核心功能

- ✅ **自动检测** - 检测国内网络和代理状态
- ✅ **智能决策** - 根据网络状态自动开关 Clash
- ✅ **故障恢复** - 网络异常时自动重启 Clash
- ✅ **状态监控** - 实时显示网络和 Clash 状态

---

## 🚀 使用方式

### 智能模式（推荐）

```bash
# 自动检测并决策
./clash-auto-control.sh smart
```

**工作流程：**
```
检测国内网络 + 代理状态
    ↓
决策逻辑：
  - 代理正常 → 保持 Clash 运行
  - 代理异常 + 国内正常 → 重启 Clash
  - 都异常 → 重启 Clash，仍异常则停止
    ↓
记录日志
```

---

### 手动模式

```bash
# 强制启动
./clash-auto-control.sh start

# 强制停止
./clash-auto-control.sh stop

# 重启
./clash-auto-control.sh restart

# 查看状态
./clash-auto-control.sh status
```

---

## 📊 决策逻辑

### 状态矩阵

| 国内网络 | 代理 | Clash 状态 | 决策 |
|---------|------|-----------|------|
| ✅ | ✅ | 🟢 | 保持运行 |
| ✅ | ✅ | 🔴 | 启动 Clash |
| ✅ | ❌ | 🟢 | 重启 Clash |
| ✅ | ❌ | 🔴 | 启动 Clash |
| ❌ | ✅ | 🟢 | 保持运行 |
| ❌ | ❌ | 🟢 | 重启→停止 |
| ❌ | ❌ | 🔴 | 启动→测试 |

---

## 📋 日志示例

### 代理正常时

```
[2026-03-11 14:10:00] ========================================
[2026-03-11 14:10:00] 🤖 Clash 智能决策开始
[2026-03-11 14:10:00] ========================================
[2026-03-11 14:10:00] 🔍 检测国内网络...
[2026-03-11 14:10:01] ✅ 国内网络正常
[2026-03-11 14:10:01] 🔍 检测代理可用性...
[2026-03-11 14:10:02] ✅ 代理可用
[2026-03-11 14:10:02] 📊 网络状态：国内=True, 代理=True
[2026-03-11 14:10:02] ✅ 代理正常，保持 Clash 运行
[2026-03-11 14:10:02] ========================================
[2026-03-11 14:10:02] ✅ Clash 智能决策完成
[2026-03-11 14:10:02] ========================================
```

---

### 代理异常时

```
[2026-03-11 14:10:00] 🔍 检测国内网络...
[2026-03-11 14:10:01] ✅ 国内网络正常
[2026-03-11 14:10:01] 🔍 检测代理可用性...
[2026-03-11 14:10:06] ❌ 代理不可用
[2026-03-11 14:10:06] 📊 网络状态：国内=True, 代理=False
[2026-03-11 14:10:06] ⚠️  代理不可用但国内网络正常
[2026-03-11 14:10:06] 💡 尝试重启 Clash 恢复代理...
[2026-03-11 14:10:06] 🔄 重启 Clash 容器...
[2026-03-11 14:10:10] ✅ Clash 已重启
[2026-03-11 14:10:15] ✅ Clash 重启后代理恢复
```

---

## ⏰ 自动调度

### Cron 配置（每 30 分钟检测）

```bash
# 编辑 crontab
crontab -e

# 添加（每 30 分钟检测）
*/30 * * * * /root/.openclaw/workspace/clash-auto-control.sh smart >> /var/log/clash-auto-control.log 2>&1

# 或（每小时检测）
0 * * * * /root/.openclaw/workspace/clash-auto-control.sh smart >> /var/log/clash-auto-control.log 2>&1

# NAS 启动时检测
@reboot /root/.openclaw/workspace/clash-auto-control.sh smart >> /var/log/clash-auto-control.log 2>&1
```

---

## 🔧 集成 SearXNG

### 联合工作流

```bash
#!/bin/bash
# 网络优化 + SearXNG 自适应

# 1. 确保 Clash 运行
/root/.openclaw/workspace/clash-auto-control.sh smart

# 2. SearXNG 自适应代理
/root/.openclaw/workspace/searxng-auto-proxy.sh

# 3. 测试 Google 搜索
curl --proxy http://192.168.1.122:7890 \
  "http://192.168.1.122:8081/search?q=test&engines=google&format=json"
```

---

## 📊 状态查看

### 快速状态

```bash
./clash-auto-control.sh status
```

**输出示例：**
```
================================
📊 Clash 状态
================================
容器状态：🟢 运行中
代理状态：🟢 可用
国内网络：🟢 正常
================================
```

---

### 详细日志

```bash
# 实时查看日志
tail -f /var/log/clash-auto-control.log

# 查看最近 50 行
tail -50 /var/log/clash-auto-control.log

# 搜索错误
grep "❌" /var/log/clash-auto-control.log
```

---

## 🎯 使用场景

### 场景 1：网络波动

**问题：** Clash 规则过期导致代理失效  
**解决：** 自动检测并重启 Clash

---

### 场景 2：NAS 重启

**问题：** NAS 重启后 Clash 未自动启动  
**解决：** Cron @reboot 自动启动

---

### 场景 3：SearXNG 搜索失败

**问题：** Google 搜索超时  
**解决：** 
```bash
# 先确保 Clash 运行
./clash-auto-control.sh smart

# 再测试搜索
curl --proxy http://192.168.1.122:7890 \
  "http://localhost:8081/search?q=test&engines=google"
```

---

## 📈 性能指标

| 指标 | 目标 | 实际 |
|------|------|------|
| 检测时间 | <10 秒 | ~5 秒 ✅ |
| 启动时间 | <10 秒 | ~5 秒 ✅ |
| 重启时间 | <15 秒 | ~10 秒 ✅ |
| 决策准确率 | >95% | 待统计 |

---

## 🛠️ 故障排查

### 问题 1：Clash 无法启动

**检查：**
```bash
# 容器状态
docker ps -a | grep clash

# 容器日志
docker logs clash --tail 50

# 配置文件
docker exec clash cat /root/config.yaml
```

**解决：**
```bash
# 重新拉取镜像
docker pull metacubex/mihomo:latest

# 重新创建容器
docker rm clash
docker run -d --name clash ...（原命令）
```

---

### 问题 2：代理检测失败

**检查：**
```bash
# 手动测试代理
curl --proxy http://192.168.1.122:7890 https://www.google.com

# 检查端口
netstat -tlnp | grep 7890
```

**解决：**
```bash
# 重启 Clash
./clash-auto-control.sh restart

# 检查 Clash 配置
docker exec clash /mihomo -t -f /root/config.yaml
```

---

### 问题 3：脚本执行失败

**检查：**
```bash
# 脚本权限
ls -la /root/.openclaw/workspace/clash-auto-control.sh

# Docker 权限
docker ps
```

**解决：**
```bash
# 添加执行权限
chmod +x /root/.openclaw/workspace/clash-auto-control.sh

# 检查 Docker
systemctl status docker
```

---

## 📞 相关文档

- [SearXNG 自适应代理](SEARXNG-PROXY-AUTO-DETECT.md)
- [Clash 配置指南](CLASH-CONFIG-GUIDE.md)
- [网络优化最佳实践](NETWORK-OPTIMIZATION.md)

---

**开发者：** 小马 🐴 + CEO 智能体（小马 🐴）  
**版本：** v1.0  
**发布日期：** 2026-03-11  
**许可：** MIT
