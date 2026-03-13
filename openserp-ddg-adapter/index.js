#!/usr/bin/env node
/**
 * DuckDuckGo HTML Search Adapter
 * 直接调用 DuckDuckGo HTML 接口，无需 SearXNG
 */

const http = require('http');
const https = require('https');
const url = require('url');

const PORT = process.env.PORT || 8766;

console.log(`🚀 DuckDuckGo Search Adapter starting...`);
console.log(`   Port: ${PORT}`);

const server = http.createServer(async (req, res) => {
  const parsedUrl = url.parse(req.url, true);
  
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Content-Type', 'application/json');
  
  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }
  
  if (parsedUrl.pathname === '/health') {
    res.writeHead(200);
    res.end(JSON.stringify({ status: 'ok', adapter: 'duckduckgo-html' }));
    return;
  }
  
  if (parsedUrl.pathname === '/search') {
    const query = parsedUrl.query.q || parsedUrl.query.query || '';
    const count = parseInt(parsedUrl.query.count || 10);
    
    if (!query) {
      res.writeHead(400);
      res.end(JSON.stringify({ error: 'Missing query parameter' }));
      return;
    }
    
    try {
      const results = await searchDuckDuckGo(query, count);
      res.writeHead(200);
      res.end(JSON.stringify(results));
    } catch (error) {
      console.error('Search error:', error.message);
      res.writeHead(500);
      res.end(JSON.stringify({ error: error.message }));
    }
    return;
  }
  
  res.writeHead(404);
  res.end(JSON.stringify({ error: 'Not found' }));
});

async function searchDuckDuckGo(query, count = 10) {
  return new Promise((resolve, reject) => {
    const ddgUrl = `https://html.duckduckgo.com/html/?q=${encodeURIComponent(query)}`;
    
    const req = https.get(ddgUrl, {
      timeout: 15000,
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; OpenClaw/1.0)'
      }
    }, (res) => {
      let html = '';
      res.on('data', chunk => html += chunk);
      res.on('end', () => {
        try {
          const results = parseDuckDuckGoHTML(html, query, count);
          resolve(results);
        } catch (error) {
          reject(new Error(`Parse error: ${error.message}`));
        }
      });
    });
    
    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('DuckDuckGo timeout (15s)'));
    });
  });
}

function parseDuckDuckGoHTML(html, query, count) {
  const results = [];
  const resultRegex = /<a class="result__a" href="([^"]+)">([^<]+)<\/a>/g;
  const snippetRegex = /<a class="result__snippet" href="[^"]*">([^<]+(?:<[^>]+>[^<]+)*)<\/a>/g;
  
  let match;
  let index = 0;
  
  while ((match = resultRegex.exec(html)) !== null && index < count) {
    const url = match[1];
    const title = match[2].replace(/<[^>]+>/g, '');
    
    let content = '';
    const snippetMatch = snippetRegex.exec(html);
    if (snippetMatch) {
      content = snippetMatch[1].replace(/<[^>]+>/g, '');
    }
    
    results.push({
      title: title,
      url: decodeURIComponent(url.split('&uddg=')[1] || url),
      content: content,
      engine: 'duckduckgo',
      score: 0
    });
    
    index++;
  }
  
  return {
    query: query,
    results: results,
    suggestions: [],
    total: results.length
  };
}

server.listen(PORT, () => {
  console.log(`✅ Server running on port ${PORT}`);
  console.log(`   Health: http://localhost:${PORT}/health`);
  console.log(`   Search: http://localhost:${PORT}/search?q=test`);
});
