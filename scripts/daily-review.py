#!/usr/bin/env python3
"""
每日 03:30 自我检讨 + 工作流优化建议生成

运行后：
1. 提取昨日 sessions 对话记录（从 jsonl 解析）
2. 分析三大工作流执行情况（精细化指标）
3. 识别问题模式和优化点
4. 生成优化建议清单
5. 输出到 logs/review-YYYY-MM-DD.md

08:00 汇报给 CEO 用户确认后，落地优化并固化
"""

import os
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from collections import defaultdict

LOG_DIR = "/root/.openclaw/workspace/logs"
SESSIONS_DIR = "/root/.openclaw/agents/main/sessions"
os.makedirs(LOG_DIR, exist_ok=True)


def get_yesterday_date():
    """获取昨天的日期"""
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


# =============================================================================
# 核心数据提取：从 jsonl sessions 解析出结构化数据
# =============================================================================

def get_sessions_history(date_str):
    """
    获取指定日期的 sessions 历史，提取所有关键字段
    返回: list of dict，每条记录包含:
      session_id, timestamp, role, content_type, text, usage, error_type, tool_call
    """
    sessions_data = []
    sessions_dir = SESSIONS_DIR

    if not os.path.exists(sessions_dir):
        print(f"sessions 目录不存在: {sessions_dir}")
        return sessions_data

    # 日期范围
    target_date = datetime.strptime(date_str, "%Y-%m-%d")
    day_start = target_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
    day_end = target_date.replace(hour=23, minute=59, second=59, microsecond=999999, tzinfo=timezone.utc)

    jsonl_files = sorted(Path(sessions_dir).glob("*.jsonl"), key=os.path.getmtime, reverse=True)

    for jsonl_file in jsonl_files:
        if '.reset.' in jsonl_file.name or '.deleted.' in jsonl_file.name:
            continue
        try:
            with open(jsonl_file, 'r', encoding='utf-8') as f:
                current_session_id = None
                pending_tool_calls = []  # toolResult 里没有 tool_name，从前序 toolCall 累积

                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        record = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    ts_str = record.get("timestamp", "")
                    if not ts_str or '2026-03-28' not in ts_str:
                        continue

                    try:
                        ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                    except Exception:
                        continue

                    if ts < day_start or ts > day_end:
                        continue

                    rec_type = record.get("type")

                    # session 开头事件：记录 session_id
                    if rec_type == "session":
                        current_session_id = record.get("id")

                    # custom 事件：提取错误
                    elif rec_type == "custom":
                        custom_type = record.get("customType", "")
                        error_data = record.get("data", {})
                        if custom_type == "openclaw:prompt-error":
                            sessions_data.append({
                                "session_id": current_session_id or "",
                                "timestamp": ts,
                                "role": "error",
                                "content_type": "prompt-error",
                                "text": error_data.get("error", ""),
                                "usage": {},
                                "error_type": error_data.get("error", "unknown"),
                                "tool_call": "",
                            })

                    # message 事件
                    elif rec_type == "message":
                        msg = record.get("message", {})
                        role = msg.get("role", "")
                        content = msg.get("content", [])
                        usage = msg.get("usage", {})

                        if isinstance(content, list):
                            for c in content:
                                ct = c.get("type", "")
                                if ct == "text":
                                    text = c.get("text", "")
                                    sessions_data.append({
                                        "session_id": current_session_id or "",
                                        "timestamp": ts,
                                        "role": role,
                                        "content_type": "text",
                                        "text": text,
                                        "usage": usage,
                                        "error_type": None,
                                        "tool_call": "",
                                    })
                                elif ct == "toolCall":
                                    tool_name = c.get("name", "")
                                    args = json.dumps(c.get("args", {}), ensure_ascii=False)[:80]
                                    pending_tool_calls.append(tool_name)  # 加入队列，等 toolResult 来消费
                                    sessions_data.append({
                                        "session_id": current_session_id or "",
                                        "timestamp": ts,
                                        "role": "assistant",
                                        "content_type": "toolCall",
                                        "text": f"{tool_name}({args})",
                                        "usage": {},
                                        "error_type": None,
                                        "tool_call": tool_name,
                                    })
                                elif ct == "toolResult":
                                    text = c.get("content", "")
                                    # 从 pending_tool_calls 队列取 tool name
                                    tool_name = ""
                                    if pending_tool_calls:
                                        tool_name = pending_tool_calls.pop(0)
                                    sessions_data.append({
                                        "session_id": current_session_id or "",
                                        "timestamp": ts,
                                        "role": "toolResult",
                                        "content_type": "toolResult",
                                        "text": str(text)[:200],
                                        "usage": {},
                                        "error_type": None,
                                        "tool_call": tool_name,
                                    })
                                elif ct == "thinking":
                                    pass  # 跳过 thinking 减少噪音

                        elif role == "assistant" and not content:
                            sessions_data.append({
                                "session_id": current_session_id or "",
                                "timestamp": ts,
                                "role": "assistant",
                                "content_type": "empty",
                                "text": "",
                                "usage": usage,
                                "error_type": None,
                                "tool_call": "",
                            })

        except Exception as e:
            print(f"读取 session 文件失败 {jsonl_file}: {e}")
            continue

    return sessions_data


