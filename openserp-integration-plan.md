# OpenSERP 集成到 OpenClaw 完整方案

## 📋 执行摘要

本方案提供将 OpenSERP（开源搜索 API 服务）集成到 OpenClaw 的完整实现，使 OpenClaw 的 `web_search` 工具能够使用自托管的 OpenSERP 服务替代 Brave Search API。

**推荐方案：方案 B - Brave API 兼容适配层**
- ✅ 无需修改 OpenClaw 源码
- ✅ 快速部署验证（1-2 小时）
- ✅ 易于维护和升级
- ✅ 可独立发布为 npm 包

---

## 🔍 核心发现

### 1. OpenClaw web_search 架构

**支持的搜索提供商：**
- `brave` - Brave Search API
- `perplexity` - Perplexity API
- `grok` - xAI Grok API  
- `gemini` - Google Gemini API
- `kimi` - Moonshot Kimi API

**配置位置：** `~/.openclaw/openclaw.json`
```json
{
  "tools": {
    "web": {
      "search": {
        "provider": "brave",
        "apiKey": "${BRAVE_API_KEY}"
      }
    }
  }
}
```

**工具参数：**
- `query` (必填) - 搜索查询
- `count` (可选) - 结果数量 (1-10)
- `country` (可选) - 国家代码 (e.g., "US", "CN")
- `search_lang` (可选) - 搜索语言
- `freshness` (可选) - 时间过滤 (pd/pw/pm/py)

### 2. Brave API 响应格式

```json
{
  "web": {
    "results": [
      {
        "title": "页面标题",
        "url": "https://example.com",
        "description": "搜索结果摘要..."
      }
    ]
  }
}
```

### 3. OpenSERP API 响应格式

OpenSERP 通常返回类似格式（以实际部署为准）：
```json
{
  "results": [
    {
      "title": "页面标题",
      "url": "https://example.com",
      "snippet": "搜索结果摘要..."
    }
  ]
}
```

**字段映射：**
- `title` → `title` ✅
- `url` → `url` ✅
- `snippet` → `description` (需映射)

---

## 🛠️ 实施方案

### 方案 A：OpenClaw 源码新增 openserp 提供商（不推荐）

**优点：**
- 原生集成
- 性能最优

**缺点：**
- 需要修改 OpenClaw 源码
- 每次 OpenClaw 升级需要重新合并
- 维护成本高

**实施步骤：**
1. 在 OpenClaw 源码中添加 `openserp` 到 `SEARCH_PROVIDERS`
2. 实现 OpenSERP API 调用逻辑
3. 添加配置字段支持
4. 重新构建 OpenClaw

---

### 方案 B：Brave API 兼容适配层（⭐ 推荐）

**核心思路：** 创建一个 HTTP 代理服务，将 OpenSERP 的响应格式转换为 Brave API 兼容格式。

**优点：**
- 无需修改 OpenClaw 源码
- 独立部署，易于维护
- 可复用给其他需要 Brave API 兼容的项目
- OpenClaw 配置无需改动（只需改 API 端点）

**缺点：**
- 需要额外部署一个服务
- 增加一次网络跳转（延迟 +10-50ms）

#### 架构设计

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│  OpenClaw   │────▶│  OpenSERP Proxy  │────▶│  OpenSERP   │
│ web_search  │     │  (适配层)         │     │   Service   │
└─────────────┘     └──────────────────┘     └─────────────┘
     │                      │                      │
     │ Brave API Format     │ Brave API Format     │ OpenSERP
     │                      │ (转换后)              │ Format
     └──────────────────────┴──────────────────────┘
                          响应转换
```

#### 实现代码

**文件：`openserp-brave-adapter/index.js`**

```javascript
#!/usr/bin/env node
/**
 * OpenSERP to Brave API Compatibility Adapter
 * 
 * 将 OpenSERP 搜索结果转换为 Brave Search API 兼容格式
 * 使 OpenClaw 等工具无需修改即可使用 OpenSERP
 */

