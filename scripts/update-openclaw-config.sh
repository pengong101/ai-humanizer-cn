#!/bin/bash
# OpenClaw 配置更新脚本 - 启用 SearXNG 搜索
# 执行方式：在 NAS 宿主机上运行此脚本

set -e

echo "=========================================="
echo "🔧 OpenClaw 配置更新 - 启用 SearXNG"
echo "=========================================="
echo ""

CONFIG_FILE="/root/.openclaw/openclaw.json"
BACKUP_DIR="/root/.openclaw/config-backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 检查配置文件
if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}❌ 配置文件不存在：${CONFIG_FILE}${NC}"
    exit 1
fi

echo "📁 配置文件：${CONFIG_FILE}"
echo ""

# 备份配置
echo "💾 备份当前配置..."
mkdir -p "$BACKUP_DIR"
cp "$CONFIG_FILE" "${BACKUP_DIR}/openclaw_backup_${TIMESTAMP}.json"
echo -e "${GREEN}✅${NC} 备份完成：${BACKUP_DIR}/openclaw_backup_${TIMESTAMP}.json"
echo ""

# 解锁配置文件（如果是只读）
if [ ! -w "$CONFIG_FILE" ]; then
    echo "🔓 解锁配置文件..."
    chmod 644 "$CONFIG_FILE"
fi

# 使用 Python 更新配置
echo "✏️  更新配置..."

python3 << 'PYTHON_SCRIPT'
import json
import sys

config_file = "/root/.openclaw/openclaw.json"

try:
    # 读取配置
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 更新 plugins 配置
    if 'plugins' not in config:
        config['plugins'] = {'entries': {}}
    
    if 'entries' not in config['plugins']:
        config['plugins']['entries'] = {}
    
    # 添加/更新 SearXNG 配置
    config['plugins']['entries']['searxng'] = {
        'enabled': True,
        'config': {
            'url': 'http://searxng:8080',
            'engines': ['google', 'baidu', 'bing', 'duckduckgo', 'wikipedia', 'brave'],
            'timeout': 10,
            'max_results': 20
        }
    }
    
    # 确保 feishu 插件启用
    config['plugins']['entries']['feishu'] = {
        'enabled': True
    }
    
    # 写回配置
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.write('\n')
    
    print("✅ 配置更新成功")
    
except Exception as e:
    print(f"❌ 配置更新失败：{e}", file=sys.stderr)
    sys.exit(1)
PYTHON_SCRIPT

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ 配置更新失败${NC}"
    echo "正在恢复备份..."
    cp "${BACKUP_DIR}/openclaw_backup_${TIMESTAMP}.json" "$CONFIG_FILE"
    exit 1
fi

echo ""

# 验证配置
echo "🔍 验证配置..."
if python3 -m json.tool "$CONFIG_FILE" >/dev/null 2>&1; then
    echo -e "${GREEN}✅${NC} JSON 格式验证通过"
else
    echo -e "${RED}❌${NC} JSON 格式验证失败"
    echo "正在恢复备份..."
    cp "${BACKUP_DIR}/openclaw_backup_${TIMESTAMP}.json" "$CONFIG_FILE"
    exit 1
fi

# 重新锁定配置文件
echo "🔒 锁定配置文件..."
chmod 444 "$CONFIG_FILE"

echo ""
echo "=========================================="
echo "✅ 配置更新完成！"
echo "=========================================="
echo ""
echo "📋 下一步操作："
echo ""
echo "1. 重启 OpenClaw 容器使配置生效："
echo "   docker restart xiaoma_new"
echo ""
echo "2. 验证搜索功能："
echo "   在飞书中发送：搜索 OpenClaw"
echo ""
echo "3. 查看日志（如有问题）："
echo "   docker logs xiaoma_new --tail 50"
echo ""
echo "=========================================="
