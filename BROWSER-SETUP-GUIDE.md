# 浏览器调用方案

**问题：** 服务器无浏览器，需要调用极空间 NAS 上的浏览器

---

## 🔍 当前状态

### 服务器环境
- ❌ 无 Chrome/Chromium 浏览器
- ❌ 无配对的节点设备
- ❌ 浏览器服务未启动

### 极空间 NAS (192.168.1.122)
- ✅ SearXNG 运行正常 (8081 端口)
- ❓ 浏览器服务未知

---

## 🎯 解决方案

### 方案 A：使用极空间 Docker 浏览器（推荐）⭐⭐⭐⭐⭐

如果极空间有安装浏览器 Docker 容器：

**步骤 1：检查极空间浏览器服务**

在极空间上检查是否有以下容器：
```bash
# SSH 登录极空间
docker ps | grep -i "browser\|chrome\|chromium"
```

**常见浏览器容器：**
- `linuxserver/chromium`
- `seleniarm/standalone-chromium`
- `browserless/chrome`

**步骤 2：配置远程调试**

如果已有浏览器容器，确保开启远程调试端口（默认 9222）：

```yaml
# docker-compose.yml
version: '3'
services:
  chromium:
    image: linuxserver/chromium
    ports:
      - 9222:9222  # 远程调试端口
      - 3000:3000  # Web 界面
    environment:
      - PUID=1000
      - PGID=1000
```

**步骤 3：配置 OpenClaw**

```json
{
  "browser": {
    "cdpUrl": "http://192.168.1.122:9222",
    "attachOnly": true
  }
}
```

---

### 方案 B：在极空间部署 browserless（推荐）⭐⭐⭐⭐⭐

如果极空间没有浏览器，部署 browserless 服务：

**步骤 1：创建 docker-compose.yml**

```yaml
version: '3.8'
services:
  browserless:
    image: browserless/chrome:latest
    container_name: browserless
    ports:
      - "9222:3000"
    environment:
      - CONNECTION_TIMEOUT=-1
      - MAX_CONCURRENT_SESSIONS=10
      - ENABLE_DEBUGGER=true
      - PREBOOT_CHROME=true
      - DEFAULT_LAUNCH_ARGS=["--no-sandbox","--disable-setuid-sandbox"]
    restart: unless-stopped
```

**步骤 2：启动服务**

```bash
cd /path/to/browserless
docker-compose up -d
```

**步骤 3：验证**

```bash
curl http://192.168.1.122:9222/json/version
```

**步骤 4：配置 OpenClaw**

编辑 `~/.openclaw/openclaw.json`：
```json
{
  "browser": {
    "target": "host",
    "cdpUrl": "http://192.168.1.122:9222",
    "attachOnly": true
  }
}
```

---

### 方案 C：使用 OpenClaw 浏览器中继（需要本地电脑）⭐⭐⭐

如果你有本地电脑（Mac/Windows）：

**步骤 1：在本地电脑安装 Chrome 扩展**

访问：https://chrome.google.com/webstore/detail/openclaw-browser-relay

**步骤 2：启动浏览器中继**

点击扩展图标，启动中继服务。

**步骤 3：配置 OpenClaw**

```json
{
  "browser": {
    "profile": "chrome",
    "target": "host"
  }
}
```

**优点：**
- ✅ 使用本地电脑浏览器
- ✅ 无需额外部署
- ✅ 可以看到浏览器界面

**缺点：**
- ⚠️ 需要本地电脑开机
- ⚠️ 依赖网络连接

---

### 方案 D：在服务器安装 Chromium（不推荐）⭐⭐

**步骤 1：安装 Chromium**

```bash
# Debian/Ubuntu
apt-get update
apt-get install -y chromium

# 或安装 Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb
apt-get install -f -y
```

**步骤 2：安装依赖**

```bash
apt-get install -y \
  libnss3 \
  libxss1 \
  libasound2 \
  libatk-bridge2.0-0 \
  libgtk-3-0 \
  libgbm1
```

**步骤 3：启动浏览器**

```bash
chromium --headless --remote-debugging-port=9222 --no-sandbox &
```

**缺点：**
- ❌ 服务器资源占用大
- ❌ 需要图形库支持
- ❌ 维护成本高

---

## 🎯 推荐方案

### 最佳选择：方案 B（browserless on NAS）

**理由：**
1. ✅ 极空间 24 小时运行
2. ✅ Docker 部署简单
3. ✅ 资源占用低
4. ✅ 无需本地电脑
5. ✅ 性能稳定

**部署时间：** 5 分钟

---

## 📋 实施步骤

### 立即执行（方案 B）

**在极空间上执行：**

```bash
# 1. 创建目录
mkdir -p /data/Docker/browserless
cd /data/Docker/browserless

# 2. 创建 docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  browserless:
    image: browserless/chrome:latest
    container_name: browserless
    ports:
      - "9222:3000"
    environment:
      - CONNECTION_TIMEOUT=-1
      - MAX_CONCURRENT_SESSIONS=10
      - ENABLE_DEBUGGER=true
      - PREBOOT_CHROME=true
      - DEFAULT_LAUNCH_ARGS=["--no-sandbox","--disable-setuid-sandbox"]
    restart: unless-stopped
EOF

# 3. 启动
docker-compose up -d

# 4. 验证
curl http://192.168.1.122:9222/json/version
```

**完成后告诉我，我配置 OpenClaw 调用！**

---

## 🔗 相关链接

- [browserless 官方文档](https://docs.browserless.io/)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [OpenClaw 浏览器配置](https://docs.openclaw.ai/tools/browser)

---

**请选择方案并执行，我随时准备配置！** 🚀
