# OpenClaw 自动化维护

## 📦 自动备份功能

### 配置说明
- **执行时间**: 每天凌晨 3:00 (Asia/Shanghai)
- **备份内容**:
  - `openclaw.json` - 主配置文件
  - `agents/` - Agent 配置
  - `cron/` - 定时任务配置
  - `workspace/` - 工作区文件
- **保留策略**: 自动保留最近 7 天的备份
- **备份位置**: `/root/.openclaw/backups/`

### 手动备份
```bash
/root/.openclaw/scripts/backup.sh
```

### 恢复备份
```bash
# 查看备份列表
ls -lh /root/.openclaw/backups/

# 恢复指定备份
tar -xzf /root/.openclaw/backups/openclaw_backup_20260310_030000.tar.gz -C /
```

---

## 🔄 自动更新检查

### 配置说明
- **检查时间**: 每周一上午 9:00 (Asia/Shanghai)
- **更新渠道**: 跟随当前配置的渠道 (stable/beta/dev)
- **更新方式**: 仅检查，不自动执行（需要用户确认）

### 手动检查更新
```bash
# 查看更新状态
openclaw update status

# 执行更新
openclaw update

# 切换到特定渠道
openclaw update --channel stable  # 或 beta / dev
```

### 更新渠道说明
| 渠道 | 说明 | 推荐 |
|------|------|------|
| `stable` | 稳定版，经过充分测试 | ✅ 生产环境 |
| `beta` | 测试版，新功能预览 | ⚠️ 测试环境 |
| `dev` | 开发版，最新代码 | ❌ 仅开发者 |

---

## ⚙️ Cron 任务管理

### 查看任务
```bash
openclaw cron list
```

### 查看任务历史
```bash
openclaw cron runs --id <job-id>
```

### 禁用/启用任务
```bash
# 禁用
openclaw cron update --id <job-id> --enabled false

# 启用
openclaw cron update --id <job-id> --enabled true
```

### 删除任务
```bash
openclaw cron remove --id <job-id>
```

---

## 📊 当前配置的任务

| 任务名称 | Cron 表达式 | 说明 |
|----------|-------------|------|
| 每日配置备份 | `0 3 * * *` | 每天凌晨 3 点备份 |
| 每周更新检查 | `0 9 * * 1` | 每周一 9 点检查更新 |

---

## 🛡️ 最佳实践

1. **定期验证备份**: 每月至少手动恢复测试一次
2. **异地备份**: 重要数据建议额外备份到云存储
3. **更新前备份**: 执行重大更新前手动备份一次
4. **监控日志**: 定期检查 `/root/.openclaw/logs/` 查看任务执行日志

---

**最后更新**: 2026-03-10
