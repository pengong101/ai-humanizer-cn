


# 科普文章工作流 v3.0 详细落地计划

**版本：** v1.0  
**日期：** 2026-04-07  
**目标：** 将 paper 阶段 v3.0 工作流落地为可执行系统  
**状态：** 规划中，待 CEO 审批后实施

---

## 一、选题流程（Phase 0）

### 1.1 现有基础
- 脚本：`/root/.openclaw/workspace/scripts/generate-topics-for-selection.py`
- 输出：`articles/topics-for-selection.json` + `articles/topics-for-selection.md`
- Cron：每天 06:00 北京时间（已有）

### 1.2 需补充的改进

**问题：** 当前脚本只有英文搜索（science breakthrough 2026），中文热点覆盖不足

**改进方案 A（推荐）：多语言+多源**
```python
SEARCH_QUERIES = [
    # 英文源（国际前沿）
    "science breakthrough 2026 latest",
    "NASA discoveries 2026",
    "AI artificial intelligence 2026 news",
    # 中文源（国内热点）
    "科技 新闻 2026 最新 突破",
    "人工智能 大模型 2026",
    "航天 最新消息 2026",
    # 趋势捕捉
    "trend topic science 2026 viral",
]

ENGINES = ["bing", "baidu", "sogou"]  # 平衡国内外
```

**改进方案 B：加入 arXiv RSS + NASA News API**
```python
# 学术前沿
ARXIV_RSS = "https://export.arxiv.org/api/query?search_query=all:main&start=0&max_results=30"

# NASA 官方新闻
NASA_NEWS_API = "https://www.nasa.gov/api/v2/news releases/all"

# 知乎热榜
ZHIHU_HOT = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=10"
```

### 1.3 选题质量标准

每个候选标题必须满足：
```
✓ 具体主题（不是泛泛的"AI发展"）
✓ 有视觉元素（适合配图）
✓ 有独特角度（不是重复已知内容）
✓ 受众覆盖面广
✓ 搜索结果中有足够参考资料
```

### 1.4 选题输出格式（改进版）

```markdown
# 科普文章选题候选

生成时间：2026-04-07 06:00

## 1. 【天文】韦伯望远镜发现最古老的黑洞：它不该存在？

- 关键词：James Webb, 黑洞, 早期宇宙
- 来源：NASA News + arXiv
- 搜索结果：42 条相关结果
- 配图可行性：⭐⭐⭐⭐⭐（NASA 官方图丰富）
- 角度亮点：挑战现有宇宙形成理论
- 难度：中高（需要理解黑洞形成机制）
- **建议优先** ✅

## 2. 【生物】GLP-1 减肥药的新战场：不只减肥，还在改变大脑

- 关键词：GLP-1, Ozempic, 脑科学
- 来源：Baidu News + PubMed
- 搜索结果：28 条
- 配图可行性：⭐⭐⭐⭐（医学图解）
- 角度亮点：减肥之外的神经保护作用
- 难度：中（数据较多，容易整理）
- 候选

## 3. 【科技】DeepSeek-V4 发布：开源模型追上 GPT-5 了吗？

- 关键词：DeepSeek, 开源大模型, AI
- 来源：知乎热榜 + Bing
- 搜索结果：35 条
- 配图可行性：⭐⭐⭐（需要自行制图）
- 角度亮点：中美 AI 竞争视角
- 难度：低（资料丰富）
- 候选

---
请回复 **序号** 选择今日主题，例如：`1`
```

### 1.5 选题 Cron 流程

```
06:00  执行 generate-topics-for-selection.py（改进版）
         ↓
06:05  输出 topics-for-selection.md（3个候选，含质量评分）
         ↓
06:05  飞书通知 CEO + 人工审批（回复序号）
         ↓
06:10  CEO 审批 → 确定主题 → 触发 Phase 1
```

---

## 二、调研流程（Phase 1）

### 2.1 执行者
- **research-agent** 独立执行
- 无需 content-agent 介入

### 2.2 调研任务模板

