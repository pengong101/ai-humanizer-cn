# 🔍 搜索功能部署计划

**目标：** 部署搜索功能，用于情报资料获取  
**基于：** GitHub 现有工程  
**日期：** 2026-03-09  
**执行：** 小马 🐴 (CEO 智能体)

---

## 📦 现有 GitHub 工程分析

### 1. openclaw-toolkit（旗舰项目）

**仓库:** https://github.com/小马 🐴/openclaw-toolkit

**文件结构:**
```
├── .gitignore
├── LICENSE
├── README.md
└── packages/
    └── nas-connector/
        ├── README.md
        ├── jisu-api.js
        ├── package.json
        └── sftp-sync.js
```

**状态:** ✅ 有基础框架，需要集成搜索功能

---

### 2. openclaw-plugin-searxng（搜索插件）

**仓库:** https://github.com/小马 🐴/openclaw-plugin-searxng

**文件结构:**
```
├── .gitignore
├── LICENSE
├── README.md
├── RELEASE-v1.0.0.md
└── docs/
    └── DEPLOYMENT.md
```

**状态:** ✅ 插件已创建，需要完善和部署

---

### 3. openclaw-searxng-search（搜索部署）

**仓库:** https://github.com/小马 🐴/openclaw-searxng-search

**文件结构:**
```
├── .gitignore
├── LICENSE
├── README.md
└── docs/
    ├── DEPLOYMENT-GUIDE.md
    ├── INTEGRATION-GUIDE.md
    ├── TEST-REPORT.md
    └── USE-CASES.md
```

**状态:** ✅ 文档齐全，需要实际部署

---

## 🎯 部署方案（3 选 1）

### 方案 A：使用 SearXNG 公共实例（最快，5 分钟）🔴

**优势:**
- ✅ 无需部署
- ✅ 立即可用
- ✅ 隐私保护

**劣势:**
- ⚠️ 可能不稳定
- ⚠️ 速度受限

**部署步骤:**

```bash
# Step 1: 配置 OpenClaw
# 编辑 ~/.openclaw/openclaw.json，添加：
{
  "tools": {
    "web": {
      "search": {
        "provider": "brave",
        "baseUrl": "https://searx.be",
        "apiKey": "dummy-key"
      }
    }
  }
}

# Step 2: 重启 Gateway
openclaw gateway restart

# Step 3: 测试搜索
# 在对话中发送："搜索 2026 毫米波雷达研究进展"
```

**推荐度:** ⭐⭐⭐⭐（立即可用）

---

### 方案 B：自建 SearXNG（推荐，30 分钟）🔴

**优势:**
- ✅ 完全自控
- ✅ 可定制搜索引擎
- ✅ 稳定可靠

**劣势:**
- ⚠️ 需要 Docker

**部署步骤:**

```bash
# Step 1: 检查 Docker
docker --version

# Step 2: 创建部署目录
mkdir -p ~/searxng && cd ~/searxng

# Step 3: 创建 docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  searxng:
    image: searxng/searxng:latest
    ports:
      - "8080:8080"
    environment:
      - SEARXNG_BASE_URL=http://localhost:8080
      - SEARCH_LIMIT=10
    volumes:
      - ./settings.yml:/etc/searxng/settings.yml:rw
    restart: unless-stopped
EOF

# Step 4: 创建 settings.yml
cat > settings.yml << 'EOF'
use_default_settings: true
search:
  formats:
    - html
    - json
server:
  secret_key: "xiaoma-secret-key-2026"
  limiter: false
  image_proxy: true
engines:
  - name: bing
    engine: bing
    shortcut: b
    disabled: false
  - name: google
    engine: google
    shortcut: g
    disabled: false
  - name: baidu
    engine: baidu
    shortcut: bd
    disabled: false
EOF

# Step 5: 启动 SearXNG
docker-compose up -d

# Step 6: 测试
curl "http://localhost:8080/search?q=test&format=json"

# Step 7: 配置 OpenClaw
# 编辑 ~/.openclaw/openclaw.json，添加：
{
  "tools": {
    "web": {
      "search": {
        "provider": "brave",
        "baseUrl": "http://localhost:8765",
        "apiKey": "dummy-key"
      }
    }
  }
}

# Step 8: 重启 Gateway
openclaw gateway restart
```

**推荐度:** ⭐⭐⭐⭐⭐（长期方案）

---

### 方案 C：使用 DuckDuckGo HTML（无需 Docker，1 分钟）🔴

**优势:**
- ✅ 无需部署
- ✅ 中国大陆可用
- ✅ 代码已有

**劣势:**
- ⚠️ 功能有限

**部署步骤:**

```bash
# Step 1: 启动适配器
cd /root/.openclaw/workspace/openserp-brave-adapter
node index-cn-v2.js &

# Step 2: 测试
wget -qO- http://localhost:8765/health

# Step 3: 配置 OpenClaw
# 编辑 ~/.openclaw/openclaw.json，添加：
{
  "tools": {
    "web": {
      "search": {
        "provider": "brave",
        "baseUrl": "http://localhost:8765",
        "apiKey": "dummy-key"
      }
    }
  }
}

# Step 4: 重启 Gateway
openclaw gateway restart
```