const http = require('http');
const https = require('https');
const { URL } = require('url');

// 配置
const CONFIG = {
  PORT: process.env.PORT || 8765,
  OPENSERP_BASE_URL: process.env.OPENSERP_BASE_URL || 'http://localhost:8080',
  OPENSERP_API_KEY: process.env.OPENSERP_API_KEY || '',
  BRAVE_API_KEY: process.env.BRAVE_API_KEY || 'dummy-key', // 用于验证
};

/**
 * 调用 OpenSERP API
 */
async function callOpenSERP(query, options = {}) {
  const { count = 10, country = 'US', search_lang, freshness } = options;
  
  // 构建 OpenSERP 请求参数
  const params = new URLSearchParams({
    q: query,
    num: count.toString(),
    gl: country.toLowerCase(),
  });
  
  if (search_lang) {
    params.append('hl', search_lang.split('-')[0]);
  }
  
  if (freshness) {
    // 映射 freshness 到 OpenSERP 的时间过滤
    const freshnessMap = {
      'pd': 'd',  // past day
      'pw': 'w',  // past week
      'pm': 'm',  // past month
      'py': 'y',  // past year
    };
    if (freshnessMap[freshness]) {
      params.append('tbs', `qdr:${freshnessMap[freshness]}`);
    }
  }
  
  const url = `${CONFIG.OPENSERP_BASE_URL}/search?${params.toString()}`;
  
  return new Promise((resolve, reject) => {
    const lib = url.startsWith('https') ? https : http;
    
    const req = lib.get(url, {
      headers: {
        'Authorization': CONFIG.OPENSERP_API_KEY ? `Bearer ${CONFIG.OPENSERP_API_KEY}` : '',
        'Accept': 'application/json',
      },
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error(`Failed to parse OpenSERP response: ${e.message}`));
        }
      });
    });
    
    req.on('error', reject);
    req.setTimeout(10000, () => {
      req.destroy();
      reject(new Error('OpenSERP request timeout'));
    });
  });
}

/**
 * 将 OpenSERP 响应转换为 Brave API 格式
 */
function transformToBraveFormat(openserpData) {
  // 根据实际 OpenSERP 响应格式调整
  const rawResults = openserpData.results || openserpData.organic || [];
  
  const results = rawResults.slice(0, 10).map(item => ({
    title: item.title || '无标题',
    url: item.url || item.link || '',
    description: item.snippet || item.description || item.summary || '',
  }));
  
  return {
    web: {
      results: results,
    },
    // 添加一些 Brave API 常见的元字段（可选）
    type: 'search',
  };
}

/**
 * HTTP 请求处理器
 */
async function handleRequest(req, res) {
  const url = new URL(req.url, `http://${req.headers.host}`);
  
  // CORS 头
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, Accept');
  
  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }
  
  // 只处理 /search 端点
  if (url.pathname !== '/search') {
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Not found' }));
    return;
  }
  
  // 验证 API Key（模拟 Brave API 验证）
  const authHeader = req.headers.authorization || '';
  const apiKey = authHeader.replace('Bearer ', '');
  
  if (apiKey && apiKey !== CONFIG.BRAVE_API_KEY && CONFIG.BRAVE_API_KEY !== 'dummy-key') {
    res.writeHead(401, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Invalid API key' }));
    return;
  }
  
  try {
    // 解析查询参数
    const query = url.searchParams.get('q');
    const count = parseInt(url.searchParams.get('count') || '10', 10);
    const country = url.searchParams.get('country') || 'US';
    const search_lang = url.searchParams.get('search_lang');
    const freshness = url.searchParams.get('freshness');
    
    if (!query) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'Missing query parameter' }));
      return;
    }
    
    // 调用 OpenSERP
    const openserpData = await callOpenSERP(query, {
      count: Math.min(count, 10),
      country,
      search_lang,
      freshness,
    });
    
    // 转换为 Brave 格式
    const braveFormat = transformToBraveFormat(openserpData);
    
    // 返回结果
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(braveFormat));
    
  } catch (error) {
    console.error('Error:', error.message);
    res.writeHead(500, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ 
      error: error.message,
      type: error.constructor.name 
    }));
  }
}