```
任务：深度调研「{主题}」

输出文件：/root/.openclaw/workspace/research/{topic}-{date}.md

调研要求：
1. 多语言搜索（中文 + 英文）
   - 英文：NASA/EHT/ESO/arXiv/Wikipedia
   - 中文：知乎/百度百科/公众号搜索
   
2. 必须包含：
   - 核心事实清单（带来源链接 + 时间）
   - 专业术语解释（带参考文献）
   - 关键数据（带来源 + 具体数值）
   - 争议/未知（标注不确定性）
   - 配图资源清单（官方图片 URL + 版权说明）

3. 禁止：
   - 未经搜索写数据
   - 使用"权威来源"标注无来源信息
   - 遗漏重要争议点

4. 输出格式：
   ## 核心事实
   ## 专业术语（术语：解释 @来源）
   ## 关键数据（数据：数值 @来源）
   ## 争议与未知
   ## 配图资源（URL + 版权）
   ## 可写性评估（难度/亮点/风险）
```

### 2.3 调研质量门槛

| 指标 | 最低要求 | 达标则进入 Phase 2 |
|------|---------|-------------------|
| 核心事实 | ≥5 条 | ✅ |
| 术语解释 | ≥3 个 | ✅ |
| 关键数据 | ≥2 个（含具体数值） | ✅ |
| 配图资源 | ≥3 个可用 URL | ✅ |
| **完整度** | **≥80%** | **✅ 进入写作** |

完整度 < 80% → 研究报告 CEO，等待补充资料

### 2.4 调研输出文件模板

```markdown
# {主题} 调研报告

**日期：** 2026-04-07  
**调研员：** research-agent  
**完整度：** 85% ✅

---

## 核心事实

1. **事实 1** @NASA 官方新闻 2026-04-01
   - 链接：https://...
   
2. **事实 2** @arXiv:2026.12345
   - 链接：https://arxiv.org/...

---

## 专业术语

| 术语 | 解释 | 来源 |
|------|------|------|
| 黑洞 | ... | Wikipedia |
| 事件视界 | ... | NASA |

---

## 关键数据

| 数据 | 数值 | 来源 |
|------|------|------|
| 黑洞质量 | 太阳的 170 亿倍 | NASA 2026-04-01 |
| 距离地球 | 5.5 亿光年 | ESO |

---

## 争议与未知

⚠️ **争议**：早期宇宙为何能形成如此巨大的黑洞？现有理论无法解释

⚠️ **未知**：该黑洞的具体形成时间尚未确定

---

## 配图资源

| 图片主题 | URL | 版权 | 备注 |
|----------|-----|------|------|
| M87 黑洞照片 | https://eventhorizontelescope.org/images | CC BY 4.0 | 官方高清 |
| 韦伯望远镜 | https://jwst.nasa.gov/images | NASA Public Domain | 官方图 |

---

## 可写性评估

- **难度：** 中（需要理解黑洞形成机制）
- **亮点：** 挑战现有宇宙理论，读者兴趣高
- **风险：** 专业术语多，需简化解释
- **配图：** NASA/EHT 官方图丰富 ✅

---

**结论：** 建议进入写作阶段 ✅
```

---

## 三、写作流程（Phase 2a）

### 3.1 执行者
- **content-agent** 执行
- 所需输入：调研报告文件路径

### 3.2 写作任务模板

