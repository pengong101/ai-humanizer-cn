# OpenSERP Brave Adapter Docker Image
# Minimal Node.js runtime for the adapter service

FROM node:20-alpine

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY package.json index.js ./

# 创建非 root 用户运行（安全最佳实践）
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# 切换用户
USER nodejs

# 暴露端口
EXPOSE 8765

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8765/health || exit 1

# 默认环境变量
ENV PORT=8765
ENV OPENSERP_BASE_URL=http://host.docker.internal:8080
ENV LOG_LEVEL=info

# 启动命令
CMD ["node", "index.js"]
