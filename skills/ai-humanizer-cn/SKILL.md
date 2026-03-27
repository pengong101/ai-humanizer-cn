---
name: ai-humanizer-cn
description: 中文 AI 文本拟人化技能 - 去除 AI 痕迹，保持专业术语与数据
license: MIT
version: 5.2.0
author: pengong101
updated: 2026-03-27
metadata:
  requires:
    api_keys:
      - DASHSCOPE_API_KEY
      - OPENAI_API_KEY
      - MINIMAX_API_KEY
---

# AI Humanizer CN v5.1.0

中文 AI 文本拟人化工具。通过规则引擎或 AI 模型（通义千问 / GPT-4 / MiniMax）将 AI 生成文本转化为更自然的人类写作风格。

## v5.2.0 更新（2026-03-27）

- 🛡️ 安全修复：API key 不再通过 subprocess 泄露，改用 requests 库
- 📄 文档重构：修复版本冲突、错误导入路径、虚假性能数据
- 🧪 测试套件：新增 21 个真实测试用例，全部通过
- 🔧 API 格式更新：阿里百炼改用 chat completions 兼容模式

---

## 核心功能

- **多强度模式**：`low`（轻微口语化）/`medium`（适度）/`high`（明显）/`auto`（根据 QC 评分自动决定）
- **文章类型感知**：支持 `tech`、`science`、`social`、`academic` 四种类型，自动调整语气词密度和专业术语保护策略
- **专业内容保护**：自动识别并保护百分比数据、英文术语、引号内容、括号注释不被修改
- **反问句密度控制**：每 500 字不超过 N 个反问句（默认 3 个），避免过度使用反问
- **多模型支持**：通义千问（默认）、GPT-4、MiniMax，API 不可用时自动降级到规则引擎
- **批量处理**：`batch_process()` 支持一次性处理多段文本

## 使用方式

### Python API

```python
from ai_humanizer import humanize, AIHumanizerV5
from ai_humanizer import HumanizerConfig

# 一行调用
result = humanize(
    "这是AI生成的文本内容。",
    intensity="medium",
    article_type="science",
    protect_terms=True,
)

# 完整 API（支持批量）
config = HumanizerConfig(
    intensity="high",
    article_type="tech",
    protect_terms=True,
    rhetorical_question_density=3,
    qc_score=8.0,
    model="dashscope/qwen-max",
    api_key="",  # 或设置环境变量 DASHSCOPE_API_KEY
)
h = AIHumanizerV5(config)

single = h.humanize("输入文本")
batch = h.batch_process(["文本1", "文本2", "文本3"])

stats = h.get_stats()
# {'version': '5.1.0', 'intensity': 'high', 'article_type': 'tech', 'elapsed_ms': xxx, ...}
```

**参数说明：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `intensity` | str | `"medium"` | 口语化强度：`low`/`medium`/`high`/`auto` |
| `article_type` | str | `"science"` | 文章类型：`tech`/`science`/`social`/`academic` |
| `protect_terms` | bool | `True` | 是否保护专业术语和数据 |
| `qc_score` | float | `8.0` | 外部质量评分，`auto` 强度时使用（≥9.0 用 low，≥8.0 用 medium，否则 high）|
| `rhetorical_question_density` | int | `3` | 每 500 字允许的最大反问句数 |
| `model` | str | `"dashscope/qwen-max"` | API 模型：`dashscope/qwen-max`/`openai/gpt-4`/`minimax/abab6.5s-chat` |
| `api_key` | str | `""` | API 密钥（优先取参数，其次环境变量）|

### CLI

```bash
python humanize_v5.py --text "输入文本" --intensity medium --article-type science

# 文件输入输出
python humanize_v5.py --input article.txt --output humanized.txt --intensity high

# 指定模型
python humanize_v5.py --text "文本" --model openai/gpt-4 --api-key sk-xxx
```

**CLI 参数：**

| 参数 | 说明 |
|------|------|
| `--text`, `-t` | 直接输入待处理文本 |
| `--input`, `-i` | 输入文件路径 |
| `--output`, `-o` | 输出文件路径 |
| `--intensity` | 口语化强度：`low`/`medium`/`high`/`auto`（默认 medium）|
| `--article-type` | 文章类型：`tech`/`science`/`social`/`academic`（默认 science）|
| `--protect-terms` | 启用专业术语保护（默认开启）|
| `--model` | API 模型（默认 dashscope/qwen-max）|
| `--api-key` | API 密钥 |
| `--qc-score` | 外部 QC 评分（默认 8.0）|

### OpenClaw 技能调用

```python
from ai_humanizer import humanize

result = humanize("你的 AI 文本", intensity="medium")
```

## 配置选项

### 环境变量

| 变量 | 对应模型 |
|------|----------|
| `DASHSCOPE_API_KEY` | 通义千问（默认） |
| `OPENAI_API_KEY` | GPT-4 |
| `MINIMAX_API_KEY` | MiniMax |

### 强度配置（INTENSITY_CONFIG）

| 强度 | 口语化比例 | 连接词比例 | 填充词密度 |
|------|-----------|-----------|-----------|
| low | 8% | 15% | 3% |
| medium | 18% | 25% | 6% |
| high | 32% | 35% | 10% |

### 文章类型配置（ARTICLE_TYPE_CONFIG）

| 类型 | 语气词密度 | 术语保护 | 数据保护 | 互动句比例 |
|------|----------|---------|---------|-----------|
| tech | 5% | ✓ | ✓ | 2% |
| science | 12% | ✓ | ✓ | 5% |
| social | 25% | ✗ | ✗ | 15% |
| academic | 3% | ✓ | ✓ | 1% |

## 工作原理

处理流程：**保护 → 分析 → 处理 → 恢复**

1. **保护阶段（`_protect_content`）**：用占位符替换专业内容（百分比、英文术语、引号、括号），防止在后续处理中被修改
2. **分析阶段（`_analyze_text`）**：统计当前文本的连接词密度、填充词密度、反问句数量等指标
3. **处理阶段**：有 API key 时调用 AI 模型（通义千问/GPT-4/MiniMax），无 API 时降级到规则引擎——通过注入口语化连接词、填充词、调整句式长短、去除"首先/其次/最后"等 AI 套话
4. **密度控制（`_control_rhetorical_density`）**：限制反问句数量不超过配置阈值
5. **恢复阶段（`_restore_content`）**：将占位符还原为原始专业内容

## 性能说明

- **有 API**：处理速度取决于外部模型响应时间（通常 < 2 秒/次）
- **无 API（规则引擎降级）**：纯本地处理，毫秒级响应，保障无 API 可用时仍可工作
- 规则引擎通过注入连接词/填充词、拆分长句、替换 AI 套话来模拟人类写作特征，效果较 AI 模型有限但稳定可用

## 版本历史

- **5.1.0**（2026-03-27）：当前版本。支持 dashscope/openai/minimax 三个 API，新增 `auto` 强度模式和 `qc_score` 参数，整合反问句密度控制，完整保护机制。
