#!/bin/bash
# GitHub 同步推送脚本
# 用途：将自研技能同步推送到 GitHub

set -e

SKILLS_DIR="/root/.openclaw/workspace/skills"
GITHUB_USER="pengong101"
GITHUB_ORG="pengong101"

echo "======================================"
echo "🔄 GitHub 同步推送脚本"
echo "======================================"
echo ""

# Git 配置
git config --global user.email "pengong101@gmail.com"
git config --global user.name "pengong101"

# 需要同步的技能列表
declare -A SKILLS=(
    ["ai-humanizer-cn"]="v4.0.0"
    ["searxng-auto-proxy"]="v3.0.0"
    ["clash-auto-control"]="v2.0.0"
    ["secretary-core"]="v3.0.0"
    ["memory-search"]="v1.0.0"
)

# 遍历技能
for skill_name in "${!SKILLS[@]}"; do
    version="${SKILLS[$skill_name]}"
    skill_path="$SKILLS_DIR/$skill_name"
    
    echo "📦 处理：$skill_name $version"
    
    if [ ! -d "$skill_path" ]; then
        echo "  ⚠️  目录不存在，跳过"
        continue
    fi
    
    cd "$skill_path"
    
    # 检查是否是 git 仓库
    if [ ! -d ".git" ]; then
        echo "  📝 初始化 Git 仓库..."
        git init
        git remote add origin "https://github.com/$GITHUB_ORG/$skill_name.git"
    fi
    
    # 创建 clawhub.json
    echo "  📄 创建 clawhub.json..."
    cat > clawhub.json << EOF
{
  "name": "$skill_name",
  "version": "$version",
  "author": "$GITHUB_USER",
  "license": "MIT",
  "description": "OpenClaw Skill - $skill_name"
}
EOF
    
    # 添加所有文件
    echo "  ➕ 添加文件..."
    git add -A
    
    # 检查是否有变更
    if git diff --staged --quiet; then
        echo "  ⏭️  无变更，跳过"
        continue
    fi
    
    # 提交
    echo "  💾 提交变更..."
    git commit -m "feat: release $version - automated sync"
    
    # 推送（如果远程存在）
    echo "  🚀 推送到 GitHub..."
    if git push -u origin main 2>/dev/null || git push -u origin master 2>/dev/null; then
        echo "  ✅ 推送成功"
    else
        echo "  ⚠️  推送失败（可能远程仓库不存在）"
        echo "  💡 请手动创建 GitHub 仓库后重试"
    fi
    
    echo ""
done

echo "======================================"
echo "✅ GitHub 同步完成！"
echo "======================================"
echo ""
echo "📊 统计："
echo "  处理技能：${#SKILLS[@]} 个"
echo "  成功推送：待确认"
echo ""
echo "📦 ClawHub 包位置："
echo "  /root/.openclaw/workspace/clawhub-packages/"
echo ""
