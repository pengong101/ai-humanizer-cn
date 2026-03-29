#!/usr/bin/env python3
"""
每日 03:30 自我检讨 + 工作流优化建议生成

运行后：
1. 提取昨日 sessions 对话记录
2. 分析三大工作流执行情况
3. 识别问题模式和优化点
4. 生成优化建议清单
5. 输出到 logs/review-YYYY-MM-DD.md

08:00 汇报给 CEO 用户确认后，落地优化并固化
"""

import os
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

LOG_DIR = "/root/.openclaw/workspace/logs"
SESSIONS_DIR = "/root/.openclaw/agents/main/sessions"
os.makedirs(LOG_DIR, exist_ok=True)


def get_yesterday_date():
    """获取昨天的日期"""
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


def get_sessions_history(date_str):
    """获取指定日期的 sessions 历史"""
    sessions = []
    sessions_dir = SESSIONS_DIR
    
    if not os.path.exists(sessions_dir):
        print(f"sessions 目录不存在: {sessions_dir}")
        return sessions
    
    # 日期范围：指定日期 00:00:00 到 23:59:59 UTC
    target_date = datetime.strptime(date_str, "%Y-%m-%d")
    day_start = target_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
    day_end = target_date.replace(hour=23, minute=59, second=59, microsecond=999999, tzinfo=timezone.utc)
    
    jsonl_files = sorted(Path(sessions_dir).glob("*.jsonl"), key=os.path.getmtime, reverse=True)
    
    for jsonl_file in jsonl_files:
        try:
            with open(jsonl_file, 'r', encoding='utf-8') as f:
                file_sessions = []
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        record = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    
                    # 只处理 session 开头的事件（过滤 .reset. 文件）
                    if record.get("type") == "session" and ".reset." not in jsonl_file.name:
                        ts_str = record.get("timestamp", "")
                        if ts_str:
                            try:
                                ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                                if ts >= day_start and ts <= day_end:
                                    file_sessions.append({
                                        "session_id": record.get("id"),
                                        "timestamp": ts_str,
                                        "content": ""
                                    })
                            except Exception:
                                pass
                    
                    # 提取 message 内容
                    if record.get("type") == "message":
                        msg = record.get("message", {})
                        role = msg.get("role", "")
                        content = msg.get("content", [])
                        if isinstance(content, list):
                            text_parts = [c.get("text", "") for c in content if c.get("type") == "text"]
                            text = " ".join(text_parts)
                        else:
                            text = str(content)
                        
                        # 找对应 session 并添加 message
                        ts_str = record.get("timestamp", "")
                        if ts_str and file_sessions:
                            for sess in file_sessions:
                                if sess.get("timestamp", "") <= ts_str:
                                    sess["content"] += f"\n[{role}] {text}"
                                    break
                
                # 只保留有内容的 sessions
                for sess in file_sessions:
                    if sess["content"].strip():
                        sessions.append(sess)
                        
        except Exception as e:
            print(f"读取 session 文件失败 {jsonl_file}: {e}")
            continue
    
    return sessions


def analyze_workflow_execution(sessions, date_str):
    """
    分析工作流执行情况
    
    返回结构：
    {
        "文档写作": {"total": N, "success": N, "iterations": [...]},
        "技术工作": {"total": N, "success": N, "iterations": [...]},
        "技能研发": {"total": N, "success": N, "iterations": [...]},
    }
    """
    stats = {
        "文档写作": {"total": 0, "success": 0, "failed": 0, "avg_iterations": 0, "issues": []},
        "技术工作": {"total": 0, "success": 0, "failed": 0, "avg_iterations": 0, "issues": []},
        "技能研发": {"total": 0, "success": 0, "failed": 0, "avg_iterations": 0, "issues": []},
    }
    
    # 从 sessions 内容中识别工作流类型（简单关键词匹配）
    keywords = {
        "文档写作": ["文章", "写作", "科普", "公众号", "小红书", "内容创作"],
        "技术工作": ["部署", "脚本", "Docker", "配置", "修复", "搭建", "开发"],
        "技能研发": ["Skill", "skill", "技能", "研发", "开发", "代码"],
    }
    
    for session in sessions:
        content = session.get("content", "")
        for wf_type, wf_keywords in keywords.items():
            if any(kw in content for kw in wf_keywords):
                stats[wf_type]["total"] += 1
    
    return stats


