#!/usr/bin/env node
/**
 * OpenSERP Brave Adapter 基础测试
 */

const http = require('http');

const BASE_URL = process.env.TEST_URL || 'http://localhost:8765';

function httpGet(url) {
  return new Promise((resolve, reject) => {
    http.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve({
            status: res.statusCode,
            headers: res.headers,
            data: JSON.parse(data),
          });
        } catch (e) {
          resolve({
            status: res.statusCode,
            headers: res.headers,
            data: data,
          });
        }
      });
    }).on('error', reject);
  });
}

async function runTests() {
  console.log('🧪 OpenSERP Brave Adapter Tests\n');
  console.log(`Target: ${BASE_URL}\n`);
  
  let passed = 0;
  let failed = 0;
  
  // Test 1: Health endpoint
  console.log('Test 1: Health endpoint');
  try {
    const res = await httpGet(`${BASE_URL}/health`);
    if (res.status === 200 && res.data.status === 'ok') {
      console.log('  ✅ PASSED\n');
      passed++;
    } else {
      console.log('  ❌ FAILED: Unexpected response\n');
      failed++;
    }
  } catch (e) {
    console.log('  ❌ FAILED:', e.message, '\n');
    failed++;
  }
  
  // Test 2: Search endpoint (basic)
  console.log('Test 2: Search endpoint (basic)');
  try {
    const res = await httpGet(`${BASE_URL}/search?q=test`);
    if (res.status === 200 && res.data.web && Array.isArray(res.data.web.results)) {
      console.log('  ✅ PASSED');
      console.log(`     Results: ${res.data.web.results.length}\n`);
      passed++;
    } else {
      console.log('  ❌ FAILED: Invalid response format\n');
      failed++;
    }
  } catch (e) {
    console.log('  ❌ FAILED:', e.message, '\n');
    failed++;
  }
  
  // Test 3: Search with parameters
  console.log('Test 3: Search with parameters');
  try {
    const res = await httpGet(`${BASE_URL}/search?q=news&count=5&country=US`);
    if (res.status === 200 && res.data.web && res.data.web.results.length <= 5) {
      console.log('  ✅ PASSED\n');
      passed++;
    } else {
      console.log('  ❌ FAILED\n');
      failed++;
    }
  } catch (e) {
    console.log('  ❌ FAILED:', e.message, '\n');
    failed++;
  }
  
  // Test 4: Missing query parameter
  console.log('Test 4: Missing query parameter (should return 400)');
  try {
    const res = await httpGet(`${BASE_URL}/search`);
    if (res.status === 400) {
      console.log('  ✅ PASSED\n');
      passed++;
    } else {
      console.log('  ❌ FAILED: Expected 400, got', res.status, '\n');
      failed++;
    }
  } catch (e) {
    console.log('  ❌ FAILED:', e.message, '\n');
    failed++;
  }
  
  // Test 5: Invalid endpoint
  console.log('Test 5: Invalid endpoint (should return 404)');
  try {
    const res = await httpGet(`${BASE_URL}/invalid`);
    if (res.status === 404) {
      console.log('  ✅ PASSED\n');
      passed++;
    } else {
      console.log('  ❌ FAILED: Expected 404, got', res.status, '\n');
      failed++;
    }
  } catch (e) {
    console.log('  ❌ FAILED:', e.message, '\n');
    failed++;
  }
  
  // Summary
  console.log('─'.repeat(50));
  console.log(`Results: ${passed} passed, ${failed} failed`);
  console.log(`Total: ${passed + failed} tests\n`);
  
  process.exit(failed > 0 ? 1 : 0);
}

runTests().catch(err => {
  console.error('Test runner error:', err);
  process.exit(1);
});
