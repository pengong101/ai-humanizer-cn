#!/usr/bin/env node
/**
 * OpenSERP Brave Adapter - 中国大陆紧急版 v2
 * 使用 DuckDuckGo HTML 接口（更易解析）
 */

const http = require('http');
const https = require('https');
const { URL } = require('url');

const CONFIG = {
  PORT: process.env.PORT || 8765,
  TIMEOUT_MS: 20000,
};

function log(level, ...args) {
  const ts = new Date().toISOString();
  console.log(`[${ts}] [${level}]`, ...args);
}

// DuckDuckGo HTML 搜索
function searchDuckDuckGo(query, count = 10) {
  return new Promise((resolve, reject) => {
    const searchUrl = `https://html.duckduckgo.com/html/?q=${encodeURIComponent(query)}`;
    log('debug', 'Searching DuckDuckGo:', searchUrl);
    
    const url = new URL(searchUrl);
    const req = https.post ? https.post(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      timeout: CONFIG.TIMEOUT_MS,
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const results = parseDuckDuckGoResults(data, count);
          resolve({ results });
        } catch (e) {
          reject(new Error(`Parse error: ${e.message}`));
        }
      });
    }) : https.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
      },
      timeout: CONFIG.TIMEOUT_MS,
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const results = parseDuckDuckGoResults(data, count);
          resolve({ results });
        } catch (e) {
          reject(new Error(`Parse error: ${e.message}`));
        }
      });
    });
    
    req.on('error', reject);
    req.setTimeout(CONFIG.TIMEOUT_MS, () => {
      req.destroy();
      reject(new Error('Search timeout'));
    });
  });
}

// 解析 DuckDuckGo HTML 结果
function parseDuckDuckGoResults(html, count) {
  const results = [];
  
  // 匹配搜索结果块
  const resultRegex = /<a[^>]*class="result__a"[^>]*href="([^"]*)"[^>]*>([^<]*)<\/a>/gi;
  const descRegex = /<a[^>]*class="result__snippet"[^>]*>([\s\S]*?)<\/a>/gi;
  
  let match;
  const urls = [];
  const titles = [];
  
  while ((match = resultRegex.exec(html)) !== null && titles.length < count) {
    urls.push(match[1]);
    titles.push(match[2].replace(/<[^>]*>/g, ''));
  }
  
  const descs = [];
  const descMatch = descRegex.exec(html);
  while ((match = descRegex.exec(html)) !== null) {
    descs.push(match[1].replace(/<[^>]*>/g, '').substring(0, 200));
  }
  
  for (let i = 0; i < Math.min(titles.length, count); i++) {
    results.push({
      title: titles[i] || '无标题',
      url: urls[i] || '',
      description: descs[i] || '',
    });
  }
  
  return results;
}

function transformToBraveFormat(searchData) {
  const results = (searchData.results || []).map(item => ({
    title: item.title || '无标题',
    url: item.url || '',
    description: item.description || '',
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
      source: 'DuckDuckGo HTML',
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
    
    const searchData = await searchDuckDuckGo(query, Math.min(count, 10));
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
  log('info', '🚀 OpenSERP Brave Adapter CN v2 started');
  log('info', `📡 Listening on port ${CONFIG.PORT}`);
  log('info', `🔗 Search source: DuckDuckGo HTML`);
  log('info', '');
  log('info', 'Test: http://localhost:' + CONFIG.PORT + '/search?q=test');
});
