# OpenClaw 配置备份与恢复指南

**版本：** 1.0  
**更新日期：** 2026-03-11  
**适用场景：** 配置修改后重启失败、配置丢失、系统崩溃恢复

---

## 🔍 问题根因分析

### 常见失败原因

1. **SearXNG 配置问题**
   - `use_default_settings: true` 覆盖自定义配置
   - 引擎因网络超时被禁用
   - 配置文件格式错误

2. **OpenClaw 配置问题**
   - 不支持的配置项（如 `web_search`）
   - JSON 格式错误
   - 模型配置与 `models.json` 不一致

3. **容器重启问题**
   - 配置文件未持久化到宿主机
   - 容器启动时覆盖配置
   - 网络未就绪导致服务启动失败

---

## 📦 备份策略

### 三级备份机制

#### 1. 自动备份（每日）
- **时间：** 每天凌晨 3:00
- **内容：** 全量配置
- **保留：** 7 天
- **位置：** `/root/.openclaw/backups/`

#### 2. 手动备份（修改前）
- **时机：** 每次修改配置前
- **命令：** `/root/.openclaw/scripts/backup.sh`
- **特点：** 即时可用

#### 3. 关键配置快照
- **文件：** 单独备份关键配置文件
- **位置：** `/root/.openclaw/workspace/config-snapshots/`

---

## 🛠️ 恢复方案

### 方案 A：自动恢复脚本

**使用场景：** 配置错误导致服务无法启动

```bash
# 1. 查看可用备份
ls -lh /root/.openclaw/backups/

# 2. 恢复最新备份
tar -xzf /root/.openclaw/backups/openclaw_backup_LATEST.tar.gz -C /

# 3. 重启服务
openclaw gateway restart

# 4. 验证状态
openclaw status
```

### 方案 B：手动恢复特定配置

**使用场景：** 部分配置错误

#### SearXNG 配置恢复

```bash
# 1. 停止 SearXNG
docker stop searxng

# 2. 恢复配置文件
cp /root/.openclaw/workspace/config-snapshots/searxng-settings.yml /root/searxng/searxng/settings.yml

# 3. 重启 SearXNG
docker start searxng

# 4. 验证
curl http://192.168.1.122:8081/
```

#### OpenClaw 配置恢复

```bash
# 1. 停止 Gateway
openclaw gateway stop

# 2. 恢复配置
cp /root/.openclaw/workspace/config-snapshots/openclaw.json /root/.openclaw/openclaw.json
cp /root/.openclaw/workspace/config-snapshots/models.json /root/.openclaw/agents/main/agent/models.json

# 3. 重启 Gateway
openclaw gateway start

# 4. 验证
openclaw status
```

### 方案 C：完全重建

**使用场景：** 系统崩溃或配置完全损坏

```bash
# 1. 创建新备份（备份当前状态）
/root/.openclaw/scripts/backup.sh

# 2. 停止所有服务
docker stop searxng
openclaw gateway stop

# 3. 删除损坏配置
rm -rf /root/.openclaw/openclaw.json
rm -rf /root/searxng/searxng/settings.yml

# 4. 从备份恢复
tar -xzf /root/.openclaw/backups/openclaw_backup_BEST.tar.gz -C /

# 5. 重启服务
docker start searxng
openclaw gateway start
```

---

## 📋 预防措施

### 1. 修改前必做

```bash
# 修改任何配置前，先备份
/root/.openclaw/scripts/backup.sh
echo "备份完成：$(ls -t /root/.openclaw/backups/ | head -1)"
```

### 2. 配置验证

```bash
# 验证 JSON 配置
python3 -m json.tool /root/.openclaw/openclaw.json > /dev/null && echo "✅ JSON 有效" || echo "❌ JSON 无效"

# 验证 YAML 配置
docker exec searxng python3 -c "import yaml; yaml.safe_load(open('/etc/searxng/settings.yml'))" && echo "✅ YAML 有效" || echo "❌ YAML 无效"
```

### 3. 渐进式修改

- 一次只修改一个配置项
- 每次修改后测试验证
- 确认无误后再继续下一步

### 4. 配置文档化

- 记录每次修改的内容
- 记录修改时间和原因
- 保存测试验证结果

---

## 🔧 快速参考

### 备份命令
```bash
/root/.openclaw/scripts/backup.sh
```

### 恢复命令
```bash
tar -xzf /root/.openclaw/backups/openclaw_backup_YYYYMMDD_HHMMSS.tar.gz -C /
```

### 验证命令
```bash
# OpenClaw 状态
openclaw status

# SearXNG 状态
curl http://192.168.1.122:8081/health

# 搜索测试
curl "http://localhost:8765/search?q=test&count=3"
```

### 日志查看
```bash
# OpenClaw 日志
openclaw gateway logs

# SearXNG 日志
docker logs searxng --tail 50
```

---

## 📞 故障排查流程

1. **检查服务状态**
   ```bash
   openclaw status
   docker ps | grep searxng
   ```

2. **查看错误日志**
   ```bash
   openclaw gateway logs
   docker logs searxng
   ```

3. **验证配置文件**
   ```bash
   python3 -m json.tool /root/.openclaw/openclaw.json
   ```

4. **尝试恢复**
   ```bash
   /root/.openclaw/scripts/backup.sh
   # 选择最近的备份恢复
   ```

5. **联系支持**
   - GitHub Issues: https://github.com/小马 🐴/openclaw-plugin-searxng/issues
   - 查看文档：`/root/.openclaw/workspace/AUTOMATION.md`

---

## 📊 备份文件说明

```
/root/.openclaw/backups/
├── openclaw_backup_20260311_030000.tar.gz  # 自动备份
├── openclaw_backup_20260311_004600.tar.gz  # 手动备份
└── ...

备份内容:
- /root/.openclaw/openclaw.json
- /root/.openclaw/agents/
- /root/.openclaw/cron/
- /root/.openclaw/workspace/
```

---

**最后更新：** 2026-03-11  
**维护人：** 小马 🐴
