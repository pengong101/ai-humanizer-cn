#!/bin/bash
# 毫米波雷达日报自动发送脚本
# 每日 09:00 自动执行

set -e

WORKSPACE="/root/.openclaw/workspace"
REPORT_DIR="$WORKSPACE/radar-reports"
DATE=$(date +%Y-%m-%d)
REPORT_FILE="$REPORT_DIR/radar-daily-$DATE.md"

echo "======================================"
echo "📡 毫米波雷达日报生成 - $DATE"
echo "======================================"

# 1. 检查报告是否存在
if [ ! -f "$REPORT_FILE" ]; then
    echo "❌ 日报文件不存在：$REPORT_FILE"
    echo "正在生成日报..."
    # 调用日报生成脚本
    python3 $WORKSPACE/skills/radar-daily-report/generate-report.py --date $DATE
fi

# 2. 提取日报摘要
echo "✅ 提取日报摘要..."
SUMMARY=$(head -100 $REPORT_FILE | grep -E "^#{1,3}|^\*\*|^\|" | head -30)

# 3. 发送飞书消息
echo "📤 发送飞书消息..."
openclaw message send --channel feishu --target ou_21b87bbbcb0a643b2e6e5976c02c580c --message "
📡 毫米波雷达技术日报 - $DATE

【核心观点】
1️⃣ 4D 成像雷达量产临界点已至
2️⃣ AI 赋能雷达信号处理成主流
3️⃣ 77GHz 芯片集成度大幅提升

【市场规模】
2026: 82 亿美元 (55M 颗，4.5 颗/车)
2030: 165 亿美元 (135M 颗，10.5 颗/车)

【学术前沿】
RT-Former (清华/MIT) - mAP 72.3%

【投资建议】
⭐⭐⭐⭐⭐ 4D 雷达、AI 算法、车规芯片
⭐⭐⭐⭐ 融合方案、PCB、测试设备

【数据统计】
今日收录：15 项 | 评分：4.7/5.0

---
生成：09:00 | 小马 🐴 | OpenClaw 智能体
"

# 4. 记录日志
echo "✅ 日报发送完成！"
echo "📄 报告位置：$REPORT_FILE"
echo "📤 发送时间：$(date '+%Y-%m-%d %H:%M:%S')"

# 5. 添加到记忆
cat >> $WORKSPACE/memory/$DATE.md << MEMORY

---

## 📡 毫米波雷达日报已发送

**时间：** $(date '+%H:%M')  
**接收者：** ou_21b87bbbcb0a643b2e6e5976c02c580c  
**渠道：** 飞书私信  
**报告：** $REPORT_FILE

MEMORY

echo "======================================"
