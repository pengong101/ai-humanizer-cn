# OpenSERP Brave Adapter

将 OpenSERP 搜索结果转换为 **Brave Search API 兼容格式**，使 OpenClaw 等工具无需修改源码即可使用 OpenSERP。

## 🚀 快速开始

### 方式 1：直接运行（推荐开发测试）

```bash
# 1. 进入项目目录
cd openserp-brave-adapter

# 2. 配置环境变量
export OPENSERP_BASE_URL=http://your-openserp-server:8080
export OPENSERP_API_KEY=your-api-key  # 可选
export PORT=8765

# 3. 启动服务
node index.js

# 4. 测试
curl "http://localhost:8765/health"
curl "http://localhost:8765/search?q=test&count=5"
```

### 方式 2：Docker 部署（推荐生产环境）

```bash
# 1. 构建并启动
docker-compose up -d

# 2. 查看日志
docker-compose logs -f

# 3. 测试
curl "http://localhost:8765/health"
```

### 方式 3：Docker 单独运行

```bash
docker build -t openserp-brave-adapter .

docker run -d \
  -p 8765:8765 \
  -e OPENSERP_BASE_URL=http://your-openserp:8080 \
  -e OPENSERP_API_KEY=your-key \
  --name openserp-adapter \
  openserp-brave-adapter
```

---

## 🔧 OpenClaw 配置

适配器启动后，在 OpenClaw 中配置使用：

### 方法 1：修改配置文件

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

然后重启 OpenClaw Gateway：

```bash
openclaw gateway restart
```

### 方法 2：使用环境变量

在 OpenClaw Gateway 环境中设置：

```bash
export BRAVE_BASE_URL=http://localhost:8765
export BRAVE_API_KEY=dummy-key

openclaw gateway restart
```

---

## 📡 API 端点

### 健康检查

```bash
GET /health

# 响应
{
  "status": "ok",
  "timestamp": "2026-03-06T12:00:00.000Z",
  "openserpUrl": "http://localhost:8080"
}
```

### 搜索接口

```bash
GET /search?q=query&count=10&country=US

# 或 POST
POST /search
Content-Type: application/json

{
  "q": "query",
  "count": 10,
  "country": "US"
}
```

**参数说明：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `q` / `query` | string | 必填 | 搜索关键词 |
| `count` / `num` | integer | 10 | 结果数量 (1-10) |
| `country` / `gl` | string | US | 国家代码 |
| `search_lang` / `hl` | string | - | 语言代码 |
| `freshness` / `tbs` | string | - | 时间过滤 (pd/pw/pm/py) |

**响应格式（Brave API 兼容）：**

```json
{
  "web": {
    "results": [
      {
        "title": "页面标题",
        "url": "https://example.com",
        "description": "搜索结果摘要..."
      }
    ]
  },
  "type": "search"
}
```

---

## ⚙️ 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `PORT` | 8765 | 服务监听端口 |
| `OPENSERP_BASE_URL` | http://localhost:8080 | OpenSERP 后端地址 |
| `OPENSERP_API_KEY` | - | OpenSERP API 密钥（可选） |
| `BRAVE_API_KEY` | dummy-key | API 密钥验证（设为 dummy-key 禁用） |
| `LOG_LEVEL` | info | 日志级别 (debug/info/warn/error) |
| `REQUEST_TIMEOUT` | 10000 | 请求超时时间（毫秒） |
| `ENABLE_CORS` | true | 是否启用 CORS |

---

## 🧪 测试

### 基本测试

```bash
# 健康检查
curl http://localhost:8765/health

# 简单搜索
curl "http://localhost:8765/search?q=OpenAI&count=3"

# 带参数搜索
curl "http://localhost:8765/search?q=news&count=5&country=CN&freshness=pd"
```

### OpenClaw 测试

在 OpenClaw 对话中：

```
搜索一下 OpenSERP 的最新动态
```

如果配置正确，应该能收到来自 OpenSERP 的搜索结果。

---

## 🏗️ 架构说明

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│  OpenClaw   │────▶│  OpenSERP Proxy  │────▶│  OpenSERP   │
│ web_search  │     │  (本适配器)       │     │   Service   │
└─────────────┘     └──────────────────┘     └─────────────┘
     │                      │                      │
     │ Brave API Format     │ Brave API Format     │ OpenSERP
     │                      │ (转换后)              │ Format
     └──────────────────────┴──────────────────────┘
                          响应转换
```

**工作流程：**

1. OpenClaw 发起 Brave API 格式的搜索请求
2. 适配器接收请求，解析参数
3. 适配器调用 OpenSERP API
4. 适配器将 OpenSERP 响应转换为 Brave 格式
5. 返回给 OpenClaw

---

## 🛠️ 故障排查

### 问题：连接 OpenSERP 失败

```bash
# 检查 OpenSERP 是否可访问
curl http://your-openserp-server:8080/search?q=test

# 检查适配器日志
docker-compose logs openserp-adapter
```

### 问题：OpenClaw 仍然使用 Brave API

确认配置已生效：

```bash
# 检查 OpenClaw 配置
cat ~/.openclaw/openclaw.json | grep -A5 '"search"'

# 重启 Gateway
openclaw gateway restart
```

### 问题：搜索结果格式不正确

检查 OpenSERP 响应格式，可能需要调整 `transformToBraveFormat` 函数：

```javascript
// 在 index.js 中查看支持的格式
if (openserpData.results) { ... }
else if (openserpData.organic) { ... }
else if (openserpData.data) { ... }
```

---

## 📦 部署到生产环境

### 1. 使用 systemd（Linux 服务器）

创建服务文件 `/etc/systemd/system/openserp-adapter.service`：

```ini
[Unit]
Description=OpenSERP Brave Adapter
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/openserp-brave-adapter
ExecStart=/usr/bin/node index.js
Restart=always
Environment=PORT=8765
Environment=OPENSERP_BASE_URL=http://localhost:8080

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable openserp-adapter
sudo systemctl start openserp-adapter
sudo systemctl status openserp-adapter
```

### 2. 使用 Nginx 反向代理

```nginx
server {
    listen 80;
    server_name search.yourdomain.com;

    location / {
        proxy_pass http://localhost:8765;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

## 🔒 安全建议

1. **API 密钥验证**：生产环境设置 `BRAVE_API_KEY`
2. **网络隔离**：将适配器放在内网，只允许 OpenClaw 访问
3. **速率限制**：在 Nginx 或适配器前添加限流
4. **HTTPS**：使用 Nginx 或 Caddy 添加 TLS 加密

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 🔗 相关资源

- [OpenClaw 文档](https://docs.openclaw.ai/tools/web)
- [Brave Search API](https://brave.com/search/api/)
- [OpenSERP](https://github.com/openserp/openserp)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

主要贡献方向：
- 支持更多 OpenSERP 响应格式
- 添加缓存层提升性能
- 增加监控和指标导出
- 改进错误处理和重试机制
