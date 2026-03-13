# 🔍 SearXNG 搜索功能部署工作计划

**基于：** GitHub 账号 `小马 🐴`  
**目标：** 部署可用的搜索功能  
**当前环境：** Alpine Linux（无 Docker）  
**日期：** 2026-03-09 13:54 (Asia/Shanghai)

---

## 📊 当前状态分析

### 已有资源
| 资源 | 状态 | 位置 |
|------|------|------|
| GitHub 账号 | ✅ 小马 🐴 | - |
| GitHub Token | ✅ [GITHUB_TOKEN_REDACTED] | 已配置 |
| 适配器代码 | ✅ OpenSERP Brave Adapter | `/root/.openclaw/workspace/openserp-brave-adapter/` |
| 中国大陆版本 | ✅ index-cn-v2.js | 使用 DuckDuckGo HTML |
| GitHub 仓库 | ✅ 已发布 11 个文件 | https://github.com/小马 🐴/openserp-brave-adapter |

### 环境限制
| 组件 | 状态 | 影响 |
|------|------|------|
| Docker | ❌ 不可用 | 无法自建 SearXNG |
| Brave API | ❌ 需要 VPN+ 付费 | 不适合中国大陆 |
| SearXNG 公共实例 | ❌ 超时 | 网络限制 |
| OpenClaw web_search | ❌ 未配置 | 需要配置 |

---

## 🎯 工作方案（3 选 1）

### 方案 A：使用 DuckDuckGo HTML（推荐，立即可用）

**优势:**
- ✅ 无需 Docker
- ✅ 无需额外部署
- ✅ 中国大陆可访问
- ✅ 代码已准备好

**步骤:**
```bash
# 1. 启动适配器（1 分钟）
cd /root/.openclaw/workspace/openserp-brave-adapter
node index-cn-v2.js &

# 2. 配置 OpenClaw（2 分钟）
# 编辑 ~/.openclaw/openclaw.json

# 3. 重启 Gateway（1 分钟）
openclaw gateway restart

# 4. 测试搜索
# 在对话中发送："搜索 2026 毫米波研究进展"
```

**预计时间:** 5 分钟  
**推荐度:** ⭐⭐⭐⭐⭐

---

### 方案 B：安装 Docker 后部署 SearXNG

**优势:**
- ✅ 完全自托管
- ✅ 数据可控
- ✅ 支持多搜索引擎

**步骤:**
```bash
# 1. 安装 Docker（需要 root 权限）
# Alpine Linux:
apk add --no-cache docker docker-compose

# 2. 启动 Docker 服务
service docker start

# 3. 部署 SearXNG（参考 SEARXNG-SETUP-GUIDE.md）
mkdir -p ~/searxng && cd ~/searxng
# 创建 docker-compose.yml 和 settings.yml
docker-compose up -d

# 4. 配置适配器
export OPENSERP_BASE_URL=http://localhost:8080
node index.js &

# 5. 配置 OpenClaw 并测试
```

**预计时间:** 30-60 分钟  
**推荐度:** ⭐⭐⭐⭐  
**前提:** 需要 root 权限安装 Docker

---

### 方案 C：使用公共 SearXNG 实例

**优势:**
- ✅ 无需部署
- ✅ 快速测试

**劣势:**
- ⚠️ 中国大陆访问不稳定
- ⚠️ 可能超时

**可用实例:**
| 实例 | 地址 | 状态 |
|------|------|------|
| 日本 | https://search.ononoki.org | ⚠️ 可能慢 |
| 欧洲 | https://searx.be | ❌ 超时 |

**预计时间:** 10 分钟  
**推荐度:** ⭐⭐⭐

---

## 📋 推荐执行计划

### 阶段 1：立即可用（5 分钟）🔴

**目标：** 快速恢复搜索功能

