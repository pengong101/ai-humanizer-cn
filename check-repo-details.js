#!/usr/bin/env node
/**
 * 查看 GitHub 仓库详细文件列表
 */

const https = require('https');

const TOKEN = '[GITHUB_TOKEN_REDACTED]';
const OWNER = 'pengong101';

function apiRequest(path) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.github.com',
      port: 443,
      path: path,
      method: 'GET',
      headers: {
        'Authorization': `token ${TOKEN}`,
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'GitHub-Status-Check',
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
            reject(new Error(`API ${res.statusCode}: ${json.message || body}`));
          }
        } catch (e) {
          reject(new Error(`Parse: ${e.message}`));
        }
      });
    });

    req.on('error', reject);
    req.end();
  });
}

async function checkRepo(repoName) {
  console.log(`\n📦 检查仓库：${repoName}`);
  console.log('─'.repeat(60));
  
  try {
    // 获取仓库详情
    const repoResult = await apiRequest(`/repos/${OWNER}/${repoName}`);
    const repo = repoResult.data;
    
    console.log(`描述：${repo.description || '无'}`);
    console.log(`默认分支：${repo.default_branch}`);
    console.log(`Star: ${repo.stargazers_count} | Fork: ${repo.forks_count}`);
    console.log(`创建时间：${new Date(repo.created_at).toLocaleString('zh-CN')}`);
    console.log(`更新时间：${new Date(repo.updated_at).toLocaleString('zh-CN')}`);
    
    // 获取文件列表
    console.log('\n📁 文件列表:');
    const filesResult = await apiRequest(`/repos/${OWNER}/${repoName}/git/trees/${repo.default_branch}?recursive=1`);
    const files = filesResult.data.tree.filter(f => f.type === 'blob');
    
    files.forEach(file => {
      console.log(`   ${file.path}`);
    });
    
    console.log(`\n共 ${files.length} 个文件`);
    
    // 获取 README
    try {
      const readmeResult = await apiRequest(`/repos/${OWNER}/${repoName}/readme`);
      const content = Buffer.from(readmeResult.data.content, 'base64').toString('utf-8');
      console.log('\n📖 README 预览:');
      console.log(content.substring(0, 500) + '...');
    } catch (e) {
      console.log('\n⚠️ 无 README');
    }
    
  } catch (error) {
    console.error('❌ 错误:', error.message);
  }
}

async function main() {
  console.log('🔍 检查 GitHub 仓库详情...\n');
  
  const repos = [
    'openclaw-toolkit',
    'openclaw-plugin-searxng',
    'openclaw-searxng-search'
  ];
  
  for (const repo of repos) {
    await checkRepo(repo);
  }
}

main();