```
任务：根据调研报告撰写科普文章

调研文件：/root/.openclaw/workspace/research/{topic}-{date}.md
输出文件：/root/.openclaw/workspace/articles/science-{topic}-{date}.md

写作要求：

1. 文章结构（公众号格式）
   - 标题（吸引人 + 含关键词）
   - 摘要（3句话，100字）
   - 引言（热点切入，200字）
   - 正文（3-4节，每节 400-500 字）
   - 结语（总结 + 展望，100字）

2. 写作标准
   - 禁止：首先/其次/最后/综上所述
   - 禁止：AI 套话（"随着时代发展..."）
   - 必须：具体数据（带来源）
   - 必须：术语解释（括号内或脚注）
   - 必须：读者视角（"你可能不知道..."）

3. 图片方案（必须同时输出）
   每篇文章需以下图片：
   
   a) 封面图（1张）
      - 需求描述：{一句话描述}
      - 生成方式：MiniMax image-01 自主生成
      - 质量要求：≥8/10，多轮优化最多 3 轮
   
   b) 内容配图（2-3张）
      - 每张需标注：
        - 位置：{文章第 X 节}
        - 主题：{图片内容描述}
        - 类型：概念图/数据图/人物图
        - 来源：优先官方 URL（如 NASA），无官方则生成
        - alt文字：{供视障人士阅读的描述}
   
   c) 版权信息（每张图必须）
      - 来源：{URL 或 "自主生成"}
      - 版权：{CC BY 4.0 / Public Domain / 自主生成}
      - 引用格式：{按公众号规范格式}

4. 平台适配
   - 公众号格式：mdnice 样式
   - 标题层级：h1 > h2 > h3
   - 段落长度：3-5 行

5. 自检清单（提交前必须全部通过）
   - [ ] 无套话序列
   - [ ] 所有数据有来源
   - [ ] 所有术语有解释
   - [ ] 字数 1500-3000
   - [ ] 图片方案完整（封面 + 2-3 配图）
   - [ ] 版权信息完整
```

### 3.3 写作输出格式

```markdown
---
title: 韦伯望远镜发现最古老的黑洞：它不该存在？
date: 2026-04-07
cover_image: /workspace/articles/images/cover-{topic}.jpg
images:
  - position: 第1节
    theme: 黑洞示意图
    type: 概念图
    source: https://eventhorizontelescope.org
    alt: "橙色圆环包围的黑色圆盘，即黑洞事件视界"
  - position: 第2节
    theme: 韦伯望远镜
    type: 实物图
    source: NASA (Public Domain)
    alt: "詹姆斯·韦伯太空望远镜在太空中的艺术图"
---

# 韦伯望远镜发现最古老的黑洞：它不该存在？

**摘要：** ...

## 引言：你可能不知道的黑洞秘密

...

## 第一章：什么是黑洞？

...

## 第二章：韦伯的新发现

...

## 第三章：为什么它不该存在？

...

## 结语

...

---

## 图片版权说明

| 图片 | 来源 | 版权 |
|------|------|------|
| 封面 | 自主生成 | - |
| 图1 | EHT Collaboration | CC BY 4.0 |
| 图2 | NASA | Public Domain |
```

---

## 四、配图流程（Phase 2b）

### 4.1 执行者
- **research-agent**：官方图片搜索
- **content-agent**：生成 + 验证

### 4.2 配图完整工作流

```
content-agent 完成初稿 + 图片方案
           ↓
research-agent 并行执行：官方图片搜索
           ↓
content-agent 执行：封面图生成 + 内容配图生成
           ↓
两路汇合：图片 + 文章 → review-agent
```

### 4.3 官方图片搜索（research-agent）

**搜索优先级：**
```
⭐⭐⭐⭐⭐ 官方科学机构（Public Domain / CC BY）
  - ESA Hubble: https://esahubble.org/images/
  - ESO: https://www.eso.org/public/images/
  - NASA: https://www.nasa.gov/image-gallery/
  - EHT: https://eventhorizontelescope.org/
  - STScI: https://www.stsci.edu/

⭐⭐⭐⭐ 科研数据库
  - NASA Exoplanet Archive
  - ADS Abstract Service
  - arXiv

⭐⭐⭐ 免费图库（科学主题）
  - Wikimedia Commons
  - Unsplash Science
```

**NASA API 调用：**
```python
import requests

def search_nasa_images(query, page_size=10):
    url = f"https://images-api.nasa.gov/search"
    params = {
        "q": query,
        "media_type": "image",
        "page_size": page_size,
        "year_start": "2020"  # 优先新图
    }
    r = requests.get(url, timeout=10)
    data = r.json()
    return [{
        "title": item["data"][0]["title"],
        "url": next(l["href"] for l in item["links"] if l["rel"] == "preview"),
        "full_url": next(l["href"] for l in item["links"] if l["rel"] == "original"),
        "nasa_id": item["data"][0]["nasa_id"],
        "keywords": item["data"][0].get("keywords", [])
    } for item in data["collection"]["items"]]
```

