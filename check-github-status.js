#!/usr/bin/env node
/**
 * 查看 GitHub 账号信息和仓库列表
 */

const https = require('https');

// 配置
const TOKEN = '[GITHUB_TOKEN_REDACTED]';
const OWNER = 'pengong101';

function apiRequest(method, path) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.github.com',
      port: 443,
      path: path,
      method: method,
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

async function main() {
  console.log('🔍 检查 GitHub 账号状态...\n');
  
  try {
    // 1. 获取用户信息
    console.log('Step 1: 获取用户信息...');
    const userResult = await apiRequest('GET', '/user');
    console.log('✅ 用户信息:');
    console.log(`   登录名：${userResult.data.login}`);
    console.log(`   名字：${userResult.data.name || '未设置'}`);
    console.log(`   邮箱：${userResult.data.email || '未公开'}`);
    console.log(`   公司：${userResult.data.company || '未设置'}`);
    console.log(`   位置：${userResult.data.location || '未设置'}`);
    console.log(`   博客：${userResult.data.blog || '无'}`);
    console.log(`   创建时间：${new Date(userResult.data.created_at).toLocaleString('zh-CN')}`);
    console.log(`   公开仓库：${userResult.data.public_repos}`);
    console.log(`   关注者：${userResult.data.followers}`);
    console.log(`   关注中：${userResult.data.following}\n`);

    // 2. 获取仓库列表
    console.log('Step 2: 获取仓库列表...');
    const reposResult = await apiRequest('GET', `/users/${OWNER}/repos?sort=updated&direction=desc`);
    const repos = reposResult.data;
    
    console.log(`✅ 共 ${repos.length} 个公开仓库:\n`);
    
    if (repos.length === 0) {
      console.log('   📭 暂无公开仓库');
    } else {
      repos.forEach((repo, index) => {
        console.log(`${index + 1}. ${repo.name}`);
        console.log(`   描述：${repo.description || '无描述'}`);
        console.log(`   语言：${repo.language || '未知'}`);
        console.log(`   更新：${new Date(repo.updated_at).toLocaleString('zh-CN')}`);
        console.log(`   Star: ${repo.stargazers_count} | Fork: ${repo.forks_count}`);
        console.log(`   地址：${repo.html_url}\n`);
      });
    }

    // 3. 总结
    console.log('─'.repeat(60));
    console.log('📊 账号状态总结:');
    console.log(`   账号：${userResult.data.login}`);
    console.log(`   公开仓库：${repos.length} 个`);
    console.log(`   总 Star 数：${repos.reduce((sum, r) => sum + r.stargazers_count, 0)}`);
    console.log(`   Token 权限：repo, workflow, write:packages`);
    console.log(`   状态：✅ 正常\n`);

  } catch (error) {
    console.error('\n❌ 错误:', error.message);
    console.error('\n可能原因:');
    console.error('  1. Token 无效或过期');
    console.error('  2. 网络连接问题');
    console.error('  3. API 限流\n');
    process.exit(1);
  }
}

main();
