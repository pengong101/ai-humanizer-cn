# Docker 监控 Cron 配置

**配置时间：** 2026-03-12  
**维护者：** 小马 🐴

---

## ⏰ Cron 任务配置

### 健康监控任务

```bash
# Docker 健康检查 - 每 5 分钟执行一次
*/5 * * * * /root/.openclaw/workspace/docker-monitor/health-check.sh >> /var/log/docker-monitor.log 2>&1

# Docker 资源监控 - 每 15 分钟执行一次
*/15 * * * * /root/.openclaw/workspace/docker-monitor/resource-monitor.sh >> /var/log/docker-resources.log 2>&1

# Docker 清理悬空镜像 - 每天凌晨 03:00 执行
0 3 * * * docker image prune -f >> /var/log/docker-cleanup.log 2>&1

# Docker 系统日志轮转 - 每周日凌晨 04:00
0 4 * * 0 find /var/log -name "docker-*.log" -mtime +7 -delete
```

---

## 📋 安装步骤

### 1. 编辑 Crontab

```bash
crontab -e
```

### 2. 添加任务

将上述 Cron 任务添加到 crontab 文件中。

### 3. 验证配置

```bash
# 查看已配置的 Cron 任务
crontab -l

# 查看 Cron 服务状态
systemctl status cron  # systemd 系统
# 或
service cron status    # init 系统
```

### 4. 查看 Cron 日志

```bash
# 实时监控 Cron 执行
tail -f /var/log/syslog | grep CRON

# 或查看专用日志
tail -f /var/log/cron.log
```

---

## 🔍 验证监控

### 手动执行测试

```bash
# 测试健康检查
/root/.openclaw/workspace/docker-monitor/health-check.sh

# 测试资源监控
/root/.openclaw/workspace/docker-monitor/resource-monitor.sh

# 测试自动恢复（仅测试，不实际执行）
/root/.openclaw/workspace/docker-monitor/auto-recover.sh xiaoma_new test
```

### 查看监控日志

```bash
# 健康检查日志
tail -f /var/log/docker-monitor.log

# 资源监控日志
tail -f /var/log/docker-resources.log

# 恢复日志
tail -f /var/log/docker-recover.log

# 清理日志
tail -f /var/log/docker-cleanup.log
```

---

## 📊 日志位置

| 日志文件 | 说明 | 轮转周期 |
|----------|------|----------|
| `/var/log/docker-monitor.log` | 健康检查日志 | 7 天 |
| `/var/log/docker-resources.log` | 资源监控日志 | 7 天 |
| `/var/log/docker-recover.log` | 恢复操作日志 | 30 天 |
| `/var/log/docker-cleanup.log` | 清理操作日志 | 7 天 |
| `/var/log/cron.log` | Cron 执行日志 | 系统默认 |

---

## 🛠️ 故障排查

### Cron 未执行

1. **检查 Cron 服务状态**
   ```bash
   systemctl status cron
   ```

2. **检查 Cron 日志**
   ```bash
   grep CRON /var/log/syslog | tail -20
   ```

3. **验证脚本权限**
   ```bash
   ls -la /root/.openclaw/workspace/docker-monitor/*.sh
   # 确保有执行权限：-rwxr-xr-x
   ```

4. **测试脚本执行**
   ```bash
   bash -x /root/.openclaw/workspace/docker-monitor/health-check.sh
   ```

### 日志文件过大

```bash
# 手动清理旧日志
find /var/log -name "docker-*.log" -mtime +7 -delete

# 配置日志轮转
cat > /etc/logrotate.d/docker-monitor << EOF
/var/log/docker-*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
EOF
```

---

## 🎯 监控指标

### 关键指标

| 指标 | 阈值 | 告警级别 |
|------|------|----------|
| 容器状态 | running | 严重 |
| 健康状态 | healthy | 警告 |
| 内存使用率 | < 80% | 警告 |
| CPU 使用率 | < 90% | 警告 |
| 磁盘使用率 | < 85% | 警告 |
| 重启次数 | < 5 次/小时 | 警告 |

### 响应时间

| 操作 | 目标时间 |
|------|----------|
| 健康检查间隔 | 5 分钟 |
| 故障检测时间 | < 5 分钟 |
| 自动恢复时间 | < 2 分钟 |
| 告警通知时间 | < 1 分钟 |

---

## 📞 告警配置

### 告警类型

- `container_down` - 容器宕机
- `memory_high` - 内存过高
- `disk_high` - 磁盘过高
- `recover_success` - 恢复成功
- `recover_failed` - 恢复失败

### 通知渠道

当前配置：飞书（通过 OpenClaw）

未来可扩展：
- 邮件通知
- 短信通知
- Webhook 通知

---

**配置版本：** v1.0  
**最后更新：** 2026-03-12
