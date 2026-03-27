#!/usr/bin/env python3
"""
AI Humanizer CN v5.1.0 - 中文 AI 文本拟人化
功能：去除 AI 痕迹，保持专业性，支持强度控制、文章类型感知、专业术语保护
"""

import re
import os
import json
import time
import hashlib
import logging
import requests
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

# ============================================================
# 配置与常量
# ============================================================

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

VERSION = "5.2.0"

INTENSITY_CONFIG = {
    "low": {"口语化比例": 0.08, "连接词比例": 0.15, "填充词密度": 0.03},
    "medium": {"口语化比例": 0.18, "连接词比例": 0.25, "填充词密度": 0.06},
    "high": {"口语化比例": 0.32, "连接词比例": 0.35, "填充词密度": 0.10},
    "auto": None,  # 由 QC 评分决定
}

ARTICLE_TYPE_CONFIG = {
    "tech": {"语气词密度": 0.05, "专业术语保护": True, "数据保护": True, "互动句比例": 0.02},
    "science": {"语气词密度": 0.12, "专业术语保护": True, "数据保护": True, "互动句比例": 0.05},
    "social": {"语气词密度": 0.25, "专业术语保护": False, "数据保护": False, "互动句比例": 0.15},
    "academic": {"语气词密度": 0.03, "专业术语保护": True, "数据保护": True, "互动句比例": 0.01},
}

# 口语化连接词库
CASUAL_CONNECTORS = [
    "然后", "接着", "还有", "另外", "说起来", "话说回来",
    "而且", "不过", "但是", "其实", "总的来说",
    "怎么说呢", "这么说吧", "有意思的是",
]

# 填充词
FILLER_WORDS = [
    "说实话", "讲真的", "你可能不知道", "有意思的是",
    "不得不承认", "说白了", "说句心里话",
]

# 反问句模板
RHETORICAL_PATTERNS = [
    (r"不(是|就|能|会|好|行)(吗|呀|吧)?\？", 1),
    (r"怎么(会|能|可|不)(呢|吗|吧)\？", 1),
    (r"难道不是吗？", 1),
    (r"不是吗？", 1),
    (r"你说对不对？", 1),
    (r"是不是？", 1),
]

