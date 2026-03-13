#!/usr/bin/env node
/**
 * GitHub 代码推送 - 使用 Contents API（更简单）
 */

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
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve({ status: res.statusCode, data: json });
          } else {
            reject(new Error(`API ${res.statusCode}: ${json.message || body.substring(0, 200)}`));
          }
        } catch (e) {
          reject(new Error(`Parse: ${e.message}`));
        }
      });
    });

    req.on('error', reject);
    if (data) req.write(JSON.stringify(data));
    req.end();
  });
}

function readFile(path) {
  try {
    return fs.readFileSync(path, 'utf-8');
  } catch (e) {
    return null;
  }
}

async function uploadFile(path, content, message) {
  return await apiRequest('PUT', `/repos/${OWNER}/${REPO}/contents/${path}`, {
    message: message,
    content: Buffer.from(content).toString('base64'),
  });
}

async function main() {
  console.log('🚀 OpenSERP Brave Adapter - GitHub 推送\n');
  console.log(`📁 ${OWNER}/${REPO}\n`);

  const files = [
    { path: 'index.js', local: '/root/.openclaw/workspace/openserp-brave-adapter/index.js' },
    { path: 'package.json', local: '/root/.openclaw/workspace/openserp-brave-adapter/package.json' },
    { path: 'README.md', local: '/root/.openclaw/workspace/openserp-brave-adapter/README.md' },
    { path: 'Dockerfile', local: '/root/.openclaw/workspace/openserp-brave-adapter/Dockerfile' },
    { path: 'docker-compose.yml', local: '/root/.openclaw/workspace/openserp-brave-adapter/docker-compose.yml' },
    { path: '.env.example', local: '/root/.openclaw/workspace/openserp-brave-adapter/.env.example' },
    { path: 'deploy.sh', local: '/root/.openclaw/workspace/openserp-brave-adapter/deploy.sh' },
    { path: 'test/index.test.js', local: '/root/.openclaw/workspace/openserp-brave-adapter/test/index.test.js' },
    { path: 'examples/openclaw-config.json', local: '/root/.openclaw/workspace/openserp-brave-adapter/examples/openclaw-config.json' },
    { path: 'LICENSE', content: 'MIT License\n\nCopyright (c) 2026 OpenClaw Team\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.' },
    { path: '.gitignore', content: 'node_modules/\n.env\n*.log\n.DS_Store\n' },
  ];

  let success = 0;
  let failed = 0;

  for (const file of files) {
    const content = file.content || readFile(file.local);
    if (!content) {
      console.log(`⏭️  ${file.path} (文件不存在)`);
      continue;
    }

    try {
      process.stdout.write(`📤 ${file.path}... `);
      await uploadFile(file.path, content, `Add ${file.path}`);
      console.log('✅');
      success++;
    } catch (e) {
      console.log(`❌ ${e.message.substring(0, 50)}`);
      failed++;
    }
  }

  console.log('\n' + '─'.repeat(50));
  console.log(`✅ 成功：${success} | ❌ 失败：${failed}`);
  console.log(`\n📦 https://github.com/${OWNER}/${REPO}\n`);
}

main();