**图片下载验证流程：**
```
搜索到图片 URL
    ↓
验证 URL 可访问（HEAD 请求）
    ↓
下载到本地（/workspace/articles/images/）
    ↓
基础检查：文件大小 > 10KB
    ↓
多模态验证（qwen3.5-plus）：
  识别内容是否匹配预期
  → 匹配度 ≥7 分 ✅ 保存
  → 匹配度 <7 分 ❌ 换备选 URL
    ↓
最多重试 3 次
    ↓
仍失败 → 标记人工审核 ⚠️
```

### 4.4 封面图生成（content-agent）

**封面图生成标准：**
```
模型：MiniMax image-01
尺寸：4K (3840×2160)
风格：科技感 / 艺术感（不能太写实）

生成 Prompt 模板：
"科普文章封面图：{主题描述}，宏大视角，科幻风格，高清，4K"

示例：
"科普文章封面图：一个巨大的黑色圆盘被橙色发光环包围，
  背景是星空，宏大视角，科幻风格，高清，4K"
```

**多轮优化流程：**
```
第1轮生成
    ↓
多模态验证（MiniMax-M2.7）
    ↓
评分：
  - 匹配度 ≥8 ✅ → 保存
  - 匹配度 6-7 → 生成变体（最多2次）
  - 匹配度 <6 → 重新生成（最多2次）
    ↓
3轮后仍不达标 → 标记人工审核 ⚠️
```

**封面图验证 Prompt：**
```
请识别这张封面图的内容：
1. 图片展示的主要元素是什么？
2. 图片风格是写实/艺术/示意图？
3. 是否适合作为科普文章封面？
4. 与主题"黑洞"的相关度？

输出：
- 匹配度评分：0-10 分
- 质量评分：0-10 分
- 建议：通过/重新生成/变体
```

### 4.5 内容配图生成（content-agent）

**生成优先级：**
```
1. 官方图片（NASA/EHT/ESO）→ 下载验证 → 通过则用
2. 无官方图 → MiniMax image-01 生成 → 验证 ≥7
3. 生成失败 → 文字图解（CSS/SVG 方式代替）
```

**生成 Prompt 模板：**
```
"科普内容配图：{具体描述}，简洁清晰，高清，适合文章内页，16:9横图"
```

### 4.6 图片格式整理

**公众号图片要求：**
| 类型 | 尺寸 | 格式 | 文件大小 |
|------|------|------|----------|
| 封面图 | 900×500 px | JPG/PNG | < 2MB |
| 内容配图 | 宽度 ≤ 900px（自适应） | JPG/PNG | < 500KB |
| 长图 | 宽度 600-800px | JPG/PNG | < 1MB |

**文件命名规范：**
```
cover-{topic}-{date}.jpg      # 封面
img-{n}-{topic}-{date}.jpg   # 内容配图（n=1,2,3...）
```

**格式自动处理脚本：**
```python
from PIL import Image
import os

def optimize_image(input_path, output_path, max_width=900, quality=85):
    """压缩 + 调整尺寸到公众号要求"""
    img = Image.open(input_path)
    
    # 保持比例，调整宽度
    if img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)
    
    # 转为 RGB（处理 PNG 透明通道）
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    
    img.save(output_path, 'JPEG', quality=quality, optimize=True)
    return os.path.getsize(output_path)
```

---

## 五、合规引用流程

### 5.1 图片版权分层

| 来源 | 版权要求 | 引用格式 |
|------|---------|---------|
| NASA | Public Domain | `来源：NASA，公共领域` |
| ESA | CC BY 4.0 | `来源：ESA/Hubble，CC BY 4.0` |
| EHT | CC BY 4.0 | `来源：EHT Collaboration，CC BY 4.0` |
| ESO | CC BY 4.0 | `来源：ESO，CC BY 4.0` |
| Wikimedia | 需查看具体 | `来源：Wikimedia Commons/[作者]` |
| 自主生成 | 无 | `来源：自主生成` |

### 5.2 公众号图片版权模板

文章末尾必须包含：

