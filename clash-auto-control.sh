#!/bin/bash
# Clash 自主控制脚本
# 功能：自动检测网络状态，智能开关 Clash 容器

set -e

CLASH_CONTAINER="clash"
CLASH_HOST="192.168.1.122"
CLASH_PORT="7890"
LOG_FILE="/var/log/clash-auto-control.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

# 检测 Clash 容器状态
check_clash_status() {
    if docker ps | grep -q "$CLASH_CONTAINER"; then
        return 0  # 运行中
    else
        return 1  # 未运行
    fi
}

# 检测代理可用性
check_proxy() {
    log "🔍 检测代理可用性..."
    
    if curl -s --max-time 5 --proxy "http://${CLASH_HOST}:${CLASH_PORT}" "https://www.google.com" > /dev/null 2>&1; then
        log "✅ 代理可用"
        return 0
    else
        log "❌ 代理不可用"
        return 1
    fi
}

# 检测国内网络
check_cn_network() {
    log "🔍 检测国内网络..."
    
    if curl -s --max-time 5 "https://www.baidu.com" > /dev/null 2>&1; then
        log "✅ 国内网络正常"
        return 0
    else
        log "❌ 国内网络异常"
        return 1
    fi
}

# 启动 Clash
start_clash() {
    log "🚀 启动 Clash 容器..."
    
    if docker start $CLASH_CONTAINER 2>/dev/null; then
        log "✅ Clash 已启动"
        sleep 3  # 等待启动完成
        return 0
    else
        log "❌ Clash 启动失败"
        return 1
    fi
}

# 停止 Clash
stop_clash() {
    log "🛑 停止 Clash 容器..."
    
    if docker stop $CLASH_CONTAINER 2>/dev/null; then
        log "✅ Clash 已停止"
        return 0
    else
        log "❌ Clash 停止失败"
        return 1
    fi
}

# 重启 Clash
restart_clash() {
    log "🔄 重启 Clash 容器..."
    
    if docker restart $CLASH_CONTAINER 2>/dev/null; then
        log "✅ Clash 已重启"
        sleep 3
        return 0
    else
        log "❌ Clash 重启失败"
        return 1
    fi
}

# 智能决策
smart_decision() {
    log "========================================"
    log "🤖 Clash 智能决策开始"
    log "========================================"
    
    # 检测网络状态
    cn_ok=false
    proxy_ok=false
    
    if check_cn_network; then
        cn_ok=true
    fi
    
    if check_proxy; then
        proxy_ok=true
    fi
    
    # 决策逻辑
    log "📊 网络状态：国内=$cn_ok, 代理=$proxy_ok"
    
    if [ "$proxy_ok" = true ]; then
        log "✅ 代理正常，保持 Clash 运行"
        if ! check_clash_status; then
            log "⚠️  代理可用但 Clash 未运行，启动 Clash..."
            start_clash
        fi
    elif [ "$cn_ok" = true ]; then
        log "⚠️  代理不可用但国内网络正常"
        if check_clash_status; then
            log "💡 尝试重启 Clash 恢复代理..."
            restart_clash
            sleep 5
            if check_proxy; then
                log "✅ Clash 重启后代理恢复"
            else
                log "⚠️  Clash 重启后代理仍不可用，保持运行（可能规则问题）"
            fi
        fi
    else
        log "❌ 国内网络和代理都异常"
        if check_clash_status; then
            log "💡 尝试重启 Clash 恢复网络..."
            restart_clash
            sleep 5
            if check_cn_network || check_proxy; then
                log "✅ Clash 重启后网络恢复"
            else
                log "❌ Clash 重启后网络仍异常，停止 Clash 使用直连..."
                stop_clash
            fi
        fi
    fi
    
    log "========================================"
    log "✅ Clash 智能决策完成"
    log "========================================"
}

# 强制开启 Clash
force_start() {
    log "🔧 强制开启 Clash..."
    start_clash
    check_proxy
}

# 强制关闭 Clash
force_stop() {
    log "🔧 强制关闭 Clash..."
    stop_clash
}

# 显示状态
show_status() {
    echo "================================"
    echo "📊 Clash 状态"
    echo "================================"
    
    echo -n "容器状态："
    if check_clash_status; then
        echo "🟢 运行中"
    else
        echo "🔴 未运行"
    fi
    
    echo -n "代理状态："
    if check_proxy 2>/dev/null; then
        echo "🟢 可用"
    else
        echo "🔴 不可用"
    fi
    
    echo -n "国内网络："
    if curl -s --max-time 3 "https://www.baidu.com" > /dev/null 2>&1; then
        echo "🟢 正常"
    else
        echo "🔴 异常"
    fi
    
    echo "================================"
}

# 主流程
case "${1:-smart}" in
    start)
        force_start
        ;;
    stop)
        force_stop
        ;;
    restart)
        restart_clash
        ;;
    status)
        show_status
        ;;
    smart|auto)
        smart_decision
        ;;
    *)
        echo "用法：$0 {start|stop|restart|status|smart}"
        echo ""
        echo "命令说明："
        echo "  start   - 强制启动 Clash"
        echo "  stop    - 强制停止 Clash"
        echo "  restart - 重启 Clash"
        echo "  status  - 显示状态"
        echo "  smart   - 智能决策（默认）"
        echo ""
        echo "示例："
        echo "  $0 smart     # 智能决策"
        echo "  $0 start     # 强制启动"
        echo "  $0 status    # 查看状态"
        exit 1
        ;;
esac
