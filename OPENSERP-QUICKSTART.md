# OpenSERP 集成快速开始指南

## 🎯 目标

在 30 分钟内完成 OpenSERP 到 OpenClaw 的集成，使 OpenClaw 的 `web_search` 工具能够使用自托管的 OpenSERP 服务。

---

## 📦 前提条件

- ✅ OpenSERP 服务已部署并可访问
- ✅ Node.js >= 18 已安装
- ✅ OpenClaw 已安装并运行

---

## 🚀 5 分钟快速部署

### 步骤 1：启动适配器服务

```bash
cd /root/.openclaw/workspace/openserp-brave-adapter

# 方式 A：直接运行（最快）
export OPENSERP_BASE_URL=http://your-openserp:8080
node index.js &

# 方式 B：使用部署脚本
./deploy.sh

# 方式 C：Docker（推荐生产）
docker-compose up -d
```

### 步骤 2：验证服务

```bash
# 健康检查
curl http://localhost:8765/health

# 测试搜索
curl "http://localhost:8765/search?q=test&count=3"
```

预期响应：
```json
{
  "web": {
    "results": [
      {
        "title": "...",
        "url": "...",
        "description": "..."
      }
    ]
  }
}
```

### 步骤 3：配置 OpenClaw

编辑 `~/.openclaw/openclaw.json`，添加或修改：

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

### 步骤 4：重启 OpenClaw

```bash
openclaw gateway restart
```

### 步骤 5：测试

在 OpenClaw 对话中：

```
搜索一下人工智能的最新进展
```

---

## 🧪 完整测试流程

```bash
# 1. 运行适配器测试
cd /root/.openclaw/workspace/openserp-brave-adapter
node test/index.test.js

# 2. 检查 OpenClaw 配置
openclaw config.get | grep -A5 search

# 3. 在对话中测试
# （通过飞书/Telegram 等发送搜索请求）
```

---

## 📁 项目文件结构

```
openserp-brave-adapter/
├── index.js              # 主程序
├── package.json          # 项目配置
├── README.md             # 详细文档
├── Dockerfile            # Docker 配置
├── docker-compose.yml    # Docker 编排
├── .env.example          # 环境变量示例
├── deploy.sh             # 快速部署脚本
├── test/
│   └── index.test.js     # 测试脚本
└── examples/
    └── openclaw-config.json  # OpenClaw 配置示例
```

---

## ⚙️ 关键配置

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `PORT` | 8765 | 适配器服务端口 |
| `OPENSERP_BASE_URL` | http://localhost:8080 | OpenSERP 地址 |
| `BRAVE_API_KEY` | dummy-key | API 密钥验证 |

### OpenClaw 配置

```json
{
  "tools": {
    "web": {
      "search": {
        "provider": "brave",
        "baseUrl": "http://localhost:8765"
      }
    }
  }
}
```

---

## 🛠️ 故障排查

### 问题 1：适配器启动失败

```bash
# 检查端口占用
lsof -i :8765

# 检查 Node.js 版本
node -v  # 需要 >= 18

# 查看详细错误
node index.js 2>&1 | head -20
```

### 问题 2：OpenSERP 连接失败

```bash
# 测试 OpenSERP 直连
curl http://your-openserp:8080/search?q=test

# 检查网络连通性
ping your-openserp

# 查看适配器日志
docker logs openserp-adapter  # Docker 部署
# 或查看控制台输出
```

### 问题 3：OpenClaw 不使用适配器

```bash
# 验证配置已加载
openclaw config.get

# 检查 Gateway 日志
openclaw gateway logs

# 强制重启
openclaw gateway stop
openclaw gateway start
```

---

## 📊 性能优化

### 添加响应缓存（高级）

在 `index.js` 中添加简单缓存：

```javascript
const cache = new Map();
const CACHE_TTL = 5 * 60 * 1000; // 5 分钟

function getCacheKey(query, options) {
  return `${query}:${JSON.stringify(options)}`;
}

function getFromCache(key) {
  const item = cache.get(key);
  if (item && Date.now() - item.timestamp < CACHE_TTL) {
    return item.data;
  }
  cache.delete(key);
  return null;
}
```

### 使用 Nginx 反向代理

```nginx
server {
    listen 80;
    server_name search.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8765;
        proxy_cache_bypass $http_pragma;
    }
}
```

---

## 📈 监控建议

### 健康检查端点

```bash
# 每 30 秒检查一次
curl -f http://localhost:8765/health || echo "Service down!"
```

### 日志收集

```bash
# Docker 部署
docker logs --tail 100 -f openserp-adapter

# 直接运行
# 查看控制台输出或使用 journalctl
```

### 指标导出（可选）

添加 Prometheus 指标端点：
- 请求总数
- 平均响应时间
- 错误率
- 缓存命中率

---

## 🎓 下一步

1. ✅ 完成基础部署和测试
2. 🔄 配置生产环境（HTTPS、认证、限流）
3. 📦 考虑部署为 systemd 服务或 Kubernetes
4. 📊 添加监控和告警
5. 🔧 根据实际需求优化性能

---

## 📞 支持

- 📖 详细文档：`openserp-brave-adapter/README.md`
- 💬 完整方案：`openserp-integration-plan.md`
- 🐛 问题反馈：检查日志并查看故障排查部分

---

**预计完成时间：30 分钟** ⏱️

开始吧！🚀
