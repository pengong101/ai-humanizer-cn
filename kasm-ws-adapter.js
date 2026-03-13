#!/usr/bin/env node
/**
 * Kasm VNC 浏览器适配器 v3.0
 * 使用 WebSocket + noVNC 协议
 */

const WebSocket = require('ws');
const fs = require('fs');

const KASM_CONFIG = {
  host: '192.168.1.122',
  wsPort: 16901,  // WebSocket 端口
  httpPort: 56901, // HTTP 端口
  password: 'Zspace123'
};

class KasmWebSocketAdapter {
  constructor(config = KASM_CONFIG) {
    this.config = config;
    this.ws = null;
    this.connected = false;
  }

  // 连接 WebSocket
  async connect() {
    return new Promise((resolve, reject) => {
      const wsUrl = `ws://${this.config.host}:${this.config.wsPort}`;
      console.log(`🔌 连接 WebSocket: ${wsUrl}`);
      
      this.ws = new WebSocket(wsUrl, {
        headers: {
          'Authorization': `Basic ${Buffer.from('admin:' + this.config.password).toString('base64')}`
        }
      });

      this.ws.on('open', () => {
        this.connected = true;
        console.log('✅ WebSocket 连接成功');
        resolve();
      });

      this.ws.on('error', (err) => {
        console.error('❌ WebSocket 错误:', err.message);
        reject(err);
      });

      this.ws.on('message', (data) => {
        console.log('📨 收到消息:', data.toString('hex').substring(0, 50));
      });

      setTimeout(() => {
        if (!this.connected) {
          reject(new Error('Connection timeout'));
        }
      }, 10000);
    });
  }

  // 截图（通过 HTTP API）
  async screenshot() {
    const http = require('http');
    
    return new Promise((resolve, reject) => {
      const url = `http://${this.config.host}:${this.config.httpPort}/api/screenshot`;
      console.log('📸 截图:', url);
      
      http.get(url, (res) => {
        const chunks = [];
        res.on('data', chunk => chunks.push(chunk));
        res.on('end', () => {
          resolve({
            success: true,
            data: Buffer.concat(chunks),
            size: chunks.length
          });
        });
      }).on('error', reject);
    });
  }

  // 断开
  async disconnect() {
    if (this.ws) {
      this.ws.close();
      this.connected = false;
    }
  }
}

// 快速测试
if (require.main === module) {
  (async () => {
    console.log('🚀 Kasm WebSocket 适配器测试 v3.0\n');
    
    const adapter = new KasmWebSocketAdapter();
    
    try {
      await adapter.connect();
      console.log('✅ 连接测试成功');
      await adapter.disconnect();
      console.log('✅ 测试完成');
    } catch (err) {
      console.error('❌ 失败:', err.message);
      process.exit(1);
    }
  })();
}

module.exports = { KasmWebSocketAdapter };
