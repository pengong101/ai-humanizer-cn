#!/bin/bash
# OpsAgent 重启后完整检测脚本
# 系统重启完成后执行，验证所有功能正常
# 用法: bash reboot-check.sh

LOG_DIR="/root/.openclaw/workspace/logs"
REPORT="$LOG_DIR/reboot-check-$(date +%Y-%m-%d-%H%M).md"
mkdir -p "$LOG_DIR"
PASS=0; FAIL=0

log() { echo -e "[$(date '+%H:%M:%S')] $1"; }
pass() { echo "  ✅ $1"; ((PASS++)); }
fail() { echo "  ❌ $1"; ((FAIL++)); }

echo "# 系统重启检测报告 - $(date '+%Y-%m-%d %H:%M')" > "$REPORT"
echo "## 基础层检查" >> "$REPORT"

# 1. exec 响应
log "检查 exec 响应..."
start=$(date +%s%N)
timeout 5 echo ok > /dev/null 2>&1
rt=$?
end=$(date +%s%N)
ms=$(( (end - start) / 1000000 ))
if [ $rt -eq 0 ] && [ $ms -lt 3000 ]; then
  pass "exec 响应: ${ms}ms"
  echo "- exec 响应: ${ms}ms ✅" >> "$REPORT"
else
  fail "exec 响应: ${ms}ms（超时或过慢）"
  echo "- exec 响应: ${ms}ms ❌" >> "$REPORT"
fi

# 2. Docker 容器
log "检查 Docker 容器..."
for container in xiaoma-new searxng clash; do
  status=$(docker inspect -f '{{.State.Running}}' $container 2>/dev/null)
  if [ "$status" = "true" ]; then
    pass "Docker $container: 运行中"
    echo "- Docker $container: 运行中 ✅" >> "$REPORT"
  else
    fail "Docker $container: 未运行"
    echo "- Docker $container: 未运行 ❌" >> "$REPORT"
  fi
done

# 3. cron 状态
log "检查 cron..."
if service cron status 2>/dev/null | grep -q "running"; then
  pass "cron: 运行中"
  echo "- cron: 运行中 ✅" >> "$REPORT"
else
  fail "cron: 未运行"
  echo "- cron: 未运行 ❌" >> "$REPORT"
fi

# 4. 内存
log "检查内存..."
avail=$(free -m | awk 'NR==2{print $7}')
if [ "$avail" -gt 1000 ]; then
  pass "内存: ${avail}MB 可用"
  echo "- 内存: ${avail}MB 可用 ✅" >> "$REPORT"
else
  fail "内存: 仅 ${avail}MB 可用"
  echo "- 内存: ${avail}MB 可用 ❌" >> "$REPORT"
fi

# 5. 磁盘
log "检查磁盘..."
usage=$(df / | awk 'NR==2{print $5}' | tr -d '%')
if [ "$usage" -lt 80 ]; then
  pass "磁盘: ${usage}% 使用"
  echo "- 磁盘: ${usage}% 使用 ✅" >> "$REPORT"
else
  fail "磁盘: ${usage}% 使用（>80%）"
  echo "- 磁盘: ${usage}% 使用 ❌" >> "$REPORT"
fi

echo "## 功能层检查" >> "$REPORT"
PASS=0; FAIL=0

# 6. SearXNG
log "检查 SearXNG..."
searxng_json=$(timeout 10 curl -s "http://searxng:8080/search?q=test&format=json" 2>/dev/null)
searxng_result=$(echo "$searxng_json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('results',[])))" 2>/dev/null)
searxng_engines=$(echo "$searxng_json" | python3 -c "import sys,json; ur=d.get('unresponsive_engines',[]); print(len(ur))" 2>/dev/null)
if [ -n "$searxng_result" ] && [ "$searxng_result" -gt 0 ]; then
  pass "SearXNG 搜索: ${searxng_result} 条结果（${searxng_engines}个引擎不可用）"
  echo "- SearXNG: ${searxng_result} 条结果 ✅" >> "$REPORT"
else
  # 用 baidu 引擎测试（不走代理）
  searxng_baidu=$(timeout 10 curl -s "http://searxng:8080/search?q=test&format=json&engines=baidu" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('results',[])))" 2>/dev/null)
  if [ -n "$searxng_baidu" ] && [ "$searxng_baidu" -gt 0 ]; then
    pass "SearXNG(baidu): ${searxng_baidu} 条结果"
    echo "- SearXNG(baidu): ${searxng_baidu} 条结果 ✅" >> "$REPORT"
  else
    fail "SearXNG 搜索: 完全无结果"
    echo "- SearXNG: 完全无结果 ❌" >> "$REPORT"
  fi
fi

# 7. 记忆系统
log "检查记忆系统..."
if [ -f /root/.openclaw/workspace/MEMORY.md ] && [ -d /root/.openclaw/workspace/memory ]; then
  mem_lines=$(wc -l /root/.openclaw/workspace/MEMORY.md 2>/dev/null | awk '{print $1}')
  pass "记忆系统: 正常（MEMORY.md ${mem_lines}行）"
  echo "- 记忆系统: 正常（${mem_lines}行）✅" >> "$REPORT"
else
  fail "记忆系统: 文件缺失"
  echo "- 记忆系统: 文件缺失 ❌" >> "$REPORT"
fi

# 8. OpenClaw 状态
log "检查 OpenClaw..."
if timeout 10 openclaw status > /dev/null 2>&1; then
  pass "OpenClaw status: 正常"
  echo "- OpenClaw: 正常 ✅" >> "$REPORT"
else
  fail "OpenClaw status: 异常"
  echo "- OpenClaw: 异常 ❌" >> "$REPORT"
fi

# 9. cron 任务列表
log "检查 cron 任务..."
cron_count=$(timeout 10 openclaw cron list 2>/dev/null | grep -c "cron" || echo 0)
if [ "$cron_count" -gt 0 ]; then
  pass "OpenClaw cron: ${cron_count} 个任务"
  echo "- OpenClaw cron: ${cron_count} 个任务 ✅" >> "$REPORT"
else
  fail "OpenClaw cron: 任务列表异常"
  echo "- OpenClaw cron: 任务列表异常 ❌" >> "$REPORT"
fi

# 10. Git 操作
log "检查 Git..."
if git -C /root/.openclaw/workspace log --oneline -1 > /dev/null 2>&1; then
  commit=$(git -C /root/.openclaw/workspace log --oneline -1 | cut -d' ' -f1)
  pass "Git 操作: 正常 (HEAD: $commit)"
  echo "- Git: 正常 (HEAD: $commit) ✅" >> "$REPORT"
else
  fail "Git 操作: 异常"
  echo "- Git: 异常 ❌" >> "$REPORT"
fi

# 总结
echo "## 总结" >> "$REPORT"
echo "- 检查项目: $((PASS+FAIL))" >> "$REPORT"
echo "- 通过: $PASS ✅" >> "$REPORT"
echo "- 失败: $FAIL ❌" >> "$REPORT"
echo "" >> "$REPORT"
if [ $FAIL -eq 0 ]; then
  echo "**结论: 全部正常 ✅**" >> "$REPORT"
else
  echo "**结论: $FAIL 项异常，需处理**" >> "$REPORT"
fi

echo ""
log "检测完成: $PASS 通过 / $FAIL 失败"
echo "报告: $REPORT"
