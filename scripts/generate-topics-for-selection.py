#!/usr/bin/env python3
"""
生成 10 篇科普文章题目
用途：供用户选择明日写作主题
"""

import json
from datetime import datetime, timedelta

# 主题库（5 大领域，每个领域 2 个题目）
TOPIC_POOL = [
    # 科技领域
    {
        "category": "科技",
        "title": "量子计算机如何改变未来",
        "keywords": ["量子计算", "量子比特", "超导", "算法"],
        "description": "探索量子计算的原理、优势和对未来的影响"
    },
    {
        "category": "科技",
        "title": "5G 之后的 6G 通信技术",
        "keywords": ["6G", "通信", "太赫兹", "万物互联"],
        "description": "揭秘下一代通信技术的突破和应用场景"
    },
    # 健康领域
    {
        "category": "健康",
        "title": "肠道菌群：你的第二大脑",
        "keywords": ["肠道菌群", "微生物", "免疫", "心理健康"],
        "description": "揭示肠道菌群如何影响身体健康和情绪"
    },
    {
        "category": "健康",
        "title": "间歇性断食的科学依据",
        "keywords": ["断食", "代谢", "长寿", "减肥"],
        "description": "解析间歇性断食对健康的益处和注意事项"
    },
    # 环境领域
    {
        "category": "环境",
        "title": "碳中和与我们的未来",
        "keywords": ["碳中和", "气候变化", "可再生能源", "环保"],
        "description": "解读碳中和目标下的生活方式变革"
    },
    {
        "category": "环境",
        "title": "海洋塑料污染的解决方案",
        "keywords": ["塑料污染", "海洋生态", "可降解", "回收"],
        "description": "探索应对海洋塑料污染的创新技术"
    },
    # 生物领域
    {
        "category": "生物",
        "title": "基因编辑技术的突破",
        "keywords": ["CRISPR", "基因编辑", "遗传病", "生物技术"],
        "description": "了解基因编辑如何治疗遗传性疾病"
    },
    {
        "category": "生物",
        "title": "人造肉：未来的餐桌革命",
        "keywords": ["人造肉", "细胞培养", "可持续", "蛋白质"],
        "description": "探索人造肉的技术原理和产业化前景"
    },
    # 天文领域
    {
        "category": "天文",
        "title": "系外行星探索新进展",
        "keywords": ["系外行星", "宜居带", "望远镜", "生命"],
        "description": "追踪寻找第二个地球的最新发现"
    },
    {
        "category": "天文",
        "title": "黑洞照片背后的科学",
        "keywords": ["黑洞", "事件视界", "引力波", "相对论"],
        "description": "解读人类首张黑洞照片的科学意义"
    }
]

def generate_topic_list():
    """生成题目列表"""
    output = {
        "generated_at": datetime.now().isoformat(),
        "for_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "topics": TOPIC_POOL
    }
    return output

def save_to_file(data):
    """保存到文件"""
    output_path = "/root/.openclaw/workspace/articles/topics-for-selection.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return output_path

def print_readable(data):
    """打印可读格式"""
    print("\n" + "="*60)
    print("📚 明日科普文章题目候选（10 篇）")
    print("="*60)
    print(f"生成时间：{data['generated_at']}")
    print(f"适用日期：{data['for_date']}")
    print("="*60 + "\n")
    
    for i, topic in enumerate(data['topics'], 1):
        print(f"{i:2d}. 【{topic['category']}】{topic['title']}")
        print(f"    关键词：{', '.join(topic['keywords'])}")
        print(f"    简介：{topic['description']}")
        print()
    
    print("="*60)
    print("💡 请选择 2 篇题目，系统将自动生成完整文章")
    print("="*60 + "\n")

def main():
    """主函数"""
    print("\n📝 生成明日科普文章题目...\n")
    
    data = generate_topic_list()
    output_path = save_to_file(data)
    
    print_readable(data)
    
    print(f"📁 题目列表已保存：{output_path}")
    print("✅ 生成完成，请用户明早选择 2 篇题目\n")

if __name__ == "__main__":
    main()
