


#!/usr/bin/env python3
"""
每日科普文章选题生成器 v2.1（联网版）
每天 06:00 执行：搜索最新科技热点，输出 3-5 个候选标题（含质量评分）
输出：topics-for-selection.json + topics-for-selection.md
用户审批后启动文章创作

v2.1 更新（2026-04-07）：
- 快速网络检测 + 本地模式降级
- 所有超时缩短（搜索 5s/20s，RSS 3s/8s，NASA 3s/10s）
- 联网时真实搜索，本地模式用高质量模板

v2.0 更新（2026-04-07）：
- 多语言搜索（英文+中文热点）
- 热度吸引力评分（反常识性/悬念感/实用性/话题性）
- 配图可行性评分
- 难度/来源/角度亮点标注
"""

import requests
import json
import os
import re
import random
from datetime import datetime

SEARXNG_URL = os.environ.get("SEARXNG_URL", "http://192.168.1.122:8089")

# =====================================================================
# 搜索查询（v2.0：多语言 + 多源）
# =====================================================================
SEARCH_QUERIES = [
    "science breakthrough 2026 latest",
    "NASA discoveries 2026",
    "AI artificial intelligence 2026 news",
    "space exploration 2026 discoveries",
    "biotechnology breakthrough 2026",
    "quantum computing 2026 progress",
    "科技 新闻 2026 最新 突破",
    "人工智能 大模型 2026 最新",
    "航天 最新消息 2026",
    "生物医学 突破 2026",
    "量子计算 研究 2026",
    "trending science topic April 2026",
]

# =====================================================================
# RSS 源配置
# =====================================================================
RSS_SOURCES = {
    "zhihu": "https://www.zhihu.com/rss",
    "tencent_news": "https://news.qq.com/rss.xml",
    "nasa_news": "https://www.nasa.gov/rss/dyn/breaking_news.rss",
}

# =====================================================================
# 快速网络检测
# =====================================================================
def quick_connectivity_check():
    """快速检测网络连通性，返回 searxng 或 local"""
    try:
        r = requests.get(f"{SEARXNG_URL}/search?q=test&format=json", timeout=(3, 8))
        if r.status_code == 200:
            print(f"✅ SearXNG 可用: {SEARXNG_URL}")
            return "searxng"
    except Exception as e:
        print(f"⚠️ SearXNG 不可用 [{type(e).__name__}], 使用本地模式")
    return "local"

# =====================================================================
# NASA 图片搜索 API
# =====================================================================
def search_nasa_images(query, page_size=5):
    """通过 NASA Images API 搜索可用配图数量（快速版）"""
    try:
        url = "https://images-api.nasa.gov/search"
        params = {"q": query, "media_type": "image", "page_size": page_size}
        resp = requests.get(url, params=params, timeout=(3, 10))
        resp.raise_for_status()
        data = resp.json()
        items = data.get("collection", {}).get("items", [])
        return len(items), items
    except Exception as e:
        print(f"  ⚠️ NASA 图片搜索失败 [{query[:20]}]: {e}")
        return 0, []

# =====================================================================
# 搜索热点话题（快速版）
# =====================================================================
def search_trending(query, engines=None, max_results=15):
    if engines is None:
        engines = ["baidu", "sogou", "bing"]
    try:
        resp = requests.get(
            f"{SEARXNG_URL}/search",
            params={"q": query, "format": "json", "engines": ",".join(engines), "max_results": max_results},
            timeout=(5, 20),
        )
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])
        return [{"title": r["title"], "url": r.get("url", ""), "engine": ",".join(engines)}
                for r in results[:max_results]]
    except Exception as e:
        print(f"  ⚠️ 搜索失败 [{query[:30]}]: {e}")
        return []

# =====================================================================
# RSS 源抓取（快速版）
# =====================================================================
def fetch_rss_source(url: str, timeout: int = 8) -> list:
    import xml.etree.ElementTree as ET
    try:
        resp = requests.get(url, timeout=(3, timeout), headers={
            'User-Agent': 'Mozilla/5.0 (TopicGenBot/1.0)',
            'Accept': 'application/rss+xml, application/xml, text/xml, */*'
        })
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
        items = []
        for item in root.findall('.//item') or root.findall('.//entry'):
            title_el = item.find('title')
            link_el = item.find('link')
            desc_el = item.find('description') or item.find('summary') or item.find('content')
            title = title_el.text.strip() if title_el is not None and title_el.text else ""
            link = (link_el.text or link_el.get('href') or "") if link_el is not None else ""
            desc = re.sub(r'<[^>]+>', '', desc_el.text)[:200] if desc_el is not None and desc_el.text else ""
            if title:
                items.append({"title": title.strip(), "url": link.strip(), "description": desc.strip()})
        return items[:10]
    except Exception as e:
        print(f"  ⚠️ RSS 失败 [{url[:40]}]: {e}")
        return []