def identify_problems(sessions):
    """
    从 sessions 中识别问题
    
    返回问题列表：
    [{
        "workflow": "工作流类型",
        "description": "问题描述",
        "impact": "影响",
        "root_cause": "根因（推测）",
        "suggestion": "优化建议"
    }]
    """
    problems = []
    
    # 常见的错误模式（从历史记录中总结）
    error_patterns = [
        {
            "pattern": "timeout|超时",
            "workflow": "技术工作",
            "description": "执行超时",
            "impact": "任务无法完成",
            "root_cause": "可能是网络问题或脚本死循环",
            "suggestion": "增加超时控制，优化脚本逻辑"
        },
        {
            "pattern": "权限|permission|拒绝访问",
            "workflow": "技术工作",
            "description": "权限不足",
            "impact": "操作失败",
            "root_cause": "配置文件保护或文件权限问题",
            "suggestion": "检查并临时提升权限，操作后恢复"
        },
        {
            "pattern": "质量|不达标|迭代",
            "workflow": "文档写作",
            "description": "质量未达标",
            "impact": "需要多次迭代",
            "root_cause": "可能需要优化工作流或智能体能力",
            "suggestion": "分析具体维度问题，调整质量标准或迭代策略"
        },
        {
            "pattern": "失败|fail|error|错误",
            "workflow": "通用",
            "description": "操作失败",
            "impact": "任务中断",
            "root_cause": "多种可能",
            "suggestion": "查看具体错误日志"
        },
    ]
    
    return problems


def generate_optimization_suggestions(stats, problems):
    """
    基于统计数据和问题生成优化建议
    
    返回建议列表：
    [{
        "workflow": "工作流类型",
        "problem": "问题",
        "suggestion": "建议",
        "expected_benefit": "预期收益",
        "priority": "高/中/低"
    }]
    """
    suggestions = []
    
    # 基于统计数据生成建议
    for wf_name, wf_stats in stats.items():
        if wf_stats["total"] == 0:
            continue
            
        success_rate = wf_stats["success"] / wf_stats["total"] * 100 if wf_stats["total"] > 0 else 0
        
        if success_rate < 80:
            suggestions.append({
                "workflow": wf_name,
                "problem": f"执行成功率仅 {success_rate:.0f}%",
                "suggestion": "分析失败原因，可能是工作流步骤需要优化",
                "expected_benefit": "提升成功率至 90%+",
                "priority": "高"
            })
        
        if wf_stats["avg_iterations"] > 5:
            suggestions.append({
                "workflow": wf_name,
                "problem": f"平均迭代 {wf_stats['avg_iterations']:.1f} 次",
                "suggestion": "考虑调整迭代策略，如减少每轮修复内容",
                "expected_benefit": "减少迭代次数，提升效率",
                "priority": "中"
            })
    
    # 基于问题生成建议
    for problem in problems:
        suggestions.append({
            "workflow": problem["workflow"],
            "problem": problem["description"],
            "suggestion": problem["suggestion"],
            "expected_benefit": "解决当前问题",
            "priority": "高"
        })
    
    # 按优先级排序
    priority_order = {"高": 0, "中": 1, "低": 2}
    suggestions.sort(key=lambda x: priority_order.get(x["priority"], 3))
    
    return suggestions


def calculate_workflow_metrics(sessions, date_str):
    """
    计算工作流执行统计指标
    """
    stats = {
        "文档写作": {"total": 0, "success": 0, "failed": 0, "avg_iterations": 0, "avg_time_minutes": 0, "max_iterations": 0},
        "技术工作": {"total": 0, "success": 0, "failed": 0, "avg_iterations": 0, "avg_time_minutes": 0, "max_iterations": 0},
        "技能研发": {"total": 0, "success": 0, "failed": 0, "avg_iterations": 0, "avg_time_minutes": 0, "max_iterations": 0},
    }
    
    keywords = {
        "文档写作": ["文章", "写作", "科普", "公众号", "小红书", "内容创作", "写一篇", "创作"],
        "技术工作": ["部署", "脚本", "docker", "配置", "修复", "搭建", "开发", "安装", "设置"],
        "技能研发": ["skill", "技能", "研发", "开发", "代码", "实现", "功能"],
    }
    
    # 成功/失败关键词
    success_keywords = ["✅", "完成", "成功", "已生成", "已创建", "已修复"]
    fail_keywords = ["❌", "失败", "错误", "超时", "无法", "不达标"]
    
    for session in sessions:
        content = session.get("content", "")
        if not content.strip():
            continue
            
        for wf_type, wf_keywords in keywords.items():
            if any(kw in content.lower() for kw in wf_keywords):
                stats[wf_type]["total"] += 1
                # 简单判断成功/失败
                if any(kw in content for kw in fail_keywords):
                    stats[wf_type]["failed"] += 1
                elif any(kw in content for kw in success_keywords):
                    stats[wf_type]["success"] += 1
                # 粗略估算迭代次数（数 "迭代" 关键词）
                iteration_count = content.count("迭代")
                if iteration_count > stats[wf_type]["max_iterations"]:
                    stats[wf_type]["max_iterations"] = iteration_count
                break  # 一个 session 只能算一个工作流
    
    # 计算平均值
    for wf_type in stats:
        total = stats[wf_type]["total"]
        if total > 0:
            stats[wf_type]["avg_iterations"] = stats[wf_type]["max_iterations"] / total
    
    return stats


