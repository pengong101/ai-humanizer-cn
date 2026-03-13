#!/bin/bash
# Docker 监控守护进程
# 功能：后台运行，持续监控 Docker 容器健康状态

set -e

MONITOR_INTERVAL=300  # 5 分钟
RESOURCE_INTERVAL=900  # 15 分钟
LOG_DIR="/var/log"
PID_FILE="/var/run/docker-monitor.pid"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_DIR/docker-monitor-daemon.log"
}

# 清理函数
cleanup() {
    log "🛑 停止监控守护进程..."
    rm -f "$PID_FILE"
    exit 0
}

trap cleanup SIGTERM SIGINT

# 启动守护进程
start_daemon() {
    log "🚀 启动 Docker 监控守护进程"
    log "健康检查间隔：${MONITOR_INTERVAL}秒"
    log "资源监控间隔：${RESOURCE_INTERVAL}秒"
    
    echo $$ > "$PID_FILE"
    
    local health_counter=0
    local resource_counter=0
    
    while true; do
        # 健康检查（每次循环）
        if [ -x "/root/.openclaw/workspace/docker-monitor/health-check.sh" ]; then
            /root/.openclaw/workspace/docker-monitor/health-check.sh
        fi
        
        # 资源监控（每 3 次循环，即 15 分钟）
        resource_counter=$((resource_counter + 1))
        if [ $resource_counter -ge 3 ] && [ -x "/root/.openclaw/workspace/docker-monitor/resource-monitor.sh" ]; then
            /root/.openclaw/workspace/docker-monitor/resource-monitor.sh
            resource_counter=0
        fi
        
        # 等待
        sleep $MONITOR_INTERVAL
    done
}

# 检查是否已在运行
if [ -f "$PID_FILE" ]; then
    old_pid=$(cat "$PID_FILE")
    if kill -0 "$old_pid" 2>/dev/null; then
        log "⚠️  监控守护进程已在运行 (PID: $old_pid)"
        exit 1
    else
        log "🗑️  清理旧的 PID 文件"
        rm -f "$PID_FILE"
    fi
fi

# 启动
start_daemon