def fetch_all_rss_sources() -> list:
    all_items = []
    for name, url in RSS_SOURCES.items():
        print(f"  📡 RSS: {name}")
        items = fetch_rss_source(url)
        print(f"    → {len(items)} 条")
        all_items.extend(items)
    return all_items

# =====================================================================
# 热度吸引力评分
# =====================================================================
HEAT_KEYWORDS = {
    "counter_intuitive": ["不应该存在", "不可能", "违反", "意外", "颠覆", "挑战", "质疑",
        "impossible", "shouldn't exist", "unexpected", "paradox", "mystery", "悖论", "谜团", "至今无解"],
    "suspense": ["会怎样", "能否", "是否", "什么时候", "为什么", "what if", "will", "can", "how", "why",
        "secret", "revealed", "即将", "终于", "首次", "第一次", "新发现"],
    "practical": ["有什么用", "如何", "怎么", "生活", "健康", "每天", "how to", "benefit", "life",
        "养生", "减肥", "护肤", "睡眠", "压力"],
    "viral": ["刷屏", "热搜", "爆火", "全网", "震惊", "炸裂", "viral", "trending", "breaking",
        "shocking", "explained", "轰动了", "沸腾", "炸锅"],
}

def score_heat(title: str, description: str = "") -> dict:
    text = (title + " " + description).lower()
    def count_stars(keywords):
        count = sum(1 for kw in keywords if kw.lower() in text)
        return min(5, max(1, count))
    return {k: count_stars(v) for k, v in HEAT_KEYWORDS.items()}

def heat_to_str(score: dict) -> str:
    return (f"反常识性{'⭐'*score['counter_intuitive']} | "
            f"悬念感{'⭐'*score['suspense']} | "
            f"实用性{'⭐'*score['practical']} | "
            f"话题性{'⭐'*score['viral']}")

# =====================================================================
# 配图可行性评分
# =====================================================================
IMAGE_CATEGORIES = {
    "天文": {"keywords": ["NASA", "韦伯", "望远镜", "黑洞", "星系", "宇宙", "太空", "星", "space", "galaxy", "Mars"],
             "nasa_queries": ["space", "galaxy", "nebula", "telescope", "universe", "star", "Mars"], "base_score": 4},
    "生物": {"keywords": ["基因", "细胞", "脑", "神经", "DNA", "蛋白", "医学", "药", "减肥", "GLP-1"],
             "nasa_queries": [], "base_score": 3},
    "科技": {"keywords": ["AI", "大模型", "GPT", "芯片", "量子", "计算", "DeepSeek", "ChatGPT", "Neuralink"],
             "nasa_queries": [], "base_score": 2},
    "量子": {"keywords": ["量子", "qubit", "量子计算", "量子霸权", "quantum"],
             "nasa_queries": ["quantum", "physics"], "base_score": 3},
    "健康": {"keywords": ["减肥", "睡眠", "肠道", "菌群", "健康", "锻炼", "睡眠"],
             "nasa_queries": [], "base_score": 2},
}

def score_image_feasibility(category: str, title: str, online: bool = True) -> tuple:
    cat_config = IMAGE_CATEGORIES.get(category, {"keywords": [], "nasa_queries": [], "base_score": 2})
    base = cat_config["base_score"]
    nasa_available = 0

    if online and cat_config.get("nasa_queries"):
        query = cat_config["nasa_queries"][0]
        nasa_available, _ = search_nasa_images(query, page_size=5)
        if nasa_available >= 3:
            base = min(5, base + 1)

    title_lower = title.lower()
    for kw in cat_config["keywords"]:
        if kw.lower() in title_lower:
            base = min(5, base + 1)
            break

    if nasa_available >= 5:
        note = f"NASA官方图{nasa_available}张"
    elif base >= 4:
        note = "官方图丰富"
    elif base >= 3:
        note = "有可用图片"
    else:
        note = "需自行生成配图"

    return base, nasa_available, note