# =============================================================================
# 核心分析：精细化工作流指标计算
# =============================================================================

def calculate_workflow_metrics(sessions_data, date_str):
    """
    精细化统计：按 task 级别提取指标

    返回: (stats_dict, tasks_list)
      stats: {wf_name: {total, success, failed, errors, total_iterations, total_tool_calls,
                         total_duration, total_cost, tasks: [...]}}
      tasks: [{session_id, wf, name, iterations, tool_calls, errors, error_count,
               duration_min, tokens_in, tokens_out, cost}]
    """
    # 工作流关键词（细分任务类型）
    wf_keywords = {
        "文档写作": {
            "trigger": ["文章", "写作", "科普", "公众号", "小红书", "内容创作", "写一篇", "创作", "日报", "报告", "总结"],
            "tool": ["write", "edit", "read"],
        },
        "技术工作": {
            "trigger": ["部署", "脚本", "docker", "配置", "修复", "搭建", "开发", "安装", "设置", "重启", "备份", "cron"],
            "tool": ["exec", "docker", "systemctl"],
        },
        "技能研发": {
            "trigger": ["skill", "技能", "研发", "开发", "代码", "实现", "功能", "skill.md", "SKILL.md"],
            "tool": ["write", "edit"],
        },
    }

    # 将 sessions_data 按 session_id 分组
    by_session = defaultdict(list)
    for item in sessions_data:
        by_session[item["session_id"]].append(item)

    tasks = []

    for session_id, items in by_session.items():
        if not items:
            continue

        # 按时间排序
        items.sort(key=lambda x: x["timestamp"])

        # 提取基本信息
        session_start = items[0]["timestamp"]
        session_end = items[-1]["timestamp"]
        duration = (session_end - session_start).total_seconds() if session_end and session_start else 0

        # 统计
        tool_calls = {"exec": 0, "read": 0, "write": 0, "browser": 0, "other": 0}
        errors = []
        iterations = 0
        tokens_in = 0
        tokens_out = 0
        cost = 0.0
        wf_detected = None
        task_texts = []

        for item in items:
            role = item["role"]
            content_type = item["content_type"]
            text = item["text"]

            # 识别工作流类型（从 user 消息触发词）
            if role == "user" and text:
                for wf, kw in wf_keywords.items():
                    if any(k in text for k in kw["trigger"]):
                        wf_detected = wf
                        # 提取任务描述（取 cron 触发词之后的内容）
                        if "请执行：" in text:
                            cmd_start = text.find("请执行：") + 4
                            task_texts.append(text[cmd_start:cmd_start+80].strip())
                        else:
                            task_texts.append(text[:80])
                        break

            # 统计 tool calls
            if role == "assistant" and content_type == "toolCall":
                iterations += 1

            # 读取 tool name（只从 toolCall 条目读取，toolResult 是结果不重复计数）
            if content_type == "toolCall" and item.get("tool_call"):
                tc = item.get("tool_call", "")
                if "exec" in tc.lower(): tool_calls["exec"] += 1
                elif "read" in tc.lower(): tool_calls["read"] += 1
                elif "write" in tc.lower() or "edit" in tc.lower(): tool_calls["write"] += 1
                elif "browser" in tc.lower(): tool_calls["browser"] += 1
                elif tc: tool_calls["other"] += 1

            # 统计错误
            if item.get("error_type"):
                errors.append(item["error_type"])

            # 统计 token
            usage = item.get("usage", {})
            if usage:
                tokens_in += usage.get("input", 0)
                tokens_out += usage.get("output", 0)
                cost += usage.get("cost", {}).get("total", 0)

        if wf_detected or task_texts:
            tasks.append({
                "session_id": session_id[:8],
                "wf": wf_detected or "未知",
                "task": "; ".join(task_texts[:2]),
                "iterations": iterations,
                "tool_calls": dict(tool_calls),
                "errors": errors,
                "error_count": len(errors),
                "duration_min": duration / 60 if duration > 0 else 0,
                "tokens_in": tokens_in,
                "tokens_out": tokens_out,
                "cost": cost,
            })

    # 聚合统计
    stats = {
        "文档写作": {"total": 0, "success": 0, "failed": 0, "errors": 0, "total_iterations": 0,
                     "total_tool_calls": 0, "total_duration": 0, "total_cost": 0.0, "tasks": []},
        "技术工作": {"total": 0, "success": 0, "failed": 0, "errors": 0, "total_iterations": 0,
                     "total_tool_calls": 0, "total_duration": 0, "total_cost": 0.0, "tasks": []},
        "技能研发": {"total": 0, "success": 0, "failed": 0, "errors": 0, "total_iterations": 0,
                     "total_tool_calls": 0, "total_duration": 0, "total_cost": 0.0, "tasks": []},
    }

    for task in tasks:
        wf = task["wf"]
        if wf not in stats:
            continue

        stats[wf]["total"] += 1
        stats[wf]["total_iterations"] += task["iterations"]
        stats[wf]["total_tool_calls"] += sum(task["tool_calls"].values())
        stats[wf]["total_duration"] += task["duration_min"]
        stats[wf]["total_cost"] += task["cost"]
        stats[wf]["errors"] += task["error_count"]

        if task["error_count"] > 0:
            stats[wf]["failed"] += 1
        else:
            stats[wf]["success"] += 1

        if len(stats[wf]["tasks"]) < 3:
            stats[wf]["tasks"].append(task)

    return stats, tasks


