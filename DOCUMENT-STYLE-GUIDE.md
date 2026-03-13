# 📝 文档风格规范

**版本：** v1.0  
**原则：** 看人下菜碟，啥文档说啥话

---

## 🎯 文档分类

### 技术文档 - 保持专业严谨

**位置：** GitHub、ClawHub、技术手册

**风格要求：**
- ✅ 专业术语（该用就用）
- ✅ 结构清晰（章节分明）
- ✅ 逻辑严谨（因果关系）
- ✅ 代码规范（标准格式）
- ✅ 数据准确（有出处）

**不适用 AI Humanizer：**
- ❌ 不用口语化
- ❌ 不加个人情感
- ❌ 不打破语法
- ❌ 不用网络用语

**示例：**
```markdown
# OpenClaw SearXNG Plugin v1.0.0

## Abstract

This plugin provides privacy-focused web search integration 
for OpenClaw AI Assistant, with China-optimized search engines 
(Baidu, Bing CN) and Redis caching layer.

## Installation

```bash
docker run -d --name searxng -p 8081:8080 searxng/searxng:latest
```

## Configuration

The plugin requires the following configuration parameters:
- `baseUrl`: SearXNG instance URL
- `timeout`: Request timeout (milliseconds)
- `engines`: Priority list of search engines
```

---

### 媒体内容 - 必须人话版

**位置：** 小红书、微信公众号、知乎、微博

**风格要求：**
- ✅ 口语化表达
- ✅ 个人色彩
- ✅ 情感态度
- ✅ 短句 + 长句结合
- ✅ 网络用语（适度）

**必须用 AI Humanizer：**
- ✅ 打破完美语法
- ✅ 加入个人经历
- ✅ 使用口语表达
- ✅ 变化句式长度
- ✅ 加入情感态度

**示例：**
```markdown
# 3 分钟部署私有 AI 搜索引擎！隐私保护太香了

家人们，今天分享一个超实用的工具！

我之前一直担心用搜索引擎被追踪，直到发现了 SearXNG。
这玩意儿真的绝了 - 自托管、无追踪、还能用百度必应！

咋部署？简单，3 分钟搞定：

1. 一行命令启动 Docker
2. 配置一下（就几个参数）
3. 开用！

看，就这么简单：
[截图]

隐私保护 + 中文搜索，两者兼得，太香了！

#AI #隐私保护 #开源 #技术分享
```

---

## 📊 文档类型判断

### 技术文档（不用 AI Humanizer）

| 文档类型 | 位置 | 风格 |
|---------|------|------|
| README.md | GitHub | 专业 |
| SKILL.md | ClawHub | 专业 |
| API 文档 | 技术文档 | 专业 |
| 部署指南 | GitHub | 专业 |
| 技术教程 | GitHub | 专业 |
| 代码注释 | 源代码 | 专业 |

### 媒体内容（用 AI Humanizer）

| 文档类型 | 位置 | 风格 |
|---------|------|------|
| 小红书笔记 | 小红书 | 人话 |
| 公众号文章 | 微信公众号 | 人话 |
| 知乎回答 | 知乎 | 人话 |
| 微博文案 | 微博 | 人话 |
| 视频脚本 | B 站/抖音 | 人话 |
| 宣传文案 | 各平台 | 人话 |

---

## 🔄 一源双发策略

### 技术内容 → 媒体内容

**流程：**
```
技术文档（GitHub）
    ↓
    ↓ AI Humanizer
    ↓
媒体内容（小红书/公众号）
```

**示例：**

**技术文档（原样）：**
```markdown
# SearXNG Deployment Guide

## Prerequisites

- Docker installed
- Port 8081 available
- Network access to search engines

## Steps

1. Create configuration directory
2. Download settings.yml
3. Enable JSON format
4. Start container
```

**媒体内容（人话版）：**
```markdown
# 手把手教你部署私有搜索引擎！

 prerequisites？别被这词吓到，其实就 3 个条件：
- 装了 Docker（没装的先去装一个）
- 8081 端口没人用
- 能上网（废话😄）

步骤？简单，4 步搞定：

1. 创建配置目录（就一个文件夹）
2. 下载配置文件（我放链接了）
3. 启用 JSON 格式（改一行代码）
4. 启动容器（一行命令）

看，就这么简单！
```

---

## 📋 执行规范

### 创建文档时

**先判断：**
1. 这文档给谁看？
   - 技术人员 → 专业风格
   - 普通用户 → 人话风格

