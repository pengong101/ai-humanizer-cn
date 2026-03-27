#!/bin/bash
# SearXNG 高效调试脚本 v2.0
# 融合方案：批量执行 + 自动化 + 并行检查
# 创建时间：2026-03-20

set -e

echo "=========================================="
echo "  SearXNG 高效调试脚本 v2.0"
echo "=========================================="
echo ""

# 配置
CONTAINER_NAME="searxng"
HOST_CONFIG="/root/.openclaw/searxng/settings.yml"
CONTAINER_CONFIG="/etc/searxng/settings.yml"
NETWORK="openclaw_openclaw-net"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}✅${NC} $1"; }
log_warn() { echo -e "${YELLOW}⚠️${NC} $1"; }
log_error() { echo -e "${RED}❌${NC} $1"; }

# 步骤 1：完全清理
echo "=== 步骤 1：完全清理 ==="
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm -v $CONTAINER_NAME 2>/dev/null || true
docker volume prune -f > /dev/null 2>&1
log_info "容器和 volume 已清理"

# 步骤 2：确认宿主机文件
echo ""
echo "=== 步骤 2：确认宿主机文件 ==="
if [ ! -f "$HOST_CONFIG" ]; then
    log_error "配置文件不存在：$HOST_CONFIG"
    exit 1
fi

HOST_LINES=$(wc -l < "$HOST_CONFIG")
HOST_SIZE=$(wc -c < "$HOST_CONFIG")
log_info "宿主机文件：$HOST_LINES 行，$HOST_SIZE 字节"

# 步骤 3：创建容器
echo ""
echo "=== 步骤 3：创建容器 ==="
docker create --name $CONTAINER_NAME \
    --network $NETWORK \
    -v "$HOST_CONFIG:$CONTAINER_CONFIG:ro" \
    -p 8081:8080 \
    -e FORCE_OWNERSHIP=false \
    searxng/searxng:latest > /dev/null

CONTAINER_ID=$(docker inspect -f '{{.Id}}' $CONTAINER_NAME | cut -c1-12)
log_info "容器 ID: $CONTAINER_ID"

# 步骤 4：验证挂载（关键！）
echo ""
echo "=== 步骤 4：验证挂载 ==="

# 用临时容器检查挂载的文件
TEMP_LINES=$(docker run --rm -v "$HOST_CONFIG:/test:ro" alpine wc -l < /test 2>/dev/null)
TEMP_SIZE=$(docker run --rm -v "$HOST_CONFIG:/test:ro" alpine wc -c < /test 2>/dev/null)

log_info "临时容器检查：$TEMP_LINES 行，$TEMP_SIZE 字节"

if [ "$HOST_LINES" != "$TEMP_LINES" ] || [ "$HOST_SIZE" != "$TEMP_SIZE" ]; then
    log_error "挂载验证失败！宿主机和容器内文件不一致"
    log_warn "宿主机：$HOST_LINES 行，$HOST_SIZE 字节"
    log_warn "容器内：$TEMP_LINES 行，$TEMP_SIZE 字节"
    log_warn "可能原因：Docker volume 覆盖了 bind mount"
    log_warn "解决方案：docker volume prune -f 后重新创建容器"
    exit 1
fi

log_info "挂载验证通过！"

# 步骤 5：启动容器
echo ""
echo "=== 步骤 5：启动容器 ==="
docker start $CONTAINER_NAME > /dev/null
log_info "容器已启动"

echo ""
echo "⏳ 等待 20 秒让容器初始化..."
sleep 20

# 步骤 6：快速测试
echo ""
echo "=== 步骤 6：快速测试 ==="

# HTML 测试
HTML_CODE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 http://localhost:8081/ 2>&1 || echo "000")
if [ "$HTML_CODE" = "200" ]; then
    log_info "HTML 测试：HTTP $HTML_CODE ✅"
else
    log_error "HTML 测试：HTTP $HTML_CODE ❌"
fi

# JSON 测试
echo -n "JSON 测试："
JSON_RESULT=$(curl -s --connect-timeout 5 "http://localhost:8081/search?q=test&format=json" 2>&1)
if echo "$JSON_RESULT" | python3 -c "import sys,json; json.load(sys.stdin)" 2>/dev/null; then
    RESULT_COUNT=$(echo "$JSON_RESULT" | python3 -c "import sys,json; print(len(json.load(sys.stdin).get('results', [])))")
    log_info "JSON API 正常！$RESULT_COUNT 条结果 ✅"
else
    log_error "JSON API 失败 ❌"
    echo "$JSON_RESULT" | head -c 200
fi

# 步骤 7：容器状态
echo ""
echo "=== 步骤 7：容器状态 ==="
CONTAINER_STATUS=$(docker inspect -f '{{.State.Status}}' $CONTAINER_NAME 2>/dev/null)
CONTAINER_RESTARTS=$(docker inspect -f '{{.RestartCount}}' $CONTAINER_NAME 2>/dev/null)

if [ "$CONTAINER_STATUS" = "running" ]; then
    log_info "容器状态：running ✅"
else
    log_warn "容器状态：$CONTAINER_STATUS"
fi

if [ "$CONTAINER_RESTARTS" = "0" ]; then
    log_info "重启次数：0 ✅"
else
    log_warn "重启次数：$CONTAINER_RESTARTS"
fi

# 完成
echo ""
echo "=========================================="
echo "  调试脚本完成"
echo "=========================================="

if [ "$HTML_CODE" = "200" ] && echo "$JSON_RESULT" | python3 -c "import sys,json; json.load(sys.stdin)" 2>/dev/null; then
    log_info "所有测试通过！SearXNG 运行正常"
    exit 0
else
    log_warn "部分测试失败，请检查日志：docker logs $CONTAINER_NAME"
    exit 1
fi
