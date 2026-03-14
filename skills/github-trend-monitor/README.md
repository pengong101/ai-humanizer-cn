# GitHub Trend Monitor

**版本：** v1.0.0  
**作者：** pengong101  
**许可证：** MIT

---

## 📖 简介

GitHub Trend Monitor 是一个实时监控 GitHub Trending 的工具，提供中文摘要生成和热点推送功能。

### 核心功能

- ✅ 实时获取 GitHub Trending
- ✅ 关键词过滤
- ✅ 编程语言过滤
- ✅ 中文摘要生成
- ✅ 历史数据保存
- ✅ 通知推送

---

## 🚀 快速开始

### 安装

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/pengong101/github-trend-monitor.git
```

### 使用

```bash
# 运行监控
python3 monitor.py

# 查看配置
python3 monitor.py config

# 设置关键词
python3 monitor.py set keywords "['AI','OpenClaw','agent']"

# 查看历史
python3 monitor.py history
```

---

## 📋 API 使用

```python
from monitor import GitHubTrendMonitor

# 初始化
monitor = GitHubTrendMonitor()

# 运行监控
summary = monitor.run()
print(summary)

# 获取历史
history = monitor.load_history(days=7)
```

---

## 🔧 配置

创建 `~/.openclaw/trend-monitor.json`:

```json
{
  "keywords": ["AI", "OpenClaw", "agent", "automation"],
  "languages": ["Python", "JavaScript", "TypeScript"],
  "since": "daily",
  "notify": true,
  "summary_language": "zh-CN"
}
```

---

## 📝 更新日志

### v1.0.0 (2026-03-14)

- 初始版本发布
- GitHub Trending 获取
- 关键词/语言过滤
- 中文摘要生成
- 历史数据保存

---

## 📄 许可证

MIT License
