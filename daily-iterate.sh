#!/bin/bash
# 技能每日迭代脚本
# 用法：./daily-iterate.sh <skill-name> [version-type]
# version-type: patch (默认) | minor | major

set -e

# 配置
WORKSPACE="/root/.openclaw/workspace"
SKILLS_DIR="$WORKSPACE/skills"
DATE=$(date +%Y-%m-%d)
DATETIME=$(date +%Y-%m-%d_%H-%M-%S)

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印函数
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
print_success() { echo -e "${GREEN}✅  $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_error() { echo -e "${RED}❌  $1${NC}"; }

# 获取当前版本号
get_current_version() {
    local skill_name=$1
    local skill_file="$SKILLS_DIR/$skill_name/SKILL.md"
    
    if [ -f "$skill_file" ]; then
        # 从 SKILL.md 最后几行提取版本号
        local version=$(grep -oP '版本：\s*v\K[0-9]+\.[0-9]+\.[0-9]+' "$skill_file" | tail -1)
        if [ -n "$version" ]; then
            echo "$version"
            return
        fi
    fi
    
    # 从 RELEASE 文件获取
    local latest_release=$(ls -t "$SKILLS_DIR/$skill_name"/RELEASE-*.md 2>/dev/null | head -1)
    if [ -n "$latest_release" ]; then
        local version=$(basename "$latest_release" | grep -oP 'RELEASE-v\K[0-9]+\.[0-9]+\.[0-9]+')
        if [ -n "$version" ]; then
            echo "$version"
            return
        fi
    fi
    
    echo "1.0.0"
}

# 递增版本号
increment_version() {
    local version=$1
    local type=${2:-patch}
    
    local major=$(echo $version | cut -d. -f1)
    local minor=$(echo $version | cut -d. -f2)
    local patch=$(echo $version | cut -d. -f3)
    
    case $type in
        major)
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        minor)
            minor=$((minor + 1))
            patch=0
            ;;
        patch|*)
            patch=$((patch + 1))
            ;;
    esac
    
    echo "$major.$minor.$patch"
}

