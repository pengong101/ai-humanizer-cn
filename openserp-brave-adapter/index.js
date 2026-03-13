#!/usr/bin/env node
/**
 * OpenSERP to Brave Search API Compatibility Adapter
 * 
 * 将 OpenSERP 搜索结果转换为 Brave Search API 兼容格式
 * 使 OpenClaw 等工具无需修改源码即可使用 OpenSERP
 * 
 * @author OpenClaw Team
 * @license MIT
 */

const http = require('http');
const https = require('https');
const { URL } = require('url');

// ============================================
// 配置
// ============================================
const CONFIG = {
  PORT: process.env.PORT || 8765,
  OPENSERP_BASE_URL: process.env.OPENSERP_BASE_URL || 'http://localhost:8080',
  OPENSERP_API_KEY: process.env.OPENSERP_API_KEY || '',
  BRAVE_API_KEY: process.env.BRAVE_API_KEY || 'dummy-key',
  TIMEOUT_MS: parseInt(process.env.REQUEST_TIMEOUT || '10000', 10),
  ENABLE_CORS: process.env.ENABLE_CORS !== 'false',
  LOG_LEVEL: process.env.LOG_LEVEL || 'info', // debug, info, warn, error
};

// ============================================
// 日志工具
// ============================================
const LOG_LEVELS = { debug: 0, info: 1, warn: 2, error: 3 };
const currentLogLevel = LOG_LEVELS[CONFIG.LOG_LEVEL] || 1;

