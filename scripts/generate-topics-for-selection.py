#!/usr/bin/env python3
"""
每日科普文章选题生成器（联网版）
每天 06:00 执行：搜索最新科技热点，输出 3-5 个候选标题
输出：topics-for-selection.json + topics-for-selection.md
用户审批后启动文章创作
"""

import requests
import json
import os
from datetime import datetime, timedelta

SEARXNG_URL = os.environ.get("SEARXNG_URL", "http://searxng:8080")

SEARCH_QUERIES = [
    "science breakthrough 2026 latest",
    "AI artificial intelligence 2026 news",
    "space exploration 2026 discoveries",
    "biotechnology breakthrough 2026",
    "quantum computing 2026 progress",
]

TOPIC_TEMPLATES = [
    {"category": "天文", "templates": [
        "NASA的Psyche任务：人类为什么要飞向一颗金属小行星？",
        "韦伯望远镜又发现了什么？",
        "太空探索2026：火星样本返回、星际航行新突破",
    ], "keywords": ["NASA", "Psyche", "space", "telescope", "Mars", "James Webb"]},
    {"category": "生物", "templates": [
        "GLP-1减肥药爆炸式增长背后的科学",
        "肠道菌群与大脑：你的第二大脑正在被研究",
        "基因编辑治疗罕见病：首批患者怎么样了？",
    ], "keywords": ["GLP-1", "Ozempic", "gut", "microbiome", "gene", "CRISPR"]},
    {"category": "科技", "templates": [
        "DeepSeek-V4：中国AI大模型最新突破",
        "GPT-5还没来，但AI助手已经改变了什么？",
        "苹果WWDC26会有多炸？",
        "自动驾驶：特斯拉FSD和萝卜快跑同时进化",
    ], "keywords": ["DeepSeek", "AI", "GPT", "Apple", "WWDC", "Tesla", "FSD"]},
    {"category": "量子", "templates": [
        "量子计算突破：纠错能力首次超过阈值",
        "量子计算机2026：实用化还有多远？",
    ], "keywords": ["quantum", "Qubit", "IBM", "Google", "error correction"]},
]

def search_trending(query, engine="bing", max_results=8):
    """搜索热点话题"""
    try:
        resp = requests.get(
            f"{SEARXNG_URL}/search",
            params={
                "q": query,
                "format": "json",
                "engines": engine,
                "max_results": max_results,
            },
            timeout=(10, 45),
        )
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])
        return [{"title": r["title"], "url": r.get("url", ""), "engine": engine}
                for r in results[:max_results]]
    except Exception as e:
        print(f"  ⚠️ 搜索失败 [{engine}/{query}]: {e}")
        return []

def extract_topics(search_results):
    """从搜索结果中提取有价值的热点词"""
    import re
    topics = []
    seen = set()

    # 技术词汇黑名单（常见无意义词）
    blacklist = {"how to", "what is", "latest", "2026", "new", "best", "top", "review", "test", "youtube", "wikipedia"}

    for result in search_results:
        title = result["title"]
        # 提取英文词（3个字母以上的词）
        words = re.findall(r'[A-Za-z][A-Za-z0-9+\-]{3,}', title)
        for w in words:
            w_lower = w.lower()
            if w_lower not in blacklist and w_lower not in seen:
                seen.add(w_lower)
                topics.append(w)
                if len(topics) >= 8:
                    break
        if len(topics) >= 8:
            break

    return topics[:8]

def build_topics(search_results):
    """用搜索结果匹配模板，生成真实标题"""
    import random
    random.seed(datetime.now().day)

    # 合并标题文本
    all_titles = " ".join(r["title"] for r in search_results).lower()

    candidates = []
    for group in TOPIC_TEMPLATES:
        category = group["category"]
        templates = group["templates"]
        trigger_words = group["keywords"]

        # 检查是否有触发词在搜索结果中
        matched_templates = []
        for kw in trigger_words:
            if kw.lower() in all_titles:
                for t in templates:
                    if kw.lower() in t.lower():
                        matched_templates.append(t)
                        break

        # 如果没有匹配，随机选一个模板
        if not matched_templates:
            matched_templates = templates

        selected = random.sample(matched_templates, min(len(matched_templates), 2))
        for t in selected:
            candidates.append({
                "title": t,
                "category": category,
                "keywords": [kw for kw in trigger_words if kw.lower() in all_titles][:3],
                "reason": "基于当日热点搜索结果生成",
            })

    return candidates[:6]

def main():
    print(f"\n{'='*60}")
    print(f"📚 每日科普文章选题生成 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")

    all_results = []
    for query in SEARCH_QUERIES:
        print(f"🔍 {query}")
        results = search_trending(query, engine="bing")
        all_results.extend(results)
        print(f"  → {len(results)} 条结果")

    if not all_results:
        print("❌ 搜索全部失败，使用备用主题库")
        # 备用：用固定主题
        candidates = [
            {"title": "脑机接口最新进展：用意念控制一切", "category": "科技", "keywords": ["脑机接口", "BCI", "Neuralink"], "reason": "热门前沿技术"},
            {"title": "量子计算突破：量子霸权再进一步", "category": "科技", "keywords": ["量子计算", "量子霸权"], "reason": "国际竞争焦点"},
            {"title": "AI大模型最新能力：GPT-5来了吗？", "category": "科技", "keywords": ["AI", "大模型", "GPT"], "reason": "最受关注的技术方向"},
        ]
    else:
        candidates = build_topics(all_results)

    output = {
        "generated_at": datetime.now().isoformat(),
        "for_date": datetime.now().strftime("%Y-%m-%d"),
        "candidates": candidates,
        "search_count": len(all_results),
    }

    # 保存 JSON
    json_path = "/root/.openclaw/workspace/articles/topics-for-selection.json"
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # 保存可读 Markdown
    md_path = "/root/.openclaw/workspace/articles/topics-for-selection.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# 科普文章选题候选\n\n")
        f.write(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        for i, c in enumerate(candidates, 1):
            f.write(f"## {i}. 【{c['category']}】{c['title']}\n\n")
            f.write(f"- 关键词：{', '.join(c['keywords'])}\n")
            f.write(f"- 理由：{c['reason']}\n\n")
        f.write("---\n\n请回复 **序号** 选择今日主题，例如：回复 `3`\n")

    print(f"\n✅ 选题生成完成：{len(candidates)} 个候选")
    print(f"📄 JSON: {json_path}")
    print(f"📄 MD:   {md_path}")
    print(f"\n请选择今日主题（回复序号）")

    # 输出到日志
    with open("/root/.openclaw/workspace/logs/topic-selection.log", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat()}] 生成 {len(candidates)} 个候选\n")
    return json_path, md_path

if __name__ == "__main__":
    main()
