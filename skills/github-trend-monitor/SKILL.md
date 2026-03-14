---
name: github-trend-monitor
description: GitHub 热点监控工具，实时获取 Trending 项目，中文摘要生成，关键词过滤，热点推送。
license: MIT
version: 1.0.0
---

# GitHub Trend Monitor

**版本：** v1.0.0  
**作者：** pengong101

---

## 🎯 功能

- ✅ 实时获取 GitHub Trending
- ✅ 关键词过滤
- ✅ 编程语言过滤
- ✅ 中文摘要生成
- ✅ 历史数据保存
- ✅ 通知推送

---

## 🚀 安装

```bash
openclaw skills install github-trend-monitor
```

---

## 📖 使用

```bash
# 运行监控
python3 monitor.py

# 查看配置
python3 monitor.py config

# 设置关键词
python3 monitor.py set keywords "['AI','OpenClaw']"
```

### Python API

```python
from monitor import GitHubTrendMonitor

monitor = GitHubTrendMonitor()
summary = monitor.run()
print(summary)
```

---

## 🔧 配置

`~/.openclaw/trend-monitor.json`:

```json
{
  "keywords": ["AI", "OpenClaw", "agent"],
  "languages": ["Python", "JavaScript"],
  "since": "daily",
  "notify": true
}
```

---

## 📝 更新日志

### v1.0.0 (2026-03-14)

- 初始版本发布
- GitHub Trending 监控
- 中文摘要生成

---

## 📄 许可证

MIT
