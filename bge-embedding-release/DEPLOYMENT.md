# 🤖 BGE Embedding 本地部署策略

**模型：** BAAI/bge-small-zh-v1.5  
**用途：** 记忆搜索语义向量嵌入  
**时间：** 2026-03-16 23:40

---

## 📊 模型信息

| 项目 | 数值 |
|------|------|
| 模型大小 | ~90MB |
| 维度 | 512 |
| 最大序列长度 | 512 tokens |
| 支持语言 | 中文、英文 |
| 推理速度 | ~50ms/句 (CPU) |
| 内存占用 | ~200MB |

---

## 🎯 部署方案

### 方案 1: Docker 容器部署（推荐）

**优点：**
- ✅ 隔离性好，不影响主容器
- ✅ 易于管理和更新
- ✅ 资源限制明确
- ✅ 安全性高

**部署步骤：**

```bash
# 1. 创建部署目录
mkdir -p /data/embedding-service
cd /data/embedding-service

# 2. 创建 Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
RUN pip install --no-cache-dir \
    flask==3.0.0 \
    flask-cors==4.0.0 \
    sentence-transformers==2.2.2 \
    torch==2.1.0 \
    --index-url https://download.pytorch.org/whl/cpu

# 复制应用
COPY app.py .

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["python", "app.py"]
EOF

# 3. 创建 Flask 应用
cat > app.py << 'EOF'
from flask import Flask, request, jsonify
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
import os

app = Flask(__name__)
CORS(app)

# 加载模型
MODEL_NAME = "BAAI/bge-small-zh-v1.5"
model = SentenceTransformer(MODEL_NAME)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "model": MODEL_NAME})

@app.route('/embed', methods=['POST'])
def embed():
    data = request.json
    texts = data.get('texts', [])
    
    if not texts:
        return jsonify({"error": "No texts provided"}), 400
    
    # 生成 embedding
    embeddings = model.encode(texts, normalize_embeddings=True).tolist()
    
    return jsonify({
        "model": MODEL_NAME,
        "embeddings": embeddings,
        "count": len(embeddings)
    })

@app.route('/similarity', methods=['POST'])
def similarity():
    data = request.json
    query = data.get('query', '')
    documents = data.get('documents', [])
    
    if not query or not documents:
        return jsonify({"error": "Missing query or documents"}), 400
    
    # 编码
    all_texts = [query] + documents
    embeddings = model.encode(all_texts, normalize_embeddings=True)
    
    # 计算余弦相似度
    query_emb = embeddings[0]
    doc_embs = embeddings[1:]
    similarities = [float(query_emb @ doc_emb) for doc_emb in doc_embs]
    
    return jsonify({
        "similarities": similarities,
        "ranked": sorted(zip(range(len(documents)), similarities), 
                        key=lambda x: x[1], reverse=True)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
EOF

# 4. 构建镜像
docker build -t bge-embedding:latest .

# 5. 启动容器
docker run -d --name bge-embedding \
  --restart=always \
  -p 5000:5000 \
  --memory=512m \
  --cpus=1.0 \
  bge-embedding:latest

# 6. 测试
sleep 10
curl http://localhost:5000/health
```

---

### 方案 2: OpenClaw 容器内集成

**优点：**
- ✅ 无需额外容器
- ✅ 调用延迟低
- ✅ 配置简单

**缺点：**
- ⚠️ 增加主容器内存占用
- ⚠️ 模型加载影响启动速度

**部署步骤：**

```bash
# 1. 安装依赖
pip install sentence-transformers torch --index-url https://download.pytorch.org/whl/cpu

# 2. 创建 embedding 技能
mkdir -p /root/.openclaw/workspace/skills/bge-embedding

# 3. 创建 embedding.py
cat > /root/.openclaw/workspace/skills/bge-embedding/embedding.py << 'EOF'
from sentence_transformers import SentenceTransformer
import numpy as np
import json

class BGEEEmbedding:
    def __init__(self):
        self.model_name = "BAAI/bge-small-zh-v1.5"
        self.model = SentenceTransformer(self.model_name)
    
    def embed(self, texts):
        """生成 embedding"""
        embeddings = self.model.encode(texts, normalize_embeddings=True)
        return embeddings.tolist()
    
    def similarity(self, query, documents):
        """计算相似度"""
        all_texts = [query] + documents
        embeddings = self.model.encode(all_texts, normalize_embeddings=True)
        
        query_emb = embeddings[0]
        doc_embs = embeddings[1:]
        similarities = [float(query_emb @ doc_emb) for doc_emb in doc_embs]
        
        return similarities
    
    def search(self, query, memory_chunks, top_k=5):
        """搜索最相关的记忆"""
        texts = [chunk['content'] for chunk in memory_chunks]
        similarities = self.similarity(query, texts)
        
        # 排序
        ranked = sorted(
            zip(range(len(memory_chunks)), similarities),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]
        
        results = []
        for idx, score in ranked:
            result = memory_chunks[idx].copy()
            result['score'] = score
            results.append(result)
        
        return results

# 单例
_embedding_instance = None

def get_embedding_model():
    global _embedding_instance
    if _embedding_instance is None:
        _embedding_instance = BGEEEmbedding()
    return _embedding_instance
EOF

# 4. 在 memory_search 技能中集成
# 修改 /root/.openclaw/workspace/skills/memory_search.py
```

---

### 方案 3: 懒加载 + 缓存（推荐用于生产）

**核心思路：**
- 首次使用时加载模型
- 加载后缓存在内存
- 设置超时自动卸载

**实现代码：**

