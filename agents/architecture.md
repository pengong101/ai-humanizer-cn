# 多智能体协作架构 v1.0

**版本：** v1.0  
**日期：** 2026-03-28  
**状态：** 设计中，需评审后固化

---

## 一、现状分析

### 当前智能体
- TextWriter（写作）
- ImageAgent（图片）
- Integrator（整合）
- QCAgent（审核）
- CEO（决策）
- 10+ 个 Skill 智能体

### 当前问题
1. 智能体定义不清——有些是固定智能体，有些是临时工作流
2. 文章、图片、整合各自分离，但实际都是"内容创作"
3. 没有统一的运维智能体
4. 多智能体协同靠人（CEO）喊话，没有标准化流程

---

## 二、核心设计原则

**固定：智能体类型 + 能力边界**  
**可变：工作流 + 协同模式**

```
智能体 = 固定能力单元（不会轻易改变）
工作流 = 任务类型决定的协作模式（随需求变化）
```

---

## 三、智能体类型定义（6个固定智能体）

### 1. ContentAgent（内容创作智能体）

**能力：** 写作 + 图片 + 整合 + 拟人化 + 平台适配

**做的事：**
- 联网搜集情报（SearXNG）
- 撰写科普文章
- 生成/选取配图
- AI 拟人化（去除机器痕迹）
- Markdown 格式适配（公众号/知乎/小红书）
- QC 质量审核

**技能：** article-writing-workflow, ai-humanizer-cn, science-article-writer, multi-search-engine

**调用时机：** 06:00 科普文章生产、临时文章任务

---

### 2. ResearchAgent（研究调研智能体）

**能力：** 深度搜索 + 信息综合 + 情报分析

**做的事：**
- 多引擎并行搜索
- 去重 + 去噪 + 质量筛选
- 信息综合整理
- 输出结构化报告

**技能：** multi-search-engine, searxng-search, iterative-research

**调用时机：** 雷达日报、技术调研、竞品分析

---

### 3. CodeAgent（代码工程智能体）

**能力：** Skill 开发 + 脚本编写 + 代码审核

**做的事：**
- 需求分析（Researcher 阶段）
- 代码实现（DevAgent 阶段）
- 单元测试
- Skill 打包发布

**技能：** skill-creation-workflow, github-skill, self-improving-agent

**调用时机：** 新 Skill 开发、自动化脚本编写

---

### 4. OpsAgent（系统运维智能体）

**能力：** 主动监控 + 故障自愈 + 性能优化 + 安全审计

**做的事：**
- **主动巡检**：每 30 分钟检查 exec 响应时间、Docker 状态、进程数、内存、CPU
- **故障自愈**：检测到 exec 卡死 → 自动杀 zombie 进程 → 重启服务 → 验证恢复
- **根因分析**：记录故障模式（同类问题不重复修复）
- **预防性维护**：备份验证、存储健康检查、依赖更新
- **紧急响应**：收到"系统太卡"反馈时立即自动介入，无需等待指令

**触发方式：**
- 被动触发：cron 定时、heartbeat 巡检、用户告警
- **主动触发：检测到 exec 响应 > 5s 即自动介入**

**技能：** healthcheck, proactive-agent, node-connect, auto-skill-installer, self-improving-agent

**关键原则：OpsAgent 发现问题 → 先修再报，不等待。**

**调用时机：** 03:00 系统备份、04:00 清理、每日健康检查、故障时

---

### 5. MemoryAgent（记忆管理智能体）

**能力：** 记忆存储 + 检索 + 复盘 + 归档

**做的事：**
- 每日 03:30 复盘（提取 sessions，优化建议）
- 08:00 汇报优化建议
- 23:00 当日总结 + 记忆归档
- MEMORY.md 维护

**技能：** secretary-core, proactive-agent

**调用时机：** 03:30 复盘、23:00 归档、每次重要决策后

---

### 6. ReviewAgent（审核决策智能体）

**能力：** QC 审核 + 决策支持 + 审批

**做的事：**
- 内容四维 QC（合规/文本/图片/格式）
- Skill 五维 QC（合规/代码/文档/创新/价值）
- 优化建议评审（优先级判定）
- CEO 决策支持

**技能：** qc-evaluator, pokayoke

**调用时机：** 所有产出物的最终审核、重大决策前

---

## 四、工作流模式（4种固定模式）

### 模式 A：内容创作流（Content Pipeline）

```
触发（06:00 cron / 用户指令）
    ↓
选题 → ResearchAgent 搜集情报
    ↓
ContentAgent 写文章
    ↓
ContentAgent 生成/选图片
    ↓
ContentAgent 拟人化 + 格式适配
    ↓
ReviewAgent QC 审核
    ↓
通过 → 发布
不通过 → 返回 ContentAgent 修改（循环）
```

**参与智能体：** ResearchAgent → ContentAgent → ReviewAgent

---