# =====================================================================
# 难度评估
# =====================================================================
def assess_difficulty(title: str, search_count: int) -> str:
    high = ["机制", "原理", "量子", "基因编辑", "理论", "physics", "mechanism", "纠错", "量子霸权"]
    low = ["来了吗", "是什么", "科普", "入门", "介绍", "how", "what is", "最新", "突破"]
    title_lower = title.lower()
    h = sum(1 for kw in high if kw.lower() in title_lower)
    l = sum(1 for kw in low if kw.lower() in title_lower)
    if h > l and search_count < 10:
        return "高（专业资料少）"
    elif h > l:
        return "中（需理解专业概念）"
    elif l > h:
        return "低（资料丰富，易理解）"
    return "中（需一定背景知识）"

# =====================================================================
# 来源汇总
# =====================================================================
def summarize_sources(search_results: list, rss_count: int) -> str:
    sources = set()
    for r in search_results:
        engine = r.get("engine", "")
        if "baidu" in engine: sources.add("百度")
        if "bing" in engine: sources.add("Bing")
        if "sogou" in engine: sources.add("搜狗")
        if engine == "rss": sources.add("RSS")
    if rss_count > 0: sources.add(f"RSS({rss_count}条)")
    return " + ".join(sorted(sources)) if sources else "搜索结果"

# =====================================================================
# 角度亮点
# =====================================================================
def extract_angle(title: str, heat_score: dict) -> str:
    if heat_score["counter_intuitive"] >= 4: return "颠覆认知，挑战现有理论"
    elif heat_score["viral"] >= 4: return "热点话题，社交传播潜力强"
    elif heat_score["practical"] >= 4: return "实用性强，与日常生活相关"
    elif heat_score["suspense"] >= 4: return "悬念感强，吸引读者想知道答案"
    return "内容扎实，有科普价值"

# =====================================================================
# 备用主题库（完全失败时使用）
# =====================================================================
FALLBACK_TOPICS = [
    {"title": "脑机接口最新进展：用意念控制一切", "category": "科技",
     "keywords": ["脑机接口", "BCI", "Neuralink"], "reason": "热门前沿技术"},
    {"title": "量子计算突破：量子霸权再进一步", "category": "量子",
     "keywords": ["量子计算", "量子霸权"], "reason": "国际竞争焦点"},
    {"title": "AI大模型最新能力：GPT-5来了吗？", "category": "科技",
     "keywords": ["AI", "大模型", "GPT"], "reason": "最受关注的技术方向"},
]

# =====================================================================
# 候选构建
# =====================================================================
TOPIC_TEMPLATES = [
    {"category": "天文", "templates": [
        "韦伯望远镜发现最古老的黑洞：它不该存在？",
        "NASA的Psyche任务：人类为什么要飞向一颗金属小行星？",
        "太空探索2026：火星样本返回、星际航行新突破",
    ], "keywords": ["NASA", "Psyche", "韦伯", "黑洞", "space", "telescope", "Mars", "James Webb"]},
    {"category": "生物", "templates": [
        "GLP-1减肥药的新战场：不只减肥，还在改变大脑",
        "肠道菌群与大脑：你的第二大脑正在被研究",
        "基因编辑治疗罕见病：首批患者怎么样了？",
    ], "keywords": ["GLP-1", "Ozempic", "肠道", "菌群", "基因", "CRISPR"]},
    {"category": "科技", "templates": [
        "DeepSeek-V4发布：开源模型追上GPT-5了吗？",
        "GPT-5还没来，但AI助手已经改变了什么？",
        "苹果WWDC26会有多炸？",
        "自动驾驶：特斯拉FSD和萝卜快跑同时进化",
    ], "keywords": ["DeepSeek", "AI", "GPT", "Apple", "WWDC", "Tesla", "FSD"]},
    {"category": "量子", "templates": [
        "量子计算突破：纠错能力首次超过阈值",
        "量子计算机2026：实用化还有多远？",
    ], "keywords": ["量子", "Qubit", "IBM", "Google", "quantum", "error correction"]},
]

def build_candidates_v2(search_results):
    random.seed(datetime.now().day)
    all_titles = " ".join(r["title"] for r in search_results).lower()
    candidates = []
    for group in TOPIC_TEMPLATES:
        matched = []
        for kw in group["keywords"]:
            if kw.lower() in all_titles:
                for t in group["templates"]:
                    if kw.lower() in t.lower() and t not in matched:
                        matched.append(t)
                        break
        if not matched:
            matched = group["templates"]
        selected = random.sample(matched, min(len(matched), 2))
        for t in selected:
            keywords = [kw for kw in group["keywords"] if kw.lower() in all_titles][:3]
            if not keywords: keywords = group["keywords"][:3]
            candidates.append({"title": t, "category": group["category"],
                               "keywords": keywords, "reason": "基于当日热点生成"})
    return candidates[:6]

