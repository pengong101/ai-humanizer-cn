# Kasm 浏览器调用方案

**状态：** ⚠️ API 认证需要特殊处理  
**容器：** browser (kasmweb/chrome:1.16.0_zspace_2.0)  
**端口：** 56901

---

## 🔍 当前状态

### ✅ 可用
- Kasm 容器运行正常
- VNC 服务正常（端口 56901）
- Web 界面可访问（需要认证）

### ❌ 问题
- Kasm API 认证返回 401
- API 路径可能与标准 Kasm 不同
- 极空间定制版本 API 未知

---

## 🎯 解决方案

### 方案 A：使用 VNC 直接连接（推荐）⭐⭐⭐⭐⭐

Kasm 本质是 VNC 服务器，可以直接使用 VNC 客户端连接。

**工具：** `kasm-adapter.js` (已创建)

**修改为 VNC 模式：**
```javascript
const config = {
  host: '192.168.1.122',
  port: 56901,
  password: 'Zspace123',
  provider: 'vnc'
};
```

**使用 noVNC（Web VNC）：**
- URL: http://192.168.1.122:56901
- 密码：Zspace123

---

### 方案 B：使用 Kasm Web 界面 + 自动化 ⭐⭐⭐⭐

通过 Selenium/Puppeteer 控制 Kasm Web 界面：

```javascript
const puppeteer = require('puppeteer');

async function useKasm() {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  // 登录 Kasm
  await page.goto('http://192.168.1.122:56901');
  await page.type('#username', 'admin');
  await page.type('#password', 'Zspace123');
  await page.click('#login-button');
  
  // 等待浏览器加载
  await page.waitForSelector('#browser-frame');
  
  // 在 Kasm 浏览器中执行操作
  const frame = page.frame({ name: 'browser-frame' });
  await frame.goto('https://example.com');
  
  // ...
}
```

---

### 方案 C：直接使用极空间 VNC 端口 ⭐⭐⭐⭐

如果极空间开放了标准 VNC 端口（5900+）：

```javascript
const config = {
  host: '192.168.1.122',
  port: 5901, // 或其他 VNC 端口
  password: 'Zspace123'
};
```

**检查 VNC 端口：**
```bash
netstat -tlnp | grep -i vnc
# 或
docker exec browser netstat -tlnp
```

---

### 方案 D：联系极空间获取 API 文档 ⭐⭐⭐

极空间可能使用了定制的 Kasm 版本，需要官方 API 文档。

**联系方式：**
- 极空间客服
- 极空间开发者社区
- GitHub issues

---

## 📋 立即执行方案

### 最佳选择：VNC 直接连接

**步骤：**

1. **测试 VNC 连接**
```bash
# 安装 VNC 客户端
apt-get install -y vncviewer

# 连接测试
vncviewer 192.168.1.122:56901
# 输入密码：Zspace123
```

2. **修改适配器为 VNC 模式**

编辑 `kasm-adapter.js`，使用 VNC 库：
```javascript
const VNC = require('rfb2');

const client = VNC.createClient({
  host: '192.168.1.122',
  port: 56901,
  password: 'Zspace123'
});

client.connect();
```

3. **集成 OpenClaw**

在 OpenClaw 中调用：
```javascript
const { KasmAdapter } = require('./kasm-adapter');

const kasm = new KasmAdapter();
await kasm.navigate('https://example.com');
const screenshot = await kasm.screenshot();
```

---

## 🔧 OpenClaw 配置

当前配置已添加到 `~/.openclaw/openclaw.json`：

```json
{
  "browser": {
    "enabled": true,
    "provider": "kasm",
    "target": "host",
    "kasm": {
      "host": "192.168.1.122",
      "port": 56901,
      "username": "admin",
      "password": "Zspace123",
      "useHttps": false,
      "timeout": 30000
    }
  }
}
```

**测试：**
```bash
openclaw browser status
openclaw browser snapshot
```

---

## 📊 性能对比

| 方案 | 延迟 | 稳定性 | 易用性 | 推荐度 |
|------|------|--------|--------|--------|
| VNC 直接 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Web 自动化 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 标准 VNC | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Kasm API | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |

---

## 🛠️ 下一步

1. **测试 VNC 连接** - 确认 56901 端口可用
2. **安装 VNC 库** - `npm install rfb2`
3. **修改适配器** - 使用 VNC 协议
4. **集成测试** - OpenClaw 调用测试

---

**维护者：** CEO 智能体（小马 🐴）  
**更新时间：** 2026-03-11  
**状态：** ⏳ 等待 VNC 测试
