#!/usr/bin/env python3
"""
毫米波雷达技术日报生成器 v3.0
参考 ChatGPT 生成的高质量日报格式

改进点：
1. 执行摘要（Executive Summary）
2. 无信息时明确说明"过去X小时无新进展"
3. 严格过滤科普文章、财经新闻、营销内容
4. 7大板块结构
5. 快速要点与行动建议

用法：
    python3 generate-report-v3.py [--date YYYY-MM-DD]
"""

import requests
import json
import os
import sys
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

# ============== 配置 ==============

OUTPUT_DIR = "/root/.openclaw/workspace/radar-reports"
SEARXNG_URL = "http://searxng:8080"
SEARCH_TIME_RANGE = "day"  # 搜索最近24小时

# 严格的质量过滤配置
QUALITY_FILTER = {
    # 科普/教程类关键词（应排除）
    'POPULAR_SCIENCE': [
        '科普', '一篇搞懂', '一文读懂', '一分钟了解', '五分钟读懂',
        '入门指南', '从零开始', '小白', '新手必看', '教程',
        '是什么', '有什么用', '哪家好', '如何选择',
        '看这一篇就够了', '看这篇就够了', '看完就懂了',
        '知乎', 'zhihu.com', 'baike.baidu.com',
        '360百科', 'MBA智库', '百科'
    ],
    # 财经/股票类关键词（应排除）
    'FINANCE': [
        '股价', '涨停', '跌停', 'IPO', '上市', '财报',
        'stock', 'stock price', 'earnings', 'IPO',
        '东方财富', '同花顺', '新浪财经', '财联社',
        '主力净流入', '换手率', '市盈率', '市值',
        '股吧', 'stockbbs', 'guba.eastmoney'
    ],
    # 营销/产品介绍类关键词（应排除）
    'MARKETING': [
        '代理商', '经销商', '报价', '多少钱', '价格',
        '优惠', '促销', '热卖', '爆款', '热销',
        '今日报价', '厂家直销', '品牌', '代理加盟',
        'product', 'shop', 'buy', 'price', 'cost',
        'alibaba', '1688.com', 'taobao', 'jd.com'
    ],
    # 必须包含的技术关键词（保留的前提）
    'TECH_MUST_HAVE': [
        '雷达', 'radar', '毫米波', 'mmWave', '77GHz',
        '探测', 'detection', '传感器', 'sensor',
        '自动驾驶', 'autonomous', 'ADAS', '智能驾驶',
        '车载', 'automotive', 'vehicle', '汽车'
    ]
}

# 有效信息最小技术词数
MIN_TECH_WORDS = 2

@dataclass
class SearchResult:
    title: str
    url: str
    content: str
    source: str
    published_date: Optional[str] = None
    category: str = ""

def search_searxng(query: str, max_results: int = 8) -> List[SearchResult]:
    """搜索"""
    try:
        params = {
            'q': query,
            'format': 'json',
            'pageno': 1,
            'time_range': SEARCH_TIME_RANGE,
            'engines': 'baidu,bing'
        }
        response = requests.get(f"{SEARXNG_URL}/search", params=params, timeout=20)
        data = response.json()
        
        results = []
        for item in data.get('results', [])[:max_results * 2]:
            title = item.get('title', '')
            url = item.get('url', '')
            content = item.get('content', '')[:150]
            
            # 过滤百度知道
            if 'zhidao.baidu.com' in url:
                continue
            
            results.append(SearchResult(
                title=title,
                url=url,
                content=content,
                source=item.get('engine', 'unknown'),
                published_date=item.get('publishedDate')
            ))
            
            if len(results) >= max_results:
                break
        
        return results
    except Exception as e:
        print(f"搜索错误: {e}")
        return []

def is_quality_content(result: SearchResult) -> Tuple[bool, str]:
    """
    检查内容质量
    返回: (是否保留, 原因)
    """
    title = result.title
    content = result.content
    url = result.url
    combined = title + ' ' + content
    
    # 1. 检查必须包含技术关键词
    tech_count = sum(1 for kw in QUALITY_FILTER['TECH_MUST_HAVE'] if kw.lower() in combined.lower())
    if tech_count < 1:
        return False, "不包含关键技术词"
    
    # 2. 检查科普/教程类（应排除）
    for kw in QUALITY_FILTER['POPULAR_SCIENCE']:
        if kw.lower() in combined.lower():
            return False, f"科普内容: {kw}"
    
    # 3. 检查财经类（应排除）
    for kw in QUALITY_FILTER['FINANCE']:
        if kw.lower() in combined.lower():
            return False, f"财经内容: {kw}"
    
    # 4. 检查营销类（应排除）
    for kw in QUALITY_FILTER['MARKETING']:
        if kw.lower() in combined.lower():
            return False, f"营销内容: {kw}"
    
    # 5. 检查标题黑名单
    blacklist = ['如何评价', '怎么样', '好不好', '多少钱', '哪家强']
    for kw in blacklist:
        if kw in title:
            return False, f"标题含杂质: {kw}"
    
    return True, "OK"