```python
# /root/.openclaw/workspace/skills/bge-embedding/lazy_loader.py
from sentence_transformers import SentenceTransformer
import threading
import time
from functools import wraps

class LazyEmbeddingLoader:
    def __init__(self, timeout=300):
        self.model_name = "BAAI/bge-small-zh-v1.5"
        self._model = None
        self._lock = threading.Lock()
        self._last_used = None
        self._timeout = timeout
        self._cleanup_thread = None
    
    def _start_cleanup(self):
        """启动清理线程"""
        def cleanup():
            while True:
                time.sleep(60)
                if self._model and self._last_used:
                    if time.time() - self._last_used > self._timeout:
                        with self._lock:
                            print(f"卸载模型以释放内存")
                            self._model = None
        
        self._cleanup_thread = threading.Thread(target=cleanup, daemon=True)
        self._cleanup_thread.start()
    
    @property
    def model(self):
        """懒加载模型"""
        if self._model is None:
            with self._lock:
                if self._model is None:
                    print(f"加载模型 {self.model_name}...")
                    self._model = SentenceTransformer(self.model_name)
                    if self._cleanup_thread is None:
                        self._start_cleanup()
        
        self._last_used = time.time()
        return self._model
    
    def embed(self, texts):
        embeddings = self.model.encode(texts, normalize_embeddings=True)
        return embeddings.tolist()
    
    def similarity(self, query, documents):
        all_texts = [query] + documents
        embeddings = self.model.encode(all_texts, normalize_embeddings=True)
        
        query_emb = embeddings[0]
        doc_embs = embeddings[1:]
        similarities = [float(query_emb @ doc_emb) for doc_emb in doc_embs]
        
        return similarities

# 全局单例
embedding_loader = LazyEmbeddingLoader(timeout=300)  # 5 分钟超时
```

---

## 🔒 安全保障

### 1. 资源限制

```bash
# Docker 容器限制
docker run -d --name bge-embedding \
  --memory=512m \        # 最大内存 512MB
  --cpus=1.0 \           # 最多 1 个 CPU
  --pids-limit=50 \      # 最多 50 个进程
  bge-embedding:latest
```

### 2. 网络隔离

```bash
# 仅允许 OpenClaw 容器访问
docker network create embedding-net
docker network connect embedding-net xiaoma-new
docker run -d --name bge-embedding \
  --network embedding-net \
  --expose 5000 \
  bge-embedding:latest
```

### 3. API 认证

```python
# 添加 API Key 验证
import os
from functools import wraps

API_KEY = os.getenv('EMBEDDING_API_KEY', 'default-key-change-me')

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get('X-API-Key')
        if key != API_KEY:
            return jsonify({"error": "Invalid API key"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/embed', methods=['POST'])
@require_api_key
def embed():
    ...
```

### 4. 输入验证

```python
@app.route('/embed', methods=['POST'])
def embed():
    data = request.json
    texts = data.get('texts', [])
    
    # 验证输入
    if not isinstance(texts, list):
        return jsonify({"error": "texts must be a list"}), 400
    
    if len(texts) > 100:
        return jsonify({"error": "Maximum 100 texts per request"}), 400
    
    for text in texts:
        if not isinstance(text, str):
            return jsonify({"error": "All texts must be strings"}), 400
        if len(text) > 2048:
            return jsonify({"error": "Text too long (max 2048 chars)"}), 400
    
    # 生成 embedding
    embeddings = model.encode(texts, normalize_embeddings=True).tolist()
    
    return jsonify({
        "model": MODEL_NAME,
        "embeddings": embeddings,
        "count": len(embeddings)
    })
```

---

## 📊 性能优化

### 1. 批处理

```python
def batch_embed(self, texts, batch_size=32):
    """批量生成 embedding"""
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        embeddings = self.model.encode(batch, normalize_embeddings=True)
        all_embeddings.extend(embeddings.tolist())
    return all_embeddings
```

### 2. 缓存热点

```python
from functools import lru_cache
import hashlib

class CachedEmbedding:
    def __init__(self):
        self.model = SentenceTransformer("BAAI/bge-small-zh-v1.5")
    
    @lru_cache(maxsize=1000)
    def _embed_cached(self, text_hash, text):
        return self.model.encode([text], normalize_embeddings=True)[0].tolist()
    
    def embed(self, texts):
        results = []
        for text in texts:
            text_hash = hashlib.md5(text.encode()).hexdigest()
            emb = self._embed_cached(text_hash, text)
            results.append(emb)
        return results
```

### 3. 量化加速

```python
# 使用 INT8 量化模型
from sentence_transformers import SentenceTransformer

# 加载后量化
model = SentenceTransformer("BAAI/bge-small-zh-v1.5")
model = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)
```

---

## 📋 推荐方案

### 开发环境
**方案 2 (OpenClaw 容器内集成) + 懒加载**
- 快速部署
- 调用方便
- 内存友好

### 生产环境
**方案 1 (Docker 容器部署) + 网络隔离**
- 安全隔离
- 资源可控
- 易于扩展

---

## 🚀 快速开始

**推荐：OpenClaw 容器内集成（懒加载）**

```bash
# 1. 安装依赖
pip install sentence-transformers torch --index-url https://download.pytorch.org/whl/cpu

# 2. 创建技能
mkdir -p /root/.openclaw/workspace/skills/bge-embedding

# 3. 复制懒加载代码
# (见上方 lazy_loader.py)

# 4. 在 memory_search 中调用
from skills.bge-embedding.lazy_loader import embedding_loader

def search_memory(query, memory_chunks):
    results = embedding_loader.search(query, memory_chunks, top_k=5)
    return results
```

---

**部署完成后可支持：**
- ✅ 中文语义搜索
- ✅ 记忆相似度匹配
- ✅ 向量数据库集成
- ✅ RAG 应用

**维护者：** 小马 🐴
