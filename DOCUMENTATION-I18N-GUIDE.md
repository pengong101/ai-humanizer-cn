# 🌐 文档国际化指南

**版本：** v1.0  
**时间：** 2026-03-11 17:05

---

## 🎯 文档格式要求

### 标题格式

```markdown
# 中文标题 / English Title

## 简介 / Introduction

## 安装 / Installation

## 使用 / Usage

## 配置 / Configuration

## 故障排查 / Troubleshooting
```

---

### 内容格式

```markdown
**中文说明文字。**

English description text.

**示例 / Example:**

```bash
# 中文注释
command --option

# English comment
command --option
```

---

### 代码注释

```python
# 中文注释
# English comment
def function():
    pass
```

```bash
#!/bin/bash
# 中文说明
# English description
```

---

## 📋 已发布技能文档更新

### openclaw-plugin-searxng

**状态：** ⏳ 待更新

**更新内容：**
- README.md 中英双语
- SKILL.md 中英双语
- 代码注释双语

---

### openclaw-searxng-search

**状态：** ⏳ 待更新

---

### openserp-searxng-adapter

**状态：** ⏳ 待更新

---

### ai-humanizer-cn

**状态：** ⏳ 待更新

---

### searxng-auto-proxy v2.0.1

**状态：** ✅ 已更新（隐私保护）
**待更新：** 文档国际化

---

### clash-auto-control v2.0.1

**状态：** ✅ 已更新（隐私保护）
**待更新：** 文档国际化

---

## 📈 更新计划

### 优先级

**P0（今日完成）：**
- searxng-auto-proxy README.md
- clash-auto-control.sh 注释

**P1（明日完成）：**
- 所有技能的 SKILL.md
- 所有技能的 README.md

**P2（本周完成）：**
- 代码注释双语化
- 示例代码双语化

---

## ✅ 检查清单

### 发布前检查

- [ ] 无 IP 地址（使用环境变量）
- [ ] 无明文密码
- [ ] 无硬编码 Token
- [ ] 无账号信息
- [ ] 文档中英双语
- [ ] 代码注释双语

### 文档检查

- [ ] 标题中英双语
- [ ] 章节标题双语
- [ ] 示例代码双语注释
- [ ] 配置说明双语
- [ ] 故障排查双语

---

**维护者：** 小马 🐴 + CEO 智能体（小马 🐴）  
**版本：** v1.0  
**最后更新：** 2026-03-11 17:05