# 生成 RELEASE 文档
generate_release_doc() {
    local skill_name=$1
    local version=$2
    local prev_version=$3
    
    local release_file="$SKILLS_DIR/$skill_name/RELEASE-v${version}.md"
    
    print_info "生成 RELEASE 文档：$release_file"
    
    # 创建 RELEASE 文档（模板）
    cat > "$release_file" << EOF
# ${skill_name^} v${version} 发布说明

**发布时间：** ${DATE}  
**状态：** GitHub Release 准备中

---

## 🎉 发布信息

### GitHub Release

**URL:** https://github.com/小马 🐴/${skill_name}/releases/tag/v${version}

**发布内容：**
- SKILL.md（技能说明）
- README.md（使用文档）
- LICENSE（许可）
- 其他相关文件

---

## 🆕 本次更新

### 新增功能

- [ ] 功能描述

### 优化改进

- [ ] 优化描述

### 问题修复

- [ ] 修复描述

---

## 📊 版本对比

| 项目 | v${prev_version} | v${version} | 提升 |
|------|-----------|-----------|------|
| 功能 | - | - | - |

---

## 🔧 安装方式

### 方式 1：GitHub 安装

\`\`\`bash
git clone https://github.com/小马 🐴/${skill_name}.git
cd ${skill_name}
openclaw plugins install -l .
\`\`\`

### 方式 2：ClawHub 安装

\`\`\`bash
clawhub install ${skill_name}
\`\`\`

---

## 📋 完整文档

- [技能说明](SKILL.md)
- [使用文档](README.md)
- [许可证](LICENSE)

---

## 🎯 后续计划

### v${version}（下一步）

- [ ] 计划功能

---

## 📞 反馈与支持

**GitHub Issues:** https://github.com/小马 🐴/${skill_name}/issues  
**Discord:** https://discord.gg/clawd

---

**技能作者：** 小马 🐴  
**版本：** v${version}  
**发布日期：** ${DATE}
EOF
    
    print_success "RELEASE 文档已生成"
}

# 更新 CHANGELOG
update_changelog() {
    local skill_name=$1
    local version=$2
    
    local changelog_file="$SKILLS_DIR/$skill_name/CHANGELOG.md"
    
    if [ ! -f "$changelog_file" ]; then
        print_warning "CHANGELOG.md 不存在，创建中..."
        cat > "$changelog_file" << EOF
# CHANGELOG - ${skill_name^}

所有重要变更将记录在此文件中。

---

## [${version}] - ${DATE}

### 新增

- ✨ 日常迭代更新

### 优化

- 🔧 持续改进

---

**维护者：** 小马 🐴
EOF
        return
    fi
    
    # 在第一个版本条目后插入新版本
    print_info "更新 CHANGELOG..."
    
    # 使用 sed 在第一个 ## [ 后插入新内容
    local temp_file=$(mktemp)
    awk -v version="$version" -v date="$DATE" '
    /^## \[/ && !inserted {
        print ""
        print "## [" version "] - " date
        print ""
        print "### 新增"
        print ""
        print "- ✨ 日常迭代更新"
        print ""
        print "### 优化"
        print ""
        print "- 🔧 持续改进"
        print ""
        inserted = 1
    }
    { print }
    ' "$changelog_file" > "$temp_file"
    
    mv "$temp_file" "$changelog_file"
    print_success "CHANGELOG 已更新"
}

# 更新 SKILL.md 版本号
update_skill_version() {
    local skill_name=$1
    local version=$2
    
    local skill_file="$SKILLS_DIR/$skill_name/SKILL.md"
    
    if [ ! -f "$skill_file" ]; then
        print_error "SKILL.md 不存在：$skill_file"
        return 1
    fi
    
    print_info "更新 SKILL.md 版本号..."
    
    # 更新版本号行
    sed -i "s/版本：v[0-9]\+\.[0-9]\+\.[0-9]\+/版本：v${version}/g" "$skill_file"
    sed -i "s/最后更新：.*/最后更新：${DATE}/g" "$skill_file"
    
    print_success "SKILL.md 已更新"
}

# Git 提交
git_commit() {
    local skill_name=$1
    local version=$2
    
    print_info "Git 提交更改..."
    
    cd "$WORKSPACE"
    
    git add "skills/$skill_name"
    git commit -m "Release ${skill_name} v${version} (${DATE})" || print_warning "Git 提交失败（可能无更改）"
    
    print_success "Git 提交完成"
}

# 主函数
main() {
    local skill_name=$1
    local version_type=${2:-patch}
    
    if [ -z "$skill_name" ]; then
        print_error "用法：$0 <skill-name> [patch|minor|major]"
        echo ""
        echo "可用技能:"
        ls -1 "$SKILLS_DIR" | grep -v "^\." | grep -v "^{"
        exit 1
    fi
    
    if [ ! -d "$SKILLS_DIR/$skill_name" ]; then
        print_error "技能不存在：$skill_name"
        exit 1
    fi
    
    echo ""
    print_info "=========================================="
    print_info "技能每日迭代更新"
    print_info "=========================================="
    echo ""
    
    # 获取版本号
    local current_version=$(get_current_version "$skill_name")
    local new_version=$(increment_version "$current_version" "$version_type")
    
    print_info "技能名称：$skill_name"
    print_info "当前版本：v$current_version"
    print_info "新版本号：v$new_version"
    print_info "更新日期：$DATE"
    echo ""
    
    # 执行更新
    update_skill_version "$skill_name" "$new_version"
    generate_release_doc "$skill_name" "$new_version" "$current_version"
    update_changelog "$skill_name" "$new_version"
    git_commit "$skill_name" "$new_version"
    
    echo ""
    print_success "=========================================="
    print_success "迭代完成！"
    print_success "=========================================="
    print_success "技能：$skill_name"
    print_success "版本：v$current_version → v$new_version"
    print_success "日期：$DATE"
    echo ""
    print_info "下一步操作:"
    print_info "  1. 检查生成的文件"
    print_info "  2. 运行 ./sync-github.sh 同步到 GitHub"
    print_info "  3. 验证 ClawHub 发布状态"
    echo ""
}

# 执行
main "$@"
