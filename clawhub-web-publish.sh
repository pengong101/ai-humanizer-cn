#!/bin/bash
# ClawHub 网页发布脚本 v1.0
# 功能：通过网页表单模拟发布技能

set -e

SKILL_DIR=$1
SLUG=$2
NAME=$3
VERSION=$4
CHANGELOG=$5

if [ -z "$SKILL_DIR" ] || [ -z "$SLUG" ] || [ -z "$NAME" ]; then
    echo "❌ 用法：$0 <技能目录> <slug> <名称> [版本] [更新日志]"
    exit 1
fi

VERSION=${VERSION:-1.0.0}
CHANGELOG=${CHANGELOG:-Auto-release}

echo "🚀 ClawHub 网页发布脚本 v1.0"
echo "================================"
echo "📦 技能目录：$SKILL_DIR"
echo "🏷️  Slug: $SLUG"
echo "📝 名称：$NAME"
echo "📋 版本：$VERSION"
echo "================================"

# 检查 SKILL.md
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "❌ 缺少 SKILL.md 文件"
    exit 1
fi

# 创建临时 ZIP 包
TEMP_DIR=$(mktemp -d)
ZIP_FILE="$TEMP_DIR/$SLUG-$VERSION.zip"

echo "📦 创建技能包..."
cd "$SKILL_DIR"
if command -v zip &> /dev/null; then
    zip -r "$ZIP_FILE" . -x "*.git*" > /dev/null 2>&1
else
    # 使用 Python 创建 ZIP
    python3 -c "
import zipfile
import os
import sys

zip_path = '$ZIP_FILE'
src_dir = '.'

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if not file.startswith('.git'):
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, src_dir)
                zipf.write(file_path, arcname)
"
fi
cd - > /dev/null

echo "📤 上传到 ClawHub..."

# 获取登录 Token（从配置文件）
CLAWHUB_TOKEN=${CLAWHUB_TOKEN:-""}
if [ -z "$CLAWHUB_TOKEN" ]; then
    # 尝试从 clawhub config 读取
    CONFIG_FILE="$HOME/.clawhub/config.json"
    if [ -f "$CONFIG_FILE" ]; then
        CLAWHUB_TOKEN=$(cat "$CONFIG_FILE" | grep -o '"token"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)
    fi
fi

if [ -z "$CLAWHUB_TOKEN" ]; then
    echo "❌ 未找到 ClawHub Token"
    echo "💡 请设置环境变量 CLAWHUB_TOKEN 或运行 'clawhub login'"
    rm -rf "$TEMP_DIR"
    exit 1
fi

# 模拟网页表单提交
RESPONSE=$(curl -s -X POST "https://clawhub.ai/api/v1/skills" \
  -H "Authorization: Bearer $CLAWHUB_TOKEN" \
  -H "Content-Type: multipart/form-data" \
  -F "slug=$SLUG" \
  -F "name=$NAME" \
  -F "version=$VERSION" \
  -F "changelog=$CHANGELOG" \
  -F "license=MIT" \
  -F "package=@$ZIP_FILE" \
  -w "\n%{http_code}")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

# 清理临时文件
rm -rf "$TEMP_DIR"

# 检查响应
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "201" ]; then
    echo "✅ 发布成功！"
    echo "🌐 ClawHub: https://clawhub.com/skill/$SLUG"
    exit 0
elif [ "$HTTP_CODE" = "400" ]; then
    echo "❌ 发布失败：400 Bad Request"
    echo "📝 响应：$BODY"
    echo ""
    echo "💡 可能是 acceptLicenseTerms 字段问题"
    echo "💡 建议使用 GitHub Release 备选方案"
    exit 1
elif [ "$HTTP_CODE" = "401" ]; then
    echo "❌ 认证失败：401 Unauthorized"
    echo "💡 请检查 Token 是否有效"
    echo "💡 运行 'clawhub login' 重新登录"
    exit 1
else
    echo "❌ 发布失败：HTTP $HTTP_CODE"
    echo "📝 响应：$BODY"
    exit 1
fi
