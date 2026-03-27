# ImageAgent v2.0 - MiniMax T2I 图片生成

**版本：** v2.0  
**更新时间：** 2026-03-27  
**模型：** MiniMax Image-01（T2I）  
**API：** `https://api.minimax.chat/v1/text_to_image`（待确认）

---

## MiniMax T2I API

### 请求格式

```python
import requests

def generate_image(prompt: str, api_key: str, group_id: str) -> dict:
    """
    调用 MiniMax T2I 生成图片
    
    Args:
        prompt: 图片描述（英文效果更佳）
        api_key: MiniMax API Key
        group_id: Group ID
    
    Returns:
        {"image_url": "https://...", "task_id": "..."}
    """
    url = "https://api.minimax.chat/v1/text_to_image"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "image-01",
        "prompt": prompt,
        "aspect_ratio": "16:9",      # 封面图用16:9
        "resolution": "1024x1024",    # 可选 512x512, 1024x1024, 1792x1024
        "n": 1
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    result = resp.json()
    # 解析任务ID，轮询获取结果
    task_id = result["data"]["task_id"]
    return poll_task_result(task_id, api_key)

def poll_task_result(task_id: str, api_key: str, max_wait: int = 60) -> dict:
    """轮询图片生成结果（通常需15-30秒）"""
    import time
    url = f"https://api.minimax.chat/v1/text_to_image/{task_id}"
    headers = {"Authorization": f"Bearer {api_key}"}
    for _ in range(max_wait // 5):
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()["data"]
        if data["status"] == "success":
            return {"image_url": data["image_url"], "task_id": task_id}
        elif data["status"] == "failed":
            raise RuntimeError(f"生成失败: {data.get('error', 'unknown')}")
        time.sleep(5)
    raise TimeoutError("图片生成超时")
```

### API 凭据

从环境变量读取：
```bash
MINIMAX_API_KEY=your_api_key
MINIMAX_GROUP_ID=your_group_id
```

---

## 工作流程

```
接收图片需求
   ↓
封面图 → MiniMax T2I 生成（必须，16:9）
   ↓
内容配图 → 优先官方源 → 备用 MiniMax T2I 生成
   ↓
多模态验证（MiniMax-M2.7 判断相关性 ≥7）
   ↓
输出：图片URL + alt文字 + 放置位置
```

---

## MiniMax T2I 提示词模板

### 封面图
```
[文章主题]，专业科普风格，高对比度，居中构图，4K高清
示例（黑洞）："Super massive black hole with accretion disk, Event Horizon Telescope photography style, scientific illustration, high contrast, centered composition, 4K HD, photorealistic"
```

### 内容分镜图
```
[具体概念] scientific diagram, clean minimalist style, no text, educational illustration, high resolution
示例："74GHz毫米波雷达 waves propagation through fog, scientific diagram, no text, clean white background"
```

### 示意图
```
[概念] professional infographic, modern design, muted colors, suitable for science article
```

---

## 图片策略

### 优先级（更新）
| 优先级 | 来源 | 说明 |
|--------|------|------|
| 1️⃣ | **MiniMax T2I 生成** | 封面图、分镜图、示意图 |
| 2️⃣ | NASA/EHT/ESO 官方 | 科学事实类图片（注明来源）|
| 3️⃣ | Wikimedia Commons | Wikipedia 同源图 |
| 4️⃣ | Unsplash/Pexels | 通用配图 |

### 为什么优先用 AI 生成？
- 封面图吸引力强
- 分镜图无版权问题
- 不依赖外部 URL 可用性
- 可生成不存在的科学概念图

---

## 输出格式

```markdown
# 图片方案 - [文章标题]

## 封面图
- 生成方式：MiniMax T2I
- 提示词：[英文提示词]
- aspect_ratio: 16:9
- 状态：✅ 生成成功
- URL：https://...
- alt文字：[描述]
- 放置：文章开头

## 配图1：[小标题]
- 生成方式：[MiniMax T2I / 官方 / Wikimedia]
- 来源/提示词：[...]
- alt文字：[...]
- 放置位置：段落后
- 相关性验证：MiniMax-M2.7 → 8.5/10 ✅

## 验证汇总
| 图片 | 方式 | 大小 | 相关性 | 状态 |
|------|------|------|--------|------|
| 封面图 | T2I | 1.2MB | 9.0/10 | ✅ |
| 配图1 | 官方 | 380KB | 8.5/10 | ✅ |
| 配图2 | T2I | 890KB | 8.0/10 | ✅ |
```

---

## 错误处理

| 错误 | 处理方式 |
|------|---------|
| API Key 无效 | 回退到官方/Wikimedia 图片 |
| 生成超时（>60s）| 回退到备选图片 |
| 图片损坏 | 重新生成（最多3次）|
| 所有方式失败 | 标记为「需手动处理」，不影响文章发布 |
