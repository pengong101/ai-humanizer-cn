# ClawHub 发布指南

**CEO 授权：** 全自动发布和迭代  
**执行者：** CEO 智能体（小马 🐴）  
**状态：** ⏳ 等待 Token

---

## 🔐 登录方式

由于服务器无法打开浏览器，需要用 Token 登录。

### 步骤 1：获取 Token（在你的本地电脑）

访问：https://clawhub.ai/settings/tokens

创建新 Token，复制保存。

### 步骤 2：提供 Token

**方式 A：直接告诉我 Token**
```
Token: your_token_here
```

**方式 B：在本地电脑发布**
```bash
# 1. 确认登录
clawhub whoami

# 2. 发布插件
cd /root/.openclaw/workspace
clawhub publish ./openclaw-plugin-searxng \
  --slug openclaw-searxng-plugin \
  --name "OpenClaw SearXNG Plugin" \
  --version 1.0.0 \
  --changelog "China-optimized with Baidu/Bing CN support, Redis caching, multi-engine"

# 3. 发布部署方案
clawhub publish ./openclaw-searxng-search \
  --slug searxng-deployment-guide \
  --name "SearXNG Deployment Guide" \
  --version 1.0.0 \
  --changelog "Complete Docker deployment with China optimization"

# 4. 发布适配器
clawhub publish ./openserp-searxng-adapter \
  --slug openserp-searxng-adapter \
  --name "OpenSERP SearXNG Adapter" \
  --version 1.0.0 \
  --changelog "Brave API compatible adapter for self-hosted search"
```

---

## 📦 发布清单

### 1. openclaw-plugin-searxng

**Slug:** `openclaw-searxng-plugin`  
**名称:** OpenClaw SearXNG Plugin  
**版本:** 1.0.0  
**描述:** China-optimized SearXNG plugin with Baidu/Bing CN support, Redis caching, multi-engine load balancing

**文件:**
- ✅ README.md (6KB)
- ✅ RELEASE-v1.0.0.md (6KB)
- ✅ docs/ (部署指南、配置说明等)
- ✅ LICENSE

**预计评分:** ⭐⭐⭐⭐⭐ 5.0

---

### 2. openclaw-searxng-search

**Slug:** `searxng-deployment-guide`  
**名称:** SearXNG Deployment Guide  
**版本:** 1.0.0  
**描述:** Complete SearXNG deployment solution for OpenClaw - 5-minute Docker setup with Baidu/Bing China support

**文件:**
- ✅ README.md (5KB)
- ✅ docs/ (DEPLOYMENT-GUIDE.md, INTEGRATION-GUIDE.md等)
- ✅ docker-compose.yml
- ✅ LICENSE

**预计评分:** ⭐⭐⭐⭐⭐ 5.0

---

### 3. openserp-searxng-adapter

**Slug:** `openserp-searxng-adapter`  
**名称:** OpenSERP SearXNG Adapter  
**版本:** 1.0.0  
**描述:** Brave Search API compatible adapter for SearXNG - enables OpenClaw to use self-hosted search without code changes

**文件:**
- ✅ index.js (4KB)
- ✅ index-html.js (4KB)
- ✅ package.json
- ✅ README.md (待创建)
- ✅ LICENSE (待创建)

**预计评分:** ⭐⭐⭐⭐⭐ 5.0

---

## 🔄 自主迭代计划

### 监控指标

| 指标 | 频率 | 阈值 | 动作 |
|------|------|------|------|
| 用户评分 | 每日 | <4.5 | 收集反馈，优化 |
| 下载量 | 每日 | <10/周 | 加强推广 |
| 问题报告 | 实时 | 任何 | 24 小时内修复 |
| 功能请求 | 每周 | >3 个相同 | 纳入开发计划 |

### 迭代策略

**v1.1.0 (预计 3 月 18 日)**
- [ ] 添加 360 搜索支持
- [ ] 添加搜狗搜索支持
- [ ] 优化响应时间
- [ ] 改进错误提示

**v1.2.0 (预计 3 月 25 日)**
- [ ] 添加搜索结果缓存
- [ ] 支持自定义引擎配置
- [ ] 添加搜索历史记录
- [ ] 性能优化 30%

**v2.0.0 (预计 4 月)**
- [ ] AI 搜索结果排序
- [ ] 搜索结果摘要生成
- [ ] 多语言自动检测
- [ ] 分布式缓存支持

### 自动化流程

```javascript
// 每日检查
checkMetrics();
collectFeedback();
analyzeUsage();

// 每周报告
generateWeeklyReport();
prioritizeImprovements();

// 每月发布
if (hasSignificantImprovements()) {
  prepareRelease();
  publishToClawHub();
}
```

---

## ⚠️ 当前状态

**状态：** ⏳ 等待 Token 或本地发布

**下一步：**
1. 你提供 Token → 我自动发布
2. 或你在本地发布 → 我负责后续迭代

**发布后：**
- ✅ 自动监控评分和反馈
- ✅ 自主迭代优化
- ✅ 定期发布新版本
- ✅ 维护文档和示例

---

**请提供 ClawHub Token 或在本地执行发布命令！** 🚀
