# ai-humanizer-cn v5.2.0 测试套件
import pytest
import sys
sys.path.insert(0, '..')
from humanize_v5 import AIHumanizerV5, HumanizerConfig, humanize, VERSION

class TestVersion:
    def test_version(self):
        assert VERSION == "5.2.0"

class TestHumanizerConfig:
    def test_default_config(self):
        cfg = HumanizerConfig()
        assert cfg.intensity == "medium"
        assert cfg.article_type == "science"
        assert cfg.protect_terms == True

    def test_resolve_intensity_low(self):
        cfg = HumanizerConfig(intensity="low")
        assert cfg.resolve_intensity()["口语化比例"] == 0.08

    def test_resolve_intensity_auto_high_score(self):
        cfg = HumanizerConfig(intensity="auto", qc_score=9.5)
        assert cfg.resolve_intensity()["口语化比例"] == 0.08  # >= 9.0 → low

    def test_resolve_intensity_auto_medium_score(self):
        cfg = HumanizerConfig(intensity="auto", qc_score=8.5)
        assert cfg.resolve_intensity()["口语化比例"] == 0.18  # >= 8.0 → medium

    def test_resolve_intensity_auto_low_score(self):
        cfg = HumanizerConfig(intensity="auto", qc_score=7.0)
        assert cfg.resolve_intensity()["口语化比例"] == 0.32  # < 8.0 → high

class TestArticleType:
    def test_article_type_science(self):
        cfg = HumanizerConfig(article_type="science")
        tc = cfg.resolve_article_type()
        assert tc["语气词密度"] == 0.12
        assert tc["专业术语保护"] == True

    def test_article_type_academic(self):
        cfg = HumanizerConfig(article_type="academic")
        tc = cfg.resolve_article_type()
        assert tc["语气词密度"] == 0.03  # 最少语气词

class TestProtectContent:
    def test_protect_percentage(self):
        h = AIHumanizerV5(HumanizerConfig(protect_terms=True))
        text = "增长率为 65%"
        protected, pm = h._protect_content(text)
        assert any('65%' in orig for _, orig in pm)

    def test_protect_english_term(self):
        h = AIHumanizerV5(HumanizerConfig(protect_terms=True))
        text = "Einstein 提出了相对论"
        protected, pm = h._protect_content(text)
        assert any('Einstein' in orig for _, orig in pm)

    def test_restore_content(self):
        h = AIHumanizerV5(HumanizerConfig(protect_terms=True))
        text = "增长率为 65%"
        protected, pm = h._protect_content(text)
        restored = h._restore_content(protected)
        assert '65%' in restored

    def test_protect_complex_unit(self):
        h = AIHumanizerV5(HumanizerConfig(protect_terms=True))
        text = "光速为 299792458 m/s，增长率达 65%。"
        protected, pm = h._protect_content(text)
        restored = h._restore_content(protected)
        assert '299792458 m/s' in restored
        assert '65%' in restored
        assert restored == text

class TestAnalyzeText:
    def test_analyze_basic(self):
        h = AIHumanizerV5()
        text = "这是一个测试。用于验证不同强度。人工智能正在快速发展。技术进步很快。"
        result = h._analyze_text(text)
        assert "word_count" in result
        assert result["word_count"] > 0

class TestRuleBasedProcess:
    def test_naturalize_patterns_removes_first(self):
        h = AIHumanizerV5()
        text = "首先我们需要分析。其次进行实验。最后得出结论。"
        result = h._naturalize_patterns(text)
        assert "首先" not in result

    def test_naturalize_patterns_with_comma(self):
        h = AIHumanizerV5()
        text = "首先，我们需要分析。其次，进行实验。"
        result = h._naturalize_patterns(text)
        assert "首先" not in result

    def test_split_long_sentence(self):
        h = AIHumanizerV5()
        text = "这是一个很长的句子，它包含了多个逗号分隔的内容。"
        result = h._split_long_sentence(text)
        assert len(result) >= len(text) - 3

class TestIntensityDifference:
    def test_low_vs_high_produces_different_output(self):
        """不同强度必须产生不同输出"""
        text = "自动驾驶技术正在快速发展。首先，感知算法不断进步。其次，决策系统日趋完善。最后，功能安全得到保障。人工智能已经应用于多个领域。"
        r_low = AIHumanizerV5(HumanizerConfig(intensity='low')).humanize(text)
        r_high = AIHumanizerV5(HumanizerConfig(intensity='high')).humanize(text)
        assert r_low != r_high, f"low和high输出应该不同: low={r_low} high={r_high}"

    def test_auto_high_qc_vs_low_qc(self):
        """auto强度：QC≥9 应映射到 low，QC<8 应映射到 high"""
        text = "这是一个测试。用于验证不同强度。人工智能正在快速发展。技术进步很快。"
        r_high_qc = AIHumanizerV5(HumanizerConfig(intensity='auto', qc_score=9.5)).humanize(text)
        r_low_qc = AIHumanizerV5(HumanizerConfig(intensity='auto', qc_score=7.0)).humanize(text)
        assert r_high_qc != r_low_qc, "auto模式下不同QC应产生不同强度"

class TestControlRhetoricalDensity:
    def test_rhetorical_limit(self):
        h = AIHumanizerV5(HumanizerConfig(rhetorical_question_density=2))
        text = "这是真的吗？难道不对吗？是不是这样？真的假的？不行吗？" * 20
        result = h._control_rhetorical_density(text)
        assert result.count("？") < text.count("？")

class TestHumanizeAPI:
    def test_humanize_empty_text(self):
        h = AIHumanizerV5()
        assert h.humanize("") == ""
        assert h.humanize("   ") == "   "

    def test_humanize_no_api_key(self):
        h = AIHumanizerV5(HumanizerConfig(api_key=""))
        text = "测试文本"
        result = h.humanize(text)
        assert result != ""  # 至少应该返回文本

    def test_get_stats(self):
        h = AIHumanizerV5()
        h.humanize("测试文本")
        stats = h.get_stats()
        assert stats["version"] == "5.2.0"
        assert "elapsed_ms" in stats

class TestHumanizeFunction:
    def test_humanize_function_default(self):
        result = humanize("测试文本")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_humanize_function_with_params(self):
        result = humanize("测试文本", intensity="high", article_type="social")
        assert isinstance(result, str)

class TestBatchProcess:
    def test_batch_process(self):
        h = AIHumanizerV5(HumanizerConfig(api_key=""))
        texts = ["文本1", "文本2", "文本3"]
        results = h.batch_process(texts)
        assert len(results) == 3
        assert all(isinstance(r, str) for r in results)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
