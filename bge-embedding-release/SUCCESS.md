# ✅ BGE Embedding Docker 部署成功

**部署时间：** 2026-03-18 08:47  
**模型：** BAAI/bge-small-zh-v1.5  
**状态：** 🟢 运行中

---

## 📊 部署信息

| 项目 | 值 |
|------|-----|
| 容器名称 | `bge-embedding` |
| 镜像 | `bge-embedding:latest` |
| 端口 | `5000` |
| 内存限制 | `1GB` |
| CPU 限制 | `2.0` |
| 模型卷 | `bge-models` |
| 部署路径 | `/data/embedding-service` |

---

## 🚀 服务状态

```bash
# 检查容器状态
docker ps | grep bge-embedding

# 查看日志
docker logs bge-embedding --tail 50

# 健康检查
curl http://localhost:5000/health
```

**当前状态：** ✅ 正常运行

---

## 🔌 API 接口

### 1. 健康检查

```bash
curl http://localhost:5000/health
```

**响应示例：**
```json
{
  "status": "healthy",
  "model": "BAAI/bge-small-zh-v1.5",
  "loaded": true
}
```

---

### 2. 生成 Embedding

```bash
curl -X POST http://localhost:5000/embed \
  -H "Content-Type: application/json" \
  -d '{"texts": ["今天天气很好", "我喜欢吃苹果"]}'
```

**响应示例：**
```json
{
  "model": "BAAI/bge-small-zh-v1.5",
  "embeddings": [[0.123, 0.456, ...], [0.789, 0.012, ...]],
  "count": 2,
  "dimension": 512
}
```

---

### 3. 相似度计算

```bash
curl -X POST http://localhost:5000/similarity \
  -H "Content-Type: application/json" \
  -d '{
    "query": "天气不错",
    "documents": ["今天下雨", "阳光明媚", "我喜欢晴天"]
  }'
```

**响应示例：**
```json
{
  "similarities": [0.584, 0.537, 0.612],
  "ranked": [[2, 0.612], [0, 0.584], [1, 0.537]]
}
```

---

### 4. 语义搜索

```bash
curl -X POST http://localhost:5000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "OpenClaw 配置问题",
    "documents": [
      "今天天气很好",
      "OpenClaw 配置文件设置",
      "我喜欢吃苹果"
    ],
    "top_k": 3
  }'
```

**响应示例：**
```json
{
  "query": "OpenClaw 配置问题",
  "results": [
    {"index": 1, "text": "OpenClaw 配置文件设置", "score": 0.855},
    {"index": 2, "text": "我喜欢吃苹果", "score": 0.705}
  ],
  "total": 3
}
```

---

## 💻 Python 调用示例

```python
import requests

# 生成 embedding
response = requests.post('http://localhost:5000/embed', json={
    'texts': ['今天天气很好', '我喜欢吃苹果']
})
embeddings = response.json()['embeddings']

# 计算相似度
response = requests.post('http://localhost:5000/similarity', json={
    'query': '天气不错',
    'documents': ['今天下雨', '阳光明媚', '我喜欢晴天']
})
similarities = response.json()['similarities']

# 语义搜索
response = requests.post('http://localhost:5000/search', json={
    'query': 'OpenClaw 配置',
    'documents': ['文档 1', '文档 2', '文档 3'],
    'top_k': 3
})
results = response.json()['results']
```

---

## 🔧 管理命令

```bash
# 重启服务
docker restart bge-embedding

# 停止服务
docker stop bge-embedding

# 启动服务
docker start bge-embedding

# 查看资源占用
docker stats bge-embedding

# 进入容器
docker exec -it bge-embedding bash

# 删除服务（谨慎！）
docker stop bge-embedding && docker rm bge-embedding
docker volume rm bge-models
```

---

## 📈 性能指标

| 指标 | 数值 |
|------|------|
| 模型大小 | ~90MB |
| 内存占用 | ~600MB (加载后) |
| 空闲内存 | ~200MB |
| 嵌入维度 | 512 |
| 推理速度 | ~50ms/句 |
| 首次加载 | ~30 秒 (下载模型) |
| 后续加载 | ~3 秒 (缓存) |

---

## 🛡️ 特性

### ✅ 已实现

1. **懒加载** - 首次请求时加载模型，节省空闲内存
2. **超时卸载** - 5 分钟未使用自动卸载模型
3. **镜像加速** - 使用 hf-mirror.com 加速模型下载
4. **持久化缓存** - 模型下载到卷 `bge-models`，重启不丢失
5. **资源限制** - 内存 1GB，CPU 2 核心
6. **自动重启** - 容器崩溃自动恢复

### 🔒 安全保障

1. **输入验证** - 限制文本数量 (最多 100 条)、长度 (最多 2048 字符)
2. **超时保护** - 请求超时自动终止
3. **线程安全** - 模型加载使用锁保护
4. **网络隔离** - 仅暴露 5000 端口

---

## 📝 部署文件

```
/data/embedding-service/
├── Dockerfile          # 镜像构建文件
├── app.py             # Flask 应用
└── README.md          # 本文档
```

---

## 🎯 集成到 OpenClaw

在 OpenClaw 中调用 BGE 服务：

```python
import requests

BGE_URL = 'http://localhost:5000'

def embed_texts(texts):
    """生成文本嵌入"""
    resp = requests.post(f'{BGE_URL}/embed', json={'texts': texts})
    return resp.json()['embeddings']

def search_memory(query, memory_chunks, top_k=5):
    """搜索相关记忆"""
    texts = [chunk['content'] for chunk in memory_chunks]
    resp = requests.post(f'{BGE_URL}/search', json={
        'query': query,
        'documents': texts,
        'top_k': top_k
    })
    
    results = []
    for r in resp.json()['results']:
        result = memory_chunks[r['index']].copy()
        result['score'] = r['score']
        results.append(result)
    
    return results
```

---

## 🐛 故障排查

### 问题 1: 模型下载超时

**症状：** 日志显示 `timed out thrown while requesting HEAD...`

**解决：**
```bash
# 检查镜像源配置
docker logs bge-embedding | grep "HF_ENDPOINT"

# 重启容器（会自动使用镜像源）
docker restart bge-embedding
```

### 问题 2: 服务无法访问

**症状：** `curl: (7) Failed to connect to localhost port 5000`

**解决：**
```bash
# 检查容器状态
docker ps | grep bge-embedding

# 查看端口映射
docker port bge-embedding

# 检查防火墙
iptables -L -n | grep 5000
```

### 问题 3: 内存不足

**症状：** 容器频繁重启，日志显示 OOM

**解决：**
```bash
# 增加内存限制
docker stop bge-embedding && docker rm bge-embedding
docker run -d --name bge-embedding \
  --restart=always \
  -p 5000:5000 \
  --memory=2g \
  --cpus=2.0 \
  -v bge-models:/app/models \
  bge-embedding:latest
```

---

## 📚 相关文档

- 详细部署策略：`/root/.openclaw/workspace/BGE-EMBEDDING-DEPLOYMENT.md`
- 快速部署指南：`/root/.openclaw/workspace/BGE-QUICK-DEPLOY.md`
- 技能文档：`/root/.openclaw/workspace/skills/bge-embedding/SKILL.md`

---

**部署完成！BGE Embedding 服务已就绪！** 🎉🐴
