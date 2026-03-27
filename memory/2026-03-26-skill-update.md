# 技能迭代更新计划

**日期：** 2026-03-26  
**准备时间：** 2026-03-25 00:59  
**制定者：** 小马 🐴

---

## 📦 待发布技能（6:00-9:00）

### 1. science-article-writer ⭐ 新发布

**状态：** 新技能，未发布

**内容：**
- SKILL.md（图片选取与验证技能）
- 组合关键词策略
- 多模态内容验证流程
- 科学图片资源库

**clawhub.json：**
```json
{
  "name": "science-article-writer",
  "version": "1.0.0",
  "author": "pengong101",
  "license": "MIT",
  "description": "科普文章写作技能 - 包含图片选取与验证、多模态验证、组合关键词策略",
  "updated": "2026-03-25",
  "features": [
    "组合关键词策略（具体主题 + 机构 + 类型）",
    "多模态内容验证（qwen3.5-plus）",
    "匹配度评分机制（≥7 分通过）",
    "科学图片资源库（NASA/ESA/EHT/ESO）",
    "自动重试机制（最多 3 次）"
  ]
}
```

---

### 2. radar-daily-report v2.5 🔄 更新

**当前版本：** v2.4

**更新内容：**
- 搜索范围：7天 → 24小时
- 最大年龄：365天 → 14天
- 跨日去重：自动过滤昨日报纸 URL
- 财经过滤：过滤股票/涨跌/IPO
- 5G过滤：过滤纯5G通信内容

**Changelog：**
```
v2.5 (2026-03-25):
- 新增：SEARCH_TIME_RANGE = "day" (24小时)
- 新增：MAX_AGE_DAYS = 14
- 新增：_load_yesterday_urls() 跨日去重
- 新增：_is_finance_news() 财经过滤
- 新增：_is_5g_only() 5G过滤
- 修复：内容质量（0财经、0重复）
```

---

### 3. ai-humanizer-cn v5.1.1 🔄 可选更新

**当前版本：** v5.1.0

**建议更新：**
- 与 science-article-writer 集成
- 添加图片上下文理解

---

## 📋 发布任务清单（6:00-9:00）

### 6:00-7:00 science-article-writer v1.0.0

- [ ] 创建 clawhub.json
- [ ] 验证 SKILL.md 完整性
- [ ] 发布到 GitHub Release
- [ ] 更新 MEMORY.md

### 7:00-8:00 radar-daily-report v2.5

- [ ] 更新 generate-report.py 版本注释
- [ ] 更新 clawhub.json changelog
- [ ] 发布到 GitHub Release
- [ ] 更新 MEMORY.md

### 8:00-9:00 测试验证

- [ ] 验证 radar-daily-report v2.5 生成正常
- [ ] 验证 science-article-writer 图片选取流程

---

## 🔧 其他技能状态

| 技能 | 版本 | 状态 | 备注 |
|------|------|------|------|
| ai-humanizer-cn | v5.1.0 | ✅ 正常 | 可选更新 |
| qc-evaluator | v3.0 | ✅ 正常 | 多模态已配置 |
| secretary-core | v4.1.0 | ✅ 正常 | 模型路由已配置 |
| searxng-auto-proxy | v3.0.0 | ✅ 正常 | - |
| multi-search-engine | v2.0.1 | ✅ 正常 | - |

---

## 📝 更新日志模板

### science-article-writer v1.0.0

```markdown
# Science Article Writer v1.0.0

**日期：** 2026-03-25

## 新功能

- ✅ 组合关键词策略
- ✅ 多模态内容验证
- ✅ 匹配度评分机制
- ✅ 科学图片资源库
- ✅ 自动重试机制

## 使用方式

```bash
# 调用技能
使用 science-article-writer 技能的图片选取流程
```
```

### radar-daily-report v2.5

```markdown
# Radar Daily Report v2.5

**日期：** 2026-03-25

## 改进

- 搜索范围：7天 → 24小时
- 最大年龄：365天 → 14天
- 跨日去重：过滤昨日报纸 URL
- 财经过滤：过滤股票/涨跌/IPO
- 5G过滤：过滤纯5G通信

## 质量提升

| 指标 | v2.4 | v2.5 |
|------|-------|-------|
| 内容新鲜度 | 7天 | 24小时 |
| 跨日重复 | 有 | 0 |
| 财经常见 | 有 | 0 |
```

---

## ⏰ 执行时间

- **6:00** 启动文章生产 cron
- **6:00-7:00** 发布 science-article-writer
- **7:00-8:00** 发布 radar-daily-report v2.5
- **8:00-9:00** 测试验证
- **9:00** 雷达日报 cron

---

**维护者：** 小马 🐴  
**状态：** 📋 待执行