```markdown
---

## 图片来源

| 序号 | 图片内容 | 来源 | 版权 |
|------|---------|------|------|
| 图1 | M87 黑洞照片 | Event Horizon Telescope | CC BY 4.0 |
| 图2 | 韦伯望远镜 | NASA | Public Domain |
| 图3 | 艺术概念图 | 自主生成 | - |

**声明：**
- 除自主生成图片外，其余图片均遵循相应开源协议
- 如有版权争议，请联系删除
```

### 5.3 数据来源引用

**文内引用格式：**
```
根据 NASA 2026年4月1日的官方新闻[X]，该黑洞的质量约为...
（文末参考文献）
```

**文末参考文献格式：**
```markdown
## 参考文献

1. NASA. "James Webb Telescope Discovers Oldest Black Hole." NASA News, 2026-04-01. https://...
2. Event Horizon Telescope Collaboration. "M87 Image Release." 2019. https://...
3. Smith et al. "Early Universe Black Hole Formation." arXiv:2026.12345. https://...
```

---

## 六、微信公众号发布流程

### 6.1 现有工具
- 脚本：`/root/.openclaw/workspace/scripts/wechat_publisher.py`
- 依赖：Playwright + Chromium
- 登录：二维码扫码一次，cookies 持久化

### 6.2 发布前准备清单

| 检查项 | 要求 | 执行者 |
|--------|------|--------|
| 标题 | 含关键词 + 吸引力 | content-agent |
| 封面图 | 900×500 px, < 2MB | content-agent |
| 正文 HTML | mdnice 格式 | content-agent |
| 图片 | 全部压缩 ≤ 900px 宽 | content-agent |
| 版权声明 | 文章末尾 | content-agent |
| 摘要 | 公众号副标题 | content-agent |
| 标签 | 3-5 个 | content-agent |

### 6.3 公众号上传流程

```python
# 使用 wechat_publisher.py
from wechat_publisher import WeChatPublisher

publisher = WeChatPublisher(
    cookies_path="/root/.openclaw/workspace/data/wechat_cookies.json",
    proxy="http://172.17.0.1:7890"  # mihomo 代理
)

# 检查 cookies 是否有效
if not publisher.check_login():
    print("⚠️ 需要重新扫码登录")
    publisher.login()  # 会打开浏览器，等待扫码

# 上传草稿
result = publisher.upload_draft(
    title="文章标题",
    content="<h1>正文标题</h1><p>段落...</p>",
    cover_image="/workspace/articles/images/cover.jpg",
    summary="摘要（可选，会自动从正文提取）"
)

print(f"✅ 草稿链接：{result.get('url')}")
```

### 6.4 异常处理

| 异常 | 处理方式 | 汇报 |
|------|---------|------|
| cookies 失效 | 通知 CEO 重新扫码 | 飞书 |
| 上传失败 | 重试 2 次 | 飞书 |
| 图片过大 | 自动压缩 | 日志 |
| 标题重复 | 警告 CEO | 飞书 |

---

## 七、质量审核流程（Phase 3）

### 7.1 审核执行者
- **review-agent** 独立执行

### 7.2 四维评分标准（重要更新）

| 维度 | 权重 | **底线** | 评分说明 |
|------|------|----------|---------|
| **隐私安全** | 30% | **≥9** | 无政治/隐私/安全内容；数据来源可靠 |
| **文本质量** | 30% | ≥7 | 流畅度/逻辑性/无AI套话/术语准确 |
| **图片质量** | 20% | ≥7 | 相关性/版权合规/清晰度 |
| **格式正确** | 20% | ≥7 | 字数/标题层级/平台规范 |

**关键更新：隐私安全底线 ≥9**（原标准是 ≥7）

### 7.3 隐私安全审核详细清单

