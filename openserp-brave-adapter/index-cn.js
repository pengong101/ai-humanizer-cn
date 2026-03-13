#!/usr/bin/env node
/**
 * OpenSERP Brave Adapter - 中国大陆紧急版
 * 使用国内可访问的搜索源
 */

const http = require('http');
const https = require('https');
const { URL } = require('url');

const CONFIG = {
  PORT: process.env.PORT || 8765,
  TIMEOUT_MS: 15000,
};

// 国内可用的搜索源
const SEARCH_SOURCES = [
  { name: 'Bing CN', url: 'https://www.bing.com/search', enabled: true },
  { name: 'Baidu', url: 'https://www.baidu.com/s', enabled: true },
];

function log(level, ...args) {
  const ts = new Date().toISOString();
  console.log(`[${ts}] [${level}]`, ...args);
}

// 简单的 HTML 解析提取搜索结果
function parseBingResults(html) {
  const results = [];
  const resultRegex = /<li class="b_algo"[^>]*>([\s\S]*?)<\/li>/g;
  let match;
  
  while ((match = resultRegex.exec(html)) !== null && results.length < 10) {
    const item = match[1];
    const titleMatch = item.match(/<h2[^>]*><a[^>]*href="([^"]*)"[^>]*>([^<]*)<\/a>/i);
    const descMatch = item.match(/<div class="b_caption"[^>]*>([\s\S]*?)<\/div>/i);
    
    if (titleMatch) {
      results.push({
        title: titleMatch[2].replace(/&[^;]+;/g, s => {
          const entities = { '&lt;': '<', '&gt;': '>', '&amp;': '&', '&quot;': '"' };
          return entities[s] || s;
        }),
        url: titleMatch[1],
        description: descMatch ? descMatch[1].replace(/<[^>]*>/g, '').substring(0, 200) : '',
      });
    }
  }
  
  return results;
}

function searchBing(query, count = 10) {
  return new Promise((resolve, reject) => {
    const searchUrl = `https://www.bing.com/search?q=${encodeURIComponent(query)}&first=1&count=${count}`;
    log('debug', 'Searching Bing:', searchUrl);
    
    const url = new URL(searchUrl);
    const req = https.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
      },
      timeout: CONFIG.TIMEOUT_MS,
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const results = parseBingResults(data);
          resolve({ results });
        } catch (e) {
          reject(new Error(`Parse error: ${e.message}`));
        }
      });
    });
    
    req.on('error', reject);
    req.setTimeout(CONFIG.TIMEOUT_MS, () => {
      req.destroy();
      reject(new Error('Bing search timeout'));
    });
  });
}

function transformToBraveFormat(searchData) {
  const results = (searchData.results || []).slice(0, 10).map(item => ({
    title: item.title || '无标题',
    url: item.url || '',
    description: item.description || item.snippet || '',
  }));
  
  return {
    web: { results },
    type: 'search',
  };
}

async function handleRequest(req, res) {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const startTime = Date.now();
  
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, Accept');
  
  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }
  
  if (url.pathname === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      status: 'ok',
      timestamp: new Date().toISOString(),
      sources: SEARCH_SOURCES.filter(s => s.enabled).map(s => s.name),
    }));
    return;
  }
  
  if (url.pathname !== '/search') {
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Not found' }));
    return;
  }
  
  if (!['GET', 'POST'].includes(req.method)) {
    res.writeHead(405, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Method not allowed' }));
    return;
  }
  
  try {
    let queryParams = {};
    
    if (req.method === 'POST') {
      const body = await new Promise((resolve, reject) => {
        let data = '';
        req.on('data', chunk => data += chunk);
        req.on('end', () => resolve(data));
        req.on('error', reject);
      });
      try {
        queryParams = JSON.parse(body);
      } catch (e) {
        queryParams = Object.fromEntries(new URLSearchParams(body));
      }
    } else {
      queryParams = Object.fromEntries(url.searchParams);
    }
    
    const query = queryParams.q || queryParams.query;
    const count = parseInt(queryParams.count || queryParams.num || '10', 10);
    
    if (!query) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'Missing query parameter' }));
      return;
    }
    
    log('info', `Search: "${query}" (count=${count})`);
    
    // 使用 Bing 搜索
    const searchData = await searchBing(query, Math.min(count, 10));
    const braveFormat = transformToBraveFormat(searchData);
    
    const duration = Date.now() - startTime;
    log('info', `Response: ${braveFormat.web?.results?.length || 0} results in ${duration}ms`);
    
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

const server = http.createServer(handleRequest);

server.listen(CONFIG.PORT, () => {
  log('info', '🚀 OpenSERP Brave Adapter CN started');
  log('info', `📡 Listening on port ${CONFIG.PORT}`);
  log('info', `🔗 Search sources: ${SEARCH_SOURCES.filter(s => s.enabled).map(s => s.name).join(', ')}`);
  log('info', '');
  log('info', 'Test: http://localhost:' + CONFIG.PORT + '/search?q=test');
});
