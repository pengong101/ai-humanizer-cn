# 🚀 手动发布指南（GitHub Release）

**原因：** ClawHub 发布遇到问题，使用 GitHub Release 作为备选

---

## 📦 发布步骤

### 1. 创建 GitHub Release

访问：https://github.com/小马 🐴/openclaw-plugin-searxng/releases/new

**Tag version:** `v1.0.0`  
**Release title:** `OpenClaw SearXNG Plugin v1.0.0`  
**Description:**
```markdown
## 🎉 OpenClaw SearXNG Plugin v1.0.0

Privacy-focused web search with China optimization!

### ✨ Features

- 🔒 Privacy-first search (no tracking)
- 🇨🇳 China-optimized (Baidu/Bing CN support)
- ⚡ Fast response with Redis caching
- 🔄 Multi-engine load balancing
- 📦 Easy Docker deployment

### 📦 Installation

#### Option 1: Docker (Recommended)

```bash
# Deploy SearXNG
docker run -d --name searxng -p 8081:8080 searxng/searxng:latest

# Enable JSON API
docker exec searxng sed -i '77 a\    - json' /etc/searxng/settings.yml
docker restart searxng

# Configure OpenClaw
{
  "plugins": {
    "searxng": {
      "enabled": true,
      "baseUrl": "http://localhost:8081"
    }
  }
}
```

#### Option 2: Manual Install

```bash
git clone https://github.com/小马 🐴/openclaw-plugin-searxng.git
cd openclaw-plugin-searxng
openclaw plugins install -l .
```

### 📚 Documentation

- [Deployment Guide](https://github.com/小马 🐴/openclaw-searxng-search/docs/DEPLOYMENT-GUIDE.md)
- [Integration Guide](https://github.com/小马 🐴/openclaw-searxng-search/docs/INTEGRATION-GUIDE.md)
- [Troubleshooting](https://github.com/小马 🐴/openclaw-searxng-search/docs/TROUBLESHOOTING.md)

### 🐛 Known Issues

- ClawHub publishing pending (server issues)

### 📝 Changelog

- Initial release
- China optimization (Baidu/Bing CN)
- Docker deployment support
- Complete documentation

### 📄 License

MIT License
```

### 2. 上传文件

**上传：**
- [x] Source code (auto-generated)
- [ ] openclaw-searxng-plugin.skill (如有)
- [ ] Installation guide PDF

### 3. 发布

点击 **Publish release**

---

## 📢 宣传推广

### 社交媒体

**Twitter:**
```
🎉 Released OpenClaw SearXNG Plugin v1.0.0!

Privacy-focused search with China optimization:
✅ Baidu/Bing CN support
✅ Docker deployment
✅ No tracking

Get it: https://github.com/小马 🐴/openclaw-plugin-searxng/releases

#OpenClaw #SearXNG #Privacy #SelfHosted
```

**Discord (OpenClaw):**
```
Hi everyone! 👋

I've released a SearXNG plugin for OpenClaw with China optimization:

🔗 https://github.com/小马 🐴/openclaw-plugin-searxng/releases/tag/v1.0.0

Features:
- Privacy-first search
- Baidu/Bing CN support
- Easy Docker deployment
- Complete documentation

Would love your feedback! 🙏
```

**知乎/公众号:**
```
【新品发布】OpenClaw SearXNG 插件 v1.0.0

专为中文用户优化的隐私搜索引擎插件！

特点：
✅ 支持百度/必应中国
✅ Docker 一键部署
✅ 无追踪保护隐私
✅ 完整中文文档

地址：https://github.com/小马 🐴/openclaw-plugin-searxng/releases/tag/v1.0.0

欢迎试用和反馈！
```

---

## 📊 监控指标

### GitHub 指标

- ⭐ Star 数
- 🍴 Fork 数
- 👁️ 观看次数
- 📥 下载量
- 💬 Issues 数

### 用户反馈

- GitHub Issues
- Discord 反馈
- 社交媒体评论
- 直接邮件

---

## 🔄 后续更新

### v1.0.1 (Bug 修复)

**触发条件：** 收到 Bug 报告  
**响应时间：** 24 小时内

### v1.1.0 (功能更新)

**计划：** 2026-03-18  
**内容：**
- 添加 360 搜索
- 添加搜狗搜索
- 性能优化

### v1.2.0 (缓存优化)

**计划：** 2026-03-25  
**内容：**
- Redis 缓存
- 自定义配置
- 搜索历史

---

**发布后立即执行：**
1. 社交媒体宣传
2. Discord 分享
3. 监控用户反馈
4. 准备迭代更新

---

**状态：** ⏳ 等待 ClawHub 问题解决后执行
