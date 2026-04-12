# 科普文章选题工作流 v1.0

**版本：** v1.0  
**日期：** 2026-04-12  
**目标：** 每日 06:00 自动搜集全网科技热点，生成 3-5 个科普文章候选标题，供 CEO 审批  
**cron：** `0 6 * * *` 北京时间  

---

## 架构

```
06:00 cron (research-agent)
    ↓
generate-topics-for-selection.py
    ↓
多引擎搜索（Google/Bing/知乎/NASA）
    ↓
topic-selection-workflow.sh（搜索执行）
    ↓
topics/YYYY-MM-DD-topics.md
    ↓
CEO 审批 → 选择主题 → 触发创作工作流
```

---

## 详细步骤

### Step 1：触发（06:00 北京时间）

**执行：** `bash /root/.openclaw/workspace/scripts/topic-selection-workflow.sh`

**搜索方向（4个主题）：**
1. 全网科普热点 — "科普 热门话题 突破 2026"
2. AI科技热点 — "AI人工智能 大模型 最新突破"
3. 太空探索热点 — "太空探索 登月 火星"
4. 生物医学热点 — "基因编辑 医学突破"

### Step 2：搜索执行

**工具：** SearXNG API (`http://172.23.0.4:8080`)

**每个方向：**
1. 发起 Google 搜索（format=json, timeout=20s）
2. 解析返回结果（title/url/published）
3. 每个方向保留 3-5 个最新热点

### Step 3：输出

**文件：** `/root/.openclaw/workspace/topics/{日期}-topics.md`

**格式：**
```markdown
# 科普文章选题 - {日期}

## 全网科普热点
- 标题: xxx | 链接: xxx | 时间: xxx
- ...

## AI科技热点
- ...

## 太空探索热点
- ...

## 生物医学热点
- ...
```

### Step 4：Git 提交

```bash
cd /root/.openclaw/workspace
git add topics/{日期}-topics.md
git commit -m "daily: 科普选题 {日期}"
```

---

## CEO 审批环节

**输出：** topics 文件路径

**CEO 动作：**
1. 读取 topics 文件
2. 选择 1 个主题（或多个）
3. 指定受众（科普小白/科技爱好者/专业研究者）
4. 触发创作工作流（spawn content-agent）

**触发格式：**
```
主题：xxx
受众：xxx
创作工作流开始
```

---

## 文件清单

| 文件 | 用途 |
|------|------|
| `scripts/topic-selection-workflow.sh` | 搜索脚本 |
| `scripts/generate-topics-for-selection.py` | Python 版选题生成（备用） |
| `topics/{日期}-topics.md` | 选题输出 |
| `skills/topic-selection-workflow/SKILL.md` | 本文档 |

---

## SEOUL.md 角色

**research-agent（小研 🔍）**

> 研究调研专家。每日 06:00 搜集全网科技热点，过滤噪音，提取真正的科普素材。
> 评估标准：新奇性（读者哇一声）/ 准确性（事实核实）/ 可图示性（能否配图）。
> 不做创作，只做选题发现和初步调研。

---

## 成功标准

- [ ] 每天 06:00 准时生成 topics 文件
- [ ] 每个方向至少 3 个候选
- [ ] CEO 每次至少有 1 个可选主题
- [ ] 选题推送到 GitHub

---

*设计：小马 🐴 | 2026-04-12 | v1.0*