```bash
# Step 1: 启动中国大陆版适配器
cd /root/.openclaw/workspace/openserp-brave-adapter
nohup node index-cn-v2.js > /tmp/adapter.log 2>&1 &

# Step 2: 验证适配器
sleep 3
wget -qO- http://localhost:8765/health

# Step 3: 配置 OpenClaw
# 编辑 ~/.openclaw/openclaw.json，添加：
{
  "tools": {
    "web": {
      "search": {
        "provider": "brave",
        "baseUrl": "http://localhost:8765",
        "apiKey": "dummy-key"
      }
    }
  }
}

# Step 4: 重启 Gateway
openclaw gateway restart

# Step 5: 测试搜索
# 在对话中发送："搜索 2026 毫米波雷达研究进展"
```

**交付:** 可用的搜索功能

---

### 阶段 2：推送中国大陆版本到 GitHub（10 分钟）🟡

**目标：** 将 `index-cn-v2.js` 推送到 GitHub

```bash
# Step 1: 准备推送脚本
# 使用已有的 github-push.js 或创建新脚本

# Step 2: 推送文件
# - index-cn-v2.js
# - 更新 README.md 添加中国大陆版本说明

# Step 3: 验证 GitHub 仓库
# 访问 https://github.com/小马 🐴/openserp-brave-adapter
```

**交付:** GitHub 仓库包含中国大陆版本

---

### 阶段 3：长期方案（可选）🟢

**选项 1:** 安装 Docker，部署 SearXNG
**选项 2:** 申请百度/必应 API
**选项 3:** 配置 GitHub Actions 自动测试

---

## 🔧 详细配置步骤

### OpenClaw 配置

编辑 `~/.openclaw/openclaw.json`:

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "bailian": {
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "apiKey": "sk-sp-8e9b8f63afc44bc4a2ce31ddfbf23430",
        "api": "openai-completions",
        "models": [
          {
            "id": "qwen3.5-plus",
            "name": "Qwen3.5-Plus",
            "reasoning": true,
            "input": ["text", "image"],
            "cost": {"input": 0, "output": 0},
            "contextWindow": 1000000,
            "maxTokens": 65536
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "bailian/qwen3.5-plus"
      }
    }
  },
  "commands": {
    "native": "auto",
    "nativeSkills": "auto",
    "restart": true,
    "ownerDisplay": "raw"
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "dmPolicy": "open",
      "allowFrom": [
        "ou_108c6b29eb9946e2cf1090f76fdd6f17",
        "ou_21b87bbbcb0a643b2e6e5976c02c580c"
      ],
      "groupPolicy": "open",
      "connectionMode": "websocket",
      "accounts": {
        "main": {
          "appId": "cli_a92012e60cf9dcc0",
          "appSecret": "UbK9vNsfxJtrCobOnep9WbaHWO1dp3E0",
          "botName": "小马 AI 助手",
          "enabled": true
        }
      }
    }
  },
  "gateway": {
    "mode": "local",
    "auth": {
      "mode": "token",
      "token": "xiaoma-token-2026"
    }
  },
  "plugins": {
    "entries": {
      "feishu": {
        "enabled": true
      }
    }
  },
  "tools": {
    "web": {
      "search": {
        "provider": "brave",
        "baseUrl": "http://localhost:8765",
        "apiKey": "dummy-key"
      }
    }
  }
}
```

---

## ✅ 验收标准

### 阶段 1 验收
- [ ] 适配器运行在 8765 端口
- [ ] 健康检查端点正常响应
- [ ] OpenClaw 配置已更新
- [ ] Gateway 已重启
- [ ] 可以执行搜索任务

### 阶段 2 验收
- [ ] `index-cn-v2.js` 已推送到 GitHub
- [ ] README.md 已更新
- [ ] GitHub 仓库显示最新提交

---

## 📞 执行建议

**立即执行：** 阶段 1（5 分钟）
- 使用 DuckDuckGo HTML 版本
- 无需额外部署
- 立即可用

**后续考虑：** 阶段 2（10 分钟）
- 完善 GitHub 仓库
- 添加中国大陆版本说明

**长期规划：** 阶段 3（可选）
- 根据实际需求选择

---

**需要我立即执行阶段 1 吗？** 🐴
