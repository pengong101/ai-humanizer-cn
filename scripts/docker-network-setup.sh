#!/bin/bash
# Docker 网络打通脚本 - 中期方案
# 执行方式：在 NAS 宿主机上运行此脚本

set -e

echo "=========================================="
echo "🔧 OpenClaw 容器网络打通脚本"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 容器名称配置
OPENCLAW_CONTAINER="xiaoma_new"
SEARXNG_CONTAINER="searxng"
CLASH_CONTAINER="clash"
NETWORK_NAME="openclaw-net"

echo "📋 检查容器状态..."
echo ""

# 检查容器是否存在
check_container() {
    local container=$1
    if docker ps -a --format '{{.Names}}' | grep -q "^${container}$"; then
        echo -e "${GREEN}✅${NC} 容器 ${container} 存在"
        return 0
    else
        echo -e "${RED}❌${NC} 容器 ${container} 不存在"
        return 1
    fi
}

# 检查容器状态
check_container_status() {
    local container=$1
    if docker ps --format '{{.Names}}:{{.Status}}' | grep "^${container}:" | grep -q "Up"; then
        echo -e "${GREEN}✅${NC} 容器 ${container} 运行中"
        return 0
    else
        echo -e "${YELLOW}⚠️${NC} 容器 ${container} 未运行"
        return 1
    fi
}

# 检查所有容器
CONTAINERS_OK=true
for container in "$OPENCLAW_CONTAINER" "$SEARXNG_CONTAINER" "$CLASH_CONTAINER"; do
    if ! check_container "$container"; then
        CONTAINERS_OK=false
    fi
done

if [ "$CONTAINERS_OK" = false ]; then
    echo ""
    echo -e "${RED}❌ 部分容器不存在，请检查容器名称${NC}"
    exit 1
fi

echo ""
echo "📋 检查容器运行状态..."
echo ""

for container in "$OPENCLAW_CONTAINER" "$SEARXNG_CONTAINER" "$CLASH_CONTAINER"; do
    check_container_status "$container" || true
done

echo ""
echo "🔧 创建共享网络..."
echo ""

# 检查网络是否已存在
if docker network ls --format '{{.Name}}' | grep -q "^${NETWORK_NAME}$"; then
    echo -e "${YELLOW}⚠️${NC} 网络 ${NETWORK_NAME} 已存在，跳过创建"
else
    docker network create "$NETWORK_NAME"
    echo -e "${GREEN}✅${NC} 网络 ${NETWORK_NAME} 创建成功"
fi

echo ""
echo "🔗 连接容器到共享网络..."
echo ""

# 连接容器到网络
connect_container() {
    local container=$1
    if docker network inspect "$NETWORK_NAME" --format '{{range .Containers}}{{.Name}} {{end}}' | grep -q "$container"; then
        echo -e "${YELLOW}⚠️${NC} 容器 ${container} 已连接到 ${NETWORK_NAME}"
    else
        docker network connect "$NETWORK_NAME" "$container"
        echo -e "${GREEN}✅${NC} 容器 ${container} 已连接到 ${NETWORK_NAME}"
    fi
}

for container in "$OPENCLAW_CONTAINER" "$SEARXNG_CONTAINER" "$CLASH_CONTAINER"; do
    connect_container "$container"
done

echo ""
echo "🧪 验证网络连接..."
echo ""

# 等待网络生效
sleep 2

# 获取容器 IP
get_container_ip() {
    local container=$1
    docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$container" 2>/dev/null
}

echo "容器 IP 地址："
for container in "$OPENCLAW_CONTAINER" "$SEARXNG_CONTAINER" "$CLASH_CONTAINER"; do
    ip=$(get_container_ip "$container")
    if [ -n "$ip" ]; then
        echo "  - ${container}: ${ip}"
    fi
done

echo ""
echo "📡 测试容器间通信..."
echo ""

# 测试 OpenClaw 到 SearXNG
if docker exec "$OPENCLAW_CONTAINER" ping -c 2 -W 2 "$SEARXNG_CONTAINER" >/dev/null 2>&1; then
    echo -e "${GREEN}✅${NC} OpenClaw → SearXNG: 连通"
