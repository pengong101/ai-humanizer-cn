# 🛡️ 配置安全审查指南

**创建时间：** 2026-03-20 10:18  
**维护者：** 小马 🐴  
**版本：** 1.0.0

---

## 📋 概述

本指南提供 OpenClaw 配置文件的安全修改流程，防止意外修改导致系统故障。

---

## 🚀 快速开始

### 修改配置（推荐方式）

```bash
# 使用安全 wrapper（自动检查）
openclaw-config set gateway.mode local

# 或手动流程
/root/.openclaw/scripts/config-safety-check.sh  # 检查
chmod 644 /root/.openclaw/openclaw.json         # 解锁
vim /root/.openclaw/openclaw.json               # 修改
python3 -m json.tool /root/.openclaw/openclaw.json > /dev/null  # 验证
openclaw doctor --non-interactive               # 检查
chmod 444 /root/.openclaw/openclaw.json         # 锁定
```

---

## 📁 文件位置

| 文件 | 位置 | 说明 |
|------|------|------|
| **安全审查脚本** | `/root/.openclaw/scripts/config-safety-check.sh` | 8 项安全检查 |
| **配置修改 wrapper** | `/root/.openclaw/scripts/openclaw-config` | 自动检查 + 解锁/锁定 |
| **Git hook** | `/root/.openclaw/workspace/.git/hooks/pre-commit` | 提交前验证 |
| **配置审计日志** | `/root/.openclaw/logs/config-audit.jsonl` | 所有配置变更记录 |
| **备份目录** | `/root/.openclaw/config-backups/` | 历史备份 |

---

## 🔍 安全检查项目

### 1. 文件存在性
检查配置文件是否存在。

### 2. JSON 格式验证
使用 `python3 -m json.tool` 验证 JSON 格式。

### 3. 备份检查
- 检查备份数量（至少 2 个）
- 自动创建新备份

### 4. 文件大小异常检测
检测文件大小骤降 >50%（可能是误操作清空）。

### 5. OpenClaw doctor 健康检查
运行 `openclaw doctor --non-interactive`。

### 6. 支持的字段检查
检查是否包含不支持的字段。

### 7. 关键配置项检查
验证必需字段是否存在。

### 8. 文件权限检查
检查权限是否为 444 或 600。

---

## ❌ 不支持字段清单

**当前版本：** 2026.3.13

```json
❌ 禁止使用：
- agents.defaults.fallback
- agents.taskOverrides
- browser.provider
- browser.target
- browser.kasm

✅ 支持：
- agents.defaults.model.primary
- agents.defaults.models.*
- models.providers.*
- channels.*
- gateway.*
- plugins.*
- commands.*
```

---

## 📊 配置审计日志

### 查看最近审计记录

```bash
tail -5 /root/.openclaw/logs/config-audit.jsonl | python3 -m json.tool
```

### 审计字段说明

| 字段 | 说明 |
|------|------|
| `ts` | 时间戳 |
| `event` | 事件类型（config.write） |
| `argv` | 执行的命令 |
| `previousBytes` / `nextBytes` | 配置大小变化 |
| `suspicious` | 可疑操作标记 |

### suspicious 标记示例

```json
"suspicious": ["size-drop:4951->524"]
```
表示文件大小从 4951B 骤降到 524B（异常！）

---

## 🔄 完整修改流程

### 修改前

```bash
# 1. 运行安全检查
/root/.openclaw/scripts/config-safety-check.sh

# 2. 解锁配置
chmod 644 /root/.openclaw/openclaw.json
```

### 修改中

```bash
# 3. 修改配置（推荐用 openclaw config 命令）
openclaw config set gateway.mode local

# 或手动编辑
vim /root/.openclaw/openclaw.json
```

### 修改后

```bash
# 4. 验证 JSON
python3 -m json.tool /root/.openclaw/openclaw.json > /dev/null

# 5. 运行 doctor
openclaw doctor --non-interactive

# 6. 重启服务（如果需要）
docker restart xiaoma-new

# 7. 验证功能
openclaw status

# 8. 重新锁定
chmod 444 /root/.openclaw/openclaw.json
```

---

## 🚨 紧急恢复

### 配置故障恢复

```bash
# 1. 停止容器
docker stop xiaoma_new

# 2. 解锁配置
chmod 644 /root/.openclaw/openclaw.json

# 3. 恢复最新备份
LATEST=$(ls -t /root/.openclaw/config-backups/*.json | head -1)
cp "$LATEST" /root/.openclaw/openclaw.json

# 4. 验证
python3 -m json.tool /root/.openclaw/openclaw.json > /dev/null

# 5. 重启
docker start xiaoma_new

# 6. 锁定
chmod 444 /root/.openclaw/openclaw.json
```

### 验证备份

```bash
# 查看备份列表
ls -lt /root/.openclaw/config-backups/*.json | head -10

# 验证备份 JSON
python3 -m json.tool /root/.openclaw/config-backups/openclaw-20260320-094029.json > /dev/null && echo "✅ 备份有效"
```

---

## 📦 Git 提交检查

### Pre-commit Hook

自动检查：
- JSON 格式
- 文件大小（>1000 bytes）
- 不支持字段

### 绕过检查（不推荐）

```bash
git commit --no-verify -m "message"
```

---

## 📝 质量审查清单

发布技能/文档前检查：

### 代码审查
- [ ] 代码有实际功能
- [ ] 经过测试验证
- [ ] 无依赖问题
- [ ] 无敏感信息

### 文档审查
- [ ] README 完整
- [ ] 使用示例清晰
- [ ] 版本信息正确
- [ ] 许可证声明

### 发布审查
- [ ] 解决真实问题
- [ ] 有创新性
- [ ] 符合发布原则

---

## 📞 相关文档

- [MEMORY.md](./MEMORY.md) - 长期记忆（包含完整安全流程）
- [CONFIG-SAFETY-GUIDE.md](./CONFIG-SAFETY-GUIDE.md) - 本指南

---

**最后更新：** 2026-03-20 10:18  
**下次审查：** 2026-03-27
