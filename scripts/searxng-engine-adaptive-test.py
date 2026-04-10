#!/usr/bin/env python3
"""
SearXNG 自适应搜索引擎测试 (使用 curl 调用 Docker API)
"""

import json
import time
import urllib.request
import urllib.error
import subprocess
import os
from datetime import datetime

# 配置
SEARXNG_URL = "http://172.23.0.4:8080"
CLASH_PROXY = "http://172.23.0.3:7890"
CONTAINER_NAME = "searxng"
SETTINGS_PATH_IN_CONTAINER = "/etc/searxng/settings.yml"
DOCKER_SOCKET = "/var/run/docker.sock"

# 要测试的引擎
ENGINES_TO_TEST = {
    "google": "https://www.google.com",
    "bing": "https://www.bing.com",
    "baidu": "https://www.baidu.com",
    "duckduckgo": "https://duckduckgo.com",
    "brave": "https://search.brave.com",
    "wikipedia": "https://www.wikipedia.org",
    "qwant": "https://www.qwant.com",
    "ecosia": "https://www.ecosia.org",
}

def docker_exec(cmd, container):
    """通过 curl 调用 Docker Socket API"""
    if isinstance(cmd, str):
        cmd_list = cmd.split()
    else:
        cmd_list = cmd
    
    payload = json.dumps({"AttachStdout": True, "AttachStderr": True, "Cmd": cmd_list})
    
    # 创建 exec（10秒超时，防止Docker socket卡死）
    r1 = subprocess.run(
        ["curl", "-s", "--unix-socket", DOCKER_SOCKET, "-X", "POST",
         f"http://localhost/containers/{container}/exec",
         "-H", "Content-Type: application/json",
         "-d", payload],
        capture_output=True, timeout=10
    )
    
    try:
        data = json.loads(r1.stdout.decode('utf-8', errors='ignore'))
        exec_id = data.get("Id")
    except:
        return None
    
    if not exec_id:
        return None
    
    # 启动 exec（10秒超时）
    r2 = subprocess.run(
        ["curl", "-s", "--unix-socket", DOCKER_SOCKET, "-X", "POST",
         f"http://localhost/exec/{exec_id}/start",
         "-H", "Content-Type: application/json",
         "-d", '{"Detach": false, "Tty": false}'],
        capture_output=True, timeout=30
    )
    
    return r2.stdout.decode('utf-8', errors='ignore')

def docker_restart(container):
    """重启容器（10秒超时）"""
    subprocess.run(
        ["curl", "-s", "--unix-socket", DOCKER_SOCKET, "-X", "POST",
         f"http://localhost/containers/{container}/restart",
         "-H", "Content-Type: application/json"],
        capture_output=True, timeout=10
    )
    return True


def check_mihomo_alive():
    """检查 mihomo 是否存活（5秒超时）"""
    try:
        r = subprocess.run(
            ["curl", "-s", "--connect-timeout", "5", "-m", "5",
             "http://clash:9090/proxies"],
            capture_output=True, timeout=8
        )
        if r.returncode == 0:
            try:
                data = json.loads(r.stdout.decode('utf-8', errors='ignore'))
                return "proxies" in data
            except:
                pass
    except:
        pass
    return False

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def test_engine_via_proxy(url):
    """通过代理测试"""
    proxy_handler = urllib.request.ProxyHandler({
        "http": CLASH_PROXY, "https": CLASH_PROXY,
    })
    opener = urllib.request.build_opener(proxy_handler)
    
    try:
        req = urllib.request.Request(url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
        start = time.time()
        r = opener.open(req, timeout=15)
        latency = (time.time() - start) * 1000
        return {"status": "ok", "latency": int(latency)} if r.getcode() in [200, 301, 302] else {"status": "error", "code": r.getcode()}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:50]}

def test_searxng_search(engine_name):
    """通过 SearXNG HTML 格式测试（避免 botdetection 403）"""
    try:
        url = f"{SEARXNG_URL}/search?q=test&engines={engine_name}"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        r = urllib.request.urlopen(req, timeout=30)
        content = r.read().decode('utf-8', errors='ignore')
        
        # 检查是否被 botdetection 拦截
        if '403 Forbidden' in content or 'Access denied' in content:
            return {"status": "error", "reason": "botdetection_blocked"}
        
        # 检查结果数量（通过结果条目粗略判断）
        result_count = content.count('result') + content.count('article')
        if result_count > 0:
            return {"status": "ok", "results": result_count}
        else:
            return {"status": "suspended", "results": 0}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:50]}

