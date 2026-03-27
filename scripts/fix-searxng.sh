#!/bin/bash
# SearXNG 修复脚本 - 彻底解决 403 问题

set -e

echo "=== Step 1: 修复配置文件 ==="
# 直接用 sed 修改（处理 \r\n 换行）
docker exec searxng sh -c "
  sed -i 's/\r$//' /etc/searxng/settings.yml
  sed -i 's/^  bind_address:.*/  bind_address: \"0.0.0.0\"/' /etc/searxng/settings.yml
  sed -i 's/^  port:.*/  port: 8080/' /etc/searxng/settings.yml
  grep -E 'bind_address|port:' /etc/searxng/settings.yml | grep -v '^#'
"

echo "=== Step 2: 重启 SearXNG ==="
docker restart searxng
sleep 8

echo "=== Step 3: 验证 SearXNG 监听 ==="
docker exec searxng sh -c "cat /proc/net/tcp /proc/net/tcp6" 2>/dev/null | python3 -c "
import sys
for l in sys.stdin.readlines():
    p = l.split()
    if len(p)<10 or p[3]!='0A': continue
    ip,port = p[1].split(':')
    print(f'Port {int(port,16)} ip={ip}')
"

echo "=== Step 4: 测试搜索 ==="
RESULT=$(docker exec xiaoma-new wget -q -O - "http://searxng:8080/search?q=Neuralink&engines=baidu&format=json" --timeout=15 2>/dev/null)
COUNT=$(echo "$RESULT" | python3 -c "import sys,json; print(len(json.load(sys.stdin).get('results',[])))" 2>/dev/null)
if [ "$COUNT" -gt 0 ]; then
  echo "✅ 搜索成功！百度结果: $COUNT 条"
else
  echo "❌ 搜索失败，HTTP响应: $RESULT"
fi
