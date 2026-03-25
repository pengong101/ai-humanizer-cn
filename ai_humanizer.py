#!/usr/bin/env python3
"""
AI Humanizer CN - 中文 AI 文本拟人化
v5.1.0 入口文件
本文件从 humanize_v5.py 导入所有功能
"""

from humanize_v5 import (
    AIHumanizerV5,
    HumanizerConfig,
    humanize,
    VERSION,
    Intensity,
    ArticleType,
)

__version__ = VERSION
__all__ = ["AIHumanizerV5", "HumanizerConfig", "humanize", "VERSION", "Intensity", "ArticleType"]
