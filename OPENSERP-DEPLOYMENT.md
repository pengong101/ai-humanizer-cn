# OpenSERP 部署指南

**更新时间：** 2026-03-06  
**目的：** 部署 OpenSERP 后端服务，配合 Brave Adapter 使用

---

## 📦 什么是 OpenSERP

OpenSERP 是开源的搜索引擎 API 服务，可以：
- 聚合多个搜索引擎结果（Google、Bing、DuckDuckGo 等）
- 提供统一的 API 接口
- 自托管，数据可控

---

## 🚀 部署方案

### 方案 A：Docker 部署（推荐）

#### 1. 使用官方镜像（如有）

```bash
docker run -d \
  -p 8080:8080 \
  -e API_KEY=your-api-key \
  -e SEARCH_PROVIDERS=google,bing \
  --name openserp \
  openserp/openserp:latest
```

#### 2. 使用开源替代方案

由于 OpenSERP 官方镜像可能不可用，推荐使用以下替代：

**Option 1: SearXNG（推荐）**

```bash
# Docker Compose 部署 SearXNG
cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  searxng:
    image: searxng/searxng:latest
    ports:
      - "8080:8080"
    environment:
      - SEARXNG_BASE_URL=http://localhost:8080
    volumes:
      - ./searxng-config:/etc/searxng
    restart: unless-stopped
EOF

docker-compose up -d
```

**配置 OpenSERP Brave Adapter 使用 SearXNG：**

```bash
# 修改适配器配置
export OPENSERP_BASE_URL=http://localhost:8080

# SearXNG API 端点
# http://localhost:8080/search?q=query&format=json
```

**Option 2: selfsearch / search-api**

```bash
# 其他开源搜索引擎 API
docker run -d -p 8080:3000 benbusby/selfsearch
```

---

### 方案 B：使用现有搜索服务

如果有其他可用的搜索 API 服务，可以直接配置适配器：

| 服务 | 配置 |
|------|------|
| SearXNG | `OPENSERP_BASE_URL=http://your-searxng:8080` |
| Google Custom Search | 需要适配层 |
| Bing Search API | 需要适配层 |

---

### 方案 C：使用 Brave API（临时方案）

在 OpenSERP 部署前，直接使用 Brave API：

```bash
# 1. 获取 Brave API Key
# https://brave.com/search/api/ (免费 2000 次/月)

# 2. 配置 OpenClaw
openclaw configure --section web

# 3. 或直接修改配置
{
  "tools": {
    "web": {
      "search": {
        "provider": "brave",
        "apiKey": "YOUR_BRAVE_API_KEY"
      }
    }
  }
}
```

---

## 🔧 适配器适配不同后端

OpenSERP Brave Adapter 已支持多种响应格式：

```javascript
// 在 index.js 中自动检测
if (openserpData.results) { ... }      // OpenSERP 格式
else if (openserpData.organic) { ... } // Google 格式
else if (openserpData.data) { ... }    // 通用格式
```

如需适配特定后端，修改 `transformToBraveFormat` 函数即可。

---

## 📋 部署检查清单

- [ ] 选择部署方案（SearXNG 推荐）
- [ ] 部署搜索后端服务
- [ ] 测试后端 API：`curl http://localhost:8080/search?q=test`
- [ ] 更新适配器配置：`export OPENSERP_BASE_URL=http://your-backend:8080`
- [ ] 重启适配器
- [ ] 测试适配器：`curl http://localhost:8765/search?q=test`
- [ ] 测试 OpenClaw：在对话中搜索

---

## 🧪 测试命令

```bash
# 1. 测试后端
curl "http://localhost:8080/search?q=test&format=json"

# 2. 测试适配器
wget -qO- "http://localhost:8765/search?q=test&count=3"

# 3. 测试 OpenClaw
# 在飞书对话中发送："搜索 2026 毫米波技术"
```

---

## 🐛 故障排查

### 问题 1：后端返回 HTML 而非 JSON

**原因：** 后端未正确配置或未运行

```bash
# 检查后端状态
curl -v http://localhost:8080/search?q=test

# 查看适配器日志
docker logs openserp-adapter
```

### 问题 2：适配器连接超时

**原因：** 网络不通或地址错误

```bash
# 测试连通性
ping your-backend-host

# 检查防火墙
iptables -L -n | grep 8080
```

### 问题 3：OpenClaw 不使用适配器

**原因：** 配置未生效

```bash
# 检查配置
openclaw config.get | grep -A5 search

# 重启 Gateway
openclaw gateway restart
```

---

## 📞 推荐方案总结

| 方案 | 难度 | 时间 | 成本 | 推荐度 |
|------|------|------|------|--------|
| SearXNG Docker | ⭐⭐ | 30 分钟 | 免费 | ⭐⭐⭐⭐⭐ |
| Brave API 直接 | ⭐ | 5 分钟 | 免费额度 | ⭐⭐⭐⭐ |
| 自建 OpenSERP | ⭐⭐⭐⭐ | 2 小时 | 免费 | ⭐⭐⭐ |

**立即可用：** 先使用 Brave API 测试，同时部署 SearXNG 作为长期方案。

---

## 🔗 相关资源

- [SearXNG 官方文档](https://docs.searxng.org/)
- [Brave Search API](https://brave.com/search/api/)
- [OpenSERP Brave Adapter](https://github.com/小马 🐴/openserp-brave-adapter)

---

**部署有问题？联系小马 🐴**
