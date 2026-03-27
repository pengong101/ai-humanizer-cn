#!/bin/bash
# GitHub 快速推送脚本
# 用法：./push-to-github.sh YOUR_GITHUB_USERNAME

set -e

if [ -z "$1" ]; then
    echo "❌ 请提供 GitHub 用户名"
    echo "用法：$0 YOUR_GITHUB_USERNAME"
    echo ""
    echo "示例："
    echo "  $0 pengong101"
    exit 1
fi

GITHUB_USER=$1
SKILLS_DIR="/root/.openclaw/workspace/skills"

echo "======================================"
echo "🚀 GitHub 快速推送"
echo "======================================"
echo "GitHub 用户：$GITHUB_USER"
echo ""

# Git 配置
git config --global user.email "pengong101@gmail.com"
git config --global user.name "pengong101"

# 技能列表
SKILLS=(
    "ai-humanizer-cn"
    "secretary-core"
    "searxng-auto-proxy"
)

SUCCESS_COUNT=0
FAIL_COUNT=0

for skill in "${SKILLS[@]}"; do
    echo "📦 推送：$skill"
    
    if [ ! -d "$SKILLS_DIR/$skill" ]; then
        echo "  ⚠️  目录不存在，跳过"
        ((FAIL_COUNT++))
        continue
    fi
    
    cd "$SKILLS_DIR/$skill"
    
    # 初始化 git（如果需要）
    if [ ! -d ".git" ]; then
        echo "  📝 初始化 Git..."
        git init
    fi
    
    # 添加所有文件
    echo "  ➕ 添加文件..."
    git add -A
    
    # 检查是否有变更
    if git diff --staged --quiet; then
        echo "  ⏭️  无变更，跳过"
        ((SUCCESS_COUNT++))
        continue
    fi
    
    # 提交
    echo "  💾 提交变更..."
    git commit -m "feat: release latest - automated sync"
    
    # 设置远程仓库
    if ! git remote get-url origin &>/dev/null; then
        echo "  ➕ 添加远程仓库..."
        git remote add origin https://github.com/$GITHUB_USER/$skill.git
    else
        echo "  🔄 更新远程仓库..."
        git remote set-url origin https://github.com/$GITHUB_USER/$skill.git
    fi
    
    # 推送
    echo "  🚀 推送到 GitHub..."
    echo "  🔗 https://github.com/$GITHUB_USER/$skill"
    
    if git push -u origin master 2>&1 || git push -u origin main 2>&1; then
        echo "  ✅ 推送成功！"
        ((SUCCESS_COUNT++))
    else
        echo "  ❌ 推送失败"
        echo "  💡 可能原因："
        echo "     1. GitHub 仓库不存在 - 请先创建空仓库"
        echo "     2. 认证失败 - 请配置 Git 凭证或 Token"
        echo "     3. 网络问题 - 请检查网络连接"
        echo ""
        echo "  🔧 解决方案："
        echo "     1. 访问 https://github.com/new 创建仓库：$skill"
        echo "     2. 配置 Git 凭证：git config --global credential.helper store"
        echo "     3. 重新运行此脚本"
        ((FAIL_COUNT++))
    fi
    echo ""
done

echo "======================================"
echo "📊 推送统计"
echo "======================================"
echo "成功：$SUCCESS_COUNT 个"
echo "失败：$FAIL_COUNT 个"
echo ""

if [ $FAIL_COUNT -gt 0 ]; then
    echo "⚠️  部分推送失败，请查看上方错误信息"
    echo ""
    echo "📖 详细指南："
    echo "   /root/.openclaw/workspace/clawhub-packages/GITHUB-SYNC-GUIDE.md"
    echo ""
    exit 1
else
    echo "🎉 全部推送成功！"
    echo ""
    echo "🔗 查看仓库："
    for skill in "${SKILLS[@]}"; do
        echo "   https://github.com/$GITHUB_USER/$skill"
    done
    echo ""
fi
