---
name: skill-evolver
description: Automatically improve and evolve existing skills based on usage patterns, user feedback, and performance metrics. Use when a skill underperforms, needs optimization, or after completing significant tasks to capture learnings.
---

# Skill Evolver

技能自动进化系统 - 让技能持续优化和成长。

## 核心理念

技能不是一成不变的，应该：
- 📈 从使用中学习
- 🔄 持续优化
- 🎯 适应用户需求
- 🧠 积累最佳实践

---

## 进化机制

### 1. 性能监控

记录每次技能使用的：
- ✅ 成功率
- ⏱️ 执行时间
- 📊 Token 消耗
- 💬 用户满意度
- 🔄 重试次数

### 2. 问题识别

自动检测技能问题：

| 问题类型 | 指标 | 阈值 |
|---------|------|------|
| 性能下降 | 执行时间 | > 平均 2 倍 |
| 质量下降 | 用户重试 | > 3 次/周 |
| 效率低下 | Token 消耗 | > 平均 50% |
| 功能缺失 | 用户请求 | 新增功能 > 5 次 |

### 3. 优化策略

#### A. 精简优化（减少 Token）

**识别：** SKILL.md 过长，上下文占用过多

**优化：**
- 移动详细内容到 `references/` 目录
- 删除冗余说明
- 使用更简洁的示例
- 添加渐进式加载

```markdown
# Before (冗长)
PDF 处理技能可以帮你做很多事情，包括旋转、裁剪、合并、分割、添加水印等等...

# After (简洁)
PDF 处理：旋转/裁剪/合并/分割/水印
详细功能：见 [FEATURES.md](references/features.md)
```

#### B. 功能增强（添加能力）

**识别：** 用户频繁请求某功能但技能不支持

**优化：**
- 添加新脚本到 `scripts/`
- 添加新示例到 `examples/`
- 更新 SKILL.md 说明

```bash
# 示例：为 pdf-editor 添加水印功能
mkdir -p pdf-editor/scripts
cat > pdf-editor/scripts/add_watermark.py << 'EOF'
# 水印添加脚本
EOF
```

#### C. 错误修复（提高稳定性）

**识别：** 技能频繁失败或报错

**优化：**
- 分析错误日志
- 修复边界条件
- 添加错误处理
- 完善输入验证

#### D. 示例更新（提高质量）

**识别：** 示例过时或不准确

**优化：**
- 收集成功案例
- 更新示例代码
- 添加最佳实践
- 补充边缘场景

---

## 进化工作流

### 步骤 1：收集反馈

```bash
# 从会话历史提取反馈
grep -r "技能.*不好用\|希望.*功能\|建议" ~/.openclaw/agents/main/sessions/
```

### 步骤 2：分析模式

识别重复出现的问题或请求：

| 用户反馈 | 出现次数 | 优先级 |
|---------|---------|--------|
| "这个技能太慢了" | 5 | 🔴 高 |
| "希望能批量处理" | 8 | 🔴 高 |
| "示例代码有误" | 2 | 🟡 中 |

### 步骤 3：制定优化方案

```markdown
## 优化计划：pdf-editor v1.1 → v1.2

### 问题
- 批量处理效率低（用户反馈 8 次）
- 缺少水印功能（用户请求 5 次）

### 方案
1. 添加批量处理脚本 `scripts/batch_process.py`
2. 添加水印功能 `scripts/add_watermark.py`
3. 优化 SKILL.md 说明

### 预期效果
- 处理速度提升 3 倍
- 支持水印功能
- Token 消耗减少 20%
```

### 步骤 4：实施优化

```bash
# 创建优化分支
cd /app/skills/pdf-editor
git checkout -b feature/batch-processing

# 添加新脚本
cat > scripts/batch_process.py << 'EOF'
#!/usr/bin/env python3
# 批量处理脚本
EOF

# 更新 SKILL.md
edit SKILL.md

# 测试
python scripts/batch_process.py test.pdf

# 提交
git add .
git commit -m "feat: add batch processing and watermark support"
```

