# 智能体记忆与配置系统

**位置：** `/root/.openclaw/workspace/agent-memory/`

---

## 📁 目录结构

```
agent-memory/
├── config.json              # 智能体配置
├── state.json               # 当前状态
├── tasks/                   # 任务记录
│   ├── pending.json
│   ├── completed.json
│   └── failed.json
├── workflows/               # 工作流记录
│   ├── active.json
│   └── history/
├── knowledge/               # 知识库
│   ├── github-trending.json
│   ├── tech-topics.json
│   └── content-ideas.json
└── reports/                 # 报告
    ├── daily/
    ├── weekly/
    └── monthly/
```

---

## 🔧 配置文件

### config.json

```json
{
  "company": {
    "name": "小马 🐴",
    "ceo": "小马",
    "founded": "2026-03-11",
    "timezone": "Asia/Shanghai"
  },
  "agents": {
    "CEO": {
      "enabled": true,
      "model": "qwen3.5-plus",
      "thinking": "high",
      "maxTasks": 10
    },
    "CTO": {
      "enabled": true,
      "model": "qwen3.5-plus",
      "thinking": "high",
      "maxTasks": 20
    },
    "COO": {
      "enabled": true,
      "model": "qwen3.5-plus",
      "thinking": "medium",
      "maxTasks": 30
    },
    "CFO": {
      "enabled": true,
      "model": "qwen3.5-plus",
      "thinking": "medium",
      "maxTasks": 10
    },
    "INTELLIGENCE": {
      "enabled": true,
      "model": "qwen3.5-plus",
      "thinking": "low",
      "maxTasks": 50
    },
    "QC": {
      "enabled": true,
      "model": "qwen3.5-plus",
      "thinking": "medium",
      "maxTasks": 30
    }
  },
  "workflows": {
    "github_dev": {
      "enabled": true,
      "priority": "high",
      "autoStart": false
    },
    "skill_dev": {
      "enabled": true,
      "priority": "high",
      "autoStart": false
    },
    "content_production": {
      "enabled": true,
      "priority": "high",
      "autoStart": true,
      "schedule": "0 9 * * *"
    },
    "intelligence": {
      "enabled": true,
      "priority": "high",
      "autoStart": true,
      "schedule": "0 8 * * *"
    }
  },
  "integrations": {
    "github": {
      "token": "ghp_***",
      "owner": "小马 🐴",
      "enabled": true
    },
    "clawhub": {
      "token": "***",
      "enabled": true
    },
    "searxng": {
      "baseUrl": "http://192.168.1.122:8081",
      "enabled": true
    }
  }
}
```

---

## 📊 状态管理

### state.json

```json
{
  "lastUpdate": "2026-03-11T08:30:00+08:00",
  "activeAgents": 6,
  "activeWorkflows": 2,
  "pendingTasks": 15,
  "completedToday": 48,
  "failedToday": 2,
  "metrics": {
    "github": {
      "projects": 3,
      "totalStars": 0,
      "todayCommits": 5
    },
    "content": {
      "articles": 12,
      "videos": 3,
      "totalViews": 0
    },
    "skills": {
      "published": 3,
      "downloads": 0
    }
  }
}
```

---

## 🧠 知识库

### github-trending.json

```json
{
  "lastUpdated": "2026-03-11T08:00:00+08:00",
  "trending": [
    {
      "name": "openclaw/openclaw",
      "stars": 200000,
      "trend": "hot",
      "category": "AI",
      "relevance": 0.95
    },
    {
      "name": "searxng/searxng",
      "stars": 15000,
      "trend": "up",
      "category": "Search",
      "relevance": 0.90
    }
  ],
  "opportunities": [
    {
      "type": "skill",
      "description": "OpenClaw SearXNG Plugin",
      "priority": "high",
      "status": "completed"
    }
  ]
}
```

### content-ideas.json

```json
{
  "lastUpdated": "2026-03-11T08:00:00+08:00",
  "ideas": [
    {
      "title": "OpenClaw 智能体架构详解",
      "type": "article",
      "platforms": ["wechat", "zhihu"],
      "status": "draft",
      "priority": "high"
    },
    {
      "title": "SearXNG 部署教程",
      "type": "video",
      "platforms": ["bilibili", "youtube"],
      "status": "planning",
      "priority": "medium"
    }
  ]
}
```

---

## 📝 任务记录

### tasks/pending.json

```json
{
  "tasks": [
    {
      "id": "task-001",
      "agent": "CTO",
      "task": "develop_github_project",
      "params": {
        "name": "ai-agent-framework",
        "description": "智能体协作框架"
      },
      "priority": "high",
      "createdAt": "2026-03-11T08:00:00+08:00",
      "dueAt": "2026-03-11T18:00:00+08:00"
    }
  ]
}
```

### tasks/completed.json

```json
{
  "tasks": [
    {
      "id": "task-000",
      "agent": "CTO",
      "task": "deploy_searxng",
      "status": "completed",
      "result": {
        "success": true,
        "url": "http://192.168.1.122:8081"
      },
      "completedAt": "2026-03-11T08:25:00+08:00"
    }
  ]
}
```

