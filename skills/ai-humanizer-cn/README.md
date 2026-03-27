# AI Humanizer CN v5.1.0

将 AI 生成的中文文本转化为更自然的人类写作风格。

**MIT License**

## 安装

```bash
pip install numpy
```

仅依赖 Python 标准库 + numpy。

## 快速开始

```python
from ai_humanizer import humanize, AIHumanizerV5

# 一行调用
result = humanize("这是AI生成的文本。", intensity="medium")

# 完整 API
config = HumanizerConfig(intensity="high", article_type="tech")
h = AIHumanizerV5(config)
result = h.humanize("你的文本")

# 批量处理
results = h.batch_process(["文本1", "文本2", "文本3"])
```

## CLI 用法

```bash
python humanize_v5.py --text "文本" --intensity medium --article-type science
python humanize_v5.py --input in.txt --output out.txt --intensity high
```

## 主要特性

- **4 种强度**：`low` / `medium` / `high` / `auto`
- **4 种文章类型**：`tech` / `science` / `social` / `academic`
- **专业内容保护**：术语、数据、引用自动跳过不修改
- **多模型支持**：通义千问（默认）、GPT-4、MiniMax
- **规则引擎降级**：无 API 时仍可正常工作

## 文件结构

```
ai-humanizer-cn/
├── humanize_v5.py   # 核心实现（唯一代码文件）
├── SKILL.md         # OpenClaw 技能文档
└── README.md        # 本文件
```

## API Keys（可选）

如使用 AI 模型降重，设置以下任一环境变量：

- `DASHSCOPE_API_KEY` — 通义千问（默认）
- `OPENAI_API_KEY` — GPT-4
- `MINIMAX_API_KEY` — MiniMax

不设置则使用内置规则引擎。