// 启动服务器
const server = http.createServer(handleRequest);

server.listen(CONFIG.PORT, () => {
  console.log(`🚀 OpenSERP Brave Adapter running on port ${CONFIG.PORT}`);
  console.log(`📡 OpenSERP backend: ${CONFIG.OPENSERP_BASE_URL}`);
  console.log(`🔑 API Key validation: ${CONFIG.BRAVE_API_KEY !== 'dummy-key' ? 'enabled' : 'disabled'}`);
});
```

**文件：`openserp-brave-adapter/package.json`**

```json
{
  "name": "openserp-brave-adapter",
  "version": "1.0.0",
  "description": "Brave Search API compatible adapter for OpenSERP",
  "main": "index.js",
  "bin": {
    "openserp-adapter": "./index.js"
  },
  "scripts": {
    "start": "node index.js",
    "dev": "node --watch index.js"
  },
  "keywords": [
    "openserp",
    "brave-search",
    "search-api",
    "adapter"
  ],
  "author": "",
  "license": "MIT",
  "engines": {
    "node": ">=18.0.0"
  }
}
```

**文件：`openserp-brave-adapter/README.md`**

```markdown
# OpenSERP Brave Adapter

将 OpenSERP 搜索结果转换为 Brave Search API 兼容格式。

## 快速开始

```bash
# 安装依赖（无外部依赖）
npm install

# 配置环境变量
export OPENSERP_BASE_URL=http://your-openserp-server:8080
export OPENSERP_API_KEY=your-api-key  # 可选
export PORT=8765

# 启动服务
npm start
```

## OpenClaw 配置

在 `~/.openclaw/openclaw.json` 中配置：

```json
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
```

## API 端点

- `GET /search?q=query&count=10&country=US` - 搜索接口

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `PORT` | 8765 | 服务端口 |
| `OPENSERP_BASE_URL` | http://localhost:8080 | OpenSERP 后端地址 |
| `OPENSERP_API_KEY` | - | OpenSERP API 密钥（可选） |
| `BRAVE_API_KEY` | dummy-key | 用于验证的 API 密钥 |
```

---

### 方案 C：OpenSERP 原生 Brave 兼容模式（需 OpenSERP 支持）

如果 OpenSERP 本身支持 Brave API 兼容端点，可直接配置：

```bash
# 在 OpenSERP 配置中启用 Brave 兼容模式
export OPENSERP_BRAVE_COMPAT=true
```

然后在 OpenClaw 中直接配置：
```json
{
  "tools": {
    "web": {
      "search": {
        "provider": "brave",
        "baseUrl": "http://your-openserp-server:8080",
        "apiKey": "your-key"
      }
    }
  }
}
```

---

## 📦 部署指南

### 1. 本地开发测试

```bash
# 1. 克隆/创建适配器项目
mkdir openserp-brave-adapter
cd openserp-brave-adapter

# 2. 创建文件（见上方代码）
# index.js, package.json, README.md

# 3. 启动服务
export OPENSERP_BASE_URL=http://localhost:8080
npm start

# 4. 测试端点
curl "http://localhost:8765/search?q=test&count=5"
```

### 2. Docker 部署

**文件：`Dockerfile`**

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package.json index.js ./

EXPOSE 8765

ENV PORT=8765
ENV OPENSERP_BASE_URL=http://host.docker.internal:8080

CMD ["node", "index.js"]
```

**文件：`docker-compose.yml`**

```yaml
version: '3.8'

services:
  openserp-adapter:
    build: .
    ports:
      - "8765:8765"
    environment:
      - OPENSERP_BASE_URL=http://openserp:8080
      - OPENSERP_API_KEY=${OPENSERP_API_KEY}
    depends_on:
      - openserp
  
  openserp:
    image: openserp/openserp:latest
    ports:
      - "8080:8080"
    environment:
      - API_KEY=${OPENSERP_API_KEY}
```

