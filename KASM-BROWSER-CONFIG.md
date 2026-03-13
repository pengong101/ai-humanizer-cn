# Kasm VVC 浏览器配置指南

**状态：** ✅ 已发现并可用  
**容器：** `browser` (kasmweb/chrome:1.16.0_zspace_2.0)  
**端口：** 56901

---

## 🔍 连接信息

### Kasm 浏览器容器

```bash
# 容器状态
CONTAINER ID: aac1d7f47317
IMAGE: kasmweb/chrome:1.16.0_zspace_2.0
PORTS: 0.0.0.0:56901->6901/tcp
STATUS: Up 5 minutes
```

### 访问方式

**Web 界面：**
- URL: http://192.168.1.122:56901
- 用户名：admin
- 密码：Zspace123

**VNC 连接：**
- Host: 192.168.1.122
- Port: 56901
- Password: Zspace123

---

## 🔧 OpenClaw 配置

### 方式 1：使用 Kasm API（推荐）

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "browser": {
    "target": "host",
    "provider": "kasm",
    "kasm": {
      "host": "192.168.1.122",
      "port": 56901,
      "username": "admin",
      "password": "Zspace123",
      "timeout": 30000
    }
  }
}
```

### 方式 2：使用 VNC

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "browser": {
    "target": "host",
    "provider": "vnc",
    "vnc": {
      "host": "192.168.1.122",
      "port": 56901,
      "password": "Zspace123"
    }
  }
}
```

### 方式 3：使用 CDP (Chrome DevTools Protocol)

如果 Kasm 开启了 CDP：

```json
{
  "browser": {
    "target": "host",
    "cdpUrl": "http://192.168.1.122:56901",
    "attachOnly": true
  }
}
```

---

## 🧪 测试连接

### 1. 测试 Web 界面

```bash
curl http://192.168.1.122:56901
```

应该返回 Kasm 的 HTML 页面。

### 2. 测试 VNC 连接

```bash
# 使用 vncviewer
vncviewer 192.168.1.122:56901
# 输入密码：Zspace123
```

### 3. 测试 OpenClaw 浏览器

```bash
openclaw browser status
openclaw browser start
```

---

## 📋 Kasm API 使用

### 认证

```bash
# 获取 Token
curl -k -X POST "https://192.168.1.122:56901/api/auth" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"Zspace123"}'
```

### 启动浏览器会话

```bash
curl -k -X POST "https://192.168.1.122:56901/api/session" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"image":"chrome","name":"test-session"}'
```

---

## 🔐 安全配置

### 1. 更改默认密码

**强烈建议更改默认密码！**

Kasm 管理界面：
- 当前：admin / Zspace123
- 建议：使用强密码

### 2. 启用 HTTPS

```bash
# 配置 SSL 证书
# 在 Kasm 管理界面设置
```

### 3. 限制访问 IP

```bash
# 防火墙规则
iptables -A INPUT -p tcp --dport 56901 -s 192.168.1.0/24 -j ACCEPT
iptables -A INPUT -p tcp --dport 56901 -j DROP
```

---

## 🚀 使用示例

### OpenClaw 中使用浏览器

```javascript
// 截图
const screenshot = await browser.screenshot();

// 导航
await browser.navigate('https://example.com');

// 点击
await browser.click('#button');

// 输入
await browser.type('#input', 'Hello World');
```

### 自动化脚本

```bash
#!/bin/bash
# 使用 Kasm 浏览器执行自动化任务

# 1. 启动会话
SESSION=$(curl -k -X POST "https://192.168.1.122:56901/api/session" \
  -H "Content-Type: application/json" \
  -d '{"image":"chrome"}')

# 2. 获取会话 ID
SESSION_ID=$(echo $SESSION | jq -r '.session_id')

# 3. 执行任务
# ...

# 4. 关闭会话
curl -k -X DELETE "https://192.168.1.122:56901/api/session/$SESSION_ID"
```

---

## 📊 性能优化

### 1. 调整资源限制

```yaml
# docker-compose.yml
services:
  browser:
    image: kasmweb/chrome:1.16.0_zspace_2.0
    ports:
      - "56901:6901"
    environment:
      - KASM_PORT=6901
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M
```

### 2. 启用 GPU 加速

```yaml
    devices:
      - /dev/dri:/dev/dri
```

### 3. 使用共享内存

```yaml
    shm_size: '2gb'
```

---

## 🛠️ 故障排查

### 问题 1：无法连接

**检查：**
```bash
# 容器状态
docker ps | grep browser

# 端口监听
netstat -tlnp | grep 56901

# 防火墙
iptables -L -n | grep 56901
```

**解决：**
```bash
# 重启容器
docker restart browser

# 检查日志
docker logs browser
```

### 问题 2：认证失败

**检查：**
- 用户名/密码是否正确
- Kasm 服务是否正常运行
- 网络连接是否正常

**解决：**
```bash
# 重置 Kasm 密码
docker exec browser /usr/bin/kasm_reset_admin_password.sh
```

### 问题 3：浏览器加载慢

**优化：**
- 增加内存限制
- 启用 GPU 加速
- 使用 SSD 存储
- 减少并发会话数

---

## 📝 维护计划

### 每日检查

- [ ] 容器运行状态
- [ ] 内存/CPU 使用率
- [ ] 日志错误
- [ ] 连接测试

### 每周维护

- [ ] 清理浏览器缓存
- [ ] 检查更新
- [ ] 备份配置
- [ ] 安全审计

### 每月更新

- [ ] 更新 Chrome 镜像
- [ ] 更新 Kasm 核心
- [ ] 审查访问日志
- [ ] 轮换密码

---

## 🔗 相关链接

- [Kasm 官方文档](https://kasmweb.com/docs/)
- [Kasm GitHub](https://github.com/kasmtech)
- [OpenClaw 浏览器文档](https://docs.openclaw.ai/tools/browser)

---

**配置完成时间：** 2026-03-11  
**维护者：** CEO 智能体（小马 🐴）  
**状态：** ✅ 可用
