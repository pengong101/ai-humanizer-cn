# MiniMax CLI 集成技能 v1.0

**版本：** v1.0  
**日期：** 2026-04-12  
**用途：** 为 content-agent 和 research-agent 提供 MiniMax CLI 能力  

---

## 安装状态

✅ 已安装：`mmx-cli v1.x`
✅ 认证状态：`~/.mmx/config.json`（API key 已配置）
✅ 配额充足：MiniMax-M2.7 24/1500, image-01 14/350

---

## 核心能力

| 能力 | 命令 | 内容-agent 用途 |
|------|------|----------------|
| **图片生成** | `mmx image "描述" --n 3 --aspect-ratio 16:9` | 封面图/配图 |
| **语音合成** | `mmx speech synthesize --text "文本" --out xxx.mp3` | 文章音频版（新增）|
| **搜索** | `mmx search "关键词"` | 实时搜索核实 |
| **视频生成** | `mmx video generate --prompt "描述"` | 文章配视频（新增）|
| **音乐生成** | `mmx music generate --prompt "描述"` | 背景音乐（新增）|

---

## 使用规范

### 图片生成（content-agent 优先使用）

```bash
# 封面图（16:9，4K质量）
mmx image "科普文章封面：黑洞概念图，星空背景，紫色光晕" --aspect-ratio 16:9 --out-dir /workspace/articles/images/

# 配图（9:16 或 1:1）
mmx image "太阳系行星示意图，简洁科普风格" --aspect-ratio 4:3 --out-dir /workspace/articles/images/

# 批量生成
mmx image "火星表面图" --n 3 --out-dir /workspace/articles/images/
```

**输出路径：** `/root/.openclaw/workspace/articles/images/`
**命名规范：** `{主题}-{类型}-{序号}.jpg`

### 语音合成（新增能力）

```bash
# 文章摘要语音（用于公众号音频）
mmx speech synthesize \
  --text "今天我们来聊聊..." \
  --voice Chinese_male_mixed_voiced \
  --speed 1.0 \
  --out /workspace/articles/audio/{日期}-summary.mp3

# 查看可用音色
mmx speech voices
```

### 搜索核实（research-agent/content-agent）

```bash
# 快速搜索
mmx search "黑洞最新发现 2026"

# 输出 JSON
mmx search "量子计算突破" --output json
```

---

## 工作流集成

### article-publishing-workflow 改造

**旧方式（API）：**
```python
requests.post("https://api.minimaxi.com/v1/images/generations",
  headers={"Authorization": f"Bearer {api_key}"},
  json={"model":"image-01", "prompt": "...", ...})
```

**新方式（mmx CLI）：**
```bash
mmx image "描述" --out /workspace/articles/images/{文件名}.jpg
```

### 优势对比

| 维度 | API 方式 | mmx CLI 方式 |
|------|---------|-------------|
| 复杂度 | 需处理 HTTP/JSON | 一行命令 |
| 认证 | 每次传 key | 自动读取 config |
| 错误处理 | 手动 | 内置重试 |
| 批量生成 | 循环调用 | `--n 3` 参数 |
| 新能力 | 仅图片 | 图片+语音+视频+音乐 |

---

## 配额参考

```
MiniMax-M2.7        24/1,500   (2%, 重置 2h41m)
image-01            14/350     (4%, 重置 6h41m)
speech-hd            0/4,000   (0%, 重置 6h41m)
music-2.6            0/100     (0%, 重置 6h41m)
```

---

## 故障排查

```bash
# 检查认证状态
mmx auth status

# 查看配置
mmx config show

# 查看配额
mmx quota

# 切换区域（cn/global）
mmx config set --key region --value cn
```

---

*设计：小马 🐴 | 2026-04-12 | v1.0*
