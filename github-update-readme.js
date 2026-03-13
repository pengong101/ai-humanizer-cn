#!/usr/bin/env node
const https = require('https');
const fs = require('fs');

const TOKEN = '[GITHUB_TOKEN_REDACTED]';
const OWNER = 'pengong101';
const REPO = 'openserp-brave-adapter';

function apiRequest(method, path, data = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.github.com',
      port: 443,
      path: path,
      method: method,
      headers: {
        'Authorization': `token ${TOKEN}`,
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'OpenClaw-Setup-Script',
        'Content-Type': 'application/json',
      },
    };
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const json = body ? JSON.parse(body) : {};
          if (res.statusCode >= 200 && res.statusCode < 300) resolve({ status: res.statusCode, data: json });
          else reject(new Error(`API ${res.statusCode}: ${json.message || body.substring(0, 100)}`));
        } catch (e) { reject(new Error(`Parse: ${e.message}`)); }
      });
    });
    req.on('error', reject);
    if (data) req.write(JSON.stringify(data));
    req.end();
  });
}

async function main() {
  console.log('📝 更新 README.md...\n');
  
  // 获取现有文件的 SHA
  const fileResult = await apiRequest('GET', `/repos/${OWNER}/${REPO}/contents/README.md`);
  const sha = fileResult.data.sha;
  console.log(`✅ 当前 SHA: ${sha}`);
  
  // 读取新内容
  const content = fs.readFileSync('/root/.openclaw/workspace/openserp-brave-adapter/README.md', 'utf-8');
  
  // 更新文件
  await apiRequest('PUT', `/repos/${OWNER}/${REPO}/contents/README.md`, {
    message: 'Update README.md with complete documentation',
    content: Buffer.from(content).toString('base64'),
    sha: sha,
  });
  
  console.log('✅ README.md 更新成功!\n');
  console.log(`📦 https://github.com/${OWNER}/${REPO}/blob/main/README.md\n`);
}

main();
