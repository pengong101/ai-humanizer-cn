# BGE Embedding 部署指南

中文文本向量化服务，用于 OpenClaw 记忆搜索。

## 快速部署

```bash
docker run -d --name bge-embedding \
  --restart=always \
  -p 5000:5000 \
  --memory=512m \
  --cpus=1.0 \
  bge-embedding:latest
```

## API 接口

- `/health` - 健康检查
- `/embed` - 生成 embedding (512 维)
- `/similarity` - 相似度计算
- `/search` - 语义搜索

## 详细信息

查看 [DEPLOYMENT.md](./DEPLOYMENT.md) 获取完整部署指南。