else
    echo -e "${YELLOW}⚠️${NC} OpenClaw → SearXNG: 不通 (尝试使用 IP)"
    SEARXNG_IP=$(get_container_ip "$SEARXNG_CONTAINER")
    if [ -n "$SEARXNG_IP" ] && docker exec "$OPENCLAW_CONTAINER" ping -c 2 -W 2 "$SEARXNG_IP" >/dev/null 2>&1; then
        echo -e "${GREEN}✅${NC} OpenClaw → SearXNG(IP): 连通"
    fi
fi

# 测试 OpenClaw 到 Clash
if docker exec "$OPENCLAW_CONTAINER" ping -c 2 -W 2 "$CLASH_CONTAINER" >/dev/null 2>&1; then
    echo -e "${GREEN}✅${NC} OpenClaw → Clash: 连通"
else
    echo -e "${YELLOW}⚠️${NC} OpenClaw → Clash: 不通 (尝试使用 IP)"
    CLASH_IP=$(get_container_ip "$CLASH_CONTAINER")
    if [ -n "$CLASH_IP" ] && docker exec "$OPENCLAW_CONTAINER" ping -c 2 -W 2 "$CLASH_IP" >/dev/null 2>&1; then
        echo -e "${GREEN}✅${NC} OpenClaw → Clash(IP): 连通"
    fi
fi

echo ""
echo "🌐 测试服务端口..."
echo ""

# 测试 SearXNG HTTP
SEARXNG_IP=$(get_container_ip "$SEARXNG_CONTAINER")
if [ -n "$SEARXNG_IP" ]; then
    if docker exec "$OPENCLAW_CONTAINER" curl -s --connect-timeout 5 "http://${SEARXNG_IP}:8080/health" >/dev/null 2>&1; then
        echo -e "${GREEN}✅${NC} SearXNG HTTP (8080): 可访问"
    else
        echo -e "${YELLOW}⚠️${NC} SearXNG HTTP (8080): 无法访问"
    fi
fi

# 测试 Clash API
CLASH_IP=$(get_container_ip "$CLASH_CONTAINER")
if [ -n "$CLASH_IP" ]; then
    if docker exec "$OPENCLAW_CONTAINER" curl -s --connect-timeout 5 "http://${CLASH_IP}:9090/health" >/dev/null 2>&1; then
        echo -e "${GREEN}✅${NC} Clash API (9090): 可访问"
    else
        echo -e "${YELLOW}⚠️${NC} Clash API (9090): 无法访问"
    fi
    
    # 测试 Clash 代理端口
    if docker exec "$OPENCLAW_CONTAINER" curl -s --connect-timeout 5 -x "http://${CLASH_IP}:7890" "https://www.google.com" >/dev/null 2>&1; then
        echo -e "${GREEN}✅${NC} Clash 代理 (7890): 可访问"
    else
        echo -e "${YELLOW}⚠️${NC} Clash 代理 (7890): 无法访问"
    fi
fi

echo ""
echo "=========================================="
echo "✅ 网络配置完成！"
echo "=========================================="
echo ""
echo "📝 下一步操作："
echo ""
echo "1. 更新 OpenClaw 配置文件："
echo "   nano /root/.openclaw/openclaw.json"
echo ""
echo "2. 添加 SearXNG 插件配置（见下方）"
echo ""
echo "3. 重启 OpenClaw 容器："
echo "   docker restart ${OPENCLAW_CONTAINER}"
echo ""
echo "=========================================="
echo ""
echo "📋 OpenClaw 配置片段："
echo ""
cat << 'EOF'
{
  "plugins": {
    "entries": {
      "feishu": { "enabled": true },
      "searxng": {
        "enabled": true,
        "config": {
          "url": "http://searxng:8080",
          "engines": ["google", "baidu", "bing", "duckduckgo", "wikipedia"],
          "timeout": 10
        }
      }
    }
  }
}
EOF
echo ""
echo "=========================================="
