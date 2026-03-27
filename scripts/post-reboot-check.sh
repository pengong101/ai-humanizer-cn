#!/bin/bash
# NAS 重启后自检脚本

echo "=========================================="
echo "🔍 NAS 重启后自检"
echo "=========================================="

# 等待 Docker 完全启动
sleep 30

# 检查容器状态
echo -e "\n📊 容器状态检查:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 检查关键服务
echo -e "\n🔧 关键服务检查:"

# OpenClaw
if docker ps | grep -q xiaoma; then
    echo "✅ OpenClaw 运行正常"
else
    echo "❌ OpenClaw 未运行"
fi

# SearXNG
if docker ps | grep -q searxng; then
    echo "✅ SearXNG 运行正常"
else
    echo "❌ SearXNG 未运行"
fi

# Clash
if docker ps | grep -q clash; then
    echo "✅ Clash 运行正常"
else
    echo "❌ Clash 未运行"
fi

# 测试搜索
echo -e "\n🔍 搜索功能测试:"
sleep 10
if curl -s --connect-timeout 5 "http://localhost:8081/search?q=test" | grep -q "SearXNG"; then
    echo "✅ SearXNG 搜索正常"
else
    echo "⚠️ SearXNG 搜索可能异常"
fi

echo -e "\n=========================================="
echo "✅ 自检完成"
echo "=========================================="