### 步骤 5：验证效果

- ✅ 运行测试用例
- ✅ 检查性能指标
- ✅ 用户验收测试

### 步骤 6：发布更新

```bash
# 更新版本号
# 编辑 SKILL.md frontmatter

# 发布到 ClawHub
clawhub publish ./pdf-editor --slug pdf-editor --version 1.2.0 --changelog "Add batch processing + watermark support, 3x faster"
```

---

## 自动进化触发器

### 定期进化（每周）

```bash
# 每周日自动检查
0 2 * * 0 /root/.openclaw/scripts/evolve-skills.sh
```

### 事件触发

| 事件 | 动作 |
|------|------|
| 技能失败 > 3 次 | 立即分析修复 |
| 用户明确反馈 | 24 小时内响应 |
| 新功能请求 > 5 次 | 纳入下周计划 |
| 性能下降 > 50% | 立即优化 |

---

## 进化记录

维护 `EVOLUTION.md` 记录每次优化：

```markdown
# pdf-editor 进化史

## v1.2.0 (2026-03-11)
- ✅ 添加批量处理功能
- ✅ 添加水印支持
- ✅ 性能提升 3 倍
- 📊 Token 减少 20%

## v1.1.0 (2026-03-04)
- ✅ 添加旋转功能
- ✅ 修复裁剪 bug

## v1.0.0 (2026-02-25)
- 🎉 初始版本
```

---

## 技能健康度评分

### 评分维度

| 维度 | 权重 | 评分标准 |
|------|------|---------|
| 成功率 | 30% | >95% = 5 分，>90% = 4 分... |
| 性能 | 25% | <2s = 5 分，<5s = 4 分... |
| 效率 | 20% | Token 消耗低于平均 = 5 分... |
| 满意度 | 15% | 用户好评率 |
| 活跃度 | 10% | 每周使用次数 |

### 健康度等级

- 🟢 **优秀** (4.5-5.0) - 保持现状
- 🟡 **良好** (3.5-4.4) - 小优化
- 🟠 **一般** (2.5-3.4) - 需要改进
- 🔴 **差** (<2.5) - 立即优化或重构

---

## 最佳实践库

从成功案例中提取模式：

```markdown
## 成功模式：渐进式加载

**问题：** SKILL.md 过长（>500 行）

**方案：**
1. 核心逻辑保留在 SKILL.md（<200 行）
2. 详细文档移到 `references/`
3. 示例代码移到 `examples/`
4. 脚本移到 `scripts/`

**效果：** Token 减少 60%，加载速度提升 3 倍
```

---

## 协作进化

### 社区贡献

1. 用户提交 issue
2. 维护者分析并修复
3. 发布新版本
4. 自动推送更新

### 版本管理

```bash
# 语义化版本
v1.2.3
│ │ │
│ │ └─ 补丁版本（bug 修复）
│ └─── 次版本（新功能）
└───── 主版本（重大变更）
```

---

## 自动化脚本

### evolve-skills.sh

```bash
#!/bin/bash
# 技能自动进化脚本

SKILLS_DIR="/app/skills"
LOG_FILE="/root/.openclaw/logs/skill-evolution.log"

echo "[$(date)] 开始技能进化检查..." >> $LOG_FILE

# 检查每个技能的健康度
for skill in $SKILLS_DIR/*/; do
    skill_name=$(basename $skill)
    
    # 分析使用日志
    # 计算成功率
    # 检查性能指标
    
    # 如果健康度 < 3.5，触发优化
    if [ $health_score -lt 35 ]; then
        echo "[$(date)] $skill_name 需要优化 (健康度：$health_score)" >> $LOG_FILE
        # 触发优化流程
    fi
done

echo "[$(date)] 检查完成" >> $LOG_FILE
```

---

**目标：** 让每个技能都成为持续成长的有机体！
