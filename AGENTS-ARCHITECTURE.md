# 智能体架构与工作流 v2.0

**版本：** v2.0  
**确立：** 2026-03-28（v1.0）→ 2026-04-03（v2.0）  
**原则：** 智能体固定，工作流可每日迭代优化  
**升级：** 基于 Danau5tin/multi-agent-coding-system + Agent Reach

---

## 一、6 个独立智能体（v2.0 角色定义）

| 智能体 | v1.0 角色 | v2.0 角色 | 产出 |
|--------|----------|----------|------|
| **main** | CEO + 调度 | **Orchestrator（纯粹）** | 任务分解、分配、汇总、汇报 |
| **ContentAgent** | 写作+配图+发布 | **Creator（Coder型）** | 文章 + 配图 + 发布 |
| **ResearchAgent** | 搜索+情报 | **Explorer（双重角色）** | 调研报告 + 验证报告 |
| **CodeAgent** | 开发+发布 | **Coder（自适应信任）** | 代码 + SKILL + Release |
| **OpsAgent** | 监控+自愈 | **Executor + Explorer** | 执行报告 + 巡检报告 |
| **ReviewAgent** | QC审核 | **Verifier** | 审核报告 + 评分 |

---

## 二、3 大核心工作流

### 工作流 1：内容创作

```
触发：用户指令 或 06:00 cron（日报）
    ↓
【选题阶段】（非日报跳过）
ResearchAgent 多引擎搜集热点 → 输出候选清单
    ↓
main 汇报 → 用户审批选题
    ↓
【创作阶段】
ResearchAgent 搜集情报（主题+关键词+数据）
    ↓
ContentAgent 写文章 + 配图 + 格式适配
    ↓
【质量迭代】（最多15轮，每3轮协调介入1次）
    ↓
ReviewAgent QC（合规≥9，其他≥7）
    ↓
┌─ 通过 → ContentAgent 发布（公众号/小红书）
└─ 不通过 → ContentAgent 修改 → 重新QC
    ↓
（5次介入仍不达标 → main 上报用户裁决）
```

### 工作流 2：技能研发

```
触发：用户需求 或 复盘优化建议审批通过
    ↓
ResearchAgent 研究现有方案 + GitHub类似项目 + 官方文档
    ↓
main 评审差异化价值
    ↓
CodeAgent 开发（代码 + SKILL.md + 测试）
    ↓
ReviewAgent QC（创新性≥9，其他≥7）
    ↓
┌─ 通过 → CodeAgent 发布（GitHub Release + ClawHub）
└─ 不通过 → CodeAgent 修改 → 重新QC
    ↓
（5次介入仍不达标 → main 上报用户裁决）
```

### 工作流 3：运维处理

```
触发：cron / heartbeat / 用户反馈 / 自动检测
    ↓
OpsAgent 健康检查（进程 + Docker + 内存 + 磁盘）
    ↓
发现问题？
    ├─ 是 → OpsAgent 自动修复 → 记录日志
    └─ 否 → 正常记录
    ↓
【重大问题】
ResearchAgent 查官方文档 + GitHub issues + 最新补丁
    ↓
main 汇报 → 用户决策
```

---

## 三、智能体 × 工作流 矩阵

| 工作流 | main | Content | Research | Code | Ops | Review |
|--------|:----:|:-------:|:--------:|:----:|:---:|:------:|
| 内容创作 | 调度+审批 | ✅ | ✅ | - | - | ✅ |
| 技能研发 | 调度+审批 | - | ✅ | ✅ | - | ✅ |
| 运维处理 | 汇报+决策 | - | ✅ | - | ✅ | - |

---

## 四、每日迭代优化机制

### 流程

```
03:30 → 每日复盘 → 生成优化建议
    ↓
08:00 → 汇报用户 → 审批优化
    ↓
次日 → 执行优化 → 固化到本文档
```

### 复盘内容

1. 任务完成情况（成功/失败/迭代次数）
2. 问题分析（根因 + 影响）
3. 优化建议（问题 + 方案 + 收益 + 优先级）

### 优化范围

- 智能体职责调整
- 工作流步骤优化
- 质量标准调整
- 迭代机制改进
- 新技能/新能力引入

### 文档更新

优化获批后：
1. 更新本文档
2. 更新相关 SKILL.md
3. 执行验证

---

## 五、Cron 任务归属

| 时间 | 任务 | 工作流 | 智能体 |
|------|------|--------|--------|
| 03:30 | 每日复盘 | 复盘改进 | main |
| 04:00 | 备份清理 | 运维 | OpsAgent |
| 06:00 | 科普文章 | 内容创作 | ContentAgent |
| 09:00 | 毫米波雷达日报 | 内容创作 | ContentAgent |
| 09:00 Mon | 每周更新检查 | 运维 | OpsAgent |
| 23:00 | 当日总结 | 内容创作 | ContentAgent |

---

## 六、Skills 归属

| Skill | 归属智能体 |
|-------|-----------|
| article-writing-workflow | ContentAgent |
| science-article-writer | ContentAgent |
| ai-humanizer-cn | ContentAgent |
| multi-search-engine | ResearchAgent |
| radar-daily-report | ResearchAgent |
| iterative-research | ResearchAgent |
| skill-creation-workflow | CodeAgent |
| self-improving-agent | CodeAgent |
| github-skill | CodeAgent |
| healthcheck | OpsAgent |
| proactive-agent | OpsAgent |
| secretary-core | main |
| qc-evaluator | ReviewAgent |
| pokayoke | ReviewAgent |
| tech-ops | OpsAgent |

---

## 七、决策记录（v1.0）

- **ContentAgent 不拆分**：文章=文字+图片，密不可分
- **Publisher 合并到 CodeAgent**：发布是开发的最后一步
- **ResearchAgent 协助所有工作流**：不只是内容创作
- **发布平台分流**：文章→公众号/小红书，代码→GitHub/ClawHub
- **每日迭代优化**：复盘→建议→审批→执行→固化

---

**最后更新：** 2026-03-28  
**下次审查：** 每日凌晨复盘后