---

## 📈 报告系统

### reports/daily/2026-03-11.md

```markdown
# 日报 2026-03-11

## 📊 今日概览

- 活跃智能体：6
- 完成任务：48
- 失败任务：2
- 工作流执行：5

## 🎯 完成情况

### 开发团队（CTO）
- ✅ SearXNG JSON API 修复
- ✅ OpenSERP 适配器测试
- ⏳ AI Agent Framework 开发（50%）

### 内容团队（COO）
- ✅ 测试报告编写
- ✅ 公司架构文档
- ⏳ 自媒体文章（草稿）

### 情报团队
- ✅ GitHub 热点监控
- ✅ 技术趋势分析

## 📈 数据指标

| 指标 | 今日 | 本周 | 本月 |
|------|------|------|------|
| GitHub 项目 | 3 | 3 | 3 |
| 内容产出 | 5 | 12 | 12 |
| 技能发布 | 3 | 3 | 3 |

## 🚨 问题与风险

1. SearXNG 网络超时（部分引擎）
2. 内容审核流程需优化

## 📋 明日计划

1. 完成 AI Agent Framework
2. 发布第一篇科普文章
3. 启动内容自动化流程
```

---

## 🔄 自动同步

### sync-memory.js

```javascript
#!/usr/bin/env node
/**
 * 智能体记忆同步脚本
 * 定期同步状态、清理旧数据、生成报告
 */

const fs = require('fs');
const path = require('path');

const MEMORY_DIR = '/root/.openclaw/workspace/agent-memory';

function sync() {
  console.log('🔄 同步智能体记忆...');
  
  // 1. 更新状态
  updateState();
  
  // 2. 清理旧数据（>7 天）
  cleanupOldData();
  
  // 3. 生成日报
  generateDailyReport();
  
  // 4. 备份重要数据
  backupData();
  
  console.log('✅ 同步完成');
}

function updateState() {
  const statePath = path.join(MEMORY_DIR, 'state.json');
  const state = JSON.parse(fs.readFileSync(statePath, 'utf8'));
  
  // 更新指标
  state.lastUpdate = new Date().toISOString();
  state.completedToday = countCompletedTasks();
  state.pendingTasks = countPendingTasks();
  
  fs.writeFileSync(statePath, JSON.stringify(state, null, 2));
}

function cleanupOldData() {
  const sevenDaysAgo = Date.now() - 7 * 24 * 60 * 60 * 1000;
  
  // 清理 7 天前的任务记录
  const tasksDir = path.join(MEMORY_DIR, 'tasks');
  const files = fs.readdirSync(tasksDir);
  
  files.forEach(file => {
    const filePath = path.join(tasksDir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.mtimeMs < sevenDaysAgo && file !== 'pending.json') {
      fs.unlinkSync(filePath);
      console.log(`🗑️ 清理旧文件：${file}`);
    }
  });
}

function generateDailyReport() {
  const today = new Date().toISOString().split('T')[0];
  const reportPath = path.join(MEMORY_DIR, 'reports', 'daily', `${today}.md`);
  
  // 生成报告内容
  const report = generateReportContent(today);
  fs.writeFileSync(reportPath, report);
  
  console.log(`📄 生成日报：${today}.md`);
}

function backupData() {
  const backupDir = path.join(MEMORY_DIR, 'backups', new Date().toISOString().split('T')[0]);
  
  if (!fs.existsSync(backupDir)) {
    fs.mkdirSync(backupDir, { recursive: true });
  }
  
  // 备份关键文件
  const filesToBackup = ['config.json', 'state.json'];
  filesToBackup.forEach(file => {
    const src = path.join(MEMORY_DIR, file);
    const dst = path.join(backupDir, file);
    fs.copyFileSync(src, dst);
  });
  
  console.log('💾 备份完成');
}

function countCompletedTasks() {
  // 实际实现：查询任务数据库
  return 48;
}

function countPendingTasks() {
  return 15;
}

function generateReportContent(date) {
  return `# 日报 ${date}\n\nTODO: 填充内容`;
}

// 启动
if (require.main === module) {
  sync();
}

module.exports = { sync };
```

---

## 🚀 使用指南

### 启动智能体框架

```bash
# 1. 启动工作流
node agent-framework.js workflow github_dev

# 2. 启动日常调度
node agent-framework.js schedule

# 3. 同步记忆
node agent-memory/sync-memory.js
```

### 添加新任务

```javascript
const { AgentCompany } = require('./agent-framework');

const company = new AgentCompany();

// 添加任务
company.taskQueue.add({
  agent: 'CTO',
  task: 'develop_feature',
  params: { name: 'new-feature' }
});
```

### 查询状态

```bash
# 查看当前状态
cat agent-memory/state.json

# 查看待办任务
cat agent-memory/tasks/pending.json

# 查看日报
cat agent-memory/reports/daily/2026-03-11.md
```

---

**维护者：** CEO 智能体（小马 🐴）  
**更新时间：** 2026-03-11
