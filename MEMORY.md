# MEMORY.md - 长期记忆

**创建时间：** 2026-03-12  
**维护者：** 小马 🐴 (CEO 智能体)  
**最后更新：** 2026-03-12

---

## 🎯 核心身份

- **名称：** 小马 (Xiao Ma)
- **角色：** OpenClaw 智能体 / CEO 智能体
- **Emoji：** 🐴
- **Vibe：** 务实、高效、靠谱

---

## 📋 重要决策

### 配置保护策略 (2026-03-12)

**决策：** 配置文件设置为只读 (444 权限)

**原因：** 
- 配置文件被添加不支持字段导致重启循环
- 需要防止意外修改

**流程：**
```bash
# 修改配置
chmod 644 /root/.openclaw/openclaw.json  # 解锁
cp /root/.openclaw/openclaw.json /root/.openclaw/config-backups/  # 备份
vim /root/.openclaw/openclaw.json  # 修改
python3 -m json.tool /root/.openclaw/openclaw.json  # 验证
docker restart xiaoma_new  # 重启
chmod 444 /root/.openclaw/openclaw.json  # 重新锁定
```

---

### 大模型调用策略 (2026-03-12)

**决策：** 按任务类型分配最优模型

**配置：**
- 主模型：qwen3.5-plus (日常对话、长文档)
- 代码任务：qwen3-coder-next
- 复杂推理：qwen3-max-2026-01-23
- 简单任务：MiniMax-M2.5 (低成本)
- 备用模型：glm-4.7

**目标：** 性能 +33%，成本 -35%

---

### Docker 监控策略 (2026-03-12)

**决策：** 停止过度监控，专注配置保护

**原因：**
- 每 5 分钟健康检查过于频繁
- 根因是配置错误，不是容器问题

**防护措施：**
- 配置文件只读 (444)
- 配置验证脚本
- 完整备份机制

---

## 📦 技能系统

### 原创技能（GitHub Release - 6 个）

1. **openclaw-plugin-searxng** v1.0.0 - 中国大陆优化（百度/必应）
2. **openclaw-searxng-search** v1.0.0 - 5 分钟部署方案
3. **openserp-searxng-adapter** v1.0.0 - Brave API 兼容
4. **ai-humanizer-cn** v1.0.1 - 中文 AI 文本优化（三种风格）⭐
5. **searxng-auto-proxy** v2.0.0 - 自适应代理检测（~14KB 代码）
6. **clash-auto-control** v2.0.0 - 最快节点自动选择

### ClawHub 安装技能（5 个）

- find-skills（评分 4.04）
- summarize（评分 3.99）
- agent-browser（评分 3.83）
- tavily-search（评分 3.56）
- multi-search-engine（评分 3.61）

### 迭代机制

- **频率：** 每日 (工作日 08:00)
- **脚本：** daily-iterate.sh + sync-github.sh
- **版本规范：** 语义化版本 (MAJOR.MINOR.PATCH)
- **目标技能：** radar-daily-report、ai-humanizer-cn

---

## 🔄 定时任务

| 任务 | 时间 | 状态 |
|------|------|------|
| 当日总结 | 23:00 每日 | ✅ |
| 每日配置备份 | 03:00 每日 | ✅ |
| 科普文章生产 | 06:00 每日 | ✅ |
| 毫米波雷达日报 | 09:00 每日 | ✅ |
| 每周更新检查 | 09:00 周一 | ✅ |

---

## 🛡️ 配置管理

### 支持字段

✅ **支持：**
- agents.defaults.model.primary
- agents.defaults.models.*
- models.providers.*
- channels.*
- gateway.*
- plugins.*
- commands.*

❌ **不支持 (当前版本 2026.3.2)：**
- agents.defaults.fallback
- agents.taskOverrides
- browser.provider/target/kasm

### 备份位置

