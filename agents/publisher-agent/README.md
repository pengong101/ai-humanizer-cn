# PublisherAgent（发布智能体）

**版本：** v1.0  
**日期：** 2026-03-28  
**核心：** 多渠道发布 + 格式适配 + 状态追踪

---

## 核心职责

- Skill 发布（GitHub Release + ClawHub）
- 文章发布（公众号 / 知乎 / 小红书）
- 发布状态追踪与记录

## 触发方式

- ReviewAgent 审核通过后（自动）
- 用户手动触发发布

## 相关文件

- `agents/publisher-agent/agent.py`
- `skills/github-skill/`
