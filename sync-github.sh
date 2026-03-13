#!/bin/bash
# GitHub 同步脚本
# 用法：./sync-github.sh [skill-name]

set -e

# 配置
WORKSPACE="/root/.openclaw/workspace"
SKILLS_DIR="$WORKSPACE/skills"
DATE=$(date +%Y-%m-%d)

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
print_success() { echo -e "${GREEN}✅  $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_error() { echo -e "${RED}❌  $1${NC}"; }

# 检查 Git 配置
check_git_config() {
    cd "$WORKSPACE"
    
    if ! git config user.name > /dev/null 2>&1; then
        print_warning "Git 用户未配置，请设置:"
        echo "  git config user.name '你的用户名'"
        echo "  git config user.email '你的邮箱'"
        return 1
    fi
    
    # 检查 remote
    if ! git remote get-url origin > /dev/null 2>&1; then
        print_warning "Git remote 未配置"
        print_info "添加 GitHub remote:"
        echo "  git remote add origin https://github.com/小马 🐴/skills.git"
        return 1
    fi
    
    return 0
}

# 推送代码到 GitHub
push_to_github() {
    local skill_name=$1
    
    cd "$WORKSPACE"
    
    print_info "推送代码到 GitHub..."
    
    # 检查是否有更改
    if git diff --quiet && git diff --cached --quiet; then
        print_info "没有需要提交的更改"
    else
        git add .
        git commit -m "Sync skills update ($DATE)" || print_warning "提交失败（可能无更改）"
    fi
    
    # 推送
    print_info "推送到远程仓库..."
    git push origin main 2>&1 || {
        print_warning "推送失败，可能需要先拉取远程更改"
        git pull --rebase origin main || print_error "拉取失败"
        git push origin main || print_error "推送失败"
    }
    
    print_success "代码已推送到 GitHub"
}

# 创建 GitHub Release
create_github_release() {
    local skill_name=$1
    local version=$2
    
    print_info "创建 GitHub Release: $skill_name v$version"
    
    # 检查是否有 RELEASE 文件
    local release_file="$SKILLS_DIR/$skill_name/RELEASE-v${version}.md"
    if [ ! -f "$release_file" ]; then
        print_warning "RELEASE 文件不存在：$release_file"
        return 1
    fi
    
    # 使用 gh CLI 创建 release（如果可用）
    if command -v gh &> /dev/null; then
        print_info "使用 gh CLI 创建 release..."
        gh release create "v${version}" \
            --repo "小马 🐴/$skill_name" \
            --title "${skill_name^} v${version}" \
            --notes-file "$release_file" \
            --generate-notes || print_warning "gh release 创建失败"
    else
        print_warning "gh CLI 未安装，请手动创建 release"
        print_info "访问：https://github.com/小马 🐴/$skill_name/releases/new"
        print_info "标签：v${version}"
        print_info "标题：${skill_name^} v${version}"
    fi
}

# 获取最新版本号
get_latest_version() {
    local skill_name=$1
    local latest_release=$(ls -t "$SKILLS_DIR/$skill_name"/RELEASE-*.md 2>/dev/null | head -1)
    
    if [ -n "$latest_release" ]; then
        basename "$latest_release" | grep -oP 'RELEASE-v\K[0-9]+\.[0-9]+\.[0-9]+'
    else
        echo "1.0.0"
    fi
}

# 同步指定技能
sync_skill() {
    local skill_name=$1
    
    print_info "=========================================="
    print_info "同步技能：$skill_name"
    print_info "=========================================="
    echo ""
    
    # 获取最新版本
    local version=$(get_latest_version "$skill_name")
    print_info "最新版本：v$version"
    
    # 创建 GitHub Release
    create_github_release "$skill_name" "$version"
    
    echo ""
}

# 验证发布
verify_releases() {
    print_info "验证 GitHub 发布..."
    
    # 检查技能目录
    for skill_dir in "$SKILLS_DIR"/*/; do
        if [ -d "$skill_dir" ]; then
            local skill_name=$(basename "$skill_dir")
            local release_count=$(ls "$skill_dir"/RELEASE-*.md 2>/dev/null | wc -l)
            
            if [ "$release_count" -gt 0 ]; then
                print_success "$skill_name: $release_count 个版本"
            else
                print_warning "$skill_name: 无 RELEASE 文件"
            fi
        fi
    done
}

# 主函数
main() {
    local skill_name=$1
    
    echo ""
    print_info "=========================================="
    print_info "GitHub 同步脚本"
    print_info "日期：$DATE"
    print_info "=========================================="
    echo ""
    
    # 检查 Git 配置
    if ! check_git_config; then
        print_error "Git 配置不完整，请先配置"
        exit 1
    fi
    
    # 如果有指定技能，只同步该技能
    if [ -n "$skill_name" ]; then
        if [ ! -d "$SKILLS_DIR/$skill_name" ]; then
            print_error "技能不存在：$skill_name"
            exit 1
        fi
        sync_skill "$skill_name"
    else
        # 同步所有技能
        print_info "同步所有技能..."
        echo ""
        
        for skill_dir in "$SKILLS_DIR"/*/; do
            if [ -d "$skill_dir" ]; then
                local skill=$(basename "$skill_dir")
                # 跳过隐藏目录和特殊目录
                if [[ ! "$skill" =~ ^\. ]] && [[ ! "$skill" =~ ^\{ ]]; then
                    sync_skill "$skill"
                fi
            fi
        done
    fi
    
    # 推送代码
    echo ""
    push_to_github
    
    # 验证
    echo ""
    verify_releases
    
    echo ""
    print_success "=========================================="
    print_success "GitHub 同步完成！"
    print_success "=========================================="
    print_info ""
    print_info "下一步:"
    print_info "  1. 检查 GitHub Releases: https://github.com/小马 🐴?tab=repositories"
    print_info "  2. 验证 ClawHub 发布状态"
    print_info "  3. 通知用户更新完成"
    echo ""
}

# 执行
main "$@"
