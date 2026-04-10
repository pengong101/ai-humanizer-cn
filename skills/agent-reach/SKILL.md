---
name: agent-reach
description: >
  Give your AI agent eyes to see the entire internet.
  17 platforms via CLI, MCP, curl, and Python scripts.
  Zero config for 8 channels.

  【路由方式】SKILL.md 包含路由表和常用命令，复杂场景需按需阅读对应分类的 references/*.md。
  分类：search / social (小红书/抖音/微博/推特/B站/V2EX/Reddit) / career(LinkedIn) / dev(github) / web(网页/文章/公众号/RSS) / video(YouTube/B站/播客).
triggers:
  - search: 搜/查/找/search/搜索/查一下/帮我搜
  - social: 小红书/xhs/抖音/twitter/推特/微博/b站/reddit/v2ex
  - career: linkedin/领英/招聘/求职
  - dev: github/仓库/gh/issue/pr/代码
  - web: 网页/链接/文章/公众号/rss/打开/读一下
  - video: youtube/视频/播客/字幕
  - finance: 雪球/股票/基金
---

# Agent Reach — 路由器

17 平台工具集合。根据用户意图选择对应分类。

## 路由表

| 用户意图 | 分类 | 详细文档 |
|---------|------|---------|
| 网页搜索/代码搜索 | search | [references/search.md](references/search.md) |
| 小红书/抖音/微博/推特/B站/V2EX/Reddit | social | [references/social.md](references/social.md) |
| 招聘/职位/LinkedIn | career | [references/career.md](references/career.md) |
| GitHub/代码 | dev | [references/dev.md](references/dev.md) |
| 网页/文章/公众号/RSS | web | [references/web.md](references/web.md) |
| YouTube/B站/播客字幕 | video | [references/video.md](references/video.md) |

## 零配置快速命令（已安装渠道）

```bash
# Exa 全网搜索（英文/技术搜索，质量最高）
mcporter call 'exa.web_search_exa(query: "query", numResults: 5)'

# 通用网页阅读（Jina Reader，转 Markdown）
curl -s "https://r.jina.ai/https://example.com/article"

# GitHub 搜索（需 gh CLI）
gh search repos "query" --sort stars --limit 10

# RSS 读取
python3 -c "import feedparser; [print(e.title, e.link) for e in feedparser.parse('FEED_URL').entries[:5]]"
```

## 与现有工具对比

| 任务 | 现有工具 | agent-reach 优势 |
|------|---------|-----------------|
| 中文搜索 | multi-search.py (baidu/bing) | Exa 更精准 |
| 英文搜索 | SearXNG | Exa 质量更高 |
| 网页内容提取 | web_fetch | Jina Reader 更稳定 |
| GitHub 搜索 | — | gh CLI 原生支持 |
| 微信公众号 | — | Exa 可搜索+阅读 |
| 技术文档 | — | Exa get_code_context |

## 工作流集成

### 调研任务（research-agent）
- 优先用 `exa.web_search_exa` 搜索英文技术内容
- 用 `curl r.jina.ai/<URL>` 读取网页内容
- 用 `gh search` 搜 GitHub 仓库/代码

### 内容任务（content-agent）
- 搜热点用 `exa.web_search_exa`
- 读文章用 Jina Reader
- 搜 GitHub 项目用 `gh search repos`

### 开发任务（code-agent）
- 搜代码/文档用 `gh search code` / `exa.get_code_context_exa`

## 安装状态
- pip 包：`agent_reach`
- mcporter exa：✅ 可用
- gh CLI：✅ 可用
- Twitter/小红书：需 Cookie（待配置）

## 详细文档
- [搜索工具](references/search.md)
- [社交媒体](references/social.md)
- [开发工具](references/dev.md)
- [网页阅读](references/web.md)
- [视频播客](references/video.md)
- [职场招聘](references/career.md)
