#!/bin/bash
# OpenSERP Brave Adapter 快速部署脚本

set -e

echo "🚀 OpenSERP Brave Adapter 快速部署"
echo "=================================="
echo ""

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误：需要 Node.js >= 18"
    echo "   请先安装 Node.js: https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ 错误：Node.js 版本过低 (需要 >= 18, 当前: $(node -v))"
    exit 1
fi

echo "✅ Node.js 版本：$(node -v)"

# 检查 Docker（可选）
DOCKER_AVAILABLE=false
if command -v docker &> /dev/null; then
    DOCKER_AVAILABLE=true
    echo "✅ Docker 可用：$(docker --version)"
fi

echo ""
echo "选择部署方式:"
echo "  1) 直接运行 (开发测试)"
echo "  2) Docker 部署 (生产环境)"
echo "  3) 仅生成配置文件"
echo ""
read -p "请选择 [1-3]: " choice

case $choice in
    1)
        echo ""
        echo "📝 配置环境变量:"
        read -p "OpenSERP 地址 [http://localhost:8080]: " openserp_url
        openserp_url=${openserp_url:-http://localhost:8080}
        
        read -p "服务端口 [8765]: " port
        port=${port:-8765}
        
        echo ""
        echo "🚀 启动服务..."
        export OPENSERP_BASE_URL=$openserp_url
        export PORT=$port
        
        node index.js
        ;;
    
    2)
        if [ "$DOCKER_AVAILABLE" = false ]; then
            echo "❌ Docker 不可用，请选择方式 1"
            exit 1
        fi
        
        echo ""
        echo "📝 配置环境变量:"
        read -p "OpenSERP 地址 [http://localhost:8080]: " openserp_url
        openserp_url=${openserp_url:-http://localhost:8080}
        
        read -p "服务端口 [8765]: " port
        port=${port:-8765}
        
        echo ""
        echo "🔨 构建 Docker 镜像..."
        docker build -t openserp-brave-adapter .
        
        echo ""
        echo "🚀 启动容器..."
        docker run -d \
            -p $port:8765 \
            -e OPENSERP_BASE_URL=$openserp_url \
            -e PORT=8765 \
            --name openserp-adapter \
            openserp-brave-adapter
        
        echo ""
        echo "✅ 部署完成!"
        echo "   查看日志：docker logs -f openserp-adapter"
        echo "   停止服务：docker stop openserp-adapter"
        echo "   测试端点：curl http://localhost:$port/health"
        ;;
    
    3)
        echo ""
        echo "📁 生成配置文件..."
        
        cat > .env << EOF
PORT=8765
OPENSERP_BASE_URL=http://localhost:8080
BRAVE_API_KEY=dummy-key
LOG_LEVEL=info
EOF
        
        echo "✅ 已生成 .env 文件"
        echo "   编辑 .env 文件配置您的环境"
        echo "   然后运行：node index.js"
        ;;
    
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac
