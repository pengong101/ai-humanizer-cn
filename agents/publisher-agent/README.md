# 发布智能体 (Publisher Agent)

**版本：** v0.1  
**职责：** 多渠道发布、格式适配、状态追踪

---

## 一、核心职责

- 📤 多渠道发布（飞书/微信/知识库）
- 📐 格式适配（各渠道格式要求）
- 📊 发布状态追踪
- 🔄 发布失败重试

---

## 二、API

```python
POST /api/v1/publisher/publish
{
  "content": "发布内容",
  "channels": ["feishu", "wechat", "knowledge_base"],
  "schedule": "2026-03-23T09:00:00Z"
}
```

---

**状态：** 框架已创建，待实现核心模块