```markdown
## 隐私安全审核（必须逐项检查）

### 政治敏感性
- [ ] 不涉及中国政治人物、领土主权争议
- [ ] 不涉及国际敏感政治话题
- [ ] 不涉及宗教、种族歧视

### 隐私保护
- [ ] 不泄露个人隐私信息
- [ ] 不使用未经授权的照片
- [ ] 不引用未经授权的数据

### 内容安全
- [ ] 不含虚假信息
- [ ] 不含夸大/误导性内容
- [ ] 不含医疗/金融虚假建议

### 来源可靠性
- [ ] 所有数据有可查来源
- [ ] 来源非谣言/假新闻
- [ ] 关键数据经过核实

### 评分标准
- 9-10 分：完全合规，无任何问题
- 7-8 分：有个小问题（如缺一个来源标注），但不严重
- 5-6 分：有明显问题，需要修改
- <5 分：有严重问题，必须重写
```

### 7.4 审核报告模板

```markdown
# QC 审核报告

**文章：** {主题}
**审核时间：** {datetime}
**审核员：** review-agent

---

## 四维评分

| 维度 | 得分 | 底线 | 状态 |
|------|------|------|------|
| 隐私安全 | **9**/10 | **≥9** | ✅ |
| 文本质量 | 8/10 | ≥7 | ✅ |
| 图片质量 | 8/10 | ≥7 | ✅ |
| 格式正确 | 8/10 | ≥7 | ✅ |
| **总分** | **33**/40 | ≥28 | ✅ |

---

## 详细问题列表

### 隐私安全
- ✅ 无政治敏感内容
- ✅ 无个人隐私泄露
- ✅ 数据来源可靠

### 文本质量
- ✅ 流畅度良好
- ⚠️ 第2节有一个"首先...其次...最后"套话 → 建议删除

### 图片质量
- ✅ 版权信息完整
- ✅ 清晰度符合要求

### 格式正确
- ✅ 字数 2100（符合 1500-3000 要求）
- ✅ 标题层级清晰

---

## 最终判定

✅ **通过** → 推送 CEO 发布

---
*review-agent | 2026-04-07*
```

### 7.5 判定规则

```
通过：全部维度 ≥ 底线 且 隐私安全 ≥ 9
返工：任一维度 < 底线，或 隐私安全 < 9，但综合 ≥ 6
拒绝：综合 < 6，或 隐私安全 < 7
```

---

## 八、Cron 定时任务设计

### 8.1 每日定时任务表

| 时间 | 任务 | 执行者 | 触发方式 |
|------|------|--------|---------|
| 06:00 | 选题生成 | 自动脚本 | cron |
| 06:05 | 飞书通知 CEO 审批 | 自动脚本 | 紧接选题 |
| **CEO 审批后** | Phase 1 调研 | research-agent | sessions_spawn |
| **调研完成后** | Phase 2a 写作 | content-agent | sessions_spawn |
| **写作完成后** | Phase 2b 图片 | research + content | 并行 sessions_spawn |
| **图片完成后** | Phase 3 审核 | review-agent | sessions_spawn |
| **审核通过后** | Phase 4 发布 | CEO/人工 | 手动/自动 |

### 8.2 自动化触发脚本（可选）

```python
#!/usr/bin/env python3
"""
文章工作流自动触发脚本
由 cron 每天 06:00 触发，生成选题后通知 CEO
CEO 回复后自动执行后续 Phase
"""

import sys
import json
from datetime import datetime

# 用法：
# python3 article_workflow_trigger.py <phase> <topic>
# phase: research | content | review | publish

PHASE_AGENTS = {
    "research": {
        "agent": "research-agent",
        "task_template": "调研主题：{topic}\n调研输出：/workspace/research/{topic}-{date}.md\n详见 SKILL.md"
    },
    "content": {
        "agent": "content-agent",
        "task_template": "写作主题：{topic}\n调研文件：/workspace/research/{topic}-{date}.md\n详见 SKILL.md"
    },
    "review": {
        "agent": "review-agent",
        "task_template": "审核文章：/workspace/articles/science-{topic}-{date}.md\n详见 SKILL.md"
    }
}

def trigger_phase(phase, topic):
    config = PHASE_AGENTS[phase]
    date = datetime.now().strftime("%Y-%m-%d")
    task = config["task_template"].format(topic=topic, date=date)
    
    # 使用 sessions_spawn 触发
    # （实际调用 openclaw sessions spawn）
    print(f"Triggering {phase} for topic: {topic}")
    print(f"Task: {task}")
    
    return {"phase": phase, "topic": topic, "status": "triggered"}

if __name__ == "__main__":
    phase = sys.argv[1]
    topic = sys.argv[2] if len(sys.argv) > 2 else ""
    result = trigger_phase(phase, topic)
    print(json.dumps(result))
```

