#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
5G vs 6G 对比信息图（修复版 - 细柱子 + 无方框）
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np

# 使用英文标签避免字体问题
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 创建 4 个子图
fig, axes = plt.subplots(2, 2, figsize=(10, 8), dpi=200, facecolor='#FAFAFA')
fig.suptitle('5G vs 6G Performance Comparison', fontsize=16, fontweight='bold', y=0.98, color='#1a1a1a')

colors = {'5G': '#FF6B6B', '6G': '#4ECDC4'}
width = 0.25  # 更细的柱子

# 图表 1：下载速度
ax1 = axes[0, 0]
bars1 = ax1.bar(0 - width/2, 360, width, color=colors['5G'], alpha=0.8, edgecolor='#E74C3C', linewidth=1.5, label='5G')
bars2 = ax1.bar(0 + width/2, 0.1, width, color=colors['6G'], alpha=0.8, edgecolor='#1ABC9C', linewidth=1.5, label='6G')
ax1.set_ylabel('Time (seconds)', fontsize=11, fontweight='bold')
ax1.set_title('Download Speed', fontsize=12, fontweight='bold', pad=10)
ax1.set_xticks([0])
ax1.set_xticklabels(['4K Movie'], fontsize=10)
ax1.legend(fontsize=10, loc='upper right')
ax1.grid(axis='y', linestyle='--', alpha=0.3)
ax1.text(0 - width/2, 380, '6 min', ha='center', fontsize=10, fontweight='bold', color='#C0392B')
ax1.text(0 + width/2, 0.12, '0.1s', ha='center', fontsize=10, fontweight='bold', color='#16A085')

# 图表 2：延迟
ax2 = axes[0, 1]
bars1 = ax2.bar(0 - width/2, 10, width, color=colors['5G'], alpha=0.8, edgecolor='#E74C3C', linewidth=1.5, label='5G')
bars2 = ax2.bar(0 + width/2, 1, width, color=colors['6G'], alpha=0.8, edgecolor='#1ABC9C', linewidth=1.5, label='6G')
ax2.set_ylabel('Latency (ms)', fontsize=11, fontweight='bold')
ax2.set_title('Network Latency', fontsize=12, fontweight='bold', pad=10)
ax2.set_xticks([0])
ax2.set_xticklabels(['Auto Driving'], fontsize=10)
ax2.legend(fontsize=10, loc='upper right')
ax2.grid(axis='y', linestyle='--', alpha=0.3)
ax2.text(0 - width/2, 10.8, '10ms', ha='center', fontsize=10, fontweight='bold', color='#C0392B')
ax2.text(0 + width/2, 1.15, '1ms', ha='center', fontsize=10, fontweight='bold', color='#16A085')

# 图表 3：连接密度
ax3 = axes[1, 0]
bars1 = ax3.bar(0 - width/2, 100, width, color=colors['5G'], alpha=0.8, edgecolor='#E74C3C', linewidth=1.5, label='5G')
bars2 = ax3.bar(0 + width/2, 1000, width, color=colors['6G'], alpha=0.8, edgecolor='#1ABC9C', linewidth=1.5, label='6G')
ax3.set_ylabel('Devices (10K/km²)', fontsize=11, fontweight='bold')
ax3.set_title('Connection Density', fontsize=12, fontweight='bold', pad=10)
ax3.set_xticks([0])
ax3.set_xticklabels(['Density'], fontsize=10)
ax3.legend(fontsize=10, loc='upper right')
ax3.grid(axis='y', linestyle='--', alpha=0.3)
ax3.text(0 - width/2, 108, '1M', ha='center', fontsize=10, fontweight='bold', color='#C0392B')
ax3.text(0 + width/2, 1080, '10M', ha='center', fontsize=10, fontweight='bold', color='#16A085')

# 图表 4：定位精度
ax4 = axes[1, 1]
bars1 = ax4.bar(0 - width/2, 100, width, color=colors['5G'], alpha=0.8, edgecolor='#E74C3C', linewidth=1.5, label='5G')
bars2 = ax4.bar(0 + width/2, 1, width, color=colors['6G'], alpha=0.8, edgecolor='#1ABC9C', linewidth=1.5, label='6G')
ax4.set_ylabel('Accuracy (relative)', fontsize=11, fontweight='bold')
ax4.set_title('Positioning Accuracy', fontsize=12, fontweight='bold', pad=10)
ax4.set_xticks([0])
ax4.set_xticklabels(['Accuracy'], fontsize=10)
ax4.legend(fontsize=10, loc='upper right')
ax4.grid(axis='y', linestyle='--', alpha=0.3)
ax4.text(0 - width/2, 108, 'Meter', ha='center', fontsize=10, fontweight='bold', color='#C0392B')
ax4.text(0 + width/2, 1.15, 'Centimeter', ha='center', fontsize=10, fontweight='bold', color='#16A085')

plt.tight_layout(rect=[0, 0, 1, 0.95])
output_path = '/root/.openclaw/workspace/articles/images-2026-03-23/article-2-6G/img-00-5g-vs-6g.png'
plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='#FAFAFA', edgecolor='none')
print(f"✅ 5G vs 6G 对比图已保存：{output_path}")
import os
print(f"📊 文件大小：{os.path.getsize(output_path)/1024:.1f} KB")
