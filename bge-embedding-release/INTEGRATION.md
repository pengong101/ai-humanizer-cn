# ✅ BGE Embedding 集成完成

**集成时间：** 2026-03-18 09:22  
**测试状态：** 🟢 6/6 通过 (100%)  
**部署模式：** Docker Host Network

---

## 📊 测试结果

| 测试项 | 状态 | 详情 |
|--------|------|------|
| 健康检查 | ✅ | 服务正常运行 |
| Embed 生成 | ✅ | 512 维向量 |
| 相似度计算 | ✅ | 语义理解准确 |
| 语义搜索 | ✅ | Top1 准确率 100% |
| 记忆搜索 | ✅ | 多场景测试通过 |
| 性能测试 | ✅ | 5.6ms/条 (批量) |

**总耗时：** 6.37 秒

---

## 🏗️ 架构说明

```
┌─────────────────────┐
│  OpenClaw 容器       │
│  (xiaoma-new)       │
│  172.17.0.4         │
└─────────┬───────────┘
          │
          │ HTTP (172.17.0.1:5000)
          │
┌─────────▼───────────┐
│   Docker Host       │
│   (宿主机网络)       │
└─────────┬───────────┘
          │
          │ localhost:5000
          │
┌─────────▼───────────┐
│  BGE 容器            │
│  (host network)     │
│  端口：5000         │
└─────────────────────┘
```

---

## 📁 文件结构

```
/root/.openclaw/workspace/skills/bge-embedding/
├── SKILL.md                    # 技能文档
├── lazy_loader.py              # 本地懒加载 (备用)
├── bge_docker_client.py        # Docker 客户端 ⭐
├── test_docker_integration.py  # 集成测试 ⭐
├── test_embedding.py           # 本地测试
└── requirements.txt            # 依赖

/root/.openclaw/workspace/skills/
└── memory_search_bge.py        # 记忆搜索集成 ⭐

/data/embedding-service/
├── Dockerfile                  # 镜像构建
├── app.py                      # Flask 服务
└── README.md                   # 使用文档
```

---

## 🔌 使用方法

### 方法 1: 直接使用客户端

```python
from skills.bge_embedding.bge_docker_client import get_bge_client

# 获取客户端（自动检测服务地址）
client = get_bge_client()

# 生成 embedding
texts = ["今天天气很好", "我喜欢吃苹果"]
embeddings = client.embed(texts)

# 计算相似度
scores = client.similarity("天气不错", ["今天下雨", "阳光明媚"])

# 语义搜索
results = client.search("OpenClaw 配置", ["文档 1", "文档 2"], top_k=3)
```

### 方法 2: 使用记忆搜索封装

```python
from skills.memory_search_bge import search_memory

# 准备记忆片段
memories = [
    {'content': 'OpenClaw 配置文件在 /root/.openclaw/openclaw.json', 'source': 'config'},
    {'content': 'SearXNG 端口是 8081', 'source': 'search'},
]

# 搜索
query = "OpenClaw 配置在哪里？"
results = search_memory(query, memories, top_k=2)

for r in results:
    print(f"[{r['score']:.3f}] {r['content']}")
```

### 方法 3: 直接调用 API

```python
import requests

# 健康检查
resp = requests.get("http://172.17.0.1:5000/health")

# 生成 embedding
resp = requests.post("http://172.17.0.1:5000/embed", 
    json={"texts": ["文本 1", "文本 2"]})

# 语义搜索
resp = requests.post("http://172.17.0.1:5000/search",
    json={"query": "查询", "documents": ["文档 1", "文档 2"], "top_k": 3})
```

---

## ⚙️ 配置说明

### 服务地址

客户端会自动检测以下地址（按优先级）：

1. `http://172.17.0.1:5000` - Docker 网关（推荐）
2. `http://localhost:5000` - 本地主机
3. `http://bge-embedding:5000` - Docker DNS

### 环境变量（可选）

```bash
# 自定义服务地址
export BGE_SERVICE_URL="http://172.17.0.1:5000"

# 超时时间
export BGE_TIMEOUT="60"

# 最大重试次数
export BGE_MAX_RETRIES="3"
```

---

## 📈 性能指标

| 指标 | 数值 | 说明 |
|------|------|------|
| 单次嵌入 | ~50ms | 单条文本 |
| 批量嵌入 | ~5.6ms/条 | 20 条批量 |
| 相似度计算 | ~60ms | 4 个文档 |
| 语义搜索 | ~70ms | 5 个文档，top_k=3 |
| 内存占用 | ~600MB | 模型加载后 |
| 空闲内存 | ~200MB | 模型卸载后 |

