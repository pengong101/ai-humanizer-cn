#!/usr/bin/env node
/**
 * GitHub 仓库创建和代码推送脚本
 * 使用 GitHub API 直接操作
 */

const https = require('https');
const http = require('http');

// 配置
const TOKEN = '[GITHUB_TOKEN_REDACTED]';
const OWNER = 'pengong101';
const REPO = 'openserp-brave-adapter';
const REPO_DESC = 'Brave Search API compatible adapter for OpenSERP - enables OpenClaw to use OpenSERP without code changes';

// 工具函数
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
    
    if (data) {
      req.write(JSON.stringify(data));
    }
    req.end();
  });
}

// 创建 Blob（文件内容）
async function createBlob(content, encoding = 'utf-8') {
  const blobData = {
    content: encoding === 'base64' ? content : Buffer.from(content).toString('base64'),
    encoding: 'base64',
  };
  return await apiRequest('POST', `/repos/${OWNER}/${REPO}/git/blobs`, blobData);
}

// 创建 Tree
async function createTree(baseTree, treeItems) {
  return await apiRequest('POST', `/repos/${OWNER}/${REPO}/git/trees`, {
    base_tree: baseTree,
    tree: treeItems,
  });
}

// 创建 Commit
async function createCommit(tree, parentCommit, message) {
  return await apiRequest('POST', `/repos/${OWNER}/${REPO}/git/commits`, {
    tree: tree,
    parents: parentCommit ? [parentCommit] : [],
    message: message,
  });
}

// 更新引用
async function updateRef(ref, sha) {
  return await apiRequest('PATCH', `/repos/${OWNER}/${REPO}/git/refs/${ref}`, {
    sha: sha,
    force: true,
  });
}

// 读取本地文件
function readFile(path) {
  const fs = require('fs');
  try {
    return fs.readFileSync(path, 'utf-8');
  } catch (e) {
    console.warn(`Warning: Could not read ${path}: ${e.message}`);
    return null;
  }
}

// 主流程
async function main() {
  console.log('🚀 OpenSERP Brave Adapter - GitHub 自动部署\n');
  console.log(`📁 仓库：${OWNER}/${REPO}\n`);

  try {
    // Step 1: 创建仓库
    console.log('Step 1/6: 创建 GitHub 仓库...');
    const repoResult = await apiRequest('POST', '/user/repos', {
      name: REPO,
      description: REPO_DESC,
      private: false,
      auto_init: true,
    });
    console.log(`   ✅ 仓库创建成功：${repoResult.data.html_url}\n`);

    // Step 2: 获取默认分支的引用
    console.log('Step 2/6: 获取默认分支信息...');
    const refResult = await apiRequest('GET', `/repos/${OWNER}/${REPO}/git/refs/heads/main`);
    const mainSha = refResult.data.object.sha;
    console.log(`   ✅ 当前 main 分支：${mainSha.substring(0, 7)}\n`);

    // Step 3: 获取当前 tree
    console.log('Step 3/6: 获取当前 tree...');
    const commitResult = await apiRequest('GET', `/repos/${OWNER}/${REPO}/git/commits/${mainSha}`);
    const baseTree = commitResult.data.commit?.tree?.sha || commitResult.data.tree?.sha;
    if (!baseTree) {
      // 如果是空仓库，创建空 tree
      console.log('   ℹ️ 空仓库，创建新 tree...');
      const emptyTree = await apiRequest('POST', `/repos/${OWNER}/${REPO}/git/trees`, { tree: [] });
      baseTree = emptyTree.data.sha;
    }
    console.log(`   ✅ 基础 tree: ${baseTree.substring(0, 7)}\n`);

    // Step 4: 读取本地文件并创建 blobs
    console.log('Step 4/6: 准备上传文件...');
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
      { path: 'LICENSE', content: 'MIT License\n\nCopyright (c) 2026 OpenClaw Team\n\nPermission is hereby granted...' },
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
    console.log(`   ✅ 共 ${treeItems.length} 个文件\n`);

    // Step 5: 创建新 tree
    console.log('Step 5/6: 创建新 tree...');
    const treeResult = await createTree(baseTree, treeItems);
    console.log(`   ✅ 新 tree: ${treeResult.data.sha.substring(0, 7)}\n`);

    // Step 6: 创建 commit 并更新分支
    console.log('Step 6/6: 创建 commit 并推送...');
    const commitResult2 = await createCommit(treeResult.data.sha, mainSha, 'Initial commit: OpenSERP Brave Adapter v1.0.0\n\nComplete implementation with Docker support, tests, and documentation.');
    
    await updateRef('heads/main', commitResult2.data.sha);
    console.log(`   ✅ Commit: ${commitResult2.data.sha.substring(0, 7)}\n`);

    // 完成
    console.log('─'.repeat(60));
    console.log('🎉 部署完成！\n');
    console.log(`📦 仓库地址：${repoResult.data.html_url}`);
    console.log(`📖 README: ${repoResult.data.html_url}/blob/main/README.md`);
    console.log(`🚀 快速开始：git clone ${repoResult.data.clone_url}\n`);

  } catch (error) {
    console.error('\n❌ 错误:', error.message);
    console.error('\n请检查:');
    console.error('  1. Token 是否有效');
    console.error('  2. 网络连接是否正常');
    console.error('  3. 仓库是否已存在（如存在请先删除或改名）');
    process.exit(1);
  }
}

main();
