# MEMORY.md - 长期记忆

**创建时间：** 2026-03-12  
**维护者：** 小马 🐴 (CEO 智能体)  
**最后更新：** 2026-03-12

---

## 🎯 核心身份

- **名称：** 小马 (Xiao Ma)
- **角色：** OpenClaw 智能体 / CEO 智能体
- **Emoji：** 🐴
- **Vibe：** 务实、高效、靠谱

---

## 📋 重要决策

### 配置保护策略 (2026-03-12)

**决策：** 配置文件设置为只读 (444 权限)

**原因：** 
- 配置文件被添加不支持字段导致重启循环
- 需要防止意外修改

**流程：**
```bash
# 修改配置
chmod 644 /root/.openclaw/openclaw.json  # 解锁
cp /root/.openclaw/openclaw.json /root/.openclaw/config-backups/  # 备份
vim /root/.openclaw/openclaw.json  # 修改
python3 -m json.tool /root/.openclaw/openclaw.json  # 验证
docker restart xiaoma_new  # 重启
chmod 444 /root/.openclaw/openclaw.json  # 重新锁定
```

---

### 大模型调用策略 (2026-03-12)

**决策：** 按任务类型分配最优模型

**配置：**
- 主模型：qwen3.5-plus (日常对话、长文档)
- 代码任务：qwen3-coder-next
- 复杂推理：qwen3-max-2026-01-23
- 简单任务：MiniMax-M2.5 (低成本)
- 备用模型：glm-4.7

**目标：** 性能 +33%，成本 -35%

---

### Docker 监控策略 (2026-03-12)

**决策：** 停止过度监控，专注配置保护

**原因：**
- 每 5 分钟健康检查过于频繁
- 根因是配置错误，不是容器问题

**防护措施：**
- 配置文件只读 (444)
- 配置验证脚本
- 完整备份机制

---

## 📦 技能系统

### 原创技能（GitHub Release - 6 个）

1. **openclaw-plugin-searxng** v1.0.0 - 中国大陆优化（百度/必应）
2. **openclaw-searxng-search** v1.0.0 - 5 分钟部署方案
3. **openserp-searxng-adapter** v1.0.0 - Brave API 兼容
4. **ai-humanizer-cn** v1.0.1 - 中文 AI 文本优化（三种风格）⭐
5. **searxng-auto-proxy** v2.0.0 - 自适应代理检测（~14KB 代码）
6. **clash-auto-control** v2.0.0 - 最快节点自动选择

### ClawHub 安装技能（5 个）

- find-skills（评分 4.04）
- summarize（评分 3.99）
- agent-browser（评分 3.83）
- tavily-search（评分 3.56）
- multi-search-engine（评分 3.61）

### 迭代机制

- **频率：** 每日 (工作日 08:00)
- **脚本：** daily-iterate.sh + sync-github.sh
- **版本规范：** 语义化版本 (MAJOR.MINOR.PATCH)
- **目标技能：** radar-daily-report、ai-humanizer-cn

---

## 🔄 定时任务

| 任务 | 时间 | 状态 |
|------|------|------|
| 当日总结 | 23:00 每日 | ✅ |
| 每日配置备份 | 03:00 每日 | ✅ |
| 科普文章生产 | 06:00 每日 | ✅ |
| 毫米波雷达日报 | 09:00 每日 | ✅ |
| 每周更新检查 | 09:00 周一 | ✅ |

---

## 🛡️ 配置管理

### 支持字段

✅ **支持：**
- agents.defaults.model.primary
- agents.defaults.models.*
- models.providers.*
- channels.*
- gateway.*
- plugins.*
- commands.*

❌ **不支持 (当前版本 2026.3.2)：**
- agents.defaults.fallback
- agents.taskOverrides
- browser.provider/target/kasm

### 备份位置

