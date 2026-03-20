#!/usr/bin/env python3
"""
毫米波雷达日报生成器 - 必应中国版
日期：2026-03-20
"""

import requests
from datetime import datetime

SEARXNG_URL = "http://searxng:8080"

KEYWORDS = {
    'industry': ['毫米波雷达 2026', '77GHz 雷达 汽车', '车载雷达 市场'],
    'academic': ['毫米波雷达 算法', 'MIMO 雷达', '雷达 目标检测'],
    'patents': ['毫米波雷达 专利', '雷达 天线 专利'],
    'products': ['毫米波雷达 模块', '77GHz 传感器', '雷达 供应商']
}

def search_bing(keyword):
    try:
        url = f"{SEARXNG_URL}/search"
        params = {'q': keyword, 'format': 'json', 'categories': 'general'}
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        results = [r for r in data.get('results', []) if r.get('engine') == 'bing']
        return results
    except Exception as e:
        print(f"搜索失败 '{keyword}': {e}")
        return []

def generate_report(date_str):
    print(f"🔍 生成 {date_str} 雷达日报...")
    report = {'date': date_str, 'generated': datetime.now().isoformat(), 'categories': {}}
    total_items = 0
    
    for category, keywords in KEYWORDS.items():
        print(f"  搜索 {category}...")
        items = []
        for kw in keywords:
            results = search_bing(kw)
            items.extend(results[:3])
            total_items += len(results[:3])
        report['categories'][category] = items
        print(f"    找到 {len(items)} 条")
    
    output_file = f"/root/.openclaw/workspace/radar-reports/radar-daily-{date_str}-final.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# 毫米波雷达日报 - {date_str}\n\n")
        f.write(f"**生成时间:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"**数据来源:** SearXNG (必应中国引擎)\n")
        f.write(f"**总条目数:** {total_items}\n\n")
        f.write("## 📊 摘要\n\n")
        f.write(f"今日共收集 {total_items} 条毫米波雷达相关信息。\n\n")
        
        names = {'industry': '🏭 行业动态', 'academic': '📚 学术研究', 'patents': '📄 专利信息', 'products': '🛒 产品资讯'}
        for cat_id, items in report['categories'].items():
            f.write(f"## {names.get(cat_id, cat_id)}\n\n")
            if items:
                for i, item in enumerate(items[:5], 1):
                    f.write(f"{i}. [{item.get('title', '无标题')}]({item.get('url', '#')})\n")
                    content = item.get('content', '')[:100]
                    if content:
                        f.write(f"   {content}...\n")
                    f.write("\n")
            else:
                f.write("*暂无数据*\n\n")
        f.write(f"---\n*报告生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
    
    print(f"\n✅ 报告已保存：{output_file}")
    print(f"📊 总计：{total_items} 条")
    return report

if __name__ == "__main__":
    generate_report(datetime.now().strftime("%Y-%m-%d"))