# =====================================================================
# 主函数
# =====================================================================
def main():
    print(f"\n{'='*60}")
    print(f"📚 每日科普文章选题生成 v2.1 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")

    mode = quick_connectivity_check()
    all_results = []
    rss_items = []

    if mode == "searxng":
        # ---- Step 1: 多引擎搜索 ----
        for query in SEARCH_QUERIES:
            engines = ["baidu", "sogou"] if any(ord(c) > 127 for c in query) else ["bing"]
            print(f"🔍 [{engines[0]}] {query}")
            results = search_trending(query, engines=engines, max_results=10)
            all_results.extend(results)
            print(f"  → {len(results)} 条")

        # ---- Step 2: RSS 补充 ----
        print(f"\n📡 抓取 RSS...")
        rss_items = fetch_all_rss_sources()
        for item in rss_items:
            all_results.append({"title": item["title"], "url": item.get("url", ""),
                                "engine": "rss", "description": item.get("description", "")})
        print(f"  RSS +{len(rss_items)} 条\n")
    else:
        print("⚠️ 本地模式：跳过网络搜索，使用高质量模板\n")

    total_results = len(all_results)

    # ---- Step 3: 生成候选 ----
    if total_results == 0:
        print("⚠️ 搜索全部失败，使用备用主题库")
        candidates = FALLBACK_TOPICS
    else:
        candidates = build_candidates_v2(all_results)

    # ---- Step 4: 质量评分 ----
    scored = []
    for c in candidates:
        heat = score_heat(c["title"])
        online = (mode == "searxng")
        img_score, nasa_count, img_note = score_image_feasibility(c["category"], c["title"], online)
        difficulty = assess_difficulty(c["title"], total_results)
        sources = summarize_sources(all_results, len(rss_items)) if online else "本地生成"
        angle = extract_angle(c["title"], heat)
        recommend = "✅" if (heat["counter_intuitive"] + heat["suspense"] >= 6 and img_score >= 3) else "候选"

        scored.append({
            **c,
            "search_results_count": total_results,
            "image_feasibility": img_score,
            "image_note": img_note,
            "heat_score": heat,
            "heat_str": heat_to_str(heat),
            "difficulty": difficulty,
            "sources": sources,
            "angle": angle,
            "recommend": recommend,
        })

    # 按综合热度排序
    scored.sort(key=lambda x: x["heat_score"]["counter_intuitive"] + x["heat_score"]["suspense"] + x["image_feasibility"], reverse=True)

    # ---- Step 5: 保存输出 ----
    output = {
        "generated_at": datetime.now().isoformat(),
        "for_date": datetime.now().strftime("%Y-%m-%d"),
        "version": "2.1",
        "mode": mode,
        "candidates": scored,
        "search_count": total_results,
    }

    json_path = "/root/.openclaw/workspace/articles/topics-for-selection.json"
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    md_path = "/root/.openclaw/workspace/articles/topics-for-selection.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# 科普文章选题候选\n\n")
        f.write(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} | v2.1 | 模式：{mode}\n\n")
        for i, c in enumerate(scored, 1):
            f.write(f"## {i}. 【{c['category']}】{c['title']}\n\n")
            f.write(f"- 关键词：{', '.join(c['keywords'])}\n")
            f.write(f"- 来源：{c['sources']}\n")
            f.write(f"- 搜索结果：{c['search_results_count']} 条\n")
            f.write(f"- 配图可行性：{'⭐'*c['image_feasibility']}（{c['image_note']}）\n")
            f.write(f"- 热度吸引力：{c['heat_str']}\n")
            f.write(f"- 角度亮点：{c['angle']}\n")
            f.write(f"- 难度：{c['difficulty']}\n")
            f.write(f"- **{c['recommend']}**\n\n")
        f.write("---\n\n请回复 **序号** 选择今日主题，例如：`1`\n")

    print(f"\n✅ 选题生成完成：{len(scored)} 个候选（含质量评分）")
    print(f"📄 JSON: {json_path}")
    print(f"📄 MD:   {md_path}")

    os.makedirs("/root/.openclaw/workspace/logs", exist_ok=True)
    with open("/root/.openclaw/workspace/logs/topic-selection.log", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat()}] v2.1 {mode} 生成 {len(scored)} 候选，搜索 {total_results} 条\n")

    return json_path, md_path

if __name__ == "__main__":
    main()
