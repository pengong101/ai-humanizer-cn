#!/usr/bin/env node
/**
 * GitHub 代码推送脚本（适用于已存在的仓库）
 */

const https = require('https');
const fs = require('fs');

// 配置
const TOKEN = '[GITHUB_TOKEN_REDACTED]';
const OWNER = 'pengong101';
const REPO = 'openserp-brave-adapter';

// API 请求
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
            reject(new Error(`API Error ${res.statusCode}: ${json.message || body}`));
          }
        } catch (e) {
          reject(new Error(`Parse error: ${e.message}`));
        }
      });
    });

    req.on('error', reject);
    if (data) req.write(JSON.stringify(data));
    req.end();
  });
}

// 读取文件
function readFile(path) {
  try {
    return fs.readFileSync(path, 'utf-8');
  } catch (e) {
    console.warn(`Warning: Could not read ${path}`);
    return null;
  }
}

// 创建 Blob
async function createBlob(content) {
  return await apiRequest('POST', `/repos/${OWNER}/${REPO}/git/blobs`, {
    content: Buffer.from(content).toString('base64'),
    encoding: 'base64',
  });
}

async function main() {
  console.log('🚀 OpenSERP Brave Adapter - 推送代码到 GitHub\n');
  console.log(`📁 仓库：${OWNER}/${REPO}\n`);

  try {
    // 获取 main 分支引用
    console.log('Step 1/5: 获取分支信息...');
    const refResult = await apiRequest('GET', `/repos/${OWNER}/${REPO}/git/refs/heads/main`);
    const mainSha = refResult.data.object.sha;
    console.log(`   ✅ main: ${mainSha.substring(0, 7)}`);

    // 获取 commit
    console.log('Step 2/5: 获取当前 commit...');
    const commitResult = await apiRequest('GET', `/repos/${OWNER}/${REPO}/git/commits/${mainSha}`);
    let baseTree = commitResult.data.commit?.tree?.sha;
    
    // 如果是初始空 commit，创建空 tree
    if (!baseTree) {
      console.log('   ℹ️ 创建空 tree...');
      const emptyTree = await apiRequest('POST', `/repos/${OWNER}/${REPO}/git/trees`, { tree: [] });
      baseTree = emptyTree.data.sha;
    }
    console.log(`   ✅ Tree: ${baseTree.substring(0, 7)}`);

    // 准备文件
    console.log('Step 3/5: 准备文件...');
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

    const treeItems = [];
    for (const file of files) {
      const content = file.content || readFile(file.local);
      if (content) {
        const blobResult = await createBlob(content);
        treeItems.push({
          path: file.path,
          mode: file.path.endsWith('.sh') || file.path.endsWith('.js') ? '100755' : '100644',
          type: 'blob',
          sha: blobResult.data.sha,
        });
        console.log(`   📄 ${file.path}`);
      }
    }
    console.log(`   ✅ 共 ${treeItems.length} 个文件`);

    // 创建 tree
    console.log('Step 4/5: 创建 tree...');
    const treeResult = await apiRequest('POST', `/repos/${OWNER}/${REPO}/git/trees`, {
      base_tree: baseTree,
      tree: treeItems,
    });
    console.log(`   ✅ New tree: ${treeResult.data.sha.substring(0, 7)}`);

    // 创建 commit
    console.log('Step 5/5: 创建 commit 并推送...');
    const newCommit = await apiRequest('POST', `/repos/${OWNER}/${REPO}/git/commits`, {
      tree: treeResult.data.sha,
      parents: [mainSha],
      message: 'Initial commit: OpenSERP Brave Adapter v1.0.0\n\nComplete implementation with:\n- Brave API compatible adapter\n- Docker support\n- Test suite\n- Documentation\n\nReady for production deployment.',
    });

    // 更新分支
    await apiRequest('PATCH', `/repos/${OWNER}/${REPO}/git/refs/heads/main`, {
      sha: newCommit.data.sha,
      force: false,
    });
    console.log(`   ✅ Commit: ${newCommit.data.sha.substring(0, 7)}`);

    // 完成
    console.log('\n' + '─'.repeat(60));
    console.log('🎉 推送成功！\n');
    console.log(`📦 仓库：https://github.com/${OWNER}/${REPO}`);
    console.log(`📖 README: https://github.com/${OWNER}/${REPO}/blob/main/README.md`);
    console.log(`🚀 克隆：git clone https://github.com/${OWNER}/${REPO}.git\n`);

  } catch (error) {
    console.error('\n❌ 错误:', error.message);
    process.exit(1);
  }
}

main();
