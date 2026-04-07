# MEMORY.md - 长期记忆

**创建时间：** 2026-03-12
**最后更新：** 2026-04-04
**版本：** v4.0（精简版）

---

## 🎯 核心身份

- **名称：** 小马 (Xiao Ma)
- **角色：** OpenClaw CEO 智能体
- **Emoji：** 🐴
- **Vibe：** 务实、高效、靠谱

---

## 🚨 紧急恢复

### 配置文件故障
```bash
docker stop xiaoma-20260402
chmod 644 /root/.openclaw/openclaw.json
cp /root/.openclaw/config-backups/latest.json /root/.openclaw/openclaw.json
chmod 444 /root/.openclaw/openclaw.json
docker start xiaoma-20260402
```

### 记忆文件损坏
```bash
cp -r /root/.openclaw/backups/memory-backup/memory/* /root/.openclaw/workspace/memory/
```

---

## 📊 系统架构（2026-04-04 最新）

### Docker 容器
| 容器 | 端口 | 版本 |
|------|------|------|
| xiaoma-20260402 | 8082/18789 | 2026.4.2（当前主力） |
| searxng | 8089 | latest |
| bge-embedding | — | host网络模式 |
| clash | 7890-7892 | mihomo |

### 数据挂载
- **主机路径：** `/data_s001/docker_appstore/.openclaw/`
- **容器路径：** `/root/.openclaw/`（完整目录挂载）
- **创建新容器命令：**
```bash
docker run -d --name xiaoma-20260402 \
  --user=0:0 -p 32773:8080 -p 8086:18789 \
  -v /data_s001/docker_appstore/.openclaw:/root/.openclaw \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --restart unless-stopped ghcr.io/openclaw/openclaw:latest
```

### 大模型配置
- **提供商：** Bailian (阿里百炼)
- **主模型：** minimax/MiniMax-M2.7
- **baseURL：** https://api.minimaxi.com/v1

---

## 📋 重要决策

### 配置文件保护（2026-03-12）
- 设置只读 (444)，修改前备份
- 仅使用当前版本支持的字段
- 不支持：thinkingDefault, agents.defaults.fallback, browser.provider/target/kasm

### 大模型策略（2026-04-04 更新）
- **主模型：** minimax/MiniMax-M2.7（当前生产环境）
- **代码任务：** qwen3-coder-next（按需）
- **搜索增强：** qwen3.5-plus（按需）

### 备份机制（2026-03-19）
- 每天 04:00 自动清理
- 保留最近 14 天备份
- Docker 镜像只保留 1 个

---

## 📦 技能清单

### 核心技能
| 技能 | 版本 | 用途 |
|------|------|------|
| radar-daily-report | 每日 | 毫米波雷达日报生成 |
| ai-humanizer-cn | v1.0.1 | AI文本风格优化 |
| secretary-core | v4.1.0 | 秘书技能核心 |
| agent-reach | — | 全网搜索（via MCP） |

### 原创技能（GitHub Release）
1. openclaw-plugin-searxng
2. openclaw-searxng-search
3. openerp-searxng-adapter
4. ai-humanizer-cn
5. searxng-auto-proxy
6. clash-auto-control

---

## 🔄 定时任务

| 任务 | 时间 | 执行者 | 状态 |
|------|------|--------|------|
| 科普文章选题 | 05:30 北京 | content-agent | ok |
| 搜索引擎协同健康检查 | 06:00 北京 | research-agent | ok |
| 每日晨会 | 07:30 北京 | main | ok |
| 毫米波雷达日报 | 09:00 北京 | main | ok |
| 每日复盘 | 03:30 北京 | main | ok |
| 备份清理 | 04:00 北京 | ops-agent | ok |

### 搜索引擎协同健康检查（2026-04-07 新增）
**ID:** 48280311-0dd9-46bf-9fe5-ff9d3e4a3de2
**流程:** research-agent 检查 → 判定 → 小问题自修/大问题 spawn ops-agent → 统一汇报
**脚本:** /root/.openclaw/workspace/scripts/searxng-engine-adaptive-test.py

---

## 🤖 智能体体系（2026-04-01 完成）

| Agent | 名称 | 职责 |
|-------|------|------|
| main | 小马 🐴 | CEO协调 |
| research-agent | 小研 🔍 | 调研分析 |
| ops-agent | 小维 ⚙️ | 运维执行 |
| code-agent | 小码 💻 | 代码开发 |
| content-agent | 小文 ✍️ | 内容创作 |
| review-agent | 小审 🔎 | 质量审核 |

### research ↔ ops 协作接口规范（2026-04-07）

**触发条件：**
- 检查正常 → 直接汇报，NO_REPLY
- 小问题（重启服务） → research-agent 直接修复
- 大问题（改配置、重启容器） → spawn ops-agent

**调用格式（sessions_spawn）：**
```
sessions_spawn(
  task = "执行 /root/.openclaw/workspace/scripts/searxng-engine-adaptive-test.py",
  runtime = "subagent",
  agentId = "ops-agent",
  mode = "run",
  attachments = [{"name": "health_check_result.json", "content": "<JSON>", "mimeType": "application/json"}]
)
```

**attachment JSON 格式：**
```json
{
  "check_time": "2026-04-07 06:00:00 CST",
  "issues_found": [{"engine": "google", "status": "suspended", "error": "...", "suggested_fix": "disable"}],
  "services": {"searxng": "healthy", "proxy": "healthy"},
  "expects": "执行修复并报告结果"
}
```

**ops-agent 响应格式：**
```json
{"action": "searxng_engine_adaptive_fix", "executed": true, "changes_made": ["google→disabled"], "restart_done": true, "summary": "..."}
```

---

## ⚠️ 已知问题

### SearXNG 搜索
- **状态：** ✅ 已修复（2026-04-07）
- **修复方式：** settings.yml 使用 dict 格式配置 outgoing.proxies
- **当前状态：** Bing + Baidu + DuckDuckGo + Brave 正常，Google 引擎因代理出口 IP 被 Google 封锁暂时禁用

### 2026.4.2 兼容性
- 不读取挂载的 /app/openclaw.json，只读内部 /home/node/.openclaw/openclaw.json
- 需要完整目录挂载而非分散文件挂载
- 新版本安全策略更严格，exec preflight 检查更复杂

---

## 📅 今日记录（2026-04-04）

### 升级到 OpenClaw 2026.4.2
- 04-04 完成升级切换
- 解决了 2026.4.2 的配置路径问题（完整目录挂载）
- 解决了 minimax 模型未自动启用问题
- **重大变更：** 旧容器 xiaoma-20260328 已停止，新容器 xiaoma-20260402 正式上位

### Doctor 发现的问题
- MEMORY.md 超标（41874 > 30000）✅ 已精简
- 记忆搜索无嵌入模型 ⚠️ 未配置
- 孤儿 session 文件 4 个 ⚠️ 待清理

---

**最后审查：** 2026-04-04 16:30
**下次审查：** 2026-04-10
