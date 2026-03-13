#!/bin/bash
# Docker 容器自动恢复脚本
# 功能：自动恢复故障容器，最多重试 3 次

set -e

# 配置
CONTAINER_NAME=$1
REASON=$2
MAX_RETRIES=3
RETRY_DELAY=10
LOG_FILE="/var/log/docker-recover.log"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 日志函数
log() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "${timestamp} [${level}] ${message}" | tee -a "$LOG_FILE"
}

log_info() { log "INFO" "${GREEN}$1${NC}"; }
log_warn() { log "WARN" "${YELLOW}$1${NC}"; }
log_error() { log "ERROR" "${RED}$1${NC}"; }

# 发送告警通知
send_alert() {
    local status=$1
    local message=$2
    
    log_info "📢 告警通知：[$status] $message"
    
    # 这里可以集成飞书、邮件等通知方式
    # 当前仅记录日志
}

# 停止容器
stop_container() {
    local container=$1
    log_info "🛑 停止容器：$container"
    docker stop "$container" 2>/dev/null || log_warn "容器 $container 未运行或已停止"
    sleep 3
}

# 删除容器
remove_container() {
    local container=$1
    log_info "🗑️  删除容器：$container"
    docker rm -f "$container" 2>/dev/null || log_warn "容器 $container 不存在"
    sleep 2
}

# 启动 OpenClaw 容器
start_openclaw() {
    log_info "🚀 启动 OpenClaw 容器..."
    
    docker run -d \
        --name xiaoma_new \
        --restart=always \
        --memory=2g \
        --memory-swap=4g \
        --cpus=2.0 \
        -p 8082:8080 \
        -v /root/.openclaw/workspace:/root/.openclaw/workspace \
        -v /root/.openclaw/data:/root/.openclaw/data \
        -e OPENCLAW_CONFIG=/root/.openclaw/data/config.json \
        -e TZ=Asia/Shanghai \
        --health-cmd="openclaw status || exit 1" \
        --health-interval=60s \
        --health-timeout=10s \
        --health-retries=3 \
        ghcr.io/openclaw/openclaw:latest
    
    return $?
}

# 启动其他容器
start_other_container() {
    local container=$1
    log_info "🚀 启动容器：$container"
    docker start "$container"
    return $?
}

# 验证容器启动
verify_container() {
    local container=$1
    local wait_time=0
    local max_wait=60
    
    log_info "⏳ 等待容器启动..."
    
    while [ $wait_time -lt $max_wait ]; do
        sleep 5
        wait_time=$((wait_time + 5))
        
        local running=$(docker inspect --format='{{.State.Running}}' "$container" 2>/dev/null)
        if [ "$running" = "true" ]; then
            log_info "✅ 容器 $container 已启动 (耗时：${wait_time}s)"
            return 0
        fi
    done
    
    log_error "❌ 容器 $container 启动超时"
    return 1
}

# 恢复容器
recover_container() {
    local container=$1
    local retry=0
    
    log_info "=========================================="
    log_info "开始恢复容器：$container"
    log_info "原因：$REASON"
    log_info "=========================================="
    
    send_alert "RECOVERING" "容器 $container 正在恢复"
    
    while [ $retry -lt $MAX_RETRIES ]; do
        retry=$((retry + 1))
        log_info "🔄 尝试恢复 (第 $retry/$MAX_RETRIES 次)"
        
        # 停止容器
        stop_container "$container"
        
        # 删除容器
        remove_container "$container"
        
        # 启动容器
        if [ "$container" = "xiaoma_new" ]; then
            start_openclaw
        else
            start_other_container "$container"
        fi
        
        # 验证启动
        if verify_container "$container"; then
            log_info "=========================================="
            log_info "✅ 容器恢复成功！"
            log_info "=========================================="
            send_alert "RECOVERED" "容器 $container 已成功恢复"
            return 0
        fi
        
        log_warn "⚠️  恢复失败，${RETRY_DELAY}秒后重试..."
        sleep $RETRY_DELAY
    done
    
    log_error "=========================================="
    log_error "❌ 容器恢复失败，已达到最大重试次数"
    log_error "=========================================="
    send_alert "FAILED" "容器 $container 恢复失败，请手动干预！"
    
    return 1
}

# 主函数
main() {
    if [ -z "$CONTAINER_NAME" ]; then
        log_error "❌ 用法：$0 <container-name> [reason]"
        exit 1
    fi
    
    recover_container "$CONTAINER_NAME"
}

main "$@"
