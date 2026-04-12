# 科普文章创作与发布工作流 v1.0

**版本：** v1.0  
**日期：** 2026-04-12  
**前置工作流：** topic-selection-workflow（选题） → 本工作流  
**触发方式：** CEO 审批选题后 spawn agents  

---

## 架构

```
CEO 审批选题
    ↓
Phase 1: 调研 (research-agent)
    ↓ 调研摘要
Phase 2: 写作 (content-agent)
    ↓ 初稿 + 图片方案
Phase 3: 图片 (research-agent 并行)
    ↓ 图片文件
Phase 4: 审核 (review-agent)
    ↓ QC报告
Phase 5: 发布 (CEO)
    ↓ 公众号草稿
```

---

## Phase 1: 调研 (research-agent)

**触发：** CEO 选择主题并 spawn research-agent

**输入：**
```
主题：xxx
受众：xxx（科普小白/科技爱好者/专业研究者）
```

**任务：**
```
1. 多引擎搜索
   - SearXNG (Google/Bing/Baidu)
   - NASA news + arXiv
   - 每主题 3+ 来源

2. 资料整理
   - 核心事实（时间/人物/数据）
   - 专业术语解释
   - 争议点/未解决问题
   - 配图资源推荐

3. 输出：调研摘要
   - 格式：[事实] / [术语] / [数据] / [争议]
   - 图片资源：[官方图片URL列表]
```

**输出：** `/workspace/research/{主题}-{日期}.md`

**汇报给 CEO：** 调研完成 + 核心发现 + 可写性评估

---

## Phase 2: 写作 (content-agent)

**触发：** CEO 确认调研后 spawn content-agent

**输入：**
```
主题：xxx
受众：xxx
调研：/workspace/research/{主题}-{日期}.md
字数：1500-3000
```

**任务：**
```
1. 撰写初稿
   - 结构：摘要 → 引言 → 正文(3-4节) → 结语
   - 每节 300-500 字
   - 禁止套话：首先/其次/综上所述

2. 设计图片方案
   - 封面图 x1
   - 内容配图 x2-3
   - 标注：位置 / 主题 / 类型(封面/概念/数据/人物)

3. 拟人化（ai-humanizer-cn）
   - intensity: medium
   - 保护：专业术语 + 数据

4. 平台适配（公众号 mdnice 格式）
```

**输出：** `/workspace/articles/{science}-{主题}-{日期}.md`

**汇报给 CEO：** 初稿完成 + 图片方案 + 自检报告

---

## Phase 2b: 图片生产 (research-agent 并行)

**触发：** CEO 确认初稿后，与 content-agent 并行执行

**工具：** MiniMax CLI（`mmx`）

**research-agent 负责：官方图片搜索**
```
1. NASA API → 下载官方图片
2. Bing Images → 验证版权
3. 输出：可用图片URL列表 + 本地路径
```

**content-agent 负责：图片生成（mmx CLI）**
```bash
# 封面图（16:9）
mmx image "科普封面：黑洞概念图，星空背景，紫色光晕" \
  --aspect-ratio 16:9 \
  --out-dir /workspace/articles/images/

# 配图（4:3）
mmx image "太阳系行星示意图，简洁科普风格" \
  --aspect-ratio 4:3 \
  --out-dir /workspace/articles/images/

# 批量变体（最多3轮，每轮选最优）
mmx image "描述" --n 3 --out-dir /workspace/articles/images/
```

**验证标准：**
| 图片类型 | 阈值 | 优化次数 |
|---------|------|---------|
| 封面图 | ≥8/10 | 最多3轮 |
| 内容配图 | ≥7/10 | 最多3次搜索 |

**输出路径：** `/root/.openclaw/workspace/articles/images/{主题}-{类型}-{序号}.jpg`

---

## Phase 3: 审核 (review-agent)

**触发：** CEO 收到图片完成后 spawn review-agent

**审核内容：**
```
1. 合规安全 ≥9（底线）
2. 文本质量 ≥7
3. 图片质量 ≥7
4. 格式正确 ≥7
```

**判定：**
- ✅ **通过** → CEO 发布
- 🔄 **返工** → 返回 content-agent 修改（最多2轮）
- ❌ **拒绝** → CEO 重新选题

---

## Phase 4: 发布 (CEO)

**触发：** review 通过后

**发布选项：**
| 平台 | 自动化 | 说明 |
|------|--------|------|
| 微信公众号 | ✅ wechat_publisher.py | 草稿上传，需cookie |
| 微信公众号+音频 | ✅ mmx speech | 同步音频版本 |
| 小红书 | ❌ 待开发 | 需API |
| 知乎 | ❌ 待开发 | 需API |

**发布流程（公众号）：**
1. CEO 读取 `/workspace/articles/{science}-{主题}-{日期}.md`
2. 复制到公众号后台
3. 上传封面图
4. 可选：生成音频版

**音频版生成（mmx CLI）：**
```bash
# 文章摘要语音（公众号音频消息）
mmx speech synthesize \
  --text "今天我们来聊聊黑洞..." \
  --voice Chinese_male_mixed_voiced \
  --speed 1.0 \
  --out /workspace/articles/audio/{日期}-summary.mp3

# 查看所有音色
mmx speech voices
```

---

## Agent 角色

### research-agent（小研 🔍）
> 研究调研专家。负责选题调研和图片资源搜集。评估标准：新奇性/准确性/可图示性。

### content-agent（小文 ✍️）
> 内容创作专家。负责初稿撰写、拟人化处理、图片生成。写作标准：禁止套话/AI痕迹/事实错误。

### review-agent（小审 🔎）
> 质量审核专家。负责四维评分。底线：合规安全≥9，任意维度<7绝不发布。

---

## 文件清单

| 文件 | 用途 |
|------|------|
| `research/{主题}-{日期}.md` | 调研摘要 |
| `articles/{science}-{主题}-{日期}.md` | 文章初稿 |
| `articles/qc-report-{日期}.md` | QC审核报告 |
| `skills/article-publishing-workflow/SKILL.md` | 本文档 |

---

## 工作流触发状态机

```
选题(cron)
    ↓
topics/YYYY-MM-DD-topics.md
    ↓ CEO审批
[选主题] → Phase1(调研)
    ↓ CEO确认
Phase2(写作) ←→ Phase2b(图片) [并行]
    ↓ CEO确认
Phase3(审核)
    ↓ CEO决定
Phase4(发布) / 返工 / 拒绝
```

---

*设计：小马 🐴 | 2026-04-12 | v1.0*
