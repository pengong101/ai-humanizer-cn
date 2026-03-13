# 技能每日迭代更新系统

**创建时间：** 2026-03-12  
**维护者：** 小马 🐴  
**目标技能：** radar-daily-report, ai-humanizer-cn

---

## 🎯 系统目标

- ✅ **每日迭代** - 每天提供新版手动部署版本
- ✅ **版本管理** - 规范的版本号和内容更新
- ✅ **GitHub 同步** - 自动推送到 GitHub 仓库
- ✅ **发布文档** - 自动生成 RELEASE 文档

---

## 📁 目录结构

```
skills/
├── radar-daily-report/
│   ├── SKILL.md              # 技能说明（每日更新）
│   ├── generate-report.py    # 主脚本（迭代更新）
│   ├── README.md             # 使用文档（迭代更新）
│   ├── RELEASE-v1.0.0.md     # 版本发布说明（每日新增）
│   └── CHANGELOG.md          # 变更日志（持续更新）
│
├── ai-humanizer-cn/
│   ├── SKILL.md              # 技能说明（每日更新）
│   ├── README.md             # 使用文档（迭代更新）
│   ├── RELEASE-v1.0.0.md     # 版本发布说明（已有）
│   ├── RELEASE-v1.0.1.md     # 版本发布说明（每日新增）
│   └── CHANGELOG.md          # 变更日志（持续更新）
│
└── iteration-system/
    ├── daily-iterate.sh      # 每日迭代脚本
    ├── sync-github.sh        # GitHub 同步脚本
    └── version-manager.py    # 版本管理工具
```

---

## 🔄 每日迭代流程

### 时间：每日 08:00

1. **检查更新需求**
   - 用户反馈
   - Bug 报告
   - 功能改进建议

2. **执行迭代更新**
   ```bash
   ./daily-iterate.sh radar-daily-report
   ./daily-iterate.sh ai-humanizer-cn
   ```

3. **生成版本发布文档**
   - 自动创建 RELEASE-vX.Y.Z.md
   - 更新 CHANGELOG.md
   - 更新 SKILL.md 版本号

4. **同步 GitHub**
   ```bash
   ./sync-github.sh
   ```

5. **验证部署**
   - 检查 GitHub Release
   - 验证 ClawHub 状态
   - 发送完成通知

---

## 📋 版本号规范

采用语义化版本号：**MAJOR.MINOR.PATCH**

### 版本号规则

- **MAJOR（主版本）**: 不兼容的 API 变更
- **MINOR（次版本）**: 向后兼容的功能新增
- **PATCH（修订号）**: 向后兼容的问题修正

### 每日迭代策略

- **每日更新**: PATCH 版本号递增（v1.0.0 → v1.0.1 → v1.0.2）
- **每周汇总**: MINOR 版本号递增（v1.0.x → v1.1.0）
- **重大更新**: MAJOR 版本号递增（v1.x.x → v2.0.0）

---

## 📝 RELEASE 文档模板

```markdown
# {技能名称} v{版本号} 发布说明

**发布时间：** {日期}  
**状态：** {GitHub Release 状态} / {ClawHub 状态}

---

## 🎉 发布信息

### GitHub Release

**URL:** {GitHub Release URL}

**发布内容：**
- SKILL.md（技能说明）
- README.md（使用文档）
- LICENSE（许可）
- {其他文件}

---

## 🆕 本次更新

### 新增功能

- [ ] 功能描述 1
- [ ] 功能描述 2

### 优化改进

- [ ] 优化描述 1
- [ ] 优化描述 2

### 问题修复

- [ ] 修复描述 1
- [ ] 修复描述 2

---

## 📊 变更对比

| 项目 | v{旧版本} | v{新版本} | 提升 |
|------|-----------|-----------|------|
| 性能 | - | - | - |
| 功能 | - | - | - |

---

## 🔧 安装方式

### 方式 1：GitHub 安装

```bash
git clone {repo_url}
cd {skill_name}
openclaw plugins install -l .
```

### 方式 2：ClawHub 安装

```bash
clawhub install {skill_name}
```

---

## 📋 完整文档

- [技能说明](SKILL.md)
- [使用文档](README.md)
- [许可证](LICENSE)

---

## 🎯 后续计划

### v{下一版本}（{计划日期}）

- [ ] 计划功能 1
- [ ] 计划功能 2

---

## 📞 反馈与支持

**GitHub Issues:** {issues_url}  
**Discord:** https://discord.gg/clawd

---

**技能作者：** {作者}  
**版本：** v{版本号}  
**发布日期：** {日期}
```

---

## 🤖 自动化脚本

### daily-iterate.sh

```bash
#!/bin/bash
# 技能每日迭代脚本

SKILL_NAME=$1
DATE=$(date +%Y-%m-%d)
VERSION=$(get_current_version $SKILL_NAME)
NEW_VERSION=$(increment_patch $VERSION)

echo "🔄 开始迭代：$SKILL_NAME"
echo "📌 版本：$VERSION → $NEW_VERSION"

# 1. 更新版本号
update_version $SKILL_NAME $NEW_VERSION

# 2. 生成 RELEASE 文档
generate_release_doc $SKILL_NAME $NEW_VERSION

# 3. 更新 CHANGELOG
update_changelog $SKILL_NAME $NEW_VERSION

# 4. Git 提交
git add skills/$SKILL_NAME
git commit -m "Release $SKILL_NAME v$NEW_VERSION ($DATE)"

echo "✅ 迭代完成：$SKILL_NAME v$NEW_VERSION"
```

### sync-github.sh

```bash
#!/bin/bash
# GitHub 同步脚本

echo "🚀 同步到 GitHub..."

# 1. 推送代码
git push origin main

# 2. 创建 GitHub Release
for skill in radar-daily-report ai-humanizer-cn; do
    VERSION=$(get_latest_version $skill)
    create_github_release $skill $VERSION
done

# 3. 验证发布
verify_github_releases

echo "✅ GitHub 同步完成"
```

---

## 📊 质量检查清单

### 发布前检查

- [ ] SKILL.md 版本号已更新
- [ ] RELEASE 文档已生成
- [ ] CHANGELOG 已更新
- [ ] 代码已测试
- [ ] 文档已校对
- [ ] Git 提交信息规范

### 发布后验证

- [ ] GitHub Release 可访问
- [ ] 文件完整上传
- [ ] 标签正确创建
- [ ] ClawHub 状态正常

---

## 📈 迭代记录

| 日期 | 技能 | 版本 | 状态 | 备注 |
|------|------|------|------|------|
| 2026-03-12 | radar-daily-report | v1.0.0 | ✅ | 初始版本 |
| 2026-03-12 | ai-humanizer-cn | v1.0.0 | ✅ | 初始版本 |
| 2026-03-13 | - | - | ⏳ | 待迭代 |

---

## 🎯 成功标准

1. **每日更新**: 每个工作日都有新版本
2. **文档完整**: RELEASE 文档 + CHANGELOG
3. **GitHub 同步**: 代码和 Release 都同步
4. **质量稳定**: 无重大 Bug，用户反馈良好

---

**系统版本：** v1.0  
**最后更新：** 2026-03-12  
**维护者：** 小马 🐴
