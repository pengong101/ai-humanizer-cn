#!/bin/bash
# mmx-image.sh - MiniMax 图片生成封装脚本
# 用法: mmx-image.sh "图片描述" [输出目录] [文件名]
# 输出: 图片保存路径

PROMPT="$1"
OUT_DIR="${2:-/root/.openclaw/workspace/articles/images}"
FILENAME="${3:-$(date +%Y%m%d_%H%M%S).jpg}"

mkdir -p "$OUT_DIR"

# 生成图片
mmx image "$PROMPT" --aspect-ratio 16:9 --out-dir "$OUT_DIR" 2>&1

# 查找最新生成的图片
LATEST=$(find "$OUT_DIR" -name "*.jpg" -o -name "*.png" | head -1)
if [ -n "$LATEST" ]; then
    # 重命名为规范名称
    mv "$LATEST" "$OUT_DIR/$FILENAME"
    echo "Saved: $OUT_DIR/$FILENAME"
fi
