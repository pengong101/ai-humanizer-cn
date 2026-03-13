---
name: auto-skill-installer
description: Automatically discover, download, and install skills from ClawHub based on user requirements. Use when the user mentions needing new capabilities, skills, or tools that aren't currently available, or when a task requires specialized functionality.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["clawhub"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "clawhub",
              "bins": ["clawhub"],
              "label": "Install ClawHub CLI (npm)",
            },
          ],
      },
  }
---

# Auto Skill Installer

自动发现、下载和安装技能，根据用户需求扩展能力。

## 工作流程

### 1. 分析需求

当用户提到需要某项功能时，分析需要的技能类型：

- **搜索相关** → search, web-search, brave-search
- **代码相关** → coding-agent, github, git
- **文档相关** → notion, obsidian, apple-notes
- **媒体相关** → openai-image-gen, video-frames, sag
- **通讯相关** → discord, slack, telegram
- **数据相关** → bigquery, postgres, mongo

### 2. 搜索 ClawHub

```bash
clawhub search "<关键词>"
```

示例：
```bash
clawhub search "pdf editor"
clawhub search "image processing"
clawhub search "database backup"
```

### 3. 检查已安装技能

```bash
clawhub list
```

避免重复安装。

### 4. 安装技能

```bash
clawhub install <skill-slug>
```

示例：
```bash
clawhub install pdf-editor
clawhub install image-processor
```

### 5. 验证安装

检查技能是否出现在 `/app/skills/` 目录中。

### 6. 告知用户

通知用户技能已安装，并说明如何使用。

---

## 自动触发场景

当用户说：

- "我需要..."
- "能不能..."
- "有...的功能吗"
- "帮我找..."
- "缺少..."
- "需要安装..."

---

## 示例对话

**用户：** 我需要编辑 PDF 文件

**助手：** 
1. 检查是否有 PDF 编辑技能
2. `clawhub search "pdf editor"`
3. 找到 `pdf-editor` 技能
4. `clawhub install pdf-editor`
5. ✅ PDF 编辑技能已安装！现在可以帮你旋转、裁剪、合并 PDF 文件。

---

## 技能推荐策略

### 优先级

1. **官方技能** - OpenClaw 官方维护
2. **高评分技能** - 用户评分 > 4.5
3. **最近更新** - 3 个月内更新
4. **高下载量** - 社区验证

### 避免

- ⚠️ 超过 6 个月未更新的技能
- ⚠️ 评分 < 3.0 的技能
- ⚠️ 与现有技能冲突
- ⚠️ 需要特殊依赖的技能（除非用户明确同意）

---

## 批量安装

当用户需要多个相关技能时：

```bash
# 安装所有搜索相关技能
clawhub install brave-search
clawhub install searxng-search
clawhub install duckduckgo-search

# 或更新所有技能
clawhub update --all
```

---

## 故障处理

### 安装失败

1. 检查网络连接
2. 检查 clawhub 登录状态：`clawhub whoami`
3. 重新登录：`clawhub login`
4. 重试安装

### 技能冲突

1. 列出已安装：`clawhub list`
2. 卸载冲突：`clawhub uninstall <skill>`
3. 重新安装

### 版本问题

指定版本安装：
```bash
clawhub install <skill> --version 1.2.3
```

---

## 技能发现

定期浏览最新技能：

```bash
clawhub explore
```

查看热门技能：

```bash
clawhub search "" --sort stars
```

---

## 注意事项

1. **权限检查** - 某些技能需要 API key 或特殊权限
2. **依赖检查** - 某些技能需要额外依赖（如 Python 包）
3. **存储空间** - 技能占用磁盘空间
4. **性能影响** - 过多技能可能影响启动速度

---

**目标：** 让用户无需手动查找和安装技能，自动扩展能力！
