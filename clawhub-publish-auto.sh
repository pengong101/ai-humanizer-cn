#!/bin/bash
# ClawHub 自主发布脚本 v2.0
# 功能：自动解决 acceptLicenseTerms 问题，实现自主发布

set -e

SKILL_DIR=$1
SLUG=$2
NAME=$3
VERSION=$4
CHANGELOG=$5

if [ -z "$SKILL_DIR" ] || [ -z "$SLUG" ] || [ -z "$NAME" ]; then
    echo "❌ 用法：$0 <技能目录> <slug> <名称> [版本] [更新日志]"
    echo ""
    echo "示例："
    echo "  $0 ./my-skill my-skill \"My Skill\" 1.0.0 \"Initial release\""
    exit 1
fi

# 默认值
VERSION=${VERSION:-1.0.0}
CHANGELOG=${CHANGELOG:-Auto-release}

echo "🚀 ClawHub 自主发布脚本 v2.0"
echo "================================"
echo "📦 技能目录：$SKILL_DIR"
echo "🏷️  Slug: $SLUG"
echo "📝 名称：$NAME"
echo "📋 版本：$VERSION"
echo "📝 更新日志：$CHANGELOG"
echo "================================"

# 检查目录存在
if [ ! -d "$SKILL_DIR" ]; then
    echo "❌ 技能目录不存在：$SKILL_DIR"
    exit 1
fi

# 检查 SKILL.md
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "❌ 缺少 SKILL.md 文件"
    exit 1
fi

# 检查 license 字段
if ! grep -q "^license:" "$SKILL_DIR/SKILL.md"; then
    echo "⚠️  SKILL.md 缺少 license 字段，自动添加..."
    sed -i 's/^---$/license: MIT\n---/' "$SKILL_DIR/SKILL.md"
    echo "✅ 已添加 license: MIT"
fi

# 检查 metadata 中的 acceptLicenseTerms
if grep -q "acceptLicenseTerms" "$SKILL_DIR/SKILL.md"; then
    echo "⚠️  移除 acceptLicenseTerms 字段（ClawHub API 不支持）..."
    sed -i '/acceptLicenseTerms/d' "$SKILL_DIR/SKILL.md"
    echo "✅ 已移除 acceptLicenseTerms"
fi

# 创建临时发布包
TEMP_DIR=$(mktemp -d)
echo "📦 创建临时发布包：$TEMP_DIR"

# 复制技能文件
cp -r "$SKILL_DIR"/* "$TEMP_DIR/"

# 创建发布元数据
cat > "$TEMP_DIR/_meta.json" << EOF
{
  "slug": "$SLUG",
  "name": "$NAME",
  "version": "$VERSION",
  "changelog": "$CHANGELOG",
  "license": "MIT",
  "publishedAt": "$(date -Iseconds)"
}
EOF

echo ""
echo "📤 发布到 ClawHub..."

# 尝试发布（带重试）
MAX_RETRIES=3
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    echo "🔄 尝试发布 (第 $((RETRY_COUNT+1)) 次)..."
    
    if clawhub publish "$TEMP_DIR" \
      --slug "$SLUG" \
      --name "$NAME" \
      --version "$VERSION" \
      --changelog "$CHANGELOG" 2>&1; then
        echo ""
        echo "✅ 发布成功！"
        echo "🌐 ClawHub: https://clawhub.com/skill/$SLUG"
        
        # 清理临时目录
        rm -rf "$TEMP_DIR"
        exit 0
    else
        echo "⚠️  发布失败"
        RETRY_COUNT=$((RETRY_COUNT+1))
        if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
            echo "⏳ 5 秒后重试..."
            sleep 5
        fi
    fi
done

# 所有重试失败
echo ""
echo "❌ 发布失败（已重试 $MAX_RETRIES 次）"
echo ""
echo "💡 建议解决方案："
echo "  1. 检查 ClawHub Token 是否有效"
echo "  2. 运行 'clawhub login' 重新登录"
echo "  3. 检查 SKILL.md 格式是否正确"
echo "  4. 使用 GitHub Release 备选方案"
echo ""
echo "📦 临时目录保留：$TEMP_DIR"
echo ""

# 创建 GitHub Release 备选方案
echo "🔄 准备 GitHub Release 备选方案..."

if [ -d "$SKILL_DIR/.git" ] || git -C "$SKILL_DIR" rev-parse --git-dir > /dev/null 2>&1; then
    echo "✅ Git 仓库存在，可以创建 GitHub Release"
    echo ""
    echo "📋 GitHub Release 命令："
    echo "  cd $SKILL_DIR"
    echo "  git tag -a v$VERSION -m \"$NAME v$VERSION\""
    echo "  git push origin v$VERSION"
    echo ""
    echo "  然后访问：https://github.com/pengong101/$SLUG/releases/new"
else
    echo "⚠️  非 Git 仓库，建议手动创建 GitHub Release"
fi

exit 1
