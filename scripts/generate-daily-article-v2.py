#!/usr/bin/env python3
"""
每日科普文章生成器（增强版 - 直接调用 API）
版本：v0.3
用途：自动生成完整科普文章
时间：每日 06:00
"""

import requests
import json
import os
from datetime import datetime

# API 配置
API_KEY = "sk-sp-a38e2667f4504d2e8e7588872c39059e"
BASE_URL = "https://coding.dashscope.aliyuncs.com/v1"

# 文章主题库
TOPICS = [
    {"category": "科技", "title": "量子计算机如何改变未来", "keywords": ["量子计算", "量子比特", "超导", "算法"]},
    {"category": "健康", "title": "睡眠科学的最新发现", "keywords": ["睡眠", "REM", "生物钟", "健康"]},
    {"category": "环境", "title": "碳中和与我们的未来", "keywords": ["碳中和", "气候变化", "可再生能源", "环保"]},
    {"category": "生物", "title": "基因编辑技术的突破", "keywords": ["CRISPR", "基因编辑", "遗传病", "生物技术"]},
    {"category": "天文", "title": "系外行星探索新进展", "keywords": ["系外行星", "宜居带", "望远镜", "生命"]}
]

def select_topic_by_date(date_str: str) -> dict:
    date = datetime.strptime(date_str, "%Y-%m-%d")
    index = date.timetuple().tm_yday % len(TOPICS)
    return TOPICS[index]

def generate_full_article(topic: dict, date_str: str) -> str:
    """调用大模型 API 生成完整文章"""
    prompt = f"""请根据以下主题写一篇科普文章：
主题：{topic['title']}
分类：{topic['category']}
关键词：{', '.join(topic['keywords'])}
要求：800-1500 字，通俗易懂，有小标题，Markdown 格式。"""
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "qwen3.5-plus",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 4096,
                "temperature": 0.7
            },
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        
        article = f"# {topic['title']}\n\n**日期:** {date_str}\n**分类:** {topic['category']}\n**关键词:** {', '.join(topic['keywords'])}\n\n---\n\n{content}\n\n---\n*自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        return article
    except Exception as e:
        return f"# {topic['title']}\n\n**日期:** {date_str}\n**分类:** {topic['category']}\n\n⚠️ API 调用失败：{e}\n"

def save_article(article: str, date_str: str, output_dir: str = "/root/.openclaw/workspace/articles"):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"article-{date_str}.md")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(article)
    return output_path

def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    import sys
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
    
    print(f"📝 生成 {date_str} 科普文章...")
    topic = select_topic_by_date(date_str)
    print(f"  主题：{topic['title']}")
    article = generate_full_article(topic, date_str)
    output_path = save_article(article, date_str)
    print(f"  ✅ 文章已保存：{output_path}")
    print(f"  📊 文章长度：{len(article)} 字")
    return output_path

if __name__ == "__main__":
    main()