---

## 🛡️ 容错机制

### 1. 自动重试

```python
# 客户端内置重试机制
client = BGEClient(BGEConfig(
    max_retries=3,      # 最多重试 3 次
    retry_delay=1.0,    # 重试间隔 1 秒
    timeout=60          # 请求超时 60 秒
))
```

### 2. 服务降级

```python
# memory_search_bge.py 实现自动降级
from memory_search_bge import search_memory

# 优先使用 Docker 服务
# Docker 不可用时自动降级到本地懒加载
results = search_memory(query, memories, use_docker=True)
```

### 3. 健康检查

```python
# 检查服务可用性
if client.is_available():
    # 服务正常
    results = client.search(...)
else:
    # 使用备用方案
    results = fallback_search(...)
```

---

## 🧪 运行测试

```bash
# 在 OpenClaw 容器内运行测试
docker exec xiaoma-new python3 \
  /root/.openclaw/workspace/skills/bge-embedding/test_docker_integration.py

# 预期输出：6/6 通过 (100%)
```

---

## 🔧 管理命令

```bash
# 查看服务状态
docker ps | grep bge-embedding

# 查看日志
docker logs bge-embedding --tail 50

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
```

---

## 📝 集成示例

### 示例 1: 记忆搜索

```python
from memory_search_bge import search_memory

# 加载记忆
memories = load_memory_chunks()

# 搜索
query = "OpenClaw 配置问题"
results = search_memory(query, memories, top_k=5)

# 处理结果
for r in results:
    print(f"[{r['score']:.3f}] {r['content']}")
    print(f"  来源：{r['source']}")
```

### 示例 2: 文档去重

```python
from skills.bge_embedding.bge_docker_client import get_bge_client
import numpy as np

client = get_bge_client()

def deduplicate(docs, threshold=0.9):
    embeddings = client.embed(docs)
    
    unique_docs = []
    unique_embs = []
    
    for doc, emb in zip(docs, embeddings):
        is_duplicate = False
        
        for unique_emb in unique_embs:
            sim = np.dot(emb, unique_emb)
            if sim > threshold:
                is_duplicate = True
                break
        
        if not is_duplicate:
            unique_docs.append(doc)
            unique_embs.append(emb)
    
    return unique_docs
```

### 示例 3: 语义聚类

```python
from skills.bge_embedding.bge_docker_client import get_bge_client
from sklearn.cluster import KMeans

client = get_bge_client()

# 生成嵌入
texts = ["文档 1", "文档 2", "文档 3"]
embeddings = client.embed(texts)

# 聚类
kmeans = KMeans(n_clusters=3)
kmeans.fit(embeddings)

# 获取类别
labels = kmeans.labels_
```

---

## 🐛 故障排查

### 问题 1: 连接被拒绝

**症状：** `ConnectionRefusedError: [Errno 111] Connection refused`

**解决：**
```bash
# 检查 BGE 容器状态
docker ps | grep bge-embedding

# 重启服务
docker restart bge-embedding

# 检查端口
docker exec xiaoma-new python3 -c \
  "import requests; print(requests.get('http://172.17.0.1:5000/health').json())"
```

### 问题 2: 超时

**症状：** `ReadTimeout: HTTPConnectionPool ... Read timed out`

**解决：**
```bash
# 增加超时时间
client = BGEClient(BGEConfig(timeout=120))

# 检查模型是否已加载
curl http://172.17.0.1:5000/health
```

### 问题 3: 内存不足

**症状：** 容器频繁重启

**解决：**
```bash
# 增加内存限制
docker stop bge-embedding && docker rm bge-embedding
docker run -d --name bge-embedding \
  --restart=always \
  --network host \
  --memory=2g \
  --cpus=2.0 \
  -v bge-models:/app/models \
  bge-embedding:latest
```

---

## 📚 相关文档

- **服务部署：** `/data/embedding-service/README.md`
- **技能文档：** `/root/.openclaw/workspace/skills/bge-embedding/SKILL.md`
- **部署记录：** `/root/.openclaw/workspace/BGE-DOCKER-DEPLOYMENT-SUCCESS.md`
- **记忆记录：** `/root/.openclaw/workspace/memory/2026-03-18.md`

---

## 🎯 下一步

1. ✅ **Docker 服务部署** - 完成
2. ✅ **客户端开发** - 完成
3. ✅ **集成测试** - 6/6 通过
4. ⏳ **集成到 memory_search** - 待完成
5. ⏳ **性能监控** - 待完成
6. ⏳ **生产环境优化** - 待完成

---

**集成完成！BGE Embedding 服务已就绪！** 🎉🐴
