# 多智能体协作架构 v1.0（已确立）

**版本：** v1.0  
**确立时间：** 2026-03-28  
**原则：** 智能体固定，工作流可变  

---

## 一、6个固定智能体

| 智能体 | 核心能力 | 边界 |
|--------|---------|------|
| **CoordinatorAgent** | 任务解析 + 调度 | 不做具体执行，只分解和调度 |
| **ContentAgent** | 写作 + 图片 + 拟人化 + 平台适配 | 不做深度调研、不做代码 |
| **ResearchAgent** | 多引擎搜索 + 情报分析 | 不做写作、不做审核 |
| **CodeAgent** | Skill开发 + 脚本 + 测试发布 | 不做内容、不做运维 |
| **OpsAgent** | 主动监控 + 故障自愈 + 巡检 | 不做内容、不做开发 |
| **ReviewAgent** | QC审核 + 决策支持 + 审批 | 客观独立 |

---

## 二、主要工作流（4种）

### 工作流 1：内容创作（日报/科普/总结）

```
触发：06:00 cron（日报）、用户指令（文章）
    ↓
Coordinator 分解任务
    ↓
ResearchAgent 多引擎搜集情报（主题 + 关键词）
    ↓
ContentAgent 联网搜索 + 写文章
    ↓
ContentAgent 生成/选取配图
    ↓
ContentAgent AI拟人化 + mdnice格式适配
    ↓
ReviewAgent 四维QC（合规≥9 / 文本≥8 / 图片≥8 / 格式≥8，总分≥35）
    ↓
通过 → PublisherAgent 发布
不通过 → ContentAgent 修改（循环）
```

**参与：** Coordinator → ResearchAgent → ContentAgent → ReviewAgent → PublisherAgent

---

### 工作流 2：Skill 开发（自动化/技能）

```
触发：用户需求 / 复盘优化建议审批通过
    ↓
Coordinator 分解任务
    ↓
CodeAgent 需求分析（问题描述 + 差异化 + 核心功能）
    ↓
ReviewAgent 评审差异化价值（≥7/10？）
    ├─ 否 → 返回重新分析
    └─ 是 → 继续
    ↓
CodeAgent 开发（代码 + 测试 + 文档）
    ↓
CodeAgent 单元测试验证
    ↓
ReviewAgent 五维QC（合规≥8 / 代码≥8 / 文档≥8 / 创新≥8，总分≥35）
    ├─ 否 → 返回修改（循环）
    └─ 是 → 发布
    ↓
PublisherAgent GitHub Release + ClawHub
    ↓
MemoryAgent 固化到 MEMORY.md
```

**参与：** Coordinator → CodeAgent → ReviewAgent → PublisherAgent → MemoryAgent

---

### 工作流 3：运维处理（系统故障/健康检查）

```
触发：cron / heartbeat / 用户反馈 / 自动检测
    ↓
OpsAgent 健康检查（exec响应 / 进程 / Docker / 内存 / 磁盘）
    ↓
发现问题？
    ├─ 是 → OpsAgent 自动修复
    │        ├─ mihomo zombie → pkill -9 mihomo; docker restart clash
    │        ├─ cron down → service cron start
    │        ├─ 存储满 → cleanup-cron.sh
    │        └─ 服务异常 → 重启 + 验证
    │        ↓
    │   OpsAgent 记录故障日志 → MemoryAgent 更新 MEMORY.md
    │
    └─ 否 → 正常记录
```

**参与：** OpsAgent → MemoryAgent

**已知故障自愈：**
| 故障 | 方案 |
|------|------|
| exec 超时/卡死 | pkill -9 mihomo → restart clash → restart cron |
| cron 不运行 | service cron start |
| Docker 网络瘫 | docker restart clash |
| 存储满 | cleanup-cron.sh |

---

### 工作流 4：每日复盘改进

```
触发：03:30 cron（每日自动）
    ↓
MemoryAgent 提取全天 sessions_history
    ↓
MemoryAgent 分析（完成任务 / 决策 / 错误 / 教训）
    ↓
MemoryAgent 生成优化建议清单（问题 + 方案 + 收益 + 优先级）
    ↓
ReviewAgent 评审优先级（P0/P1/P2）
    ↓
08:00 CEO 汇报 → 用户审批（✅批准 / ❌拒绝）
    ↓
批准 → CodeAgent 执行优化
    ↓
MemoryAgent 固化改进到工作流文档
```

**参与：** MemoryAgent → ReviewAgent → CodeAgent

---

## 三、运维 Agent 主动巡检

OpsAgent 每 30 分钟自动巡检，不等待触发：

```
exec 响应时间（> 5s → 立即修复）
进程数 / zombie 进程
Docker 容器状态（xiaoma-new / searxng / clash）
内存可用（< 1GB → 告警）
磁盘使用率（> 80% → 清理）
cron 服务状态
```

---

## 四、智能体 × 工作流 矩阵

| 工作流 | Coordinator | Research | Content | Code | Ops | Review | Publisher | Memory |
|--------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 内容创作 | ✅ | ✅ | ✅ | - | - | ✅ | ✅ | - |
| Skill开发 | ✅ | - | - | ✅ | - | ✅ | ✅ | ✅ |
| 运维处理 | - | - | - | - | ✅ | - | - | ✅ |
| 复盘改进 | - | - | - | ✅ | - | ✅ | - | ✅ |
| 故障修复 | - | ✅ | - | ✅ | ✅ | - | - | - |

---

## 五、OpenClaw cron 任务归属

| cron 时间 | 任务 | 工作流 | 智能体 |
|-----------|------|--------|--------|
| 03:00 | 系统配置备份 | 运维处理 | OpsAgent |
| 03:30 | 每日复盘 | 复盘改进 | MemoryAgent |
| 04:00 | 备份自动清理 | 运维处理 | OpsAgent |
| 06:00 | 科普文章生产 | 内容创作 | ContentAgent |
| 09:00 | 毫米波雷达日报 | 内容创作 | ResearchAgent |
| 09:00 Mon | 每周更新检查 | 运维处理 | OpsAgent |
| 23:00 | 当日总结 | 内容创作 | ContentAgent |

---

## 六、Skills 归属

| Skill | 归属智能体 |
|-------|-----------|
| article-writing-workflow | ContentAgent |
| ai-humanizer-cn | ContentAgent |
| science-article-writer | ContentAgent |
| multi-search-engine | ResearchAgent |
| radar-daily-report | ResearchAgent |
| iterative-research | ResearchAgent |
| skill-creation-workflow | CodeAgent |
| self-improving-agent | CodeAgent |
| github-skill | PublisherAgent |
| healthcheck | OpsAgent |
| proactive-agent | OpsAgent |
| secretary-core | MemoryAgent |
| qc-evaluator | ReviewAgent |
| pokayoke | ReviewAgent |

---

## 七、决策记录

- **ContentAgent 不拆分**：文章=文字+图片，密不可分，统一输出
- **ReviewAgent 独立**：保证客观审核，不自己审自己
- **OpsAgent 主动巡检**：检测到问题先修再报，不等待
- **智能体间通信**：共享文件（产出物写文件路径，下一个读）
