#!/bin/bash
# ClawHub 一键发布脚本
# 用法：./clawhub-publish.sh <技能目录> <slug> <名称>

set -e

SKILL_DIR=$1
SLUG=$2
NAME=$3
CHANGELOG=${4:-"Auto-release"}

if [ -z "$SKILL_DIR" ] || [ -z "$SLUG" ] || [ -z "$NAME" ]; then
    echo "❌ 用法：$0 <技能目录> <slug> <名称> [更新日志]"
    echo ""
    echo "示例："
    echo "  $0 ./my-skill my-skill \"My Skill\" \"Initial release\""
    exit 1
fi

echo "🚀 发布技能到 ClawHub..."
echo "================================"
echo "📦 技能目录：$SKILL_DIR"
echo "🏷️  Slug: $SLUG"
echo "📝 名称：$NAME"
echo "📋 更新日志：$CHANGELOG"
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

# 发布
echo ""
echo "📤 发布中..."
clawhub publish "$SKILL_DIR" \
  --slug "$SLUG" \
  --name "$NAME" \
  --changelog "$CHANGELOG"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 发布成功！"
    echo "🌐 ClawHub: https://clawhub.com/skill/$SLUG"
else
    echo ""
    echo "❌ 发布失败！"
    echo "💡 检查 ClawHub Token 是否配置正确"
    echo "💡 运行 'clawhub login' 重新登录"
    exit 1
fi
