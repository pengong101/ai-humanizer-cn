# 技能每日迭代 Cron 配置

**配置时间：** 2026-03-12  
**维护者：** 小马 🐴

---

## ⏰ Cron 任务配置

### 每日迭代任务

**执行时间：** 每日 08:00（工作日）  
**任务内容：** 自动迭代更新技能

```bash
# 技能每日迭代 - 工作日 08:00
0 8 * * 1-5 /root/.openclaw/workspace/daily-iterate.sh radar-daily-report patch >> /var/log/skill-iteration.log 2>&1
0 8 * * 1-5 /root/.openclaw/workspace/daily-iterate.sh ai-humanizer-cn patch >> /var/log/skill-iteration.log 2>&1

# GitHub 同步 - 工作日 08:30
30 8 * * 1-5 /root/.openclaw/workspace/sync-github.sh >> /var/log/skill-iteration.log 2>&1
```

### 安装 Cron 任务

```bash
# 编辑 crontab
crontab -e

# 添加上述任务
```

### 验证 Cron 状态

```bash
# 查看 Cron 服务状态
systemctl status cron

# 查看已配置的任务
crontab -l

# 查看 Cron 日志
tail -f /var/log/skill-iteration.log
```

---

## 📊 任务说明

### daily-iterate.sh

**功能：** 执行技能迭代更新

**参数：**
- `skill-name`: 技能名称（radar-daily-report 或 ai-humanizer-cn）
- `version-type`: 版本类型（patch/minor/major，默认 patch）

**执行流程：**
1. 获取当前版本号
2. 递增版本号（patch +1）
3. 更新 SKILL.md 版本号
4. 生成 RELEASE 文档
5. 更新 CHANGELOG
6. Git 提交

**输出：** `/var/log/skill-iteration.log`

---

### sync-github.sh

**功能：** 同步到 GitHub

**参数：**
- `skill-name`: （可选）指定技能，不传则同步所有

**执行流程：**
1. 检查 Git 配置
2. 推送代码到 GitHub
3. 创建 GitHub Release
4. 验证发布状态

**输出：** `/var/log/skill-iteration.log`

---

## 🔔 通知机制

### 完成通知

每日迭代完成后，自动发送通知：

```bash
# 在 sync-github.sh 末尾添加
echo "✅ 技能迭代完成 ($(date))" | message send --channel feishu --message "技能每日迭代完成"
```

### 错误通知

如果任务失败，发送告警：

```bash
# 在脚本中添加错误处理
if [ $? -ne 0 ]; then
    echo "❌ 技能迭代失败 ($(date))" | message send --channel feishu --message "技能迭代失败，请检查日志"
fi
```

---

## 📈 监控与日志

### 日志位置

- **迭代日志：** `/var/log/skill-iteration.log`
- **Git 日志：** `/root/.openclaw/workspace/.git/logs/`
- **Cron 日志：** `/var/log/syslog` (grep CRON)

### 日志轮转

```bash
# /etc/logrotate.d/skill-iteration
/var/log/skill-iteration.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
}
```

---

## 🛠️ 手动执行

### 测试迭代

```bash
# 手动执行迭代（测试用）
./daily-iterate.sh radar-daily-report patch
./daily-iterate.sh ai-humanizer-cn patch
```

### 测试同步

```bash
# 手动同步到 GitHub
./sync-github.sh
```

### 查看状态

```bash
# 查看最新版本
ls -lt skills/*/RELEASE-*.md | head -10

# 查看 Git 状态
cd /root/.openclaw/workspace && git status

# 查看最近提交
cd /root/.openclaw/workspace && git log --oneline -10
```

---

## 📋 检查清单

### 每日检查

- [ ] Cron 任务正常执行
- [ ] 日志无错误
- [ ] GitHub Release 已创建
- [ ] 版本号正确递增
- [ ] 文档已更新

### 每周检查

- [ ] 日志文件大小正常
- [ ] Git 仓库大小正常
- [ ] 用户反馈收集
- [ ] 迭代计划调整

---

## 🎯 成功标准

1. **准时执行：** 每日 08:00 自动执行
2. **无错误：** 日志中无 ERROR 级别错误
3. **版本递增：** 版本号每日 +1
4. **GitHub 同步：** 代码和 Release 都同步
5. **文档完整：** RELEASE + CHANGELOG 都更新

---

**配置版本：** v1.0  
**最后更新：** 2026-03-12
