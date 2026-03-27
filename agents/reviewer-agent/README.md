# 审核智能体 (Reviewer Agent)

**版本：** v0.1  
**职责：** 质量检查、敏感词过滤、事实核查

---

## 一、核心职责

- ✅ 质量检查（语法、逻辑、连贯性）
- ✅ 敏感词过滤
- ✅ 事实核查
- ✅ 格式检查

---

## 二、API

```python
POST /api/v1/reviewer/check
{
  "content": "待审核内容",
  "check_types": ["quality", "sensitivity", "facts"]
}
```

---

**状态：** 框架已创建，待实现核心模块