def get_settings():
    """获取当前配置"""
    return docker_exec(["cat", SETTINGS_PATH_IN_CONTAINER], CONTAINER_NAME)

def update_settings_and_restart(new_content):
    """写入配置并重启"""
    import base64
    encoded = base64.b64encode(new_content.encode('utf-8')).decode('ascii')
    
    write_cmd = f"echo '{encoded}' | base64 -d > {SETTINGS_PATH_IN_CONTAINER}.new"
    docker_exec(["sh", "-c", write_cmd], CONTAINER_NAME)
    
    mv_cmd = f"mv {SETTINGS_PATH_IN_CONTAINER}.new {SETTINGS_PATH_IN_CONTAINER}"
    docker_exec(["sh", "-c", mv_cmd], CONTAINER_NAME)
    
    docker_restart(CONTAINER_NAME)
    return True

def modify_settings(content, enabled, disabled):
    """修改配置"""
    if not content:
        return None
    
    lines = content.split('\n')
    result_lines = []
    current_engine = None
    
    for line in lines:
        stripped = line.strip()
        
        if stripped.startswith('name:'):
            parts = stripped.split('name:', 1)
            if len(parts) > 1:
                current_engine = parts[1].strip().strip('"\'')
        elif current_engine and stripped.startswith('disabled:'):
            if current_engine in enabled:
                result_lines.append('    disabled: false')
            elif current_engine in disabled:
                result_lines.append('    disabled: true')
            else:
                result_lines.append(line)
            current_engine = None
        else:
            result_lines.append(line)
    
    return '\n'.join(result_lines)

def main():
    log("=" * 50)
    log("🚀 SearXNG 自适应引擎测试开始")
    log("=" * 50)
    
    # Step 0: 检查 mihomo 是否可用（快速失败，不卡死）
    log("📡 Step 0: 检查 mihomo 健康状态...")
    if not check_mihomo_alive():
        log("⚠️  mihomo 未运行或无法连接，跳过本次引擎测试（避免卡死）")
        log("💡 提示: 若 mihomo 长期故障，搜索引擎将使用直连引擎（baidu）")
        log("=" * 50)
        return
    log("✅ mihomo 在线")
    
    # Step 1: 测试代理
    log("📡 Step 1: 测试代理连通性...")
    proxy_test = test_engine_via_proxy("https://www.google.com")
    proxy_available = proxy_test["status"] == "ok"
    if proxy_available:
        log(f"✅ 代理可用 (延迟: {proxy_test['latency']}ms)")
    else:
        log(f"⚠️  代理不可用（mihomo 可能已故障），跳过引擎测试: {proxy_test.get('reason', proxy_test)}")
        log("💡 提示: 下次健康检查将重新评估，或手动重启 mihomo")
        log("=" * 50)
        return
    
    # Step 2: 测试所有引擎
    log("\n📡 Step 2: 通过 SearXNG API 测试引擎...")
    api_results = {}
    
    for engine in ENGINES_TO_TEST:
        result = test_searxng_search(engine)
        api_results[engine] = result
        if result["status"] == "ok":
            log(f"  ✅ {engine}: {result['results']} 结果")
        elif result["status"] == "suspended":
            log(f"  ❌ {engine}: suspended")
        else:
            log(f"  ⚠️  {engine}: {result}")
    
    # Step 3: 决定启用/禁用
    log("\n📡 Step 3: 自适应调整...")
    enabled = [e for e, r in api_results.items() if r["status"] == "ok" and r["results"] > 0]
    disabled = [e for e, r in api_results.items() if r["status"] != "ok" or r["results"] == 0]
    
    for e in enabled:
        log(f"  ✅ 启用 {e}")
    for e in disabled:
        log(f"  ❌ 禁用 {e}")
    
    # Step 4: 更新配置
    log("\n📡 Step 4: 更新配置...")
    current = get_settings()
    if current:
        new_content = modify_settings(current, enabled, disabled)
        if new_content:
            update_settings_and_restart(new_content)
            log("✅ 配置已更新，SearXNG 重启中...")
        else:
            log("❌ 配置修改失败")
    else:
        log("❌ 无法获取当前配置")
    
    time.sleep(12)
    
    # Step 5: 报告
    log("\n" + "=" * 50)
    log("📊 测试报告")
    log("=" * 50)
    log(f"代理状态: {'✅ 可用' if proxy_available else '❌ 不可用'}")
    log(f"启用 ({len(enabled)}): {', '.join(enabled) or '无'}")
    log(f"禁用 ({len(disabled)}): {', '.join(disabled) or '无'}")
    log("=" * 50)

if __name__ == "__main__":
    main()