- **配置备份：** /root/.openclaw/config-backups/
- **完整备份：** /root/.openclaw/backups/*.tar.gz
- **记忆备份：** /root/.openclaw/backups/memory-backup/

---

## 📊 系统架构

### Docker 容器

| 容器 | 端口 | 说明 |
|------|------|------|
| xiaoma-20260328 | 8082 | OpenClaw 主容器（生产） |
| searxng | 8081 | 搜索引擎 |
| clash | 7890-7892, 9090 | 代理 |
| browser | 56901 | Kasm 浏览器 |

### 大模型配置

- **提供商：** Bailian (阿里百炼)
- **基座 URL：** https://coding.dashscope.aliyuncs.com/v1
- **API 类型：** OpenAI 兼容
- **可用模型：** 8 个

---

## 📝 重要日期

| 日期 | 事件 |
|------|------|
| 2026-03-08 | 系统恢复 |
| 2026-03-09 | 配置优化 |
| 2026-03-10 | 自动化配置 |
| 2026-03-11 | 技能开发 + ClawHub 发布（6 个原创技能） |
| 2026-03-12 | 配置故障修复 + 更新部署 + 记忆系统建立 |

### 昨日工作详情 (2026-03-11)

**工作时间：** 08:45 - 17:00 (~500 分钟)  
**迭代轮次：** 25 轮  
**完成任务：** 40+ 个  
**产出文档：** 50+ 个

**主要成果：**
1. ✅ 发布 6 个原创技能（GitHub Release）
2. ✅ 安装 5 个 ClawHub 技能
3. ✅ Clash 配置优化（最快节点自动选择）
4. ✅ SearXNG 部署优化（自适应代理检测）
5. ✅ 确立发布原则（无实际代码不发布）

**待恢复任务：**
- ⏳ 等待 ClawHub Discord 响应
- ⏳ 测试 ClawHub API 发布
- ⏳ 监控 GitHub Release 下载量

---

## 🎯 当前目标

### 系统稳定
1. **配置保护** - 只读权限 (444)，避免重启循环
2. **备份机制** - 配置 + 记忆完整备份
3. **更新部署** - 等待 PC 端协助更新到最新版

### 技能迭代
1. **每日更新** - radar-daily-report 和 ai-humanizer-cn (v1.0.1 → v1.0.2)
2. **GitHub 同步** - 自动推送 Release
3. **文档完善** - RELEASE + CHANGELOG

### 业务恢复（昨日工作）
1. **ClawHub 发布** - 等待 Discord 官方响应
2. **技能发布** - 6 个原创技能 GitHub Release
3. **Clash 优化** - 最快节点自动选择（每 5 分钟测速）
4. **SearXNG 部署** - 自适应代理检测 + 中国大陆优化
5. **文章生产** - 每日 2 篇（06:00 开始流程）
6. **雷达日报** - 每日 09:00 自动生成

### 成本优化
1. **大模型策略** - 按任务分配最优模型
2. **目标** - 性能 +33%，成本 -35%

---

## 📞 紧急恢复

### 配置故障

```bash
docker stop xiaoma_new
chmod 644 /root/.openclaw/openclaw.json
LATEST=$(ls -t /root/.openclaw/config-backups/*.json | head -1)
cp "$LATEST" /root/.openclaw/openclaw.json
docker start xiaoma_new
chmod 444 /root/.openclaw/openclaw.json
```

### 记忆恢复

```bash
cp -r /root/.openclaw/backups/memory-backup/memory/* \
      /root/.openclaw/workspace/memory/
```

### 技能迭代恢复

```bash
# 手动执行迭代
/root/.openclaw/workspace/daily-iterate.sh radar-daily-report patch
/root/.openclaw/workspace/daily-iterate.sh ai-humanizer-cn patch

# 同步 GitHub
/root/.openclaw/workspace/sync-github.sh
```

---

## 📋 发布原则（确立于 2026-03-11）

1. **无实际代码不发布** - 必须有可运行的代码
2. **无实际问题不发布** - 必须解决真实问题
3. **无创新性不发布** - 必须有独特价值
4. **坚决杜绝空壳工程** - 每个技能必须经测试验证

## 💡 经验教训

### 配置管理
- 配置文件必须设置只读保护 (444)
- 修改前必须备份
- 仅使用当前版本支持的字段
- 不支持字段：fallback, taskOverrides, browser.provider/target/kasm

### 更新流程
- 更新前完整备份（配置 + 记忆）
- 验证备份可用
- 执行更新
- 验证功能正常

### 技能发布
- GitHub Release 是可靠渠道（100% 可用）
- ClawHub 存在 API Bug（等待修复）
- 每个技能必须有实际价值

---

**最后审查：** 2026-03-16 14:05  
**下次审查：** 2026-03-23 (每周)  
**记忆版本：** v3.0（已重建 3 月 13-15 日记忆）
技能迭代恢复

```bash
# 手动执行迭代
/root/.openclaw/workspace/daily-iterate.sh radar-daily-report patch
/root/.openclaw/workspace/daily-iterate.sh ai-humanizer-cn patch

# 同步 GitHub
/root/.openclaw/workspace/sync-github.sh
```

---

## 📋 发布原则（确立于 2026-03-11）

1. **无实际代码不发布** - 必须有可运行的代码
2. **无实际问题不发布** - 必须解决真实问题
3. **无创新性不发布** - 必须有独特价值
4. **坚决杜绝空壳工程** - 每个技能必须经测试验证

## 💡 经验教训

### 配置管理
- 配置文件必须设置只读保护 (444)
- 修改前必须备份
- 仅使用当前版本支持的字段
- 不支持字段：fallback, taskOverrides, browser.provider/target/kasm

### 更新流程
- 更新前完整备份（配置 + 记忆）
- 验证备份可用
- 执行更新
- 验证功能正常

### 技能发布
- GitHub Release 是可靠渠道（100% 可用）
- ClawHub 存在 API Bug（等待修复）
- 每个技能必须有实际价值

### 备份管理 (2026-03-19)

**问题：** 3 月 18 日备份异常增大到 634M（正常 2-3M）

**根因分析：**
1. Docker 镜像备份占 2.6G（/root/.openclaw/backups/docker-images/）
2. Session 文件积累（reset/deleted 文件未清理）
3. 备份脚本未限制包含范围

**解决方案：**
- ✅ 创建自动清理脚本（cleanup-cron.sh）
- ✅ 设置 cron 任务（每天 04:00 执行）
- ✅ 保留策略：14 天备份 + 至少 2 个完整备份
- ✅ Docker 镜像备份只保留最近 1 个
- ✅ 清理报告保留最近 5 个

**清理脚本位置：**
- `/root/.openclaw/backups/cleanup-cron.sh` (cron 执行)
- `/root/.openclaw/backups/cleanup-backups.sh` (手动执行)

**Cron 任务：**
- 每天 04:00 自动执行
- 生成清理报告到 backup 目录

---

### 搜索系统故障 (2026-03-31)

**问题**：Google/DDG/Brave/Wikipedia/Google Scholar 全部被 CAPTCHA 或超时

**根因**：
- Google/DDG：所有出口 IP（mihomo/CF Workers）都被识别为数据中心流量
- Brave API：直连超时
- Wikipedia：OpenClaw 容器直连超时
- CF Workers：返回压缩二进制数据，调用方无法解压

**最优解**：`cn.bing.com/search?q=...&format=rss` via mihomo proxy

**验证结果**：
- ✅ Bing RSS via mihomo = 10条/次，完美 XML，真实 URL + 标题 + 描述 + 时间
- ✅ 中文查询：10条结果
- ✅ 英文查询：10条结果
- ✅ 跨语言稳定

**技术细节**：
- mihomo 代理：172.18.0.4:7890（clash 容器，在 openclaw_openclaw-net 网络）
- Bing RSS 端点：`https://cn.bing.com/search?q={q}&format=rss`
- OpenClaw 容器内使用 curl 调用，subprocess 方式绕过 Python urllib 的 context 参数问题

**脚本位置**：`/root/.openclaw/workspace/scripts/multi-search.py`

**已知可用数据源**：
| 来源 | 方法 | 状态 |
|------|------|------|
| Bing RSS | cn.bing.com + mihomo | ✅ 10条 |
| Baidu | SearXNG 聚合 | ✅ 9条 |
| Sogou | SearXNG 聚合 | ✅ 8条 |
| GitHub API | 直连 | ✅ 可用 |
| NPM API | 直连 | ✅ 可用 |
| Stack Exchange | 直连 | ✅ 可用 |

**彻底失败**：
- Google：所有 IP（mihomo/CF）全部 CAPTCHA
- DuckDuckGo：via mihomo = CAPTCHA
- Wikipedia：直连超时（via mihomo 未测试）
- Brave Search API：需要 Key 或直连超时
- CF Workers 做搜索代理：压缩问题无法绕过

**教训**：简单替换策略（换代理/换IP）无法解决 Google 等对自动化流量的主动防御。RSS 端点是结构化数据突破口。

**问题：** SearXNG 重建后外国引擎全部超时

**根因：**
1. SearXNG 的 httpx 不读取 `HTTP_PROXY` 环境变量，需要在 `settings.yml` 的 `outgoing.proxies` 中显式配置
2. mihomo（容器名 clash）在 `openclaw_openclaw-net`，IP `172.18.0.2`

**正确配置（SearXNG）：**
```bash
# 启动
docker run -d --name searxng \
  --network openclaw_openclaw-net \
  -e SEARXNG_SECRET="xiaoma2026" \
  searxng/searxng:latest

# 开启 json + mihomo 代理（修改 settings.yml）
docker exec searxng python3 -c "
content = open('/etc/searxng/settings.yml','rb').read()
old = b'  #  proxies:\n    all://:\n      - http://proxy1:8080'
new = b'  proxies:\n    all://:\n      - http://clash:7890'
content = content.replace(old, new)
open('/etc/searxng/settings.yml','wb').write(content)
"
docker restart searxng

# 备份（容器重建后恢复）
docker cp searxng:/etc/searxng/settings.yml /root/searxng-settings.yml
```

**引擎可用性（2026-03-27，via mihomo）：**
- ✅ bing: 10 results，中文最丰富
- ✅ sogou: 10 results
- ✅ wikipedia: 有结果（需更长超时）
- ❌ google: "access denied"（被 mihomo 规则拦截）
- ❌ duckduckgo: CAPTCHA（via 代理）
- ❌ wikidata/brave/yandex/startpage/qwant: timeout

**雷达日报配置（国际搜索优先）：**
- `SEARCH_ENGINES`: `["bing", "wikipedia", "sogou"]`（wikipedia via mihomo）
- `SEARCH_TIME_RANGE`: `"week"`
- `QUALITY_THRESHOLD`: `-6`
- `MAX_PER_CATEGORY`: `10`
- `MAX_RESULTS_PER_ENGINE`: 15（扩量）

**日报效果：** 23 条，质量大幅提升

**雷达日报脚本自适应超时：** `timeout=(10, 60)`（连接10秒/总响应60秒）

**重要教训：** SearXNG 的 httpx 不读 `HTTP_PROXY` 环境变量，必须在 `settings.yml` 的 `proxies.all://` 显式配置；mihomo 代理对大多数国际站点封禁/超时，bing 英文内容依赖直连

**日报效果（修复后）：** 26 条/类，质量大幅提升，全为真实毫米波雷达内容

---

### 搜索服务故障 (2026-03-19)

**问题：** SearXNG 无法启动，搜索引擎全部超时

**错误根因：**
1. 使用 host 网络模式导致端口冲突（`Address already in use`）
2. 容器未配置 Clash 代理，无法访问外网
3. DNS 解析失败（searxng 容器无法解析 clash 主机名）

**正确配置（已验证）：**
```bash
docker run -d --name searxng \
  -p 8081:8080 \
  -e SEARXNG_SECRET="xiaoma2026" \
  -e HTTP_PROXY="http://clash:7890" \
  -e HTTPS_PROXY="http://clash:7890" \
  --network openclaw_openclaw-net \
  searxng/searxng:latest
```

**关键步骤：**
1. Clash 必须连接到 `openclaw_openclaw-net` 网络
2. SearXNG 使用 bridge 网络（非 host 模式）
3. 代理环境变量指向容器名（非 IP）

**降级方案（紧急恢复）：**
1. web_fetch - 直接抓取搜索页面（可用）
2. Brave API - 配置 `openclaw configure --section web`
3. multi-search-engine 技能 - 本地多引擎聚合

**教训：**
- ⚠️ 每日工作前 30 分钟检查服务状态
- ⚠️ 有效配置必须文档化（MEMORY.md）
- ⚠️ 不要应付，直接解决问题

---

**最后审查：** 2026-03-19 09:09  
**下次审查：** 2026-03-26 (每周)  
**记忆版本：** v3.0（已添加备份管理机制）

---

## 🖼️ 图片选取与验证系统（2026-03-24 新增）

### 背景

2026-03-23 文章生产中出现严重图片问题：
- 5 组重复图片（宽泛关键词导致）
- 1 张错误配图（黑洞文章配玻璃瓶）
- 7 张 0 字节文件（并发下载失败）
- 过度依赖 Unsplash（资源单一）

---

## 📡 雷达日报优化（2026-03-24 10:35）

### 问题

**用户批评：** "日报就是日报，不应该出来很多之前的信息，每日内容不应该有重复"

**根因分析：**
1. ❌ 搜索范围太宽：7 天（应该 24 小时）
2. ❌ 日期过滤太松：365 天（应该 14 天）
3. ❌ 无跨日去重：和昨天内容重复
4. ❌ 情报质量差：旧闻当新闻

### 解决方案

**已实施改进：**
1. ⏰ **搜索范围：** 7 天 → 24 小时（`SEARCH_TIME_RANGE = "day"`）
2. 📅 **最大年龄：** 365 天 → 14 天（`MAX_AGE_DAYS = 14`）
3. 🚫 **跨日去重：** 自动加载并过滤昨日报纸 URL
4. 📊 **精选数量：** 40 条 → 17 条（质量优先）

**效果对比：**

| 指标 | 改进前 | 改进后 | 改进 |
|------|--------|--------|------|
| 总条目数 | 40 条 | 17 条 | -57% |
| 昨日重复 | 未过滤 | 19 条已过滤 | ✅ 100% |
| 日期范围 | 3 月 17-20 日 | 3 月 23-24 日 | ✅ 新鲜 |
| 搜索范围 | 7 天 | 24 小时 | ✅ 严格 |

### 文件修改

- `skills/radar-daily-report/generate-report.py`
  - 添加 `_load_yesterday_urls()` 函数
  - 修改 `SEARCH_TIME_RANGE = "day"`
  - 修改 `MAX_AGE_DAYS = 14`
  - 添加跨日去重逻辑

---

## 🖼️ 图片选取与验证系统（2026-03-24 新增）

### 解决方案

#### 1. 组合关键词策略

**公式：** `具体主题 + 官方来源 + 图片类型`

**示例：**
```
❌ black hole → ✅ M87 black hole EHT official
❌ exoplanet → ✅ Kepler-452b NASA artist concept
```

#### 2. 多模态验证流程

```
下载 → qwen3.5-plus 识别 → 匹配度评分 → ≥7 分通过
                                    ↓
                                <7 分重试（3 次）
```

#### 3. 科学图片资源库

**优先级：** NASA/ESA/EHT/ESO（官方）> 科研数据库 > 免费图库

### 已创建文件

- `skills/science-article-writer/SKILL.md` - 图片选取技能
- `resources/image-sources.md` - 科学图片资源库
- `articles/image-selection-system-summary.md` - 实施总结

### 质量指标

| 指标 | 改进前 | 目标 |
|------|--------|------|
| 图片重复率 | 5 组 | 0% |
| 错误图片率 | 1 张 | 0% |
| 下载成功率 | 60% | ≥95% |

### 测试验证

✅ EHT 黑洞对比图测试通过（匹配度 9.75/10）

---

**最后审查：** 2026-03-24 09:37  
**下次审查：** 2026-03-31 (每周)  
**记忆版本：** v3.1（已添加图片选取系统）

---

## 🛡️ 配置安全审查流程 (2026-03-20 新增)

### 背景

2026-03-20 发生多次配置错误修改，导致：
- 添加不支持的字段（memorySearch.provider 等）
- 配置文件大小异常波动
- Gateway 配置被意外清空

**教训：** 必须有严格的安全审查流程。

---

### 2026-04-01 配置修改记录

**修改内容：**
- research-agent：`name="小研 🔍"`, `identity.name="小研"`, `identity.emoji="🔍"` ✅
- ops-agent：`name="小维 ⚙️"`, `identity.name="小维"`, `identity.emoji="⚙️"` ✅

### 配置修改完整流程

#### 修改前（必须执行）

```bash
# 1. 运行安全审查脚本
/root/.openclaw/scripts/config-safety-check.sh

# 2. 解锁配置（自动备份）
chmod 644 /root/.openclaw/openclaw.json

# 3. 查看当前配置（可选）
cat /root/.openclaw/openclaw.json | python3 -m json.tool

# 4. 备份到 config-backups/
cp /root/.openclaw/openclaw.json /root/.openclaw/config-backups/
```

#### 修改中

```bash
# 4. 修改配置
vim /root/.openclaw/openclaw.json

# 或使用 openclaw config 命令（推荐）
openclaw config set gateway.mode local
```

#### 修改后（必须执行）

```bash
# 5. 验证 JSON 格式
python3 -m json.tool /root/.openclaw/openclaw.json > /dev/null && echo "✅ JSON 有效" || echo "❌ JSON 无效"

# 6. 运行 doctor 检查
openclaw doctor --non-interactive

# 7. 检查不支持的字段
grep -E "fallback|taskOverrides|browser\.(provider|target|kasm)|thinkingDefault" /root/.openclaw/openclaw.json && echo "⚠️ 发现不支持字段" || echo "✅ 字段检查通过"

# 8. 重启服务
docker restart xiaoma-new

# 9. 验证功能
openclaw status
openclaw memory status

# 10. 重新锁定配置
chmod 444 /root/.openclaw/openclaw.json
```

---

### 安全审查脚本

**位置：** `/root/.openclaw/scripts/config-safety-check.sh`

**检查项目：**
1. ✅ 文件存在性
2. ✅ JSON 格式验证
3. ✅ 备份检查（自动创建备份）
4. ✅ 文件大小异常检测（检测骤降 >50%）
5. ✅ OpenClaw doctor 健康检查
6. ✅ 支持的字段检查
7. ✅ 关键配置项检查
8. ✅ 文件权限检查

**使用：**
```bash
# 常规检查
/root/.openclaw/scripts/config-safety-check.sh

# 检查指定文件
/root/.openclaw/scripts/config-safety-check.sh /path/to/config.json

# 强制跳过（不推荐）
/root/.openclaw/scripts/config-safety-check.sh --force
```

---

### 不支持字段清单（当前版本 2026.3.24）

❌ **禁止使用：**
- `agents.defaults.fallback`
- `agents.taskOverrides`
- `browser.provider`
- `browser.target`
- `browser.kasm`
- `thinkingDefault` ❌ — 会报 "Unrecognized key" 错误，Gateway 无法启动
- **任何不认识的字段都会导致 Gateway 无法启动**

✅ **支持：**
- `agents.defaults.model.primary`
- `agents.defaults.models.*`
- `models.providers.*`
- `channels.*`
- `gateway.*`
- `plugins.*`
- `commands.*`
- `identity.name` ✅
- `identity.emoji` ✅
- `name` ✅

---

### 配置审计日志

**位置：** `/root/.openclaw/logs/config-audit.jsonl`

**监控字段：**
- `suspicious` - 可疑操作标记（如文件大小骤降）
- `previousBytes` / `nextBytes` - 配置大小变化
- `argv` - 修改配置的命令

**查看最近审计记录：**
```bash
tail -5 /root/.openclaw/logs/config-audit.jsonl | python3 -m json.tool
```

---

### 备份策略

**备份位置：** `/root/.openclaw/config-backups/`

**保留策略：**
- 每次修改前自动备份
- 保留最近 14 天的备份
- 至少保留 2 个完整备份

**恢复配置：**
```bash
# 查看备份
ls -lt /root/.openclaw/config-backups/*.json | head -10

# 恢复最新备份
LATEST=$(ls -t /root/.openclaw/config-backups/*.json | head -1)
cp "$LATEST" /root/.openclaw/openclaw.json
python3 -m json.tool /root/.openclaw/openclaw.json > /dev/null  # 验证
docker restart xiaoma-new  # 重启
```

---

### 紧急恢复流程

```bash
# 1. 停止容器
docker stop xiaoma_new

# 2. 解锁配置
chmod 644 /root/.openclaw/openclaw.json

# 3. 恢复备份
LATEST=$(ls -t /root/.openclaw/config-backups/*.json | head -1)
cp "$LATEST" /root/.openclaw/openclaw.json

# 4. 验证
python3 -m json.tool /root/.openclaw/openclaw.json > /dev/null

# 5. 重启
docker start xiaoma_new

# 6. 重新锁定
chmod 444 /root/.openclaw/openclaw.json
```

---

### 质量审查（发布内容）

发布技能/文档到 GitHub 前必须检查：

**代码审查：**
- [ ] 代码是否有实际功能（非空壳）
- [ ] 是否经过测试验证
- [ ] 是否有依赖问题
- [ ] 是否有敏感信息（API key 等）

**文档审查：**
- [ ] README 是否完整
- [ ] 使用示例是否清晰
- [ ] 版本信息是否正确
- [ ] 许可证是否声明

**发布审查：**
- [ ] 是否解决真实问题
- [ ] 是否有创新性
- [ ] 是否符合发布原则

---

**审查流程建立时间：** 2026-03-20 10:18  
**责任人：** 小马 🐴  
**下次审查：** 2026-03-27

---

## 🤖 秘书技能模型路由 (2026-03-20 新增)

### 背景

为了优化大模型调用成本，在 secretary-core v4.1.0 中添加了智能模型路由功能。

### 实现方案

**双层模型架构：**
1. **分析层** - qwen3.5-flash (极速、最低成本)
   - 意图识别
   - 情感分析
   - 任务分类

2. **执行层** - 根据分析结果选择最优模型
   - qwen-turbo: 简单任务
   - qwen3.5-plus: 默认平衡
   - qwen3-max: 复杂推理
   - qwen3-coder-plus: 代码任务
   - qwen-long: 长文档
   - qwen3.5-flash: 紧急任务

### 路由逻辑

```python
ModelRouter.select_model(
    intent: str,        # 意图类型
    context_length: int, # 上下文长度
    emotion: str,       # 情绪 (urgent/normal)
    task_type: str      # 任务类型 (code/chat/analysis)
)
```

**决策流程：**
1. 超长上下文 (>500K) → qwen-long
2. 紧急情况 → qwen3.5-flash
3. 代码任务 → qwen3-coder-plus
4. 复杂推理 → qwen3-max
5. 简单问题 → qwen-turbo
6. 默认 → qwen3.5-plus

### 测试结果

**测试通过率：** 8/8 (100%)

**模型使用统计示例：**
```
总请求数：6
- qwen3.5-plus: 5 次 (83%)
- qwen3.5-flash: 1 次 (17%, 紧急任务)
```

### 成本优化效果

**预计节省：** 50-70%

| 场景 | 优化前 | 优化后 | 节省 |
|------|--------|--------|------|
| 简单问答 | plus | turbo | 50% |
| 紧急任务 | plus | flash | 60% |
| 复杂推理 | plus | max | -123% (必要成本) |
| 长文档 | plus | long | 0% |

### 文件位置

- 核心代码：`/root/.openclaw/workspace/skills/secretary-core/secretary_v3.0.0.py`
- 测试脚本：`/root/.openclaw/workspace/skills/secretary-core/test_model_router.py`
- 文档：`/root/.openclaw/workspace/skills/secretary-core/SKILL.md`

### MiniMax TTS 语音生成（2026-04-02 修正）

**端点**：`POST /v1/t2a_pro`  
**模型**：`speech-02`（openclaw.json 配置）/ `speech-01`（API 接受）
**API Key**：`sk-cp-A45DfoCOhSRJwVxe2Q7gapiPBQMXkkk_UTv9s6TFO_BgdkFczMj7jmgOINWfCXhvDX8fl1TOFtSaRQst-BNqufelmuypNojNbvcVmPmZw8cWVPC6Ia`
**字段**：`text`（不是 `input`）  
**音色**：`female-tianmei`（有效，pass 音色验证）
**返回**：JSON含 `audio_file` URL（保留原始URL字符串下载）  
**音频格式**：MP3（ID3头部）

**CF Worker 回调**：已部署 `https://minimax-callback.pengong101.win`（Token: xiaoma2026callback）

**⚠️ 当前状态（2026-04-02 16:24）：配额耗尽**
- `status_code: 1008 insufficient balance`
- 音色 `female-tianmei` 和 `female-shaonv` 通过验证（返回 1008 而非 voice not exist）
- 其他音色（female-bellaixi, male-yonger 等）返回 "voice id not exist" (2054)
- 根因：MiniMaxSpeech 2.6 配额已耗尽，需要充值
- openclaw.json 中 `speech-02` 配置正确，无需修改

**✅ 历史验证成功（2026-04-02 07:36）**：
- 用户截图确认：`speech-01` + `female-tianmei` 语音生成成功
- 毫米波雷达语音内容：`"毫米波雷达日报为您服务，今日最新技术动态已生成，请查收。"`

### Git 提交

```
a2a5186 Update clawhub.json to v4.1.0
b260f5e Add model router test suite
dc017e7 Upgrade to v4.1.0: Add Model Router
```

### 下一步

- [ ] 推送到 ClawHub
- [ ] 监控实际使用情况和成本
- [ ] 根据数据优化路由策略

---

## 统一工作流系统 (2026-03-28)

### 三大核心工作流

| 工作流 | 适用场景 | 质量门 |
|--------|---------|--------|
| 📝 文档写作 | 科普文章、公号文章、文档编写 | 合规安全≥9，其他≥7 |
| 🔧 技术工作 | 脚本开发、工具搭建、环境配置 | 安全性≥9，其他≥7 |
| 🛠️ 技能研发 | Skill 开发、迭代优化、发布上线 | 创新性≥9，其他≥7 |

### 核心机制

**协调智能体轮次介入：**
- 每 3 轮迭代，协调智能体介入 1 次
- 分析根因（引用原文）、给出优化方案、分配任务
- 最多 5 次介入（15 轮），仍不达标上报 CEO 裁决

**禁止降级发布：**
- 有维度低于最低标准绝不发布
- 最终发布必须满足所有维度≥最低标准

### 工作流优化机制

**每日复盘（03:30）：**
1. 提取昨日 sessions 记录
2. 分析三大工作流执行情况
3. 识别问题模式和优化点
4. 生成优化建议清单
5. 输出到 logs/review-YYYY-MM-DD.md

**08:00 汇报 CEO 用户：**
1. 审阅优化建议
2. 确认哪些优化需要落地
3. 反馈给智能体执行

**优化落地：**
1. 执行确认的优化
2. 更新 UNIFIED-WORKFLOW-SYSTEM.md
3. 更新相关技能文档
4. 验证优化效果

### 关键文件

- `UNIFIED-WORKFLOW-SYSTEM.md` - 三大工作流完整规范
- `skills/article-writing-workflow/SKILL.md` - 文档写作工作流技能
- `scripts/daily-review.py` - 每日复盘脚本

### Cron 任务

| 任务 | 时间 | 状态 |
|------|------|------|
| 每日复盘 | 03:30 | ok |
| 科普文章选题 | 06:00 | error |
| 毫米波雷达日报 | 09:00 | ok |
| 每周更新检查 | 周一 09:00 | idle |
| 当日总结 | 23:00 | error |

### 重要决策记录 (2026-03-28)

1. **关键项自适应** — 不预设维度，关键项=当前具体问题
2. **安全合规≥9** — 最终发布条件，不可妥协
3. **轮次介入** — 每3轮介入1次协调智能体，5次上限后上报

---

**功能实现时间：** 2026-03-20 11:40  
**责任人：** 小马 🐴  
**状态：** ✅ 已完成测试

---

## TUN 模式调试记录 (2026-03-27) - 失败

### 目标
让 mihomo TUN 模式接管服务器流量，使 SearXNG 引擎走全局代理，访问 google/duckduckgo/wikipedia 等国际站点。

### 环境限制
- **服务器：虚拟化环境，/dev/net/tun 权限受限**
- `operation not permitted` - 内核 TUN 权限不足，无法创建 tun 设备
- `system` stack 和 `gvisor` stack 都无法成功初始化 TUN

### 失败过程
1. `stack: system` → "operation not permitted"
2. `stack: gvisor` → TUN 设备创建成功，但 `auto-route: true` 接管所有流量
3. mihomo 代理服务器被 TUN 劫持 → 回路死锁 → 网络完全瘫痪
4. `auto-bypass` 配置格式错误 → mihomo 启动失败（`dns-hijack` 需要 URL 格式如 `https://dns.google/dns-query`，不能用裸 IP）
5. `exclude-cidr: 103.27.186.253/32` 可以避免死锁，但环境无 TUN 权限

### 教训
- **TUN 需要 `CAP_NET_ADMIN` 权限**，虚拟机/容器环境可能无法使用
- **TUN auto-route 劫持所有流量**，必须同时配置 exclude-cidr 排除代理服务器 IP
- **mihomo dns-hijack 必须是 URL 格式**，如 `8.8.8.8:53` 无效，`https://dns.google/dns-query` 有效

### 当前可用方案（已验证）
SearXNG + mihomo HTTP 代理（端口 7890）：
- ✅ duckduckgo: 10 results
- ✅ bing: 10 results
- ✅ sogou: 10 results
- ❌ google/wikipedia/wikidata/qwant/startpage: 代理 IP 被屏蔽/超时

**TUN 模式在此环境不可行，不继续调试。**


---

## 🤖 智能体协作体系（确立于 2026-03-30）

### 标准工作流
```
用户提需求
    ↓
协调智能体（小马）：分析任务类型
    ↓
research-agent：调研，列出所有可能方案（≥3个）
    ↓
协调智能体（小马）：汇总，推荐方案 + 优劣分析
    ↓
用户决策
    ↓
ops-agent：执行选定的方案
    ↓
结果汇报
```

### 职责划分
- **CEO用户**：提需求、做决策
- **协调智能体（小马）**：判断类型、分配任务、整合结果、汇报
- **research-agent**：调研、探索、方案对比（只调研，不执行）
- **ops-agent**：执行配置、部署、故障排查（只执行，不调研）

### session 持久化机制
- **问题**：之前用 `mode=run` spawn 一次性任务，智能体无法记住长期上下文
- **解决方案**：对需要记住配置、持续工作的任务，用 `mode=session`
- **限制**：飞书不支持 `thread=true`，无法建立真正持久 session；支持平台：Discord、Telegram
- **变通**：每次 spawn 时通过 context 传递完整记忆，尽量让智能体写本地记忆文件

### ops-agent 关键记忆
- **系统架构**：OpenClaw(xiaoma_new:8082), SearXNG(searxng:8081), mihomo(clash:7890-7892)
- **SearXNG**：必须加入 openclaw_openclaw-net；settings.yml 中 outgoing.proxies 指向 http://clash:7890
- **CF Workers**：ai-proxy/arxiv-fetcher/nasa-images 已部署；Token 在 .cf-workers-credentials.json
- **配置安全**：修改前备份 → 验证JSON → chmod 444

### research-agent 关键记忆
- **调研标准**：≥3个方案 + 优劣分析 + 推荐；不购买付费API；GUI优先用API替代
- **已有能力**：SearXNG搜索、CF Workers、advanced-search(arXiv/Scholar)
- **约定**：时间加注北京时间、结构化输出

---

## 🔄 CEO智能体运作机制（确立于 2026-03-30）

### 核心原则

**MEMORY.md = 公司数据库**，不是历史记录，是实时状态。

每次事件后立即更新，不是会话结束再整理。

### 每日晨会

- **时间**：每日 07:30 北京时间
- **Cron ID**: b483b743-d3e8-4d38-b2e6-c50bfcf7d094
- **职责**：
  1. 读取 MEMORY.md + memory/YYYY-MM-DD.md
  2. 健康检查（Cron状态/日报/备份）
  3. 向用户主动汇报
  4. 更新记忆

### 任务完成后的强制记录

每次子智能体完成任务，必须立即写入 MEMORY.md：
```
## [智能体名] 任务记录
- 时间：
- 任务：
- 结果：
- 经验教训：
```

### 汇报原则

**主动汇报，不等用户问。**
- 有结果立即汇报
- 有问题立即汇报
- 有进展立即汇报

### 飞书多Bot vs 独立智能体

- 飞书支持多 Bot（每智能体独立 Bot）
- 但**不需要多 Bot**，用户只管CEO(我)，我协调所有子智能体
- 真正需要的是：MEMORY.md 持久化 + 主动汇报机制

### 调研原则（重要）

遇到问题时，**先调研再执行**：
1. 调研 OpenClaw 支持的能力
2. 对比各方案
3. 再执行最优方案

**禁止**：不调研就假设，不调研就执行。


---

## 📋 当前项目状态（2026-03-30）

### 进行中
- [ ] **CF Workers 稳定性监控** - ai-proxy/nasa-images/arxiv-fetcher 已部署，需监控是否正常
- [ ] **SearXNG 维护** - Bing/Baidu/Sogou 聚合正常，Google/DDG 等不可用

### 今日完成（2026-03-31）
- [x] **搜索系统重建** - Bing RSS via mihomo = 最优方案，10条/次
- [x] **多引擎搜索脚本** - `/root/.openclaw/workspace/scripts/multi-search.py`
- [x] **SearXNG 修复** - JSON API 格式修复（添加 json 到 formats 白名单）
- [x] **search-proxy CF Worker v2** - 部署完成（但 CF IP 仍被 Google CAPTCHA）
- [x] **Cron 任务修复** - 3个任务全部 ok

### 飞书转发问题（未解决）
- [ ] **announce 配置错误** - ops-agent 调研有误，announce 不在 agents.defaults 支持字段
- [ ] **独立智能体体系** - MEMORY.md 机制建立中

### 今日完成
- [x] CF Workers 部署（ai-proxy, nasa-images, arxiv-fetcher）
- [x] 自定义域名绑定（pengong101.win）
- [x] Cron 修复（科普文章选题/日报/当日总结）
- [x] 每日晨会建立

### 待用户决策
- [ ] **CF Workers 稳定性** - 明天验证 3 个 Worker 是否正常访问
- [ ] **飞书多Bot** - 暂不需要，当前架构满足需求


### 新任务：浏览器控制调用 Gemini/Grok
- 时间：2026-03-30 16:35
- 执行者：ops-agent
- 目标：通过浏览器自动化绕过IP封锁，调用 Gemini/Grok
- 状态：调研中

### 主动汇报机制（核心教训，2026-03-30）

**问题**：今天所有汇报都是用户问了我才说，没有主动汇报。

**后果**：用户感觉不被主动告知，智能体"不汇报"。

**解决**：CEO智能体(我)必须主动汇报，不等用户问。

**规则**：
1. 子智能体完成 → 立即向用户汇报结果
2. 发现问题 → 立即向用户汇报
3. 有进展 → 立即向用户汇报
4. 用户只问一次，我应该已经主动说了

**禁止**：
- 收到结果后"等用户来问"
- 只在用户问时才汇报
- 让用户追着问进度

### 进行中任务：测试 Gemini/Grok 访问
- 时间：2026-03-30 16:42
- 执行者：ops-agent
- 目标：找到可用代理节点，通过 Kasm Browser 访问 Gemini/Grok
- 状态：测试中

### 进行中：扩展 ai-proxy 支持 Grok
- 时间：2026-03-31 00:21
- 状态：执行中

### 协调者核心职责（确立于 2026-03-31）

**每收到任何消息，必须立即通知用户。**

收到子智能体结果 → 立即完整转发 → 用户
不允许：等一等、不重要就不说、用户没问就不说

**协调者 = 用户与智能体之间的唯一桥梁**
所有信息必须经过我，用户不需要直接与子智能体沟通

---

## 📋 当前项目状态（2026-03-31 00:38）

### 进行中
- [ ] **浏览器控制 Gemini/Grok** - ai-proxy 已支持 Grok 路由，测试通过

### 今日完成
- [x] ai-proxy 扩展 Grok 支持（/grok/ → HTTP 200 ✅）
- [x] 每日晨会 Cron 建立（07:30 北京时间）
- [x] MEMORY.md 主动汇报机制确立

### 待用户决策
- [ ] **飞书多Bot 或 thread 模式** - 需建立真正的 ops-agent 直接汇报机制

### 教训
- 协调者必须第一时间转发所有消息
- 不允许"等一等再汇报"

### 严格转发规则（确立于 2026-03-31）

**收到子智能体结果 = 必须立即发送给用户**

禁止：
- 收到结果后"等一等"
- 认为"用户知道了就不用说"
- 只在用户问时才转发

允许：
- 完整转发（ops-agent说什么我就说什么）
- 简化转发（保留核心结论即可）

技术限制：ops-agent 无法直接向用户发消息，必须经过我。

### 禁止使用 message tool 发送飞书消息

**原因**：`message` tool 在飞书 channel 失败（Unknown channel: feishu），错误通知会推送给用户

**规则**：
- ❌ 禁止使用 `message` tool 发送飞书消息
- ✅ 只用对话回复（`<final>` 标签）
- ✅ 用户所有消息都通过当前飞书对话回复

---

## 📋 当前项目状态（2026-04-01）

### Phase 1 改进已完成
- [x] **research-agent** - 重写 SOUL.md，置信度评分 + 用户确认节点
- [x] **ops-agent** - 重写 SOUL.md，分阶段汇报 + 问题即停
- [x] **main SOUL.md** - 增加 CEO 协调者规则
- [x] **智能体名称配置** - research-agent（"小研 🔍"）和 ops-agent（"小维 ⚙️"）配置完成

### Phase 2 待实施
- [ ] BITable 任务状态追踪（open/claimed/done/failed）
- [ ] Input Filter 机制

### ⚠️ 配置安全规则（重要）

修改 openclaw.json 前必须：
1. `chmod 644` 解锁
2. 备份到 config-backups/
3. `python3 -m json.tool` 验证 JSON
4. 修改后再次验证
5. `openclaw doctor --non-interactive` 健康检查
6. `docker restart xiaoma-new` 重启
7. `chmod 444` 重新锁定

### 多智能体调研报告（2026-04-01）
- `reports/multi-agent-collaboration-research-2026-04-01.md` - Claude Code + OpenClaw
- `reports/clawteam-open-source-research-2026-04-01.md` - ClawTeam 3仓库
- `reports/multi-agent-improvement-evaluation-2026-04-01.md` - 主流框架对比 + 改进方案

### 推荐改进路径
1. 置信度评分（已实施）
2. 用户确认节点（已实施）
3. Role明确化（已实施）
4. 任务状态追踪（待BITable）
5. Input Filter（待实施）

---

## 多智能体完整定义（Phase 1+2 完成，2026-04-01）

### 6个Agent配置文件完整度

| Agent | IDENTITY | SOUL | HEARTBEAT | MEMORY(workspace) | MEMORY(agentDir) | openclaw.json |
|-------|----------|------|-----------|-------------------|-----------------|---------------|
| main | ✅ | ✅ CEO规则 | — | ✅ | ✅ | ✅ name+identity |
| research-agent | ✅ 小研🔍 | ✅ 置信度+确认 | ✅ 搜索服务检查 | ✅ | ✅ | ✅ |
| ops-agent | ✅ 小维⚙️ | ✅ 分阶段汇报 | ✅ 系统+Docker检查 | ✅ | ✅ | ✅ |
| code-agent | ✅ 小码💻 | ✅ 复杂设计先确认 | — | ✅ | ✅ | ✅ |
| content-agent | ✅ 小文✍️ | ✅ 大纲先确认 | — | ✅ | ✅ | ✅ |
| review-agent | ✅ 小审🔎 | ✅ 三级审核 | — | ✅ | ✅ | ✅ |

### openclaw.json 不支持字段（2026.3.24）
- `thinkingDefault` ❌
- `agents.defaults.fallback` ❌
- `agents.taskOverrides` ❌
- `browser.provider/target/kasm` ❌

### 配置文件路径规范
- Layer 2: `~/.openclaw/workspace-<id>/` (IDENTITY/SOUL/AGENTS/MEMORY/HEARTBEAT/TOOLS)
- Layer 3: `~/.openclaw/agents/<id>/agent/MEMORY.md` (私有记忆)

---

## 技能分配方案（2026-04-01 执行）

### 技能目录结构

| 位置 | 说明 | 可见性 |
|------|------|--------|
| `~/.openclaw/skills/` | 共享技能 | 所有 agents |
| `~/.openclaw/workspace-<id>/skills/` | 专用技能 | 该 agent 专用 |
| `~/.openclaw/workspace/skills/` | main 剩余 | main 专用 |

### 共享技能（all agents）
`find-skills`, `proactive-agent`, `memory_search.py`

### 各 Agent 专用技能

| Agent | 专用技能 |
|-------|---------|
| research | multi-search-engine, radar-daily-report, tavily-search |
| ops | tech-ops, searxng-auto-proxy |
| code | github-skill, self-improving-agent, skill-creation-workflow, skill-evolver |
| content | ai-humanizer-cn, article-writing-workflow, science-article-writer, tasks |
| review | qc-evaluator, vetter-pro, pokayoke + 5个QC规范文件 |

### 技能加载优先级
`workspace/skills` > `~/.openclaw/skills` > `bundled skills` > `extraDirs`

---

## 智能体架构 v2.0（2026-04-03 升级）

### 升级来源
- **Danau5tin/multi-agent-coding-system** — 斯坦福 Terminal Bench #13，Orchestrator/Explorer/Coder 三角色架构
- **Agent Reach** — 已安装（6/16渠道可用），全网搜索+网页读取+公众号+RSS

### v2.0 核心改变

#### 原则1：Orchestrator 不碰执行
main（CEO）只做：接收需求 → 分解任务 → 分配 → 汇总 → 汇报
禁止：直接写代码、改配置、写文章

#### 原则2：Explorer = 只读验证
ResearchAgent 双重角色：
- 调研模式（主动）：搜集情报
- 验证模式（被动）：只读核查其他 Agent 产出

#### 原则3：自适应信任
根据任务复杂度调整子 Agent 自主权：
- Simple：高信任，直接执行
- Medium：中信任，关键节点汇报
- Complex：低信任，每步确认

#### 原则4：任务分配格式标准化
必须包含：任务描述 + 返回格式 + 验收标准 + 复杂度

### 各 Agent SOUL.md（v2.0 已更新）
| Agent | SOUL.md 位置 |
|-------|-------------|
| main | `/root/.openclaw/workspace/SOUL.md` |
| research-agent | `/root/.openclaw/agents/research-agent/SOUL.md` |
| code-agent | `/root/.openclaw/agents/code-agent/SOUL.md` |
| content-agent | `/root/.openclaw/agents/content-agent/SOUL.md` |
| ops-agent | `/root/.openclaw/agents/ops-agent/SOUL.md` |
| review-agent | `/root/.openclaw/agents/review-agent/SOUL.md` |

### Agent Reach（已安装，2026-04-03）
- **位置**：Docker 容器 xiaoma-20260328
- **可用渠道**：全网搜索(Jina/Exa)、网页读取、RSS、微信公众号、YouTube、GitHub
- **使用**：`mcporter call exa.web_search_exa` / `curl https://r.jina.ai/<URL>`
- **技能文件**：`/root/.openclaw/skills/agent-reach/SKILL.md`

---

## 智能体架构 v3.0（2026-04-03）

### 核心改进：协作迭代模式

**问题：** v2.0 星型结构 main 成为瓶颈，Agent 间缺乏直接协作

**解决：** Research ↔ 执行 Agent 直接协作，main 只布置任务和汇报

### 四大工作流（v3.0）

| 工作流 | 协作模式 | 审核 |
|--------|---------|------|
| 内容创作 | Research ↔ Content 直接协作 | 自评分<7时审核 |
| 技能研发 | Research ↔ Code 直接协作 | 必须审核 |
| 雷达日报 | Research → Content 直接生成 | 简化流程 |
| 运维故障 | Ops ↔ Research 协作 | 自动处理为主 |

### 关键文件
- 架构文档：`AGENTS-ARCHITECTURE.md`（v3.0）
- 工作流详细设计：`WORKFLOWS-V3.md`
- 内容创作v3.0：`WORKFLOW-CONTENT-V3.md`
- 各Agent SOUL.md：更新为v3.0协作模式

### 交接材料标准
- 素材包（Research → Content）
- 技术调研包（Research → Code）
- 作品提交（Content → Review）
- 审核反馈（Review → Agent）
