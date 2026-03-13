#!/usr/bin/env node
/**
 * Kasm 浏览器适配器
 * 用于 OpenClaw 调用极空间 Kasm VVC 浏览器
 */

const http = require('http');
const https = require('https');

const KASM_CONFIG = {
  host: '192.168.1.122',
  port: 5901,  // VNC 端口（容器内）
  username: 'admin',
  password: 'Zspace123',
  useHttps: false,
  provider: 'vnc'
};

class KasmAdapter {
  constructor(config = KASM_CONFIG) {
    this.config = config;
    this.token = null;
    this.sessionId = null;
  }

  // 认证获取 Token
  async authenticate() {
    return new Promise((resolve, reject) => {
      const data = JSON.stringify({
        username: this.config.username,
        password: this.config.password
      });

      const options = {
        hostname: this.config.host,
        port: this.config.port,
        path: '/api/auth',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': data.length
        },
        rejectUnauthorized: false
      };

      const req = (this.config.useHttps ? https : http).request(options, (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => {
          if (res.statusCode === 200) {
            try {
              const result = JSON.parse(body);
              this.token = result.token;
              resolve(result);
            } catch (e) {
              reject(new Error('Failed to parse auth response'));
            }
          } else {
            reject(new Error(`Auth failed: ${res.statusCode}`));
          }
        });
      });

      req.on('error', reject);
      req.write(data);
      req.end();
    });
  }

  // 创建浏览器会话
  async createSession(image = 'chrome') {
    if (!this.token) {
      await this.authenticate();
    }

    return new Promise((resolve, reject) => {
      const data = JSON.stringify({
        image: image,
        name: 'openclaw-session'
      });

      const options = {
        hostname: this.config.host,
        port: this.config.port,
        path: '/api/session',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': data.length,
          'Authorization': `Bearer ${this.token}`
        },
        rejectUnauthorized: false
      };

      const req = (this.config.useHttps ? https : http).request(options, (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => {
          if (res.statusCode === 200) {
            try {
              const result = JSON.parse(body);
              this.sessionId = result.session_id;
              resolve(result);
            } catch (e) {
              reject(new Error('Failed to parse session response'));
            }
          } else {
            reject(new Error(`Create session failed: ${res.statusCode}`));
          }
        });
      });

      req.on('error', reject);
      req.write(data);
      req.end();
    });
  }

  // 执行 JavaScript
  async executeJavaScript(code) {
    if (!this.sessionId) {
      throw new Error('No active session');
    }

    return new Promise((resolve, reject) => {
      const data = JSON.stringify({ code });

      const options = {
        hostname: this.config.host,
        port: this.config.port,
        path: `/api/session/${this.sessionId}/execute`,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': data.length,
          'Authorization': `Bearer ${this.token}`
        },
        rejectUnauthorized: false
      };

      const req = (this.config.useHttps ? https : http).request(options, (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => {
          if (res.statusCode === 200) {
            try {
              const result = JSON.parse(body);
              resolve(result);
            } catch (e) {
              reject(new Error('Failed to parse execute response'));
            }
          } else {
            reject(new Error(`Execute failed: ${res.statusCode}`));
          }
        });
      });

      req.on('error', reject);
      req.write(data);
      req.end();
    });
  }

  // 截图
  async screenshot() {
    if (!this.sessionId) {
      throw new Error('No active session');
    }

    return new Promise((resolve, reject) => {
      const options = {
        hostname: this.config.host,
        port: this.config.port,
        path: `/api/session/${this.sessionId}/screenshot`,
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${this.token}`
        },
        rejectUnauthorized: false
      };

      const req = (this.config.useHttps ? https : http).request(options, (res) => {
        const chunks = [];
        res.on('data', chunk => chunks.push(chunk));
        res.on('end', () => {
          if (res.statusCode === 200) {
            resolve(Buffer.concat(chunks));
          } else {
            reject(new Error(`Screenshot failed: ${res.statusCode}`));
          }
        });
      });

      req.on('error', reject);
      req.end();
    });
  }

  // 导航到 URL
  async navigate(url) {
    return await this.executeJavaScript(`window.location.href = '${url}'`);
  }

  // 关闭会话
  async closeSession() {
    if (!this.sessionId) return;

    return new Promise((resolve, reject) => {
      const options = {
        hostname: this.config.host,
        port: this.config.port,
        path: `/api/session/${this.sessionId}`,
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${this.token}`
        },
        rejectUnauthorized: false
      };

      const req = (this.config.useHttps ? https : http).request(options, (res) => {
        if (res.statusCode === 200) {
          this.sessionId = null;
          resolve();
        } else {
          reject(new Error(`Close session failed: ${res.statusCode}`));
        }
      });

      req.on('error', reject);
      req.end();
    });
  }
}

// 命令行测试
if (require.main === module) {
  (async () => {
    console.log('🚀 Kasm 浏览器适配器测试...\n');

    const adapter = new KasmAdapter();

    try {
      // 测试认证
      console.log('1️⃣ 测试认证...');
      await adapter.authenticate();
      console.log('✅ 认证成功\n');

      // 测试创建会话
      console.log('2️⃣ 创建浏览器会话...');
      const session = await adapter.createSession();
      console.log('✅ 会话创建成功:', session.session_id, '\n');

      // 测试导航
      console.log('3️⃣ 导航到 example.com...');
      await adapter.navigate('https://example.com');
      console.log('✅ 导航成功\n');

      // 等待页面加载
      await new Promise(resolve => setTimeout(resolve, 3000));

      // 测试截图
      console.log('4️⃣ 截图...');
      const screenshot = await adapter.screenshot();
      console.log('✅ 截图成功:', screenshot.length, 'bytes\n');

      // 保存截图
      const fs = require('fs');
      fs.writeFileSync('/tmp/kasm-screenshot.png', screenshot);
      console.log('📸 截图已保存到：/tmp/kasm-screenshot.png\n');

      // 关闭会话
      console.log('5️⃣ 关闭会话...');
      await adapter.closeSession();
      console.log('✅ 会话已关闭\n');

      console.log('🎉 所有测试通过！');
    } catch (error) {
      console.error('❌ 测试失败:', error.message);
      process.exit(1);
    }
  })();
}

module.exports = { KasmAdapter };
