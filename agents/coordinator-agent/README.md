# CoordinatorAgent（任务协调智能体）

**版本：** v1.0  
**日期：** 2026-03-28  
**核心：** 任务解析 + 子任务分解 + 多智能体调度 + 结果汇总

---

## 核心职责

- 接收用户原始指令，拆解为子任务
- 判断任务类型，选择对应工作流
- 调度多个智能体协同工作
- 汇总各智能体结果，输出最终产出

## 任务类型判断

| 任务特征 | 判定工作流 |
|---------|----------|
| 需要写文章/图片/拟人化 | 内容创作流 |
| 需要深度搜索/情报分析 | 调研流 |
| 需要开发新 Skill / 脚本 | Skill 开发流 |
| 系统报错/需要运维 | 运维处理流 |
| 每日定时复盘 | 复盘改进流 |

## 工作流调度

```
用户指令
    ↓
Coordinator 分析任务类型
    ↓
分配到对应工作流
    ├─ 内容创作流 → ResearchAgent → ContentAgent → ReviewAgent
    ├─ 调研流 → ResearchAgent → ReviewAgent
    ├─ Skill开发流 → CodeAgent → ReviewAgent → MemoryAgent
    ├─ 运维处理流 → OpsAgent → MemoryAgent
    └─ 复盘改进流 → MemoryAgent → ReviewAgent → CodeAgent
    ↓
汇总结果 → 输出
```

## 触发方式

- 用户所有指令（第一入口）
- 定时任务触发（cron）

## 相关文件

- `agents/coordinator-agent/agent.py` — 核心代码
- `agents/architecture.md` — 整体架构定义
