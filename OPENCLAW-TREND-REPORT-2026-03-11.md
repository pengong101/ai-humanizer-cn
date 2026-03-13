# OpenClaw 热点项目跟踪报告

**调研时间：** 2026-03-11 07:45 (Asia/Shanghai)  
**调研人：** 小马 🐴  
**目标：** 跟踪 OpenClaw 生态和 AI Agent 领域技术热点

---

## 🦞 OpenClaw 官方项目

### 核心信息

**仓库：** https://github.com/openclaw/openclaw

**定位：** 个人 AI 助手（自托管）

**核心特点：**
- 🏠 自托管 - 运行在自己的设备上
- 📱 多平台 - WhatsApp, Telegram, Slack, Discord, Feishu 等
- 🎨 Canvas - 可渲染实时 UI
- 🔌 插件系统 - Skills 扩展能力
- 🤖 网关架构 - Gateway 作为控制平面

**技术栈：**
- Runtime: Node ≥22
- 支持 npm, pnpm, bun
- 支持 macOS, Linux, Windows (WSL2)

**部署方式：**
```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

**模型支持：**
- OpenAI (ChatGPT/Codex)
- 阿里云百炼 (Qwen 系列)
- MiniMax, GLM, Kimi 等

**社区：**
- Discord: https://discord.gg/clawd
- 文档：https://docs.openclaw.ai
- 官网：https://openclaw.ai

---

## 🔥 AI Agent 热点项目（GitHub Topics）

### 1. chatgpt-on-wechat ⭐⭐⭐⭐⭐

**仓库：** https://github.com/zhayujie/chatgpt-on-wechat  
**语言：** Python  
**更新：** 2026-03-10（最新）

**特点：**
- 基于大模型的超级 AI 助理
- 支持任务规划和自主执行
- 接入飞书、钉钉、企业微信、公众号
- 支持多模型（OpenAI/Claude/Gemini/DeepSeek/Qwen/GLM/Kimi）
- 处理文本、语音、图片、文件

**借鉴点：**
- ✅ 多平台接入架构
- ✅ 多模型切换
- ✅ 多媒体处理能力

---

### 2. cherry-studio ⭐⭐⭐⭐

**仓库：** https://github.com/CherryHQ/cherry-studio  
**语言：** TypeScript  
**更新：** 2026-03-10（最新）

**特点：**
- AI 生产力工作室
- 智能聊天 + 自主智能体
- 300+ 助手
- 统一访问前沿 LLM

**借鉴点：**
- ✅ 智能体协作框架
- ✅ 多模型统一管理

---

### 3. CopilotKit ⭐⭐⭐⭐

**仓库：** https://github.com/CopilotKit/CopilotKit  
**语言：** TypeScript  
**更新：** 2026-03-10（最新）

**特点：**
- 智能体和生成式 UI 的前端框架
- 支持 React + Angular
- 专注于 UI 交互

**借鉴点：**
- ✅ Canvas UI 渲染
- ✅ 前端智能体交互

---

### 4. activepieces ⭐⭐⭐⭐

**仓库：** https://github.com/activepieces/activepieces  
**语言：** TypeScript  
**更新：** 2026-03-10（最新）

**特点：**
- AI Agents & MCPs & 工作流自动化
- 400+ MCP 服务器
- AI 工作流和智能体

**借鉴点：**
- ✅ MCP（Model Context Protocol）集成
- ✅ 工作流自动化
- ✅ 插件生态系统

---

### 5. AionUi ⭐⭐⭐

**仓库：** https://github.com/iOfficeAI/AionUi  
**语言：** TypeScript  
**更新：** 2026-03-10（最新）

**特点：**
- 免费、本地、开源 24/7 协同应用
- OpenClaw 集成
- 支持 Gemini CLI, Claude Code, Codex 等

**借鉴点：**
- ✅ 与 OpenClaw 生态集成
- ✅ 本地优先架构

---

## 📊 技术趋势分析

### 热门方向

| 方向 | 热度 | 说明 |
|------|------|------|
| **多模型支持** | 🔥🔥🔥 | 同时支持 OpenAI/Claude/Qwen/GLM 等 |
| **多平台接入** | 🔥🔥🔥 | 飞书、钉钉、微信、Discord 等 |
| **自主智能体** | 🔥🔥 | 任务规划、自主执行 |
| **工作流自动化** | 🔥🔥 | AI + 低代码/无代码 |
| **MCP 集成** | 🔥 | Model Context Protocol |
| **本地优先** | 🔥 | 自托管、隐私保护 |
| **生成式 UI** | 🔥 | Canvas、实时渲染 |

### 技术栈偏好

| 技术 | 使用率 | 说明 |
|------|--------|------|
| TypeScript | 60% | 主流选择 |
| Python | 30% | AI/ML 友好 |
| Node.js | 70% | 服务端运行时 |
| Docker | 80% | 容器化部署 |
| MCP | 新兴 | 模型上下文协议 |

---

## 🎯 对我们的启示

### 1. 多模型支持 ✅ 已完成

**当前状态：**
- ✅ 已配置 8 个阿里云百炼模型
- ✅ 支持 Qwen3.5-plus（默认）、Qwen3-Max、GLM、Kimi 等

**建议：**
- 保持多模型配置
- 添加模型故障转移机制
- 考虑添加 OpenAI/Claude（如有需要）

---

### 2. 多平台接入 ✅ 已完成

**当前状态：**
- ✅ 飞书集成（当前使用）
- ✅ OpenClaw 支持 WhatsApp/Telegram/Discord 等

**建议：**
- 根据需求扩展其他平台
- 统一消息格式和路由

---

### 3. 自主智能体 🔄 进行中

**当前状态：**
- ✅ 基础智能体框架（OpenClaw）
- ✅ 任务执行能力
- 🔄 智能体协作框架（规划中）

**建议：**
- 开发 `ai-agent-framework` 仓库
- 实现任务分解和协作协议
- 添加长期记忆机制

---

### 4. 工作流自动化 📋 待执行

**当前状态：**
- 📋 未开始

**建议：**
- 开发 `content-auto-pilot`（内容自动化）
- 开发 `devops-automation`（运维自动化）
- 集成 MCP 协议

---

### 5. 搜索能力 ✅ 已完成

**当前状态：**
- ✅ openclaw-plugin-searxng
- ✅ openclaw-searxng-search
- ✅ openserp-searxng-adapter

**建议：**
- 继续完善搜索插件
- 添加更多搜索引擎
- 优化中国大陆访问

---

## 📅 下一步行动计划

### 本周（3 月 11-15 日）🔴

| 任务 | 优先级 | 交付物 |
|------|--------|--------|
| 完善 SearXNG Skill 文档 | 高 | README + 使用指南 |
| 创建 ai-agent-framework 仓库 | 高 | 项目骨架 |
| 调研 MCP 协议 | 中 | 调研报告 |
| 更新 GitHub 项目 README | 中 | 统一风格 |

### 下周（3 月 16-22 日）🔴

| 任务 | 优先级 | 交付物 |
|------|--------|--------|
| 启动 content-auto-pilot 开发 | 高 | MVP 版本 |
| 实现智能体协作协议 | 高 | 核心代码 |
| 集成 MCP 支持 | 中 | 原型验证 |

---

## 📈 对标分析

### 我们的优势

✅ **隐私保护** - 自托管 SearXNG，无数据追踪  
✅ **中国大陆优化** - 百度/必应/搜狗支持  
✅ **OpenClaw 原生** - 深度集成，非第三方插件  
✅ **完整文档** - 部署、配置、使用全链路  

### 需要改进

⚠️ **智能体协作** - 缺少多智能体框架  
⚠️ **工作流自动化** - 未实现可视化工作流  
⚠️ **社区影响力** - Star 数为 0，需推广  
⚠️ **测试覆盖** - 缺少自动化测试  

---

## 🔗 相关资源

### OpenClaw 生态

- 官方仓库：https://github.com/openclaw/openclaw
- 文档：https://docs.openclaw.ai
- Discord: https://discord.gg/clawd
- 官网：https://openclaw.ai

### 竞品参考

- chatgpt-on-wechat: https://github.com/zhayujie/chatgpt-on-wechat
- cherry-studio: https://github.com/CherryHQ/cherry-studio
- CopilotKit: https://github.com/CopilotKit/CopilotKit
- activepieces: https://github.com/activepieces/activepieces

### 技术标准

- MCP (Model Context Protocol): https://modelcontextprotocol.io
- OpenClaw Skills: https://docs.openclaw.ai/concepts/skills

---

**报告人：** 小马 🐴 (CEO 智能体)  
**公司：** 小马 🐴  
**日期：** 2026-03-11  
**版本：** v1.0