function log(level, ...args) {
  if (LOG_LEVELS[level] >= currentLogLevel) {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] [${level.toUpperCase()}]`, ...args);
  }
}

// ============================================
// HTTP 请求工具
// ============================================
function httpGet(url, options = {}) {
  return new Promise((resolve, reject) => {
    const lib = url.startsWith('https') ? https : http;
    const reqUrl = new URL(url);
    
    const req = lib.get(url, {
      headers: {
        'Accept': 'application/json',
        'User-Agent': 'OpenSERP-Brave-Adapter/1.0',
        ...(options.headers || {}),
      },
      timeout: CONFIG.TIMEOUT_MS,
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve({
            status: res.statusCode,
            headers: res.headers,
            data: data ? JSON.parse(data) : null,
          });
        } catch (e) {
          reject(new Error(`JSON parse error: ${e.message}`));
        }
      });
    });
    
    req.on('error', (err) => {
      reject(new Error(`Request failed: ${err.message}`));
    });
    
    req.setTimeout(CONFIG.TIMEOUT_MS, () => {
      req.destroy();
      reject(new Error(`Request timeout (${CONFIG.TIMEOUT_MS}ms)`));
    });
  });
}

// ============================================
// OpenSERP API 调用
// ============================================
async function callOpenSERP(query, options = {}) {
  const { count = 10, country = 'US', search_lang, freshness } = options;
  
  const params = new URLSearchParams({
    q: query,
    num: Math.min(count, 10).toString(),
    gl: country.toLowerCase(),
  });
  
  // 语言参数
  if (search_lang) {
    const lang = search_lang.split('-')[0];
    params.append('hl', lang);
  }
  
  // 时间过滤 (freshness: pd/pw/pm/py)
  if (freshness) {
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
  
  log('debug', 'Calling OpenSERP:', url);
  
  const headers = {};
  if (CONFIG.OPENSERP_API_KEY) {
    headers['Authorization'] = `Bearer ${CONFIG.OPENSERP_API_KEY}`;
  }
  
  const response = await httpGet(url, { headers });
  
  if (response.status !== 200) {
    throw new Error(`OpenSERP returned status ${response.status}`);
  }
  
  return response.data;
}

// ============================================
// 响应格式转换
// ============================================
function transformToBraveFormat(openserpData) {
  // 支持多种 OpenSERP 响应格式
  let rawResults = [];
  
  if (Array.isArray(openserpData)) {
    rawResults = openserpData;
  } else if (openserpData.results && Array.isArray(openserpData.results)) {
    rawResults = openserpData.results;
  } else if (openserpData.organic && Array.isArray(openserpData.organic)) {
    rawResults = openserpData.organic;
  } else if (openserpData.data && Array.isArray(openserpData.data)) {
    rawResults = openserpData.data;
  }
  
  // 转换并限制最多 10 条结果
  const results = rawResults.slice(0, 10).map(item => ({
    title: item.title || item.name || '无标题',
    url: item.url || item.link || item.displayUrl || '',
    description: item.snippet || item.description || item.summary || item.abstract || '',
  }));
  
  // Brave API 兼容格式
  return {
    web: {
      results: results,
    },
    type: 'search',
  };
}

// ============================================
// HTTP 请求处理
// ============================================
async function handleRequest(req, res) {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const startTime = Date.now();
  
  // CORS 头
  if (CONFIG.ENABLE_CORS) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, Accept, X-Api-Key');
  }
  
  // OPTIONS 预检请求
  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }
  
  // 健康检查端点
  if (url.pathname === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      status: 'ok',
      timestamp: new Date().toISOString(),
      openserpUrl: CONFIG.OPENSERP_BASE_URL,
    }));
    return;
  }
  
  // 只处理 /search 端点
  if (url.pathname !== '/search') {
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Not found', path: url.pathname }));
    return;
  }
  
  // 只支持 GET 和 POST
  if (!['GET', 'POST'].includes(req.method)) {
    res.writeHead(405, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Method not allowed' }));
    return;
  }
  
  // API Key 验证（模拟 Brave API）
  const authHeader = req.headers.authorization || req.headers['x-api-key'] || '';
  const apiKey = authHeader.replace('Bearer ', '').trim();
  
  if (apiKey && apiKey !== CONFIG.BRAVE_API_KEY && CONFIG.BRAVE_API_KEY !== 'dummy-key') {
    log('warn', 'Invalid API key attempt');
    res.writeHead(401, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Invalid API key' }));
    return;
  }
  
  try {
    // 解析查询参数
    let queryParams = {};
    
    if (req.method === 'POST') {
      // POST 请求从 body 解析
      const body = await new Promise((resolve, reject) => {
        let data = '';
        req.on('data', chunk => data += chunk);
        req.on('end', () => resolve(data));
        req.on('error', reject);
      });
      
      try {
        queryParams = JSON.parse(body);
      } catch (e) {
        // 如果不是 JSON，尝试解析为 URLSearchParams
        queryParams = Object.fromEntries(new URLSearchParams(body));
      }
    } else {
      // GET 请求从 URL 解析
      queryParams = Object.fromEntries(url.searchParams);
    }
    
    const query = queryParams.q || queryParams.query;
    const count = parseInt(queryParams.count || queryParams.num || '10', 10);
    const country = queryParams.country || queryParams.gl || 'US';
    const search_lang = queryParams.search_lang || queryParams.hl;
    const freshness = queryParams.freshness || queryParams.tbs;
    
    if (!query) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'Missing query parameter', required: 'q or query' }));
      return;
    }
    
    log('info', `Search: "${query}" (count=${count}, country=${country})`);
    
    // 调用 OpenSERP
    const openserpData = await callOpenSERP(query, {
      count: Math.min(count, 10),
      country,
      search_lang,
      freshness,
    });
    
    // 转换为 Brave 格式
    const braveFormat = transformToBraveFormat(openserpData);
    
    // 计算响应时间
    const duration = Date.now() - startTime;
    log('info', `Response: ${braveFormat.web?.results?.length || 0} results in ${duration}ms`);
    
    // 返回结果
    res.writeHead(200, { 
      'Content-Type': 'application/json',
      'X-Response-Time': `${duration}ms`,
    });
    res.end(JSON.stringify(braveFormat));
    
  } catch (error) {
    const duration = Date.now() - startTime;
    log('error', `Error: ${error.message} (${duration}ms)`);
    
    res.writeHead(500, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ 
      error: error.message,
      type: error.constructor.name,
      duration: `${duration}ms`,
    }));
  }
}

// ============================================
// 启动服务器
// ============================================
const server = http.createServer(handleRequest);

server.listen(CONFIG.PORT, () => {
  log('info', '🚀 OpenSERP Brave Adapter started');
  log('info', `📡 Listening on port ${CONFIG.PORT}`);
  log('info', `🔗 OpenSERP backend: ${CONFIG.OPENSERP_BASE_URL}`);
  log('info', `🔑 API Key validation: ${CONFIG.BRAVE_API_KEY !== 'dummy-key' ? 'enabled' : 'disabled (dummy mode)'}`);
  log('info', `⏱️  Request timeout: ${CONFIG.TIMEOUT_MS}ms`);
  log('info', '');
  log('info', 'Test endpoints:');
  log('info', `  - Health: http://localhost:${CONFIG.PORT}/health`);
  log('info', `  - Search: http://localhost:${CONFIG.PORT}/search?q=test`);
});

// 优雅关闭
process.on('SIGTERM', () => {
  log('info', 'SIGTERM received, shutting down...');
  server.close(() => {
    log('info', 'Server closed');
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  log('info', 'SIGINT received, shutting down...');
  server.close(() => {
    log('info', 'Server closed');
    process.exit(0);
  });
});

// 错误处理
server.on('error', (err) => {
  log('error', 'Server error:', err);
  process.exit(1);
});
