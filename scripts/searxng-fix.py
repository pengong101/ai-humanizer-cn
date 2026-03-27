#!/usr/bin/env python3
"""修复 SearXNG 配置：将 bind_address 改为 0.0.0.0，port 改为 8080"""
import subprocess, time, sys

def run(cmd):
    print(f"CMD: {cmd[:80]}")
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
    print(f"OUT: {r.stdout[:200]}")
    if r.stderr: print(f"ERR: {r.stderr[:200]}")
    return r

# Step 1: Fix config
print("=== Fix config ===")
run('docker exec searxng sed -i \'s/^  bind_address:.*/  bind_address: "0.0.0.0"/\' /etc/searxng/settings.yml')
run('docker exec searxng sed -i \'s/^  port:.*/  port: 8080/\' /etc/searxng/settings.yml')
run('docker exec searxng grep -E "bind_address|port:" /etc/searxng/settings.yml | grep -v "^#"')

# Step 2: Restart
print("=== Restart ===")
run('docker restart searxng')
time.sleep(8)

# Step 3: Test
print("=== Test ===")
r = run('docker exec xiaoma-new wget -q -O - "http://searxng:8080/search?q=Neuralink&engines=baidu&format=json" --timeout=15')
try:
    import json
    d = json.loads(r.stdout)
    count = len(d.get('results', []))
    print(f"✅ 百度结果: {count}条")
    if count > 0:
        for x in d['results'][:2]:
            print(f"   - {x['title'][:40]}")
    print(f"CAPTCHA: {d.get('unresponsive_engines', [])[:1]}")
except:
    print(f"❌ 解析失败: {r.stdout[:300]}")
