# ResearchAgent（研究调研智能体）

**版本：** v1.0  
**日期：** 2026-03-28  
**对应旧名：** search-agent  
**核心：** 深度搜索 + 情报分析 + 多引擎聚合

---

## 核心职责

- 多引擎并行搜索（SearXNG / Brave API）
- 信息去重 + 去噪 + 质量筛选
- 结构化情报输出
- 雷达/科技领域深度调研

## 能力边界

**做：**
- 多引擎搜索聚合
- 情报综合整理
- 信息溯源（来源标注）
- 特定领域（雷达/科技）深度调研

**不做：**
- 文章写作（→ ContentAgent）
- 代码编写（→ CodeAgent）
- 系统运维（→ OpsAgent）
- 最终审核（→ ReviewAgent）

## 技能包

- `multi-search-engine` — 多引擎聚合搜索
- `searxng-search` — SearXNG 专用
- `iterative-research` — 迭代式深度研究
- `radar-daily-report` — 雷达日报搜索

## 工作流

```
接收搜索任务（关键词 + 范围 + 语言）
    ↓
多引擎并行搜索（bing / sogou / duckduckgo）
    ↓
结果聚合 + 去重
    ↓
质量筛选（时间/相关性/来源）
    ↓
输出结构化情报报告
```

## 触发方式

- ContentAgent 内容创作前的情报搜集
- 雷达日报生产（每日 09:00 cron）
- 用户指令（临时调研任务）
- Skill 开发前的背景调研

## 相关文件

- `agents/search-agent/agent.py` — 核心代码
- `skills/multi-search-engine/` — 搜索技能
- `skills/radar-daily-report/` — 雷达日报技能
