#!/bin/bash
# 安全加载账号凭证

set -e

CREDENTIALS_FILE="/root/.openclaw/workspace/.credentials.enc"

if [ ! -f "$CREDENTIALS_FILE" ]; then
    echo "❌ 凭证文件不存在：$CREDENTIALS_FILE"
    exit 1
fi

# 检查文件权限
PERMS=$(stat -c %a "$CREDENTIALS_FILE")
if [ "$PERMS" != "600" ]; then
    echo "⚠️  警告：凭证文件权限不是 600，正在修复..."
    chmod 600 "$CREDENTIALS_FILE"
fi

# 解码并导出凭证
export CLAWHUB_TOKEN=$(grep "^CLAWHUB_TOKEN:" "$CREDENTIALS_FILE" 2>/dev/null | cut -d':' -f2 | base64 -d 2>/dev/null || echo "")
export GITHUB_TOKEN=$(grep "^GITHUB_TOKEN:" "$CREDENTIALS_FILE" 2>/dev/null | cut -d':' -f2 | base64 -d 2>/dev/null || echo "")
export ZSPACE_IP=$(grep "^ZSPACE_IP:" "$CREDENTIALS_FILE" 2>/dev/null | cut -d':' -f2 | base64 -d 2>/dev/null || echo "192.168.1.122")

# 验证
if [ -n "$CLAWHUB_TOKEN" ]; then
    echo "✅ ClawHub Token 已加载"
else
    echo "⚠️  ClawHub Token 未找到"
fi

if [ -n "$GITHUB_TOKEN" ]; then
    echo "✅ GitHub Token 已加载"
else
    echo "⚠️  GitHub Token 未找到"
fi

if [ -n "$ZSPACE_IP" ]; then
    echo "✅ 极空间 IP: $ZSPACE_IP"
fi

echo ""
echo "💡 使用方式:"
echo "  source /root/.openclaw/workspace/load-credentials.sh"
echo ""
