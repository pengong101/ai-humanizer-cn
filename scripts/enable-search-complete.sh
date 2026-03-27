#!/bin/bash
# 完整搜索能力启用脚本 - 一键执行所有步骤
# 执行方式：在 NAS 宿主机上运行此脚本

set -e

echo "=========================================="
echo "🚀 OpenClaw 完整搜索能力启用脚本"
echo "=========================================="
echo ""
echo "此脚本将执行："
echo "  1. 创建共享网络"
echo "  2. 连接所有容器"
echo "  3. 更新 OpenClaw 配置"
echo "  4. 重启 OpenClaw 容器"
echo "  5. 验证搜索功能"
echo ""
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 配置
OPENCLAW_CONTAINER="xiaoma_new"
SEARXNG_CONTAINER="searxng"
CLASH_CONTAINER="clash"
NETWORK_NAME="openclaw-net"
CONFIG_FILE="/root/.openclaw/openclaw.json"
BACKUP_DIR="/root/.openclaw/config-backups"

# 步骤 1：检查容器
echo "📋 步骤 1/6: 检查容器状态..."
echo ""

for container in "$OPENCLAW_CONTAINER" "$SEARXNG_CONTAINER" "$CLASH_CONTAINER"; do
    if docker ps -a --format '{{.Names}}' | grep -q "^${container}$"; then
        status=$(docker ps --format '{{.Names}}:{{.Status}}' | grep "^${container}:" | cut -d: -f2)
        if [[ "$status" == *"Up"* ]]; then
            echo -e "${GREEN}✅${NC} ${container}: 运行中"
        else
            echo -e "${YELLOW}⚠️${NC} ${container}: 已停止"
        fi
    else
        echo -e "${RED}❌${NC} ${container}: 不存在"
        exit 1
    fi
done

echo ""

# 步骤 2：创建网络
echo "📋 步骤 2/6: 创建共享网络..."
echo ""

if docker network ls --format '{{.Name}}' | grep -q "^${NETWORK_NAME}$"; then
    echo -e "${YELLOW}⚠️${NC} 网络已存在，跳过创建"
else
    docker network create "$NETWORK_NAME"
    echo -e "${GREEN}✅${NC} 网络 ${NETWORK_NAME} 创建成功"
fi

echo ""

# 步骤 3：连接容器
echo "📋 步骤 3/6: 连接容器到共享网络..."
echo ""

for container in "$OPENCLAW_CONTAINER" "$SEARXNG_CONTAINER" "$CLASH_CONTAINER"; do
    if docker network inspect "$NETWORK_NAME" --format '{{range .Containers}}{{.Name}} {{end}}' | grep -q "$container"; then
        echo -e "${YELLOW}⚠️${NC} ${container} 已连接"
    else
        docker network connect "$NETWORK_NAME" "$container"
        echo -e "${GREEN}✅${NC} ${container} 已连接"
    fi
done

echo ""

# 步骤 4：更新配置
echo "📋 步骤 4/6: 更新 OpenClaw 配置..."
echo ""

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p "$BACKUP_DIR"

# 备份
if [ -f "$CONFIG_FILE" ]; then
    cp "$CONFIG_FILE" "${BACKUP_DIR}/openclaw_backup_${TIMESTAMP}.json"
    echo -e "${GREEN}✅${NC} 配置已备份"
fi

# 解锁
[ ! -w "$CONFIG_FILE" ] && chmod 644 "$CONFIG_FILE"

# 更新配置
python3 << 'PYTHON_SCRIPT'
import json

config_file = "/root/.openclaw/openclaw.json"

with open(config_file, 'r', encoding='utf-8') as f:
    config = json.load(f)

if 'plugins' not in config:
    config['plugins'] = {'entries': {}}
if 'entries' not in config['plugins']:
    config['plugins']['entries'] = {}

config['plugins']['entries']['searxng'] = {
    'enabled': True,
    'config': {
        'url': 'http://searxng:8080',
        'engines': ['google', 'baidu', 'bing', 'duckduckgo', 'wikipedia', 'brave'],
        'timeout': 10,
        'max_results': 20
    }
}

config['plugins']['entries']['feishu'] = {'enabled': True}

with open(config_file, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
    f.write('\n')

print("✅ 配置已更新")
PYTHON_SCRIPT

# 验证
if python3 -m json.tool "$CONFIG_FILE" >/dev/null 2>&1; then
    echo -e "${GREEN}✅${NC} 配置验证通过"
else
    echo -e "${RED}❌${NC} 配置验证失败"
    exit 1
fi

# 锁定
chmod 444 "$CONFIG_FILE"

echo ""

# 步骤 5：重启容器
echo "📋 步骤 5/6: 重启 OpenClaw 容器..."
echo ""

docker restart "$OPENCLAW_CONTAINER"
echo -e "${GREEN}✅${NC} 容器已重启"

# 等待容器启动
echo "⏳ 等待容器启动..."
sleep 10

echo ""

# 步骤 6：验证
echo "📋 步骤 6/6: 验证服务..."
echo ""

# 获取容器 IP
SEARXNG_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$SEARXNG_CONTAINER" 2>/dev/null)
CLASH_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$CLASH_CONTAINER" 2>/dev/null)

echo "容器 IP："
echo "  - SearXNG: ${SEARXNG_IP:-未知}"
echo "  - Clash: ${CLASH_IP:-未知}"
echo ""

# 测试连接
if docker exec "$OPENCLAW_CONTAINER" ping -c 1 -W 2 "$SEARXNG_CONTAINER" >/dev/null 2>&1; then
    echo -e "${GREEN}✅${NC} OpenClaw → SearXNG: 连通"
else
    echo -e "${YELLOW}⚠️${NC} OpenClaw → SearXNG: 不通"
fi

if docker exec "$OPENCLAW_CONTAINER" ping -c 1 -W 2 "$CLASH_CONTAINER" >/dev/null 2>&1; then
    echo -e "${GREEN}✅${NC} OpenClaw → Clash: 连通"
else
    echo -e "${YELLOW}⚠️${NC} OpenClaw → Clash: 不通"
fi

echo ""
echo "=========================================="
echo "✅ 全部完成！"
echo "=========================================="
echo ""
echo "🎉 搜索能力已启用！"
echo ""
echo "📝 测试方法："
echo ""
echo "1. 在飞书中发送消息："
echo "   搜索 OpenClaw"
echo ""
echo "2. 或使用搜索命令："
echo "   /search <关键词>"
echo ""
echo "3. 查看日志（如有问题）："
echo "   docker logs xiaoma_new --tail 100"
echo ""
echo "=========================================="
