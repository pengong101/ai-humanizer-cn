#!/bin/bash
# SearXNG 自适应代理检测脚本
# 功能：自动检测代理可用性，启用/禁用全球搜索引擎

set -e

CLASH_HOST="192.168.1.122"
CLASH_PORT="7890"
SEARXNG_CONTAINER="searxng"
LOG_FILE="/var/log/searxng-proxy-check.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

# 检测代理可用性
check_proxy() {
    log "🔍 检测 Clash 代理可用性..."
    
    if curl -s --max-time 5 --proxy "http://${CLASH_HOST}:${CLASH_PORT}" "https://www.google.com" > /dev/null 2>&1; then
        log "✅ 代理可用，可以访问全球搜索引擎"
        return 0
    else
        log "❌ 代理不可用，降级到国内搜索引擎"
        return 1
    fi
}

# 启用全球搜索引擎
enable_global_engines() {
    log "🌐 启用全球搜索引擎（Google, DuckDuckGo, Wikipedia...）"
    
    docker exec $SEARXNG_CONTAINER python3 << 'PYEOF'
import yaml

with open('/etc/searxng/settings.yml', 'r') as f:
    config = yaml.safe_load(f)

for engine in config.get('engines', []):
    if engine.get('name') in ['google', 'duckduckgo', 'wikipedia', 'brave', 'startpage']:
        engine['disabled'] = False
        print(f"✅ 启用：{engine['name']}")

with open('/etc/searxng/settings.yml', 'w') as f:
    yaml.dump(config, f, default_flow_style=False)

print("✅ 全球搜索引擎已启用")
PYEOF
}

# 禁用全球搜索引擎
disable_global_engines() {
    log "🇨🇳 禁用全球搜索引擎，仅保留国内引擎"
    
    docker exec $SEARXNG_CONTAINER python3 << 'PYEOF'
import yaml

with open('/etc/searxng/settings.yml', 'r') as f:
    config = yaml.safe_load(f)

for engine in config.get('engines', []):
    if engine.get('name') in ['google', 'duckduckgo', 'wikipedia', 'brave', 'startpage']:
        engine['disabled'] = True
        print(f"⚠️  禁用：{engine['name']}")

with open('/etc/searxng/settings.yml', 'w') as f:
    yaml.dump(config, f, default_flow_style=False)

print("✅ 已降级到国内搜索引擎")
PYEOF
}

# 重启 SearXNG
restart_searxng() {
    log "🔄 重启 SearXNG 容器..."
    docker restart $SEARXNG_CONTAINER
    sleep 5
    log "✅ SearXNG 已重启"
}

# 测试搜索
test_search() {
    log "🧪 测试搜索功能..."
    
    # 测试 Google
    if curl -s --max-time 15 "http://localhost:8081/search?q=test&format=json&engines=google" | grep -q "results"; then
        log "✅ Google 搜索正常"
    else
        log "⚠️  Google 搜索异常"
    fi
    
    # 测试百度
    if curl -s --max-time 15 "http://localhost:8081/search?q=test&format=json&engines=baidu" | grep -q "results"; then
        log "✅ 百度搜索正常"
    else
        log "⚠️  百度搜索异常"
    fi
}

# 主流程
main() {
    log "========================================"
    log "🚀 SearXNG 自适应代理检测启动"
    log "========================================"
    
    if check_proxy; then
        enable_global_engines
    else
        disable_global_engines
    fi
    
    restart_searxng
    test_search
    
    log "========================================"
    log "✅ 自适应代理检测完成"
    log "========================================"
}

# 执行
main