# 专业术语保护模式（不修改这些内容）
PROTECTED_PATTERNS = [
    (r'\d+\.?\d*%', 'DATA'),  # 百分比
    (r'\d+\.?\d*\s*(km/h|km/s|m/s|倍|年|月|日|时|分|秒|℃|km|m|kg|Hz|GHz|MHz)', 'DATA'),  # 复合单位+普通单位
    (r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*', 'PROPER'),  # 英文术语/人名（首字母大写）
    (r'["""](?:[^"""""（）()]|["""][^""""""])*["""]', 'QUOTE'),  # 引号内容
    (r'[（\(][^（）]*[）\)]', 'BRACKET'),  # 括号内容
]


# ============================================================
# 数据结构
# ============================================================

class Intensity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    AUTO = "auto"

class ArticleType(Enum):
    TECH = "tech"
    SCIENCE = "science"
    SOCIAL = "social"
    ACADEMIC = "academic"

@dataclass
class HumanizerConfig:
    intensity: str = "medium"
    article_type: str = "science"
    protect_terms: bool = True
    rhetorical_question_density: int = 3  # 每500字最大反问句数
    qc_score: float = 8.0  # 外部QC评分，用于auto模式
    model: str = "dashscope/qwen-max"
    api_key: str = ""

    def resolve_intensity(self) -> Dict:
        if self.intensity == "auto":
            if self.qc_score >= 9.0:
                return INTENSITY_CONFIG["low"]
            elif self.qc_score >= 8.0:
                return INTENSITY_CONFIG["medium"]
            else:
                return INTENSITY_CONFIG["high"]
        return INTENSITY_CONFIG.get(self.intensity, INTENSITY_CONFIG["medium"])

    def resolve_article_type(self) -> Dict:
        return ARTICLE_TYPE_CONFIG.get(self.article_type, ARTICLE_TYPE_CONFIG["science"])


# ============================================================
# 核心类
# ============================================================

class AIHumanizerV5:
    """中文 AI 文本拟人化核心类"""

    def __init__(self, config: Optional[HumanizerConfig] = None):
        self.config = config or HumanizerConfig()
        self._protected_map: List[Tuple[str, str]] = []  # (placeholder, original_text)
        self._stats = {}

    # --------------------------------------------------------
    # 公开 API
    # --------------------------------------------------------

    def humanize(self, text: str) -> str:
        """主入口：拟人化一段文本"""
        if not text or not text.strip():
            return text

        start = time.time()

        # Step 1: 保护专业内容
        protected_text, self._protected_ranges = self._protect_content(text)

        # Step 2: 分析当前文本特征
        analysis = self._analyze_text(protected_text)

        # Step 3: 获取强度配置
        intensity_cfg = self.config.resolve_intensity()
        type_cfg = self.config.resolve_article_type()

        # Step 4: AI 模型处理（如果配置了 API key）
        if self.config.api_key and self.config.model:
            result = self._ai_process(protected_text, analysis, intensity_cfg, type_cfg)
        else:
            result = self._rule_based_process(protected_text, analysis, intensity_cfg, type_cfg)

        # Step 5: 反问句密度控制
        result = self._control_rhetorical_density(result)

        # Step 6: 恢复保护内容
        result = self._restore_content(result)

        elapsed = time.time() - start
        self._stats = {
            "version": VERSION,
            "intensity": self.config.intensity,
            "article_type": self.config.article_type,
            "elapsed_ms": round(elapsed * 1000),
            "input_len": len(text),
            "output_len": len(result),
        }
        return result

    def batch_process(self, texts: List[str]) -> List[str]:
        """批量处理"""
        return [self.humanize(t) for t in texts]

    def get_stats(self) -> Dict:
        """获取处理统计"""
        return self._stats.copy()

    # --------------------------------------------------------
    # Step 1: 专业内容保护
    # --------------------------------------------------------

    def _protect_content(self, text: str) -> Tuple[str, List]:
        """识别并保护专业内容，替换为占位符"""
        self._protected_map: List[Tuple[str, str]] = []

        # 从后往前扫描，收集所有保护范围（避免位置偏移问题）
        protected_ranges: List[Tuple[int, int, str, str]] = []  # (start, end, original, label)
        for pattern, label in PROTECTED_PATTERNS:
            for m in re.finditer(pattern, text):
                start, end = m.start(), m.end()
                # 检查是否与已有范围重叠
                if not any(not (end <= r[0] or start >= r[1]) for r in protected_ranges):
                    protected_ranges.append((start, end, m.group(), label))

        # 按位置从后往前排序
        protected_ranges.sort(key=lambda x: x[0], reverse=True)

        # 逐一替换为占位符
        result = text
        for start, end, original, label in protected_ranges:
            idx = len(self._protected_map)
            placeholder = f"__PROT_{label}_{idx}__"
            result = result[:start] + placeholder + result[end:]
            self._protected_map.append((placeholder, original))

        return result, self._protected_map

    def _restore_content(self, text: str) -> str:
        """恢复被保护的内容"""
        result = text
        for placeholder, original in self._protected_map:
            result = result.replace(placeholder, original, 1)
        return result

    # --------------------------------------------------------
    # Step 2: 文本分析
    # --------------------------------------------------------

    def _analyze_text(self, text: str) -> Dict:
        """分析文本当前特征"""
        sentences = re.split(r'[。！？；\n]', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        word_count = len(text)
        connector_count = sum(1 for c in CASUAL_CONNECTORS if c in text)
        filler_count = sum(1 for f in FILLER_WORDS if f in text)

        rhetorical_count = 0
        for pattern, weight in RHETORICAL_PATTERNS:
            rhetorical_count += len(re.findall(pattern, text))

        return {
            "word_count": word_count,
            "sentence_count": len(sentences),
            "connector_ratio": connector_count / max(word_count, 1),
            "filler_ratio": filler_count / max(word_count, 1),
            "rhetorical_count": rhetorical_count,
        }

    # --------------------------------------------------------
    # Step 3 & 4: AI 模型处理
    # --------------------------------------------------------

    def _ai_process(self, text: str, analysis: Dict, intensity_cfg: Dict, type_cfg: Dict) -> str:
        """通过 AI 模型进行拟人化处理"""
        intensity_label = self.config.intensity
        article_type = self.config.article_type

        prompt = self._build_prompt(text, intensity_label, article_type, analysis)

        # 根据模型选择调用方式
        if "dashscope" in self.config.model or "qwen" in self.config.model:
            return self._call_dashscope(prompt, text)
        elif "openai" in self.config.model or "gpt" in self.config.model:
            return self._call_openai_compatible(prompt, text, "https://api.openai.com/v1/chat/completions")
        elif "minimax" in self.config.model:
            return self._call_minimax(prompt, text)
        else:
            return self._rule_based_process(text, analysis, intensity_cfg, type_cfg)

    def _build_prompt(self, text: str, intensity: str, article_type: str, analysis: Dict) -> str:
        intensity_desc = {
            "low": "轻微口语化，保留正式语气，适合技术文档",
            "medium": "适度口语化，平衡专业与可读，适合科普文章",
            "high": "明显口语化，轻松自然，适合社交媒体",
            "auto": "根据文本质量自动调整",
        }
        article_desc = {
            "tech": "技术文章，保持严谨，少用语气词",
            "science": "科普文章，平衡专业与通俗",
            "social": "社交媒体，自然轻松，可有情感表达",
            "academic": "学术论文，最小改动，保持严谨",
        }
        return f"""你是一位中文写作专家。请将以下AI生成的文章进行拟人化处理。

要求：
- 强度：{intensity_desc.get(intensity, intensity_desc['medium'])}
- 文章类型：{article_desc.get(article_type, article_desc['science'])}
- 保持原文专业术语、数据、引用不变
- 调整连接词、语气词、句式结构，使其更像人类写作
- 不要添加原文没有的新信息

原文：
{text}

请直接输出修改后的文章，不需要解释。"""

    def _call_dashscope(self, prompt: str, original: str) -> str:
        """调用阿里百炼 API"""
        try:
            import json as json_mod
            api_key = self.config.api_key or os.environ.get("DASHSCOPE_API_KEY", "")
            if not api_key:
                return self._fallback_to_rule_based(original)

            url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "qwen-max",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 2000
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            logging.warning(f"Dashscope API call failed: {e}")
        return self._fallback_to_rule_based(original)

    def _call_openai_compatible(self, prompt: str, original: str, endpoint: str) -> str:
        """调用 OpenAI 兼容 API"""
        try:
            import json as json_mod
            api_key = self.config.api_key or os.environ.get("OPENAI_API_KEY", "")
            if not api_key:
                return self._fallback_to_rule_based(original)

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "gpt-4",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 2000
            }
            resp = requests.post(endpoint, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            logging.warning(f"OpenAI API call failed: {e}")
        return self._fallback_to_rule_based(original)

    def _call_minimax(self, prompt: str, original: str) -> str:
        """调用 MiniMax API"""
        try:
            import json as json_mod
            api_key = self.config.api_key or os.environ.get("MINIMAX_API_KEY", "")
            if not api_key:
                return self._fallback_to_rule_based(original)

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "abab6.5s-chat",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 2000
            }
            resp = requests.post(
                "https://api.minimaxi.com/v1/text/chatcompletion_v2",
                headers=headers,
                json=payload,
                timeout=30
            )
            resp.raise_for_status()
            result = resp.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["messages"][-1]["content"].strip()
        except Exception as e:
            logging.warning(f"MiniMax API call failed: {e}")
        return self._fallback_to_rule_based(original)

    # --------------------------------------------------------
    # Step 4 alt: 规则引擎处理（无 API 时降级）
    # --------------------------------------------------------

    def _rule_based_process(self, text: str, analysis: Dict,
                            intensity_cfg: Dict, type_cfg: Dict) -> str:
        """纯规则引擎拟人化（无 API 时使用）"""
        result = text

        # 1. 调整连接词密度
        target_connector_ratio = intensity_cfg.get("连接词比例", 0.25)
        current_ratio = analysis.get("connector_ratio", 0)
        if current_ratio < target_connector_ratio:
            result = self._inject_connectors(result, target_connector_ratio - current_ratio)

        # 2. 注入填充词
        target_filler_ratio = intensity_cfg.get("填充词密度", 0.06)
        current_filler_ratio = analysis.get("filler_ratio", 0)
        if current_filler_ratio < target_filler_ratio:
            result = self._inject_fillers(result, target_filler_ratio - current_filler_ratio)

        # 3. 调整句式（长短句交替）
        result = self._vary_sentence_length(result)

        # 4. 去除过度工整的句式
        result = self._naturalize_patterns(result)

        return result

    def _fallback_to_rule_based(self, text: str) -> str:
        """API 调用失败时降级到规则引擎"""
        analysis = self._analyze_text(text)
        intensity_cfg = self.config.resolve_intensity()
        type_cfg = self.config.resolve_article_type()
        return self._rule_based_process(text, analysis, intensity_cfg, type_cfg)

    # --------------------------------------------------------
    # 规则引擎辅助方法
    # --------------------------------------------------------

    def _inject_connectors(self, text: str, target_ratio: float) -> str:
        """根据目标连接词密度，在句子间均匀注入口语化连接词"""
        # 按句子分隔（保留分隔符）
        parts = re.split(r'([。！？；\n]+)', text)
        if len(parts) <= 2:
            return text

        # 找非空句子（长度>4）
        non_empty = [p for p in parts if len(p.strip()) > 4]
        total_slots = max(1, len(non_empty) - 1)

        # 用比例直接计算插入间隔（而非 count）
        # target_ratio: 0.15=low, 0.25=medium, 0.35=high
        # 间隔越小 → 插入越多
        if target_ratio <= 0:
            return text

        # 计算插入间隔（向下取整，确保至少 1）
        interval = max(1, int(1.0 / target_ratio))
        insert_positions = list(range(interval, total_slots * 2, interval))

        result = []
        conn_idx = 0
        for i, seg in enumerate(parts):
            if i in insert_positions and seg.strip() and len(seg) > 3:
                connector = CASUAL_CONNECTORS[conn_idx % len(CASUAL_CONNECTORS)]
                result.append(connector + "，")
                conn_idx += 1
            result.append(seg)
        return "".join(result)

    def _inject_fillers(self, text: str, ratio: float) -> str:
        """注入填充词"""
        count = int(len(text) / 50 * ratio * 5)
        for _ in range(min(count, 5)):
            filler = FILLER_WORDS[hashlib.md5(text.encode()).digest()[0] % len(FILLER_WORDS)]
            sentences = re.split(r'([。！？\n])', text)
            if len(sentences) > 2:
                pos = len(sentences) // 3
                sentences.insert(pos, "，" + filler)
                text = "".join(sentences)
        return text

    def _vary_sentence_length(self, text: str) -> str:
        """让句式长短交替，更自然"""
        sentences = re.split(r'([。！？；\n]+)', text)
        result = []
        for i, seg in enumerate(sentences):
            if seg.strip() and len(seg) > 30 and i % 4 == 0:
                # 拆分超长句
                seg = self._split_long_sentence(seg)
            result.append(seg)
        return "".join(result)

    def _split_long_sentence(self, sentence: str) -> str:
        """拆分过长的句子"""
        split_points = [",", "，", "并且", "而且", "同时"]
        for sp in split_points:
            if sp in sentence and len(sentence) > 40:
                parts = sentence.split(sp, 1)
                if len(parts[0]) > 15:
                    return parts[0] + "，" + sp.join(parts[1:])
        return sentence

    def _naturalize_patterns(self, text: str) -> str:
        """去除过度工整的AI套话（无逗号限制）"""
        # 替换"首先/其次/最后"序列（支持有/无逗号）
        text = re.sub(r'首先，?', '先说', text)
        text = re.sub(r'其次，?', '然后', text)
        text = re.sub(r'最后，?', '最后呢', text)
        # 替换"总而言之"为更口语
        text = re.sub(r'总而言之，?', '说白了', text)
        text = re.sub(r'综上所述，?', '这么来看', text)
        # 去除"值得注意的是"等套话
        text = re.sub(r'值得注意的是，?', '', text)
        # 去除"需要指出的是"等
        text = re.sub(r'需要指出的是，?', '', text)
        return text

    # --------------------------------------------------------
    # Step 5: 反问句密度控制
    # --------------------------------------------------------

    def _control_rhetorical_density(self, text: str) -> str:
        """限制反问句密度：每500字不超过N个"""
        max_per_500 = self.config.rhetorical_question_density
        word_count = len(text)
        max_allowed = int(word_count / 500 * max_per_500) + 1

        for pattern, weight in RHETORICAL_PATTERNS:
            matches = list(re.finditer(pattern, text))
            if len(matches) > max_allowed:
                # 保留前 max_allowed 个，其余替换为句号
                for m in reversed(matches[max_allowed:]):
                    text = text[:m.start()] + "。" + text[m.end():]
        return text


# ============================================================
# 便捷入口函数
# ============================================================

def humanize(text: str,
             intensity: str = "medium",
             article_type: str = "science",
             protect_terms: bool = True,
             model: str = "dashscope/qwen-max",
             api_key: str = "",
             qc_score: float = 8.0) -> str:
    """一行调用接口"""
    config = HumanizerConfig(
        intensity=intensity,
        article_type=article_type,
        protect_terms=protect_terms,
        model=model,
        api_key=api_key,
        qc_score=qc_score,
    )
    h = AIHumanizerV5(config)
    return h.humanize(text)


# ============================================================
# CLI 入口
# ============================================================

if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description="AI Humanizer CN v5.1.0")
    parser.add_argument("--input", "-i", help="输入文件")
    parser.add_argument("--output", "-o", help="输出文件")
    parser.add_argument("--intensity", default="medium",
                        choices=["low", "medium", "high", "auto"])
    parser.add_argument("--article-type", default="science",
                        choices=["tech", "science", "social", "academic"])
    parser.add_argument("--protect-terms", action="store_true", default=True)
    parser.add_argument("--model", default="dashscope/qwen-max")
    parser.add_argument("--api-key", default=os.environ.get("DASHSCOPE_API_KEY", ""))
    parser.add_argument("--text", "-t", help="直接输入文本")
    parser.add_argument("--qc-score", type=float, default=8.0)

    args = parser.parse_args()

    # 输入路径校验
    if args.input:
        input_path = Path(args.input).resolve()
        if not input_path.exists() or not input_path.is_file():
            logging.error(f"输入文件不存在或不是有效文件: {args.input}")
            exit(1)
        if not input_path.is_relative_to(Path.cwd()) and not input_path.is_relative_to(Path.home()):
            logging.error(f"输入路径不安全: {args.input}")
            exit(1)

    # 输出路径校验
    if args.output:
        output_path = Path(args.output).resolve()
        if not output_path.parent.exists():
            logging.error(f"输出目录不存在: {output_path.parent}")
            exit(1)

    # 读取输入
    if args.text:
        text = args.text
    elif args.input:
        with open(args.input, encoding="utf-8") as f:
            text = f.read()
    else:
        print("请提供 --text 或 --input")
        exit(1)

    # 处理
    config = HumanizerConfig(
        intensity=args.intensity,
        article_type=args.article_type,
        protect_terms=args.protect_terms,
        model=args.model,
        api_key=args.api_key,
        qc_score=args.qc_score,
    )
    h = AIHumanizerV5(config)
    result = h.humanize(text)

    # 输出
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"✅ 已保存到 {args.output}")
        stats = h.get_stats()
        print(f"   处理 {stats['input_len']} → {stats['output_len']} 字，耗时 {stats['elapsed_ms']}ms")
    else:
        print(result)