# =============================================================================
# 优化建议生成
# =============================================================================

def generate_optimization_suggestions(stats, tasks):
    """基于精细化统计数据和问题生成优化建议"""
    suggestions = []

    for wf_name, wf_stats in stats.items():
        if wf_stats["total"] == 0:
            continue

        success_rate = wf_stats["success"] / wf_stats["total"] * 100
        avg_iter = wf_stats["total_iterations"] / wf_stats["total"] if wf_stats["total"] > 0 else 0
        avg_cost = wf_stats["total_cost"] / wf_stats["total"] if wf_stats["total"] > 0 else 0
        avg_duration = wf_stats["total_duration"] / wf_stats["total"] if wf_stats["total"] > 0 else 0
        avg_tools = wf_stats["total_tool_calls"] / wf_stats["total"] if wf_stats["total"] > 0 else 0

        if success_rate < 80:
            suggestions.append({
                "workflow": wf_name,
                "problem": f"成功率 {success_rate:.0f}%（{wf_stats['failed']} 次失败 / {wf_stats['total']} 次执行）",
                "suggestion": f"分析 {wf_name} 失败根因，检查错误日志",
                "expected_benefit": "成功率提升至 90%+",
                "priority": "高"
            })

        if avg_iter > 8:
            max_iter = max((t["iterations"] for t in wf_stats["tasks"]), default=0)
            suggestions.append({
                "workflow": wf_name,
                "problem": f"平均迭代 {avg_iter:.0f} 次（最高 {max_iter} 次）",
                "suggestion": "减少每轮修复内容，或增加每次迭代的工作量",
                "expected_benefit": "减少迭代次数，提升效率",
                "priority": "中"
            })

        if avg_cost > 1.0:
            suggestions.append({
                "workflow": wf_name,
                "problem": f"单次平均成本 ${avg_cost:.4f}",
                "suggestion": "考虑使用更小模型处理中间步骤",
                "expected_benefit": "降低单次成本",
                "priority": "中"
            })

        if avg_duration > 30:
            suggestions.append({
                "workflow": wf_name,
                "problem": f"单次平均耗时 {avg_duration:.1f} 分钟",
                "suggestion": "检查耗时节点，优化脚本或增加并发",
                "expected_benefit": "缩短执行时间",
                "priority": "低"
            })

        if wf_stats["errors"] > 0:
            error_tasks = [t for t in wf_stats["tasks"] if t["error_count"] > 0]
            error_sample = error_tasks[0]["errors"][0] if error_tasks else ""
            suggestions.append({
                "workflow": wf_name,
                "problem": f"共 {wf_stats['errors']} 次错误（示例：{error_sample[:50]}）",
                "suggestion": "检查错误模式，更新工作流错误处理",
                "expected_benefit": "减少错误率",
                "priority": "高"
            })

    # 按优先级排序
    priority_order = {"高": 0, "中": 1, "低": 2}
    suggestions.sort(key=lambda x: priority_order.get(x["priority"], 3))

    return suggestions