**推荐度:** ⭐⭐⭐⭐（快速可用）

---

## 🚀 推荐执行计划

### 阶段 1：立即部署（5 分钟）🔴

**目标：** 快速恢复搜索能力

**方案:** 使用 SearXNG 公共实例

```bash
# 1. 配置 OpenClaw
# 2. 重启 Gateway
# 3. 测试搜索
```

**交付:** 可用的搜索功能

---

### 阶段 2：自建 SearXNG（30 分钟）🟡

**目标：** 稳定的搜索服务

**方案:** Docker 部署 SearXNG

```bash
# 1. 部署 SearXNG
# 2. 配置搜索引擎
# 3. 测试和验证
# 4. 配置 OpenClaw
```

**交付:** 自托管搜索服务

---

### 阶段 3：完善 GitHub 工程（1 小时）🟢

**目标：** 完善现有仓库

**任务:**
- [ ] 更新 openclaw-toolkit 集成搜索
- [ ] 完善 openclaw-plugin-searxng 文档
- [ ] 更新 openclaw-searxng-search 部署指南
- [ ] 创建 Release v1.0.0

**交付:** 完整的搜索工具链

---

## 📊 情报资料获取场景

### 1. 技术研究情报

**搜索关键词:**
- "2026 毫米波雷达 研究进展"
- "6G 通信技术 最新"
- "AI 芯片 技术突破"
- "相控阵雷达 民用"

**用途:**
- 技术趋势分析
- 研究方向选择
- 竞品分析

---

### 2. 投资研究情报

**搜索关键词:**
- "半导体 ETF 分析"
- "AI 概念股 估值"
- "雷达上市公司"
- "通信行业 投资报告"

**用途:**
- 行业研究
- 投资标的筛选
- 风险评估

---

### 3. 内容创作情报

**搜索关键词:**
- "科技热点 2026"
- "科普视频 创意"
- "抖音 科技博主"
- "B 站 科普 爆款"

**用途:**
- 选题策划
- 内容优化
- 竞品分析

---

## 🔧 OpenClaw 配置

### 完整配置示例

编辑 `~/.openclaw/openclaw.json`:

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "bailian": {
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "apiKey": "sk-sp-8e9b8f63afc44bc4a2ce31ddfbf23430",
        "api": "openai-completions",
        "models": [
          {
            "id": "qwen3.5-plus",
            "name": "Qwen3.5-Plus",
            "reasoning": true,
            "input": ["text", "image"],
            "cost": {"input": 0, "output": 0},
            "contextWindow": 1000000,
            "maxTokens": 65536
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "bailian/qwen3.5-plus"
      }
    }
  },
  "commands": {
    "native": "auto",
    "nativeSkills": "auto",
    "restart": true,
    "ownerDisplay": "raw"
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "dmPolicy": "open",
      "allowFrom": [
        "ou_108c6b29eb9946e2cf1090f76fdd6f17",
        "ou_21b87bbbcb0a643b2e6e5976c02c580c"
      ],
      "groupPolicy": "open",
      "connectionMode": "websocket",
      "accounts": {
        "main": {
          "appId": "cli_a92012e60cf9dcc0",
          "appSecret": "UbK9vNsfxJtrCobOnep9WbaHWO1dp3E0",
          "botName": "小马 AI 助手",
          "enabled": true
        }
      }
    }
  },
  "gateway": {
    "mode": "local",
    "auth": {
      "mode": "token",
      "token": "xiaoma-token-2026"
    }
  },
  "plugins": {
    "entries": {
      "feishu": {
        "enabled": true
      }
    }
  },
  "tools": {
    "web": {
      "search": {
        "provider": "brave",
        "baseUrl": "http://localhost:8765",
        "apiKey": "dummy-key"
      }
    }
  }
}
```

---

## ✅ 验收标准

### 功能验收

- [ ] 可以在对话中执行搜索
- [ ] 搜索结果格式正确
- [ ] 支持中文搜索
- [ ] 响应时间 < 5 秒

### 情报告景验收

- [ ] 搜索"毫米波雷达"返回相关结果
- [ ] 搜索"AI 芯片"返回相关结果
- [ ] 搜索"半导体 ETF"返回相关结果

### GitHub 工程验收

- [ ] openclaw-toolkit 集成搜索
- [ ] openclaw-plugin-searxng 文档完善
- [ ] openclaw-searxng-search 可部署

---

## 📝 立即执行

**推荐方案:** 方案 A（公共实例）+ 方案 B（自建）并行

**步骤:**

1. **立即配置公共实例**（5 分钟）
   - 修改 OpenClaw 配置
   - 重启 Gateway
   - 测试搜索

2. **同时部署 SearXNG**（30 分钟）
   - Docker 部署
   - 配置优化
   - 切换配置

3. **完善 GitHub 工程**（1 小时）
   - 更新文档
   - 创建 Release
   - 推送代码

---

**需要我立即执行吗？** 🐴

**请选择:**
- [ ] 方案 A：使用公共实例（最快）
- [ ] 方案 B：自建 SearXNG（推荐）
- [ ] 方案 C：DuckDuckGo HTML（无需 Docker）
