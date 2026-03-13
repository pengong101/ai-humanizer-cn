# 🚨 OpenSERP 紧急部署方案（中国大陆可用）

**更新时间：** 2026-03-06 21:30  
**紧急程度：** 🔴 非常高  
**目标：** 30 分钟内部署可用的搜索 API

---

## 🎯 立即可用方案

### 方案 1：使用国内搜索引擎 API（推荐）

#### 1.1 百度搜索 API（最快）

```bash
# 申请地址：https://ai.baidu.com/tech/search
# 免费额度：每月 5000 次

# 配置适配器使用百度
# 需要修改 index.js 添加百度支持
```

#### 1.2 必应中国 API

```bash
# Azure Bing Search API
# 有免费额度，国内可用
# https://azure.microsoft.com/zh-cn/products/cognitive-services/bing-web-search-api/
```

---

### 方案 2：自建 SearXNG（30 分钟）

**步骤：**

```bash
# 1. 创建目录
mkdir -p ~/searxng && cd ~/searxng

# 2. 创建 docker-compose.yml
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

# 3. 创建配置文件
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
EOF

# 4. 启动
docker-compose up -d

# 5. 测试
curl "http://localhost:8080/search?q=test&format=json"
```

**配置适配器：**

```bash
# 停止当前适配器
# 重启指向本地 SearXNG
export OPENSERP_BASE_URL=http://localhost:8080
node index.js
```

---

### 方案 3：使用国内公开实例（临时）

**国内可访问的 SearXNG 实例：**

| 实例 | 地址 | 状态 |
|------|------|------|
| 台湾 | https://searx.tw | 测试中 |
| 日本 | https://search.ononoki.org | 可用 |
| 欧洲 | https://searx.be | 可能慢 |

**立即测试：**

```bash
# 使用日本实例
export OPENSERP_BASE_URL=https://search.ononoki.org
node index.js &

# 测试
curl "http://localhost:8765/search?q=test"
```

---

## 🚀 小马紧急执行计划

### 阶段 1（5 分钟）：测试国内实例

```bash
# 测试日本实例
wget -qO- "http://localhost:8765/search?q=毫米波+radar&count=5"
```

### 阶段 2（30 分钟）：自建 SearXNG

如果公共实例不可用，立即自建。

### 阶段 3（10 分钟）：OpenClaw 集成

配置完成后立即测试搜索功能。

---

## 📋 当前状态

- [x] OpenSERP Brave Adapter 已部署
- [ ] 搜索后端可用（进行中）
- [ ] OpenClaw web_search 可用
- [ ] 执行搜索任务

---

## 🔧 立即行动

**请选择：**

1. **测试国内公共实例** - 我立即尝试日本/台湾实例
2. **自建 SearXNG** - 我帮你部署（需要 Docker）
3. **申请百度 API** - 我指导你快速申请

**情报官待命，等待指令！** 🐴
