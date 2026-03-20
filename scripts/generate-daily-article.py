#!/usr/bin/env python3
"""
每日科普文章生成器
用途：自动生成科普文章 topics 和大纲
时间：每日 06:00
"""

import json
from datetime import datetime

# 今日主题（可配置）
TOPICS = [
    {
        "category": "科技",
        "title": "量子计算机如何改变未来",
        "keywords": ["量子计算", "量子比特", "超导", "算法"],
        "outline": [
            "什么是量子计算机",
            "量子比特 vs 经典比特",
            "实际应用场景",
            "未来发展趋势"
        ]
    },
    {
        "category": "健康",
        "title": "睡眠科学的最新发现",
        "keywords": ["睡眠", "REM", "生物钟", "健康"],
        "outline": [
            "睡眠的四个阶段",
            "REM 睡眠的重要性",
            "如何改善睡眠质量",
            "最新研究成果"
        ]
    },
    {
        "category": "环境",
        "title": "碳中和与我们的生活",
        "keywords": ["碳中和", "碳排放", "可再生能源", "环保"],
        "outline": [
            "什么是碳中和",
            "全球碳排放现状",
            "个人能做什么",
            "未来能源结构"
        ]
    }
]

def generate_article_topic(date_str: str) -> dict:
    """根据日期选择今日主题"""
    # 简单轮询
    day_of_year = datetime.strptime(date_str, "%Y-%m-%d").timetuple().tm_yday
    topic_idx = day_of_year % len(TOPICS)
    return TOPICS[topic_idx]

def save_article(topic: dict, date_str: str, output_dir: str = "/root/.openclaw/workspace/articles"):
    """保存文章大纲"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    article = {
        "date": date_str,
        "category": topic["category"],
        "title": topic["title"],
        "keywords": topic["keywords"],
        "outline": topic["outline"],
        "status": "draft",
        "created_at": datetime.now().isoformat()
    }
    
    filename = f"{output_dir}/article-{date_str}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# {topic['title']}\n\n")
        f.write(f"**日期:** {date_str}\n")
        f.write(f"**分类:** {topic['category']}\n")
        f.write(f"**关键词:** {', '.join(topic['keywords'])}\n\n")
        f.write("## 大纲\n\n")
        for i, section in enumerate(topic["outline"], 1):
            f.write(f"{i}. {section}\n")
        f.write(f"\n---\n*自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
    
    return filename

if __name__ == "__main__":
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"📝 生成 {today} 科普文章...")
    
    topic = generate_article_topic(today)
    print(f"主题：{topic['title']}")
    print(f"分类：{topic['category']}")
    print(f"关键词：{', '.join(topic['keywords'])}")
    
    filename = save_article(topic, today)
    print(f"✅ 文章大纲已保存：{filename}")
