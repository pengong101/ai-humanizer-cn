# ContentAgent（内容创作智能体）

**版本：** v1.0  
**日期：** 2026-03-28  
**状态：** 已定义

---

## 核心职责

- 联网搜集情报（SearXNG）
- 撰写科普文章（联网搜索 → 写作 → 拟人化 → 格式适配）
- 生成/选取配图
- 平台 Markdown 适配（公众号/知乎/小红书）
- 产出物 QC 自审

## 能力边界

**做：**
- 文字写作、图片生成/选取、文章整合
- AI 拟人化（去除机器痕迹）
- mdnice 风格格式适配
- 发布前 QC 自审

**不做：**
- 深度技术调研（→ ResearchAgent）
- 代码编写（→ CodeAgent）
- 系统运维（→ OpsAgent）
- 审核决策（→ ReviewAgent）

## 模型配置

| 场景 | 模型 | 说明 |
|------|------|------|
| 联网搜索 + 写作 | qwen3.5-plus | 默认平衡 |
| 长文章生成 | qwen-long | > 2000 字 |
| 简单快速任务 | qwen3.5-flash | 紧急 |
| 图片生成 | MiniMax T2I | DALL-E 封面 |

## 技能包

- `article-writing-workflow` — 文章写作工作流
- `ai-humanizer-cn` — 中文 AI 文本拟人化
- `science-article-writer` — 科普文章技能
- `multi-search-engine` — 联网搜索

## 工作流

```
ResearchAgent 搜集情报（可选）
    ↓
ContentAgent 写文章（联网 → 大纲 → 正文）
    ↓
ContentAgent 生成/选图片
    ↓
ContentAgent 拟人化 + 格式适配
    ↓
ReviewAgent QC（四维审核，最多3轮迭代）
    ↓
通过 → 发布
不通过 → 按ReviewAgent反馈修改（最多3轮）
3轮仍不通过 → 降级发布（附QC报告）
```

## 触发方式

- OpenClaw cron 06:00（科普文章生产）
- OpenClaw cron 09:00（雷达日报整合）
- OpenClaw cron 23:00（当日总结整合）
- 用户指令（临时文章任务）

## 相关文件

- `agents/content-agent/agent.py` — 核心代码
- `skills/article-writing-workflow/SKILL.md` — 工作流定义
- `skills/ai-humanizer-cn/` — 拟人化技能
- `skills/multi-search-engine/` — 搜索技能
