# 🔍 SearXNG 搜索插件配置指南

**项目：** OpenSERP Brave Adapter  
**GitHub:** https://github.com/小马 🐴/openserp-brave-adapter  
**更新时间：** 2026-03-09 13:18 (Asia/Shanghai)

---

## ✅ 是否已配备 SearXNG？

**答案：** ⚠️ **代码已支持，但未实际部署**

### 当前状态

| 组件 | 状态 | 说明 |
|------|------|------|
| 适配器代码 | ✅ 已部署 | 支持 SearXNG 后端 |
| SearXNG 服务 | ❌ 未运行 | 需要 Docker 部署 |
| 配置文件 | ✅ 已准备 | 本地有完整配置文档 |
| GitHub 仓库 | ✅ 已发布 | 包含部署说明 |

---

## 📋 SearXNG 配置方法

### 方案 1：自建 SearXNG（推荐，30 分钟）

**前提条件：** Docker + Docker Compose

#### Step 1: 创建目录

```bash
mkdir -p ~/searxng && cd ~/searxng
```

#### Step 2: 创建 docker-compose.yml

```yaml
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
```

#### Step 3: 创建配置文件 (settings.yml)

```yaml
use_default_settings: true
search:
  formats:
    - html
    - json
server:
  secret_key: "your-secret-key-2026"
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
  - name: duckduckgo
    engine: duckduckgo
    shortcut: ddg
    disabled: false
```

#### Step 4: 启动 SearXNG

```bash
docker-compose up -d
```

#### Step 5: 验证安装

```bash
# 测试 SearXNG
curl "http://localhost:8080/search?q=test&format=json"

# 查看日志
docker-compose logs -f
```

#### Step 6: 配置适配器

```bash
cd /root/.openclaw/workspace/openserp-brave-adapter

# 停止当前适配器
# (找到进程号后 kill)

# 重启适配器指向 SearXNG
export OPENSERP_BASE_URL=http://localhost:8080
node index.js &
```

#### Step 7: 测试完整链路

```bash
# 测试适配器
wget -qO- "http://localhost:8765/search?q=test&count=5"

# 在 OpenClaw 中测试
# 发送消息："搜索 2026 毫米波研究进展"
```

---

### 方案 2：使用公共 SearXNG 实例（临时，5 分钟）

**适合：** 快速测试，无需部署

#### 可用实例

| 实例 | 地址 | 中国大陆访问 | 推荐度 |
|------|------|-------------|--------|
| 日本 | https://search.ononoki.org | ⚠️ 可能慢 | ⭐⭐⭐ |
| 欧洲 | https://searx.be | ❌ 超时 | ⭐⭐ |
| 台湾 | https://searx.tw | ⚠️ 测试中 | ⭐⭐ |

#### 配置方法

```bash
cd /root/.openclaw/workspace/openserp-brave-adapter

# 使用日本实例
export OPENSERP_BASE_URL=https://search.ononoki.org
node index.js &

# 测试
wget -qO- "http://localhost:8765/health"
wget -qO- "http://localhost:8765/search?q=test&count=3"
```

---

### 方案 3：使用中国大陆专用版本（无需 SearXNG）

**适合：** 中国大陆用户，无需 Docker

#### 使用 DuckDuckGo HTML 接口

```bash
cd /root/.openclaw/workspace/openserp-brave-adapter

# 启动中国大陆版本
node index-cn-v2.js &

# 测试
wget -qO- "http://localhost:8765/health"
wget -qO- "http://localhost:8765/search?q=mmWave+radar&count=5"
```

**优点:**
- ✅ 无需 Docker
- ✅ 无需额外部署
- ✅ 中国大陆可访问

**缺点:**
- ⚠️ 搜索结果可能有限
- ⚠️ 依赖 DuckDuckGo HTML 接口稳定性

---

## 🔧 OpenClaw 集成配置

### 修改 OpenClaw 配置

编辑 `~/.openclaw/openclaw.json`：

```json
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
```

### 重启 OpenClaw Gateway

```bash
openclaw gateway restart
```

### 测试搜索

在飞书对话中发送：
> "搜索 2026 毫米波雷达研究进展"

---

## 📊 方案对比

| 方案 | 难度 | 时间 | 成本 | 中国大陆 | 推荐度 |
|------|------|------|------|---------|--------|
| 自建 SearXNG | ⭐⭐ | 30 分钟 | 免费 | ✅ | ⭐⭐⭐⭐⭐ |
| 公共实例 | ⭐ | 5 分钟 | 免费 | ⚠️ | ⭐⭐⭐ |
| 中国大陆版 | ⭐ | 1 分钟 | 免费 | ✅ | ⭐⭐⭐⭐ |
| Brave API | ⭐ | 5 分钟 | 免费额度 | ❌ | ⭐⭐ |

---

## 🐛 故障排查

### 问题 1: Docker 不可用

```bash
# 检查 Docker
docker --version

# 如果没有 Docker，使用中国大陆版本
node index-cn-v2.js
```

### 问题 2: SearXNG 启动失败

```bash
# 查看日志
docker-compose logs

# 检查端口占用
netstat -tlnp | grep 8080

# 修改端口
# 编辑 docker-compose.yml，改为其他端口如 8888
```

### 问题 3: 适配器连接超时

```bash
# 测试 SearXNG 是否可用
curl "http://localhost:8080/search?q=test&format=json"

# 检查适配器配置
echo $OPENSERP_BASE_URL

# 重启适配器
pkill -f "node index.js"
export OPENSERP_BASE_URL=http://localhost:8080
node index.js &
```

---

## 📁 本地配置文件位置

| 文件 | 路径 | 说明 |
|------|------|------|
| 部署指南 | `/root/.openclaw/workspace/OPENSERP-DEPLOYMENT.md` | 完整部署文档 |
| 紧急方案 | `/root/.openclaw/workspace/OPENSERP-EMERGENCY.md` | 中国大陆紧急部署 |
| 适配器代码 | `/root/.openclaw/workspace/openserp-brave-adapter/` | 适配器源码 |
| 项目状态 | `/root/.openclaw/workspace/GITHUB-PROJECT-STATUS.md` | GitHub 项目报告 |

---

## 🔗 相关资源

- **SearXNG 官方文档:** https://docs.searxng.org/
- **GitHub 仓库:** https://github.com/小马 🐴/openserp-brave-adapter
- **SearXNG 公共实例:** https://searx.space/

---

## 🎯 推荐行动

### 立即可用（1 分钟）

```bash
# 启动中国大陆版本
cd /root/.openclaw/workspace/openserp-brave-adapter
node index-cn-v2.js &

# 配置 OpenClaw
# 编辑 ~/.openclaw/openclaw.json 添加 web_search 配置

# 重启 Gateway
openclaw gateway restart
```

### 长期方案（30 分钟）

```bash
# 部署 SearXNG
mkdir -p ~/searxng && cd ~/searxng
# 创建 docker-compose.yml 和 settings.yml
docker-compose up -d

# 配置适配器
export OPENSERP_BASE_URL=http://localhost:8080
node index.js &
```

---

**需要我帮你执行哪个方案？** 🐴
