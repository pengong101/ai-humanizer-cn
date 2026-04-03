#!/bin/bash
# 科普文章选题工作流 - 每日定时执行
# 输出到 topics/YYYY-MM-DD-topics.md
# 需要时推送到 GitHub

DATE=$(date +%Y-%m-%d)
OUTPUT_DIR="/root/.openclaw/workspace/topics"
mkdir -p "$OUTPUT_DIR"
OUTPUT_FILE="$OUTPUT_DIR/${DATE}-topics.md"

echo "=== 科普文章选题工作流 ===" > "$OUTPUT_FILE"
echo "执行时间：$(date '+%Y-%m-%d %H:%M:%S')" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# 多方向搜索
search_and_append() {
    local query="$1"
    local section="$2"
    echo "### $section" >> "$OUTPUT_FILE"
    echo '```' >> "$OUTPUT_FILE"
    docker exec xiaoma-20260328 bash -c "mcporter call exa.web_search_exa query='$query' numResults=8 freshness=month 2>&1" | grep -E "^Title:|^Published:|^URL:" | head -15 >> "$OUTPUT_FILE" 2>/dev/null || echo "搜索失败" >> "$OUTPUT_FILE"
    echo '```' >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
}

# 搜索各方向热点
search_and_append "科普 热门话题 突破 2026" "全网科普热点"
search_and_append "AI人工智能 大模型 最新突破" "AI科技热点"
search_and_append "太空探索 登月 火星" "太空探索热点"
search_and_append "基因编辑 医学突破" "生物医学热点"
search_and_append "量子计算 科学进展" "量子科技热点"

echo "=== 搜索完成 ===" >> "$OUTPUT_FILE"
echo "保存位置：$OUTPUT_FILE" >> "$OUTPUT_FILE"

# 推送到 GitHub（如果有必要）
cd /root/.openclaw/workspace
git add topics/"${DATE}"-topics.md 2>/dev/null
git commit -m "daily: 科普选题 $(date +%Y-%m-%d)" 2>/dev/null || true

echo "完成：$OUTPUT_FILE"
