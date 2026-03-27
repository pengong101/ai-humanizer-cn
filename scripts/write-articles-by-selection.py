#!/usr/bin/env python3
"""
根据用户选择的题目生成文章
用法：python3 write-articles-by-selection.py 1 3
      （选择第 1 篇和第 3 篇题目生成文章）
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "services"))

from model_router.client import LLMClient

API_KEY = "sk-sp-a38e2667f4504d2e8e7588872c39059e"
BASE_URL = "https://coding.dashscope.aliyuncs.com/v1"

def load_topics():
    """加载题目列表"""
    topics_path = "/root/.openclaw/workspace/articles/topics-for-selection.json"
    with open(topics_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['topics']

def generate_article(topic: dict, date_str: str) -> str:
    """生成完整文章"""
    client = LLMClient(api_key=API_KEY, base_url=BASE_URL)
    
    prompt = f"""请根据以下主题写一篇科普文章：

主题：{topic['title']}
分类：{topic['category']}
关键词：{', '.join(topic['keywords'])}
简介：{topic['description']}

要求：
1. 文章长度 1000-2000 字
2. 语言通俗易懂，适合大众阅读
3. 包含实际案例、数据或研究结果
4. 结构清晰，有 3-5 个小标题
5. 结尾有总结和展望
6. 使用 Markdown 格式

请输出完整的文章内容。"""
    
    response = client.chat(
        model="qwen3.5-plus",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096,
        temperature=0.7,
        timeout_ms=90000
    )
    
    if response.success:
        article = f"""# {topic['title']}

**日期:** {date_str}
**分类:** {topic['category']}
**关键词:** {', '.join(topic['keywords'])}

---

{response.content}

---
*自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        return article
    else:
        return f"# {topic['title']}\n\n⚠️ API 调用失败：{response.error}\n"

def save_article(article: str, topic: dict, date_str: str):
    """保存文章"""
    safe_title = topic['title'].replace(' ', '-').replace(':', '-')
    filename = f"article-{date_str}-{safe_title}.md"
    output_dir = "/root/.openclaw/workspace/articles"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(article)
    
    return output_path

def main():
    if len(sys.argv) < 2:
        print("❌ 请提供选择的题目编号")
        print("用法：python3 write-articles-by-selection.py 1 3")
        print("      （选择第 1 篇和第 3 篇题目生成文章）")
        sys.exit(1)
    
    # 解析用户选择的编号
    selected_indices = []
    for arg in sys.argv[1:]:
        try:
            idx = int(arg)
            if 1 <= idx <= 10:
                selected_indices.append(idx)
            else:
                print(f"⚠️  编号 {idx} 超出范围（1-10），已跳过")
        except ValueError:
            print(f"⚠️  '{arg}' 不是有效数字，已跳过")
    
    if not selected_indices:
        print("❌ 没有有效的题目编号")
        sys.exit(1)
    
    print(f"\n📝 开始生成 {len(selected_indices)} 篇文章...\n")
    
    # 加载题目列表
    topics = load_topics()
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # 生成选中的文章
    for idx in selected_indices:
        topic = topics[idx - 1]  # 转换为 0-based 索引
        print(f"📄 生成第 {idx} 篇：{topic['title']}")
        
        article = generate_article(topic, date_str)
        output_path = save_article(article, topic, date_str)
        
        word_count = len(article)
        print(f"  ✅ 已保存：{output_path}")
        print(f"  📊 字数：{word_count}\n")
    
    print("="*60)
    print(f"✅ 完成！共生成了 {len(selected_indices)} 篇文章")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