def search_category(category: str, keywords: List[str]) -> Tuple[List[SearchResult], str]:
    """
    搜索单个分类
    返回: (过滤后的结果列表, 状态描述)
    """
    all_results = []
    for kw in keywords:
        results = search_searxng(kw)
        all_results.extend(results)
    
    # 去重（基于URL）
    seen_urls = set()
    unique_results = []
    for r in all_results:
        if r.url not in seen_urls:
            seen_urls.add(r.url)
            unique_results.append(r)
    
    # 质量过滤
    filtered = []
    rejected = []
    for r in unique_results:
        keep, reason = is_quality_content(r)
        if keep:
            filtered.append(r)
        else:
            rejected.append((r, reason))
    
    # 生成状态描述
    total = len(all_results)
    kept = len(filtered)
    
    if total == 0:
        status = f"⚠️ 过去24小时无{category}相关新公开资料"
    elif kept == 0:
        status = f"⚠️ 过去24小时{category}无符合质量标准的新内容（检索到{total}条，已过滤）"
    else:
        status = f"✅ 过去24小时{category}检索到{kept}条有效信息"
    
    return filtered, status

def generate_executive_summary(categories: Dict[str, List], total_hours: int = 36) -> str:
    """生成执行摘要"""
    lines = [
        f"## 执行摘要",
        "",
        f"过去{total_hours}小时（自{datetime.now().strftime('%Y年%m月%d日')}算起）毫米波雷达领域公开资料分析：",
        ""
    ]
    
    has_content = False
    key_findings = []
    
    for cat_name, results in categories.items():
        if results:
            has_content = True
            key_findings.append(f"- **{cat_name}**：{len(results)}条新进展")
        else:
            lines.append(f"- **{cat_name}**：过去{total_hours}小时无新公开资料")
    
    if has_content:
        lines.extend([
            "",
            "### 主要发现"
        ])
        lines.extend(key_findings)
    else:
        lines.extend([
            "",
            "### 说明",
            "注：若扩大检索窗口至7天仍无新资料，可能处于技术发布周期低谷期。建议关注头部企业（特斯拉、华为、大陆集团等）官方公告。"
        ])
    
    return '\n'.join(lines)

def generate_report_content():
    """生成完整日报"""
    
    # 搜索关键词（分类）
    SEARCH_KEYWORDS = {
        '专利': [
            '"毫米波雷达" 专利 车载 2026',
            '"77GHz radar" patent automotive',
            '"4D imaging radar" patent'
        ],
        '研究动态': [
            '"毫米波雷达" 信号处理 算法',
            '"mmWave radar" signal processing',
            '"automotive radar" academic research'
        ],
        '产业与公司': [
            '"毫米波雷达" 车企 智能驾驶 2026',
            '"automotive radar" industry news 2026',
            '"77GHz radar" autonomous driving ADAS'
        ],
        '供应链': [
            '"毫米波雷达" 芯片 供应商',
            '"radar chip" supplier automotive',
            '"mmWave radar" Tier1 Bosch Continental'
        ],
        '标准与法规': [
            '"毫米波雷达" 标准 法规 频谱',
            '"mmWave radar" standards regulation',
            '"automotive radar" FCC IEEE'
        ]
    }
    
    print("🔍 开始检索...")
    
    categories = {}
    status_report = []
    
    for cat_name, keywords in SEARCH_KEYWORDS.items():
        print(f"  搜索 {cat_name}...")
        results, status = search_category(cat_name, keywords)
        categories[cat_name] = results
        status_report.append(status)
        print(f"    {status}")
        if not results:
            print(f"    检索词: {keywords[0]}")
    
    # 生成执行摘要
    summary = generate_executive_summary(categories)
    
    # 生成正文
    content_lines = [
        "# Millimeter Wave Radar Daily Report",
        f"**日期：** {datetime.now().strftime('%Y-%m-%d')}",
        f"**生成时间：** {datetime.now().strftime('%H:%M:%S')}",
        "",
        summary,
        "",
        "---",
        ""
    ]
    
    # 各分类详情
    for cat_name, results in categories.items():
        content_lines.append(f"## {cat_name}")
        
        if not results:
            content_lines.append(f"*过去36小时无新公开资料。*")
            content_lines.append("")
            continue
        
        for i, r in enumerate(results[:5], 1):  # 最多5条
            content_lines.append(f"### {i}. {r.title}")
            content_lines.append(f"**来源：** {r.source}")
            if r.published_date:
                content_lines.append(f"**日期：** {r.published_date}")
            content_lines.append(f"**URL：** {r.url}")
            if r.content:
                content_lines.append(f"**摘要：** {r.content[:200]}...")
            content_lines.append("")
    
    # 快速要点与行动建议
    content_lines.extend([
        "---",
        "",
        "## 快速要点与行动建议",
        "",
        "1. **研发建议**：持续关注毫米波雷达信号处理算法与4D成像技术进展",
        "2. **产业跟踪**：关注特斯拉、华为、小鹏等车企雷达方案进展",
        "3. **供应链关注**：留意芯片供应情况及替代方案",
        "4. **合规提示**：关注毫米波频谱分配及出口管制政策变化",
        "",
        "---",
        "",
        f"*本报告由 AI 自动生成 | 检索时间范围：过去24-36小时*"
    ])
    
    return '\n'.join(content_lines)

def main():
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    # 解析参数
    for arg in sys.argv[1:]:
        if arg.startswith('--date='):
            date_str = arg.split('=')[1]
    
    print(f"📡 毫米波雷达技术日报生成器 v3.0")
    print(f"   日期: {date_str}")
    print(f"   检索时窗: 过去24-36小时")
    print("-" * 40)
    
    # 生成报告
    content = generate_report_content()
    
    # 保存
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, f"radar-daily-{date_str}.md")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("-" * 40)
    print(f"✅ 报告已保存: {output_file}")
    
    # 统计
    lines = content.split('\n')
    item_count = content.count('### ')
    print(f"   内容条数: {item_count}")
    
    return output_file

if __name__ == '__main__':
    main()