### 模式 B：运维处理流（Ops Pipeline）

```
触发（cron / heartbeat / 用户 / 自动检测）
    ↓
OpsAgent 健康检查（exec 响应 / 进程数 / 内存 / Docker）
    ↓
发现问题？
    ├─ 是 → OpsAgent 自动修复（不等待）
    │        ├─ exec 卡死 → 杀 zombie 进程 → 重启服务
    │        ├─ 存储满 → 清理临时文件
    │        └─ 服务 down → 重启 + 验证
    │        ↓
    │   MemoryAgent 记录故障 + 更新 MEMORY.md
    └─ 否 → 正常记录
    ↓
MemoryAgent 更新状态
```

**已知故障模式（MEMORY.md 记录）：**
- mihomo zombie → `pkill -9 mihomo; service cron restart`
- Docker 网络卡死 → `docker restart clash`
- exec 超时 → 检查 zombie 进程 + 清理

**参与智能体：** OpsAgent → MemoryAgent

---

### 模式 C：Skill 开发流（Engineering Pipeline）

```
触发（用户需求 / 发现痛点）
    ↓
CodeAgent 需求分析（输出：需求文档）
    ↓
ReviewAgent 评审需求（差异化 ≥7/10？）
    ├─ 否 → 拒绝，重新分析
    └─ 是 → 继续
    ↓
CodeAgent 开发（输出：可运行 Skill）
    ↓
CodeAgent 单元测试
    ↓
ReviewAgent QC（五维审核，总分≥35？）
    ├─ 否 → 返回修改（循环）
    └─ 是 → 发布
    ↓
MemoryAgent 固化（记录到 MEMORY.md）
```

**参与智能体：** CodeAgent → ReviewAgent → MemoryAgent

---

### 模式 D：复盘改进流（Improvement Pipeline）

```
触发（03:30 每日 cron）
    ↓
MemoryAgent 提取全天 sessions
    ↓
MemoryAgent 分析（任务/决策/错误/教训）
    ↓
MemoryAgent 生成优化建议清单
    ↓
ReviewAgent 评审优先级
    ↓
08:00 用户审批（CEO 汇报）
    ↓
批准 → CodeAgent 执行优化
    ↓
MemoryAgent 固化改进
```

**参与智能体：** MemoryAgent → ReviewAgent → CodeAgent

---

## 五、智能体 vs 工作流矩阵

| 工作流 | ResearchAgent | ContentAgent | CodeAgent | OpsAgent | MemoryAgent | ReviewAgent |
|--------|:---:|:---:|:---:|:---:|:---:|:---:|
| 内容创作 | ✅ | ✅ | - | - | - | ✅ |
| 雷达日报 | ✅ | - | - | - | - | ✅ |
| 运维处理 | - | - | - | ✅ | ✅ | - |
| Skill 开发 | - | - | ✅ | - | ✅ | ✅ |
| 每日复盘 | - | - | ✅ | - | ✅ | ✅ |
| 故障修复 | ✅ | - | ✅ | ✅ | - | - |

---

## 六、当前技能归属

| 技能 | 归属智能体 |
|------|-----------|
| article-writing-workflow | ContentAgent |
| ai-humanizer-cn | ContentAgent |
| science-article-writer | ContentAgent |
| multi-search-engine | ResearchAgent |
| iterative-research | ResearchAgent |
| radar-daily-report | ResearchAgent |
| skill-creation-workflow | CodeAgent |
| self-improving-agent | CodeAgent |
| github-skill | CodeAgent |
| healthcheck | OpsAgent |
| proactive-agent | OpsAgent |
| node-connect | OpsAgent |
| secretary-core | MemoryAgent |
| qc-evaluator | ReviewAgent |
| pokayoke | ReviewAgent |

---

## 七、待解决的设计问题

1. **ContentAgent 是否需要拆分为"写作"和"图片"两个独立智能体？**
   - 当前方案：合并，因为文章=文字+图片，密不可分
   - 风险：能力过于广泛，难以专精

2. **ReviewAgent 独立还是并入其他智能体？**
   - 当前方案：独立，保证客观审核
   - 替代方案：每个智能体自带 QC 内核

3. **OpsAgent 在无故障时做什么？**
   - 预防性监控：log 检查、备份验证、存储检查
   - 空闲时学习：更新知识库、分析趋势

4. **智能体之间如何通信？**
   - 方案 A：共享文件（产出物写文件，下一个读文件）
   - 方案 B：消息队列（RabbitMQ / Redis）
   - 方案 C：session 传递（sessions_send）

---

## 八、下一步

- [ ] CEO 评审架构设计
- [ ] OpsAgent 主动巡检实现（检测 exec 响应 > 5s 自动介入）
- [ ] OpsAgent 已知故障模式固化（MEMORY.md 记录）
- [ ] 确定 ContentAgent 是否拆分
- [ ] 实现 ContentAgent 统一技能包