### 3. OpenClaw 配置

**方式 1：修改配置文件**

编辑 `~/.openclaw/openclaw.json`：

```json
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
```

**方式 2：使用环境变量**

```bash
# 在 OpenClaw Gateway 环境中设置
export BRAVE_API_KEY=dummy-key
export BRAVE_BASE_URL=http://localhost:8765

# 重启 Gateway
openclaw gateway restart
```

---

## ✅ 测试验证

### 1. 适配器服务测试

```bash
# 测试基本搜索
curl -s "http://localhost:8765/search?q=OpenAI&count=3" | jq

# 预期输出
{
  "web": {
    "results": [
      {
        "title": "...",
        "url": "...",
        "description": "..."
      }
    ]
  }
}
```

### 2. OpenClaw web_search 测试

```javascript
// 在 OpenClaw 中测试
const result = await web_search({
  query: "OpenSERP integration",
  count: 5,
  country: "US"
});

console.log(result);
```

### 3. 端到端测试

1. 启动 OpenSERP 服务
2. 启动 OpenSERP Brave Adapter
3. 配置 OpenClaw 使用适配器
4. 重启 OpenClaw Gateway
5. 在对话中测试：`搜索一下 OpenSERP`

---

## ⚠️ 风险评估

| 风险 | 等级 | 缓解措施 |
|------|------|----------|
| OpenSERP 响应格式变化 | 中 | 在适配器中添加格式检测和多版本支持 |
| 适配器服务宕机 | 中 | 配置健康检查和自动重启 |
| 性能开销 | 低 | 增加响应缓存层 |
| OpenClaw 升级不兼容 | 低 | 适配器独立于 OpenClaw 版本 |

---

## 📅 实施路线图

### 短期（1-2 天）

- [ ] 创建 OpenSERP Brave Adapter 基础代码
- [ ] 本地测试验证
- [ ] 编写单元测试
- [ ] 文档完善

### 中期（1 周）

- [ ] Docker 容器化
- [ ] 添加监控和日志
- [ ] 性能优化（缓存、连接池）
- [ ] GitHub 仓库发布

### 长期（2-4 周）

- [ ] npm 包发布
- [ ] 多 OpenSERP 实例负载均衡
- [ ] 高级功能（结果去重、质量评分）
- [ ] 社区推广

---

## 📁 项目文件结构

```
openserp-integration/
├── openserp-brave-adapter/
│   ├── index.js           # 主程序
│   ├── package.json       # 项目配置
│   ├── README.md          # 使用说明
│   ├── Dockerfile         # 容器配置
│   ├── docker-compose.yml # 编排配置
│   └── test/
│       └── index.test.js  # 单元测试
├── docs/
│   ├── integration-guide.md    # 集成指南
│   └── troubleshooting.md      # 故障排查
├── examples/
│   └── openclaw-config.json    # OpenClaw 配置示例
└── README.md              # 项目总览
```

---

## 🔗 相关资源

- [OpenClaw 文档](https://docs.openclaw.ai/tools/web)
- [Brave Search API 文档](https://brave.com/search/api/)
- [OpenSERP GitHub](https://github.com/openserp/openserp)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)

---

## 👥 团队分工建议

| 角色 | 职责 |
|------|------|
| 后端工程师 | OpenSERP Brave Adapter 开发 |
| DevOps 工程师 | Docker 部署、CI/CD |
| 测试工程师 | 端到端测试、性能测试 |
| 技术文档 | 使用文档、API 文档 |

---

**方案总结：** 采用方案 B（Brave API 兼容适配层）是最快、最稳妥的实施路径。可在 1-2 天内完成 MVP，后续逐步完善。

**下一步：** 开始创建 `openserp-brave-adapter` 项目代码。
