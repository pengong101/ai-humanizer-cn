#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系外行星发现数量增长图表（最终版 - 显式加载字体）
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager as fm

# 显式加载中文字体
font_path = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'
chinese_font = fm.FontProperties(fname=font_path)

# 数据
years = [1992, 1995, 2000, 2005, 2009, 2014, 2016, 2019, 2022, 2026]
counts = [2, 51, 50, 150, 350, 1000, 3500, 4000, 5000, 5600]

# 创建图表
fig, ax = plt.subplots(figsize=(10, 6), dpi=200, facecolor='#FAFAFA')

# 绘制折线
ax.plot(years, counts, marker='o', linewidth=2.5, markersize=8, 
        color='#E74C3C', markerfacecolor='#FFFFFF', markeredgewidth=2, markeredgecolor='#C0392B')

ax.fill_between(years, counts, alpha=0.15, color='#E74C3C')

# 标注
annotations = [
    (1992, 2, '首颗确认', 'left', 300),
    (2009, 350, '开普勒发射', 'right', 400),
    (2014, 1000, '突破 1000 颗', 'right', 400),
    (2016, 3500, '数据爆发', 'left', 400),
    (2022, 5000, '突破 5000 颗', 'right', 400),
    (2026, 5600, '韦伯时代', 'left', 400),
]

for year, count, text, align, offset in annotations:
    bbox_props = dict(boxstyle='round,pad=0.4', facecolor='#F39C12', alpha=0.9, edgecolor='#D35400', linewidth=1.5)
    arrow_props = dict(arrowstyle='->', connectionstyle='arc3,rad=0.3', color='#D35400', linewidth=1.5)
    
    if align == 'left':
        xytext = (year - 6, count + offset)
    else:
        xytext = (year + 3, count + offset)
    
    ax.annotate(text, xy=(year, count), xytext=xytext, 
                fontsize=9, fontweight='bold', fontproperties=chinese_font, color='#FFFFFF',
                bbox=bbox_props, arrowprops=arrow_props, ha='center')

ax.set_title('系外行星发现数量增长 (1992-2026)', fontsize=16, fontweight='bold', fontproperties=chinese_font, pad=15, color='#1a1a1a')
ax.set_xlabel('年份', fontsize=12, fontweight='bold', fontproperties=chinese_font, color='#34495E')
ax.set_ylabel('累计发现数量', fontsize=12, fontweight='bold', fontproperties=chinese_font, color='#34495E')

ax.grid(True, linestyle='--', alpha=0.3, color='#95A5A6', linewidth=1)
ax.set_axisbelow(True)
ax.set_xticks(years)
ax.set_xticklabels(years, fontsize=10, fontproperties=chinese_font)
ax.set_yticks([0, 1000, 2000, 3000, 4000, 5000, 6000])
ax.set_yticklabels(['0', '1K', '2K', '3K', '4K', '5K', '6K'], fontsize=10)

plt.tight_layout()
output_path = '/root/.openclaw/workspace/articles/images-2026-03-23/article-9-exoplanet/img-00-exoplanet-growth.png'
plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='#FAFAFA', edgecolor='none')
print(f"✅ 系外行星增长图表已保存：{output_path}")
import os
print(f"📊 文件大小：{os.path.getsize(output_path)/1024:.1f} KB")