2. 发在哪？
   - GitHub/ClawHub → 专业
   - 小红书/公众号 → 人话

3. 干啥用？
   - 技术参考 → 专业
   - 宣传推广 → 人话

### 转换文档时

**技术 → 媒体：**
1. 运行 AI Humanizer
2. 检查口语化程度
3. 加入个人色彩
4. 添加情感态度
5. 调整句式长度

**媒体 → 技术：**
1. 去除口语化
2. 规范术语
3. 严谨逻辑
4. 标准格式
5. 添加引用

---

## ✅ 检查清单

### 技术文档检查

- [ ] 术语准确
- [ ] 结构清晰
- [ ] 代码规范
- [ ] 数据有出处
- [ ] 无口语化表达
- [ ] 无个人情感
- [ ] 逻辑严谨

### 媒体内容检查

- [ ] 口语化表达
- [ ] 有个人色彩
- [ ] 有情感态度
- [ ] 句式有变化
- [ ] 有互动引导
- [ ] 标题吸引人
- [ ] 配图合适

---

## 🎯 常见场景

### 场景 1：发布新技能

**技术文档（GitHub/ClawHub）：**
```markdown
# OpenClaw SearXNG Plugin v1.0.0

## Features

- Privacy-focused search
- China-optimized engines
- Redis caching
- Multi-engine support
```

**媒体内容（小红书/公众号）：**
```markdown
# 隐私保护神器！支持百度必应的 AI 搜索插件来了！

家人们，我们团队搞了个大事情！

这个插件真的绝了：
✅ 隐私保护（无追踪）
✅ 支持百度必应（中文搜索 yyds）
✅ 速度快（有缓存）
✅ 多引擎（一个不够用？给你一堆！）

部署简单，3 分钟搞定！
```

---

### 场景 2：技术教程

**技术文档（GitHub）：**
```markdown
# OpenClaw Architecture Guide

## System Components

1. Gateway Layer
   - WebSocket server
   - Message routing
   - Session management

2. Model Layer
   - LLM providers
   - Model selection
   - Failover mechanism
```

**媒体内容（公众号）：**
```markdown
# OpenClaw 架构详解：从 0 到 1 构建 AI 助手

先说说 OpenClaw 是啥。

简单理解，它就是个"中间人"：
- 你通过微信/Telegram 跟它聊天
- 它帮你调用 AI 模型
- 然后把回复发给你

核心就两层：

1. Gateway 层（传话筒）
   - 接收你的消息
   - 转发给 AI
   - 把回复发给你

2. 模型层（大脑）
   - 连接各种 AI（Qwen、GPT 等）
   - 选最合适的模型
   - 一个挂了自动换另一个

看，就这么简单！
```

---

## 📈 效果对比

### 技术文档

**优点：**
- ✅ 专业可信
- ✅ 准确无误
- ✅ 易于参考
- ✅ 便于维护

**适用：**
- 技术人员
- 开发者
- 需要准确信息的人

---

### 媒体内容

**优点：**
- ✅ 易于理解
- ✅ 有亲和力
- ✅ 易于传播
- ✅ 互动性强

**适用：**
- 普通用户
- 潜在用户
- 需要快速理解的人

---

## 🎯 最佳实践

### 技术文档

**要做的：**
- ✅ 用标准术语
- ✅ 保持结构清晰
- ✅ 提供完整示例
- ✅ 添加参考资料
- ✅ 版本控制

**别做的：**
- ❌ 用口语
- ❌ 加个人情感
- ❌ 省略关键步骤
- ❌ 用模糊描述

---

### 媒体内容

**要做的：**
- ✅ 说人话
- ✅ 加个人经历
- ✅ 用口语表达
- ✅ 引导互动
- ✅ 配好图

**别做的：**
- ❌ 太专业（让人看不懂）
- ❌ 太正式（让人不想看）
- ❌ 太长（让人没耐心）
- ❌ 太水（让人失望）

---

## 🔄 持续优化

### 技术文档优化

**频率：** 每周  
**内容：**
- 更新示例
- 补充说明
- 修复错误
- 优化结构

---

### 媒体内容优化

**频率：** 每日  
**内容：**
- 调整标题
- 优化配图
- 改进表达
- 增加互动

---

**维护者：** CEO 智能体（小马 🐴）  
**版本：** v1.0  
**最后更新：** 2026-03-11  
**下次优化：** 2026-03-18
