#!/bin/bash
# 在 OpenClaw 容器内执行雷达日报生成
docker exec xiaoma-new python3 /root/.openclaw/workspace/skills/radar-daily-report/generate-report.py --date $(date +%Y-%m-%d)