# =============================================================================
# 报告生成
# =============================================================================

def generate_review_report(date_str):
    """生成完整的复盘报告"""

    # 获取 sessions
    sessions_data = get_sessions_history(date_str)

    # 计算指标（精细化）
    stats, tasks = calculate_workflow_metrics(sessions_data, date_str)

    # 生成建议
    suggestions = generate_optimization_suggestions(stats, tasks)

    # 格式化数字辅助
    def avg(dur, cnt):
        return dur / cnt if cnt > 0 else 0

    # 构建报告
    report = f"""# 每日复盘 - {date_str}

## 📊 任务完成情况

| 工作流 | 总数 | 成功 | 失败 | 成功率 | 平均迭代 | 平均工具调用 | 平均耗时 | 成本 |
|--------|------|------|------|--------|---------|------------|---------|------|
| 文档写作 | {stats['文档写作']['total']} | {stats['文档写作']['success']} | {stats['文档写作']['failed']} | {stats['文档写作']['success']/max(1,stats['文档写作']['total'])*100:.0f}% | {avg(stats['文档写作']['total_iterations'],stats['文档写作']['total']):.1f} | {avg(stats['文档写作']['total_tool_calls'],stats['文档写作']['total']):.0f} | {avg(stats['文档写作']['total_duration'],stats['文档写作']['total']):.1f}m | ${stats['文档写作']['total_cost']:.4f} |
| 技术工作 | {stats['技术工作']['total']} | {stats['技术工作']['success']} | {stats['技术工作']['failed']} | {stats['技术工作']['success']/max(1,stats['技术工作']['total'])*100:.0f}% | {avg(stats['技术工作']['total_iterations'],stats['技术工作']['total']):.1f} | {avg(stats['技术工作']['total_tool_calls'],stats['技术工作']['total']):.0f} | {avg(stats['技术工作']['total_duration'],stats['技术工作']['total']):.1f}m | ${stats['技术工作']['total_cost']:.4f} |
| 技能研发 | {stats['技能研发']['total']} | {stats['技能研发']['success']} | {stats['技能研发']['failed']} | {stats['技能研发']['success']/max(1,stats['技能研发']['total'])*100:.0f}% | {avg(stats['技能研发']['total_iterations'],stats['技能研发']['total']):.1f} | {avg(stats['技能研发']['total_tool_calls'],stats['技能研发']['total']):.0f} | {avg(stats['技能研发']['total_duration'],stats['技能研发']['total']):.1f}m | ${stats['技能研发']['total_cost']:.4f} |

"""

    # Task 明细（按工作流分组）
    report += "## 📋 Task 执行明细\n\n"
    wf_labels = {"文档写作": "📝", "技术工作": "🔧", "技能研发": "🛠️"}
    has_tasks = False
    for wf_name in ["文档写作", "技术工作", "技能研发"]:
        wf_tasks = stats[wf_name]["tasks"]
        if not wf_tasks:
            continue
        has_tasks = True
        emoji = wf_labels.get(wf_name, "📋")
        report += f"### {emoji} {wf_name}\n\n"
        report += "| # | Session | 任务描述 | 迭代 | 工具调用 | 错误 | 耗时 | 成本 |\n"
        report += "|---|---------|---------|------|---------|------|------|------|\n"
        for i, t in enumerate(wf_tasks, 1):
            tc = sum(t["tool_calls"].values())
            report += f"| {i} | `{t['session_id']}` | {t['task'][:40]} | {t['iterations']} | {tc} | {t['error_count']} | {t['duration_min']:.1f}m | ${t['cost']:.4f} |\n"
        report += "\n"

    if not has_tasks:
        report += "*昨日无记录的工作流任务*\n\n"

    # 问题分析
    report += "## 🔍 问题分析\n\n"
    problems = []
    for wf_name in ["文档写作", "技术工作", "技能研发"]:
        wf_stats = stats[wf_name]
        if wf_stats["errors"] > 0:
            error_tasks = [t for t in wf_stats["tasks"] if t["error_count"] > 0]
            if error_tasks:
                err = error_tasks[0]["errors"][0]
                problems.append({
                    "workflow": wf_name,
                    "description": f"{wf_name}发生 {wf_stats['errors']} 次错误",
                    "root_cause": err[:80],
                    "suggestion": f"检查 {wf_name} 错误日志，定位根因"
                })

    if not problems:
        report += "*昨日无明显问题，继续保持*\n\n"
    else:
        for i, p in enumerate(problems, 1):
            report += f"### 问题 {i}：{p['description']}\n"
            report += f"- **根因：** {p['root_cause']}\n"
            report += f"- **建议：** {p['suggestion']}\n\n"

    # 优化建议
    report += "## 💡 优化建议\n\n"
    if not suggestions:
        report += "*暂无优化建议*\n\n"
    else:
        for i, s in enumerate(suggestions, 1):
            report += f"### 建议 {i}：{s['workflow']}\n"
            report += f"- **问题：** {s['problem']}\n"
            report += f"- **建议：** {s['suggestion']}\n"
            report += f"- **预期收益：** {s['expected_benefit']}\n"
            report += f"- **优先级：** {s['priority']}\n\n"

    # 今日待确认
    report += "## 🏁 今日待确认（08:00 汇报）\n\n"
    if not suggestions:
        report += "*暂无待确认的优化建议*\n\n"
    else:
        for i, s in enumerate(suggestions, 1):
            report += f"- [ ] 建议{i}：{s['suggestion']}（{s['priority']}优先级）\n"
    report += "\n"

    report += f"""---

**报告生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**数据来源：** {len(sessions_data)} 条 session 记录
**复盘周期：** {date_str}
"""
    return report


def main():
    date_str = get_yesterday_date()
    report = generate_review_report(date_str)

    if report is None:
        report = f"# 每日复盘 - {date_str}\n\n*报告生成失败，请检查日志*\n"
        print("⚠️ 报告生成返回 None，使用错误报告")

    # 输出到文件
    report_file = f"{LOG_DIR}/review-{date_str}.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"✅ 复盘报告已生成: {report_file}")
    print()
    print(report)

    return report_file


if __name__ == "__main__":
    main()