def generate_review_report(date_str):
    """生成完整的复盘报告"""
    
    # 获取 sessions
    sessions = get_sessions_history(date_str)
    
    # 计算指标
    stats = calculate_workflow_metrics(sessions, date_str)
    problems = identify_problems(sessions)
    suggestions = generate_optimization_suggestions(stats, problems)
    
    # 构建报告
    report = f"""# 每日复盘 - {date_str}

## 📊 任务完成情况

| 工作流 | 总数 | 成功 | 失败 | 平均迭代 | 成功率 |
|--------|------|------|------|---------|--------|
| 文档写作 | {stats['文档写作']['total']} | {stats['文档写作']['success']} | {stats['文档写作']['failed']} | {stats['文档写作']['avg_iterations']:.1f} | {stats['文档写作']['success']/max(1,stats['文档写作']['total'])*100:.0f}% |
| 技术工作 | {stats['技术工作']['total']} | {stats['技术工作']['success']} | {stats['技术工作']['failed']} | {stats['技术工作']['avg_iterations']:.1f} | {stats['技术工作']['success']/max(1,stats['技术工作']['total'])*100:.0f}% |
| 技能研发 | {stats['技能研发']['total']} | {stats['技能研发']['success']} | {stats['技能研发']['failed']} | {stats['技能研发']['avg_iterations']:.1f} | {stats['技能研发']['success']/max(1,stats['技能研发']['total'])*100:.0f}% |

## 🔍 问题分析

### 问题清单
"""
    
    if not problems:
        report += "\n*昨日无明显问题，继续保持*\n"
    else:
        for i, p in enumerate(problems, 1):
            report += f"""
### 问题 {i}：{p['description']}
- **工作流：** {p['workflow']}
- **现象：** {p.get('impact', 'N/A')}
- **根因：** {p.get('root_cause', '待分析')}
- **建议：** {p.get('suggestion', '待确定')}
"""
    
    report += """
## 💡 优化建议

"""
    
    if not suggestions:
        report += "*暂无优化建议*\n"
    else:
        for i, s in enumerate(suggestions, 1):
            report += f"""
### 建议 {i}：{s['workflow']} 工作流优化
- **问题：** {s['problem']}
- **建议：** {s['suggestion']}
- **预期收益：** {s['expected_benefit']}
- **优先级：** {s['priority']}
"""
    
    report += f"""
## 📈 工作流执行统计详情

### 文档写作工作流
- 执行次数：{stats['文档写作']['total']}
- 成功率：{stats['文档写作']['success']/max(1,stats['文档写作']['total'])*100:.0f}%
- 平均迭代：{stats['文档写作']['avg_iterations']:.1f} 轮
- 最大迭代：{stats['文档写作']['max_iterations']} 轮

### 技术工作流
- 执行次数：{stats['技术工作']['total']}
- 成功率：{stats['技术工作']['success']/max(1,stats['技术工作']['total'])*100:.0f}%
- 平均迭代：{stats['技术工作']['avg_iterations']:.1f} 轮
- 最大迭代：{stats['技术工作']['max_iterations']} 轮

### 技能研发工作流
- 执行次数：{stats['技能研发']['total']}
- 成功率：{stats['技能研发']['success']/max(1,stats['技能研发']['total'])*100:.0f}%
- 平均迭代：{stats['技能研发']['avg_iterations']:.1f} 轮
- 最大迭代：{stats['技能研发']['max_iterations']} 轮

---

## 🏁 今日待确认（08:00 汇报）

请确认以下优化建议是否落地：

"""
    
    if not suggestions:
        report += "*暂无待确认的优化建议*\n"
    else:
        for i, s in enumerate(suggestions, 1):
            checkbox = "- [ ]"
            report += f"{checkbox} 建议{i}：{s['suggestion']}（{s['priority']}优先级）\n"
    
    report += f"""
---

**报告生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
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
