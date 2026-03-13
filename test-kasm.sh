#!/bin/bash
# Kasm 浏览器快速测试脚本 v1.0
# 使用 curl 直接测试

KASM_HOST="192.168.1.122"
KASM_PORT="56901"
KASM_USER="admin"
KASM_PASS="Zspace123"

echo "🚀 Kasm 浏览器测试 v1.0"
echo ""

# 测试 1: Web 界面
echo "1️⃣ 测试 Web 界面..."
HTTP_CODE=$(curl -k -s -o /dev/null -w "%{http_code}" "https://${KASM_HOST}:${KASM_PORT}/")
if [ "$HTTP_CODE" = "401" ] || [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Web 界面可访问 (HTTP $HTTP_CODE)"
else
    echo "❌ Web 界面不可访问 (HTTP $HTTP_CODE)"
    exit 1
fi

# 测试 2: VNC 端口
echo "2️⃣ 测试 VNC 连接..."
timeout 2 bash -c "echo > /dev/tcp/${KASM_HOST}/5901" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ VNC 端口 5901 可访问"
else
    echo "⚠️  VNC 端口 5901 不可直接访问（正常，需要通过 Kasm）"
fi

# 测试 3: WebSocket 端口
echo "3️⃣ 测试 WebSocket 端口..."
timeout 2 bash -c "echo > /dev/tcp/${KASM_HOST}/16901" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ WebSocket 端口 16901 可访问"
else
    echo "⚠️  WebSocket 端口不可直接访问"
fi

# 测试 4: 容器状态
echo "4️⃣ 检查容器状态..."
CONTAINER_STATUS=$(docker ps --filter "name=browser" --format "{{.Status}}")
if [ -n "$CONTAINER_STATUS" ]; then
    echo "✅ 容器运行中：$CONTAINER_STATUS"
else
    echo "❌ 容器未运行"
    exit 1
fi

echo ""
echo "🎉 Kasm 浏览器状态正常！"
echo ""
echo "📋 连接信息:"
echo "  Web 界面：https://${KASM_HOST}:${KASM_PORT}"
echo "  用户名：${KASM_USER}"
echo "  密码：${KASM_PASS}"
echo ""
echo "💡 使用方式:"
echo "  1. 浏览器访问 Web 界面"
echo "  2. 或使用 OpenClaw browser 工具"
echo "  3. 或等待 API 集成完成"