### 8.3 飞书通知模板

**选题生成后通知 CEO：**
```
📚 科普文章选题候选已生成

主题候选：
1. 【天文】韦伯望远镜发现最古老的黑洞...
2. 【生物】GLP-1 减肥药的新战场...
3. 【科技】DeepSeek-V4 发布...

请回复 **序号** 选择今日主题，例如：`1`

（回复后自动开始调研）
```

**Phase 完成通知 CEO：**
```
✅ 调研完成：韦伯望远镜发现最古老的黑洞

核心发现：
- 该黑洞质量为太阳的 170 亿倍
- 形成于宇宙大爆炸后 5.7 亿年
- 挑战现有黑洞形成理论

配图资源：NASA 官方图 5 张，EHT 1 张

→ 等待 CEO 确认后开始写作
```

---

## 九、所需脚本/技能清单

| 序号 | 名称 | 位置 | 状态 |
|------|------|------|------|
| 1 | generate-topics-for-selection.py | scripts/ | ✅ 已有，需改进 |
| 2 | science-article-writer SKILL | skills/ | ✅ 已有 |
| 3 | ai-humanizer-cn | skills/ | ✅ 已有 |
| 4 | wechat_publisher.py | scripts/ | ✅ 已有 |
| 5 | image-optimize.py | scripts/ | ❌ 待创建 |
| 6 | article-workflow-trigger.py | scripts/ | ❌ 待创建 |
| 7 | content-agent SOUL.md | workspaces/content/ | ✅ 已有 |
| 8 | review-agent SOUL.md | workspaces/review/ | ⚠️ 需更新（隐私≥9） |

---

## 十、落地优先级

### P0（必须先做）
1. ✅ 选题脚本改进（多语言 + 中文热点）
2. ✅ review-agent SOUL.md 更新（隐私安全底线 ≥9）
3. ✅ 图片优化脚本（image-optimize.py）

### P1（发布前必须完成）
4. 写作 SKILL 补充图片方案输出格式
5. 配图合规引用模板固化
6. 飞书通知模板

### P2（可选优化）
7. article-workflow-trigger.py 半自动化
8. 小红书/知乎 多平台发布

---

## 十一、风险与对策

| 风险 | 概率 | 影响 | 对策 |
|------|------|------|------|
| 选题质量差 | 中 | 高 | CEO 严格审批，低于 80% 完整度不进写作 |
| 官方图片不足 | 低 | 中 | 提前准备 DALL-E 生成兜底 |
| review-agent 误判隐私 | 低 | 高 | review SOUL.md 明确底线，人工抽检 |
| 微信登录失效 | 中 | 高 | cookies 定期检查 + 备用方案 |
| 图片版权纠纷 | 低 | 高 | 仅用 NASA/ESA/EHT/CC0 图片，自主生成封面 |

---

## 十二、完整流程图

```
06:00 选题生成（自动脚本）
         ↓ topics-for-selection.md
06:05 飞书通知 CEO 审批
         ↓ CEO 回复序号
06:10 触发 Phase 1

Phase 1: research-agent 调研
         ↓ research/{topic}-{date}.md
    CEO 确认完整度 ≥80%

Phase 2a: content-agent 写作
         ↓ articles/science-{topic}-{date}.md
    + 图片方案（含来源标注）

Phase 2b: research+content 并行
    research: 官方图片搜索下载
    content: 封面图生成 + 内容配图生成
         ↓ 图片全部到位

Phase 3: review-agent 审核
         ↓ 四维评分
    隐私安全 ≥9，其他 ≥7
         ↓ 通过

Phase 4: CEO 发布
    content-agent 调用 wechat_publisher.py
         ↓ 草稿链接
    飞书通知用户
```

---

*设计：小马 🐴 | 2026-04-07 | v1.0*