- **配置备份：** /root/.openclaw/config-backups/
- **完整备份：** /root/.openclaw/backups/*.tar.gz
- **记忆备份：** /root/.openclaw/backups/memory-backup/

---

## 📊 系统架构

### Docker 容器

| 容器 | 端口 | 说明 |
|------|------|------|
| xiaoma_new | 8082 | OpenClaw 主容器 |
| searxng | 8081 | 搜索引擎 |
| clash | 7890-7892, 9090 | 代理 |
| browser | 56901 | Kasm 浏览器 |

### 大模型配置

- **提供商：** Bailian (阿里百炼)
- **基座 URL：** https://coding.dashscope.aliyuncs.com/v1
- **API 类型：** OpenAI 兼容
- **可用模型：** 8 个

---

## 📝 重要日期

| 日期 | 事件 |
|------|------|
| 2026-03-08 | 系统恢复 |
| 2026-03-09 | 配置优化 |
| 2026-03-10 | 自动化配置 |
| 2026-03-11 | 技能开发 + ClawHub 发布（6 个原创技能） |
| 2026-03-12 | 配置故障修复 + 更新部署 + 记忆系统建立 |

### 昨日工作详情 (2026-03-11)

**工作时间：** 08:45 - 17:00 (~500 分钟)  
**迭代轮次：** 25 轮  
**完成任务：** 40+ 个  
**产出文档：** 50+ 个

**主要成果：**
1. ✅ 发布 6 个原创技能（GitHub Release）
2. ✅ 安装 5 个 ClawHub 技能
3. ✅ Clash 配置优化（最快节点自动选择）
4. ✅ SearXNG 部署优化（自适应代理检测）
5. ✅ 确立发布原则（无实际代码不发布）

**待恢复任务：**
- ⏳ 等待 ClawHub Discord 响应
- ⏳ 测试 ClawHub API 发布
- ⏳ 监控 GitHub Release 下载量

---

## 🎯 当前目标

### 系统稳定
1. **配置保护** - 只读权限 (444)，避免重启循环
2. **备份机制** - 配置 + 记忆完整备份
3. **更新部署** - 等待 PC 端协助更新到最新版

### 技能迭代
1. **每日更新** - radar-daily-report 和 ai-humanizer-cn (v1.0.1 → v1.0.2)
2. **GitHub 同步** - 自动推送 Release
3. **文档完善** - RELEASE + CHANGELOG

### 业务恢复（昨日工作）
1. **ClawHub 发布** - 等待 Discord 官方响应
2. **技能发布** - 6 个原创技能 GitHub Release
3. **Clash 优化** - 最快节点自动选择（每 5 分钟测速）
4. **SearXNG 部署** - 自适应代理检测 + 中国大陆优化
5. **文章生产** - 每日 2 篇（06:00 开始流程）
6. **雷达日报** - 每日 09:00 自动生成

### 成本优化
1. **大模型策略** - 按任务分配最优模型
2. **目标** - 性能 +33%，成本 -35%

---

## 📞 紧急恢复

### 配置故障

```bash
docker stop xiaoma_new
chmod 644 /root/.openclaw/openclaw.json
LATEST=$(ls -t /root/.openclaw/config-backups/*.json | head -1)
cp "$LATEST" /root/.openclaw/openclaw.json
docker start xiaoma_new
chmod 444 /root/.openclaw/openclaw.json
```

### 记忆恢复

```bash
cp -r /root/.openclaw/backups/memory-backup/memory/* \
      /root/.openclaw/workspace/memory/
```

### 技能迭代恢复

```bash
# 手动执行迭代
/root/.openclaw/workspace/daily-iterate.sh radar-daily-report patch
/root/.openclaw/workspace/daily-iterate.sh ai-humanizer-cn patch

# 同步 GitHub
/root/.openclaw/workspace/sync-github.sh
```

---

## 📋 发布原则（确立于 2026-03-11）

1. **无实际代码不发布** - 必须有可运行的代码
2. **无实际问题不发布** - 必须解决真实问题
3. **无创新性不发布** - 必须有独特价值
4. **坚决杜绝空壳工程** - 每个技能必须经测试验证

## 💡 经验教训

### 配置管理
- 配置文件必须设置只读保护 (444)
- 修改前必须备份
- 仅使用当前版本支持的字段
- 不支持字段：fallback, taskOverrides, browser.provider/target/kasm

### 更新流程
- 更新前完整备份（配置 + 记忆）
- 验证备份可用
- 执行更新
- 验证功能正常

### 技能发布
- GitHub Release 是可靠渠道（100% 可用）
- ClawHub 存在 API Bug（等待修复）
- 每个技能必须有实际价值

---

**最后审查：** 2026-03-16 14:05  
**下次审查：** 2026-03-23 (每周)  
**记忆版本：** v3.0（已重建 3 月 13-15 日记忆）
技能迭代恢复

```bash
# 手动执行迭代
/root/.openclaw/workspace/daily-iterate.sh radar-daily-report patch
/root/.openclaw/workspace/daily-iterate.sh ai-humanizer-cn patch

# 同步 GitHub
/root/.openclaw/workspace/sync-github.sh
```

---

## 📋 发布原则（确立于 2026-03-11）

1. **无实际代码不发布** - 必须有可运行的代码
2. **无实际问题不发布** - 必须解决真实问题
3. **无创新性不发布** - 必须有独特价值
4. **坚决杜绝空壳工程** - 每个技能必须经测试验证

## 💡 经验教训

### 配置管理
- 配置文件必须设置只读保护 (444)
- 修改前必须备份
- 仅使用当前版本支持的字段
- 不支持字段：fallback, taskOverrides, browser.provider/target/kasm

### 更新流程
- 更新前完整备份（配置 + 记忆）
- 验证备份可用
- 执行更新
- 验证功能正常

### 技能发布
- GitHub Release 是可靠渠道（100% 可用）
- ClawHub 存在 API Bug（等待修复）
- 每个技能必须有实际价值

### 备份管理 (2026-03-19)

**问题：** 3 月 18 日备份异常增大到 634M（正常 2-3M）

**根因分析：**
1. Docker 镜像备份占 2.6G（/root/.openclaw/backups/docker-images/）
2. Session 文件积累（reset/deleted 文件未清理）
3. 备份脚本未限制包含范围

**解决方案：**
- ✅ 创建自动清理脚本（cleanup-cron.sh）
- ✅ 设置 cron 任务（每天 04:00 执行）
- ✅ 保留策略：14 天备份 + 至少 2 个完整备份
- ✅ Docker 镜像备份只保留最近 1 个
- ✅ 清理报告保留最近 5 个

**清理脚本位置：**
- `/root/.openclaw/backups/cleanup-cron.sh` (cron 执行)
- `/root/.openclaw/backups/cleanup-backups.sh` (手动执行)

**Cron 任务：**
- 每天 04:00 自动执行
- 生成清理报告到 backup 目录

---

### 搜索服务故障 (2026-03-19)

**问题：** SearXNG 无法启动，搜索引擎全部超时

**错误根因：**
1. 使用 host 网络模式导致端口冲突（`Address already in use`）
2. 容器未配置 Clash 代理，无法访问外网
3. DNS 解析失败（searxng 容器无法解析 clash 主机名）

**正确配置（已验证）：**
```bash
docker run -d --name searxng \
  -p 8081:8080 \
  -e SEARXNG_SECRET="xiaoma2026" \
  -e HTTP_PROXY="http://clash:7890" \
  -e HTTPS_PROXY="http://clash:7890" \
  --network openclaw_openclaw-net \
  searxng/searxng:latest
```

**关键步骤：**
1. Clash 必须连接到 `openclaw_openclaw-net` 网络
2. SearXNG 使用 bridge 网络（非 host 模式）
3. 代理环境变量指向容器名（非 IP）

**降级方案（紧急恢复）：**
1. web_fetch - 直接抓取搜索页面（可用）
2. Brave API - 配置 `openclaw configure --section web`
3. multi-search-engine 技能 - 本地多引擎聚合

**教训：**
- ⚠️ 每日工作前 30 分钟检查服务状态
- ⚠️ 有效配置必须文档化（MEMORY.md）
- ⚠️ 不要应付，直接解决问题

---

**最后审查：** 2026-03-19 09:09  
**下次审查：** 2026-03-26 (每周)  
**记忆版本：** v3.0（已添加备份管理机制）

---

## 🛡️ 配置安全审查流程 (2026-03-20 新增)

### 背景

2026-03-20 发生多次配置错误修改，导致：
- 添加不支持的字段（memorySearch.provider 等）
- 配置文件大小异常波动
- Gateway 配置被意外清空

**教训：** 必须有严格的安全审查流程。

---

### 配置修改完整流程

#### 修改前（必须执行）

```bash
# 1. 运行安全审查脚本
/root/.openclaw/scripts/config-safety-check.sh

# 2. 解锁配置（自动备份）
chmod 644 /root/.openclaw/openclaw.json

# 3. 查看当前配置（可选）
cat /root/.openclaw/openclaw.json | python3 -m json.tool
```

#### 修改中

```bash
# 4. 修改配置
vim /root/.openclaw/openclaw.json

# 或使用 openclaw config 命令（推荐）
openclaw config set gateway.mode local
```

#### 修改后（必须执行）

```bash
# 5. 验证 JSON 格式
python3 -m json.tool /root/.openclaw/openclaw.json > /dev/null && echo "✅ JSON 有效" || echo "❌ JSON 无效"

# 6. 运行 doctor 检查
openclaw doctor --non-interactive

# 7. 检查不支持的字段
grep -E "fallback|taskOverrides|browser\.(provider|target|kasm)" /root/.openclaw/openclaw.json && echo "⚠️ 发现不支持字段" || echo "✅ 字段检查通过"

# 8. 重启服务（如果需要）
docker restart xiaoma-new

# 9. 验证功能
openclaw status
openclaw memory status

# 10. 重新锁定配置
chmod 444 /root/.openclaw/openclaw.json
```

---

### 安全审查脚本

**位置：** `/root/.openclaw/scripts/config-safety-check.sh`

**检查项目：**
1. ✅ 文件存在性
2. ✅ JSON 格式验证
3. ✅ 备份检查（自动创建备份）
4. ✅ 文件大小异常检测（检测骤降 >50%）
5. ✅ OpenClaw doctor 健康检查
6. ✅ 支持的字段检查
7. ✅ 关键配置项检查
8. ✅ 文件权限检查

**使用：**
```bash
# 常规检查
/root/.openclaw/scripts/config-safety-check.sh

# 检查指定文件
/root/.openclaw/scripts/config-safety-check.sh /path/to/config.json

# 强制跳过（不推荐）
/root/.openclaw/scripts/config-safety-check.sh --force
```

---

### 不支持字段清单（当前版本 2026.3.13）

❌ **禁止使用：**
- `agents.defaults.fallback`
- `agents.taskOverrides`
- `browser.provider`
- `browser.target`
- `browser.kasm`

✅ **支持：**
- `agents.defaults.model.primary`
- `agents.defaults.models.*`
- `models.providers.*`
- `channels.*`
- `gateway.*`
- `plugins.*`
- `commands.*`

---

### 配置审计日志

**位置：** `/root/.openclaw/logs/config-audit.jsonl`

**监控字段：**
- `suspicious` - 可疑操作标记（如文件大小骤降）
- `previousBytes` / `nextBytes` - 配置大小变化
- `argv` - 修改配置的命令

**查看最近审计记录：**
```bash
tail -5 /root/.openclaw/logs/config-audit.jsonl | python3 -m json.tool
```

---

### 备份策略

**备份位置：** `/root/.openclaw/config-backups/`

**保留策略：**
- 每次修改前自动备份
- 保留最近 14 天的备份
- 至少保留 2 个完整备份

**恢复配置：**
```bash
# 查看备份
ls -lt /root/.openclaw/config-backups/*.json | head -10

# 恢复最新备份
LATEST=$(ls -t /root/.openclaw/config-backups/*.json | head -1)
cp "$LATEST" /root/.openclaw/openclaw.json
python3 -m json.tool /root/.openclaw/openclaw.json > /dev/null  # 验证
docker restart xiaoma-new  # 重启
```

---

### 紧急恢复流程

```bash
# 1. 停止容器
docker stop xiaoma_new

# 2. 解锁配置
chmod 644 /root/.openclaw/openclaw.json

# 3. 恢复备份
LATEST=$(ls -t /root/.openclaw/config-backups/*.json | head -1)
cp "$LATEST" /root/.openclaw/openclaw.json

# 4. 验证
python3 -m json.tool /root/.openclaw/openclaw.json > /dev/null

# 5. 重启
docker start xiaoma_new

# 6. 重新锁定
chmod 444 /root/.openclaw/openclaw.json
```

---

### 质量审查（发布内容）

发布技能/文档到 GitHub 前必须检查：

**代码审查：**
- [ ] 代码是否有实际功能（非空壳）
- [ ] 是否经过测试验证
- [ ] 是否有依赖问题
- [ ] 是否有敏感信息（API key 等）

**文档审查：**
- [ ] README 是否完整
- [ ] 使用示例是否清晰
- [ ] 版本信息是否正确
- [ ] 许可证是否声明

**发布审查：**
- [ ] 是否解决真实问题
- [ ] 是否有创新性
- [ ] 是否符合发布原则

---

**审查流程建立时间：** 2026-03-20 10:18  
**责任人：** 小马 🐴  
**下次审查：** 2026-03-27
