#!/bin/bash
# Docker 资源监控脚本
# 功能：监控容器资源使用情况，超过阈值时告警

set -e

# 配置
MEMORY_THRESHOLD=80   # 内存使用率告警阈值 (%)
DISK_THRESHOLD=85     # 磁盘使用率告警阈值 (%)
CPU_THRESHOLD=90      # CPU 使用率告警阈值 (%)
LOG_FILE="/var/log/docker-resources.log"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# 检查容器内存使用
check_memory() {
    local container=$1
    
    local mem_info=$(docker stats --no-stream --format "{{.MemUsage}}" "$container" 2>/dev/null)
    if [ -z "$mem_info" ]; then
        log_warn "⚠️  无法获取容器 $container 内存信息"
        return 1
    fi
    
    local used=$(echo $mem_info | cut -d'/' -f1 | sed 's/[^0-9.]//g')
    local limit=$(echo $mem_info | cut -d'/' -f2 | sed 's/[^0-9.]//g')
    
    if [ -n "$used" ] && [ -n "$limit" ] && [ "$limit" != "0" ]; then
        local percent=$(awk "BEGIN {printf \"%.1f\", ($used/$limit)*100}")
        
        if (( $(echo "$percent > $MEMORY_THRESHOLD" | bc -l 2>/dev/null || echo 0) )); then
            log_warn "⚠️  容器 $container 内存使用率过高：${percent}% (阈值：${MEMORY_THRESHOLD}%)"
            return 1
        fi
        log_info "✅ 容器 $container 内存：${used}/${limit} (${percent}%)"
    fi
    
    return 0
}

# 检查磁盘使用
check_disk() {
    local disk_info=$(df -h /var/lib/docker 2>/dev/null | tail -1)
    
    if [ -n "$disk_info" ]; then
        local usage=$(echo $disk_info | awk '{print $5}' | tr -d '%')
        local available=$(echo $disk_info | awk '{print $4}')
        
        if [ "$usage" -gt "$DISK_THRESHOLD" ]; then
            log_warn "⚠️  Docker 磁盘使用率过高：${usage}% (阈值：${DISK_THRESHOLD}%)，可用：$available"
            return 1
        fi
        log_info "✅ Docker 磁盘使用率：${usage}% (可用：$available)"
    fi
    
    return 0
}

# 检查 CPU 使用
check_cpu() {
    local container=$1
    
    local cpu_percent=$(docker stats --no-stream --format "{{.CPUPerc}}" "$container" 2>/dev/null | tr -d '%')
    
    if [ -n "$cpu_percent" ]; then
        if (( $(echo "$cpu_percent > $CPU_THRESHOLD" | bc -l 2>/dev/null || echo 0) )); then
            log_warn "⚠️  容器 $container CPU 使用率过高：${cpu_percent}% (阈值：${CPU_THRESHOLD}%)"
            return 1
        fi
        log_info "✅ 容器 $container CPU：${cpu_percent}%"
    fi
    
    return 0
}

# 清理悬空镜像
cleanup_images() {
    log_info "🧹 清理悬空镜像..."
    local freed=$(docker image prune -f 2>/dev/null | tail -1)
    log_info "清理结果：$freed"
}

# 生成资源报告
generate_report() {
    log_info "=========================================="
    log_info "Docker 资源使用报告"
    log_info "=========================================="
    
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}" 2>/dev/null | while read line; do
        log_info "$line"
    done
    
    log_info "=========================================="
}

# 主函数
main() {
    log_info "=========================================="
    log_info "Docker 资源监控"
    log_info "=========================================="
    
    local issues=0
    
    # 检查所有运行中的容器
    for container in $(docker ps --format '{{.Names}}'); do
        check_memory "$container" || issues=$((issues + 1))
        check_cpu "$container" || issues=$((issues + 1))
    done
    
    # 检查磁盘
    check_disk || issues=$((issues + 1))
    
    # 生成报告
    generate_report
    
    # 总结
    if [ $issues -eq 0 ]; then
        log_info "✅ 资源监控正常，无告警"
    else
        log_warn "⚠️  发现 $issues 个资源告警"
    fi
}

main "$@"
