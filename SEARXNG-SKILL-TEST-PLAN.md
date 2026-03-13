# SearXNG 技能测试计划

**测试目标：** 验证 SearXNG 技能的有效性、稳定性和性能  
**测试时间：** 2026-03-11  
**测试人：** 小马 🐴

---

## 📋 测试范围

### 1. 核心功能测试
- [ ] 基本搜索功能
- [ ] 多引擎支持
- [ ] 搜索结果质量
- [ ] 错误处理

### 2. 性能测试
- [ ] 响应时间
- [ ] 并发能力
- [ ] 资源消耗
- [ ] 缓存效果

### 3. 集成测试
- [ ] OpenClaw 集成
- [ ] OpenSERP 适配器
- [ ] 配置兼容性

### 4. 兼容性测试
- [ ] 中国大陆网络环境
- [ ] 不同搜索引擎
- [ ] 不同查询类型

---

## 🧪 测试用例

### 测试用例 1：基本搜索功能

**测试目标：** 验证基本搜索是否正常工作

**测试步骤：**
```bash
# 1. 检查 SearXNG 服务状态
curl http://localhost:8081/health

# 2. 执行基本搜索
curl "http://localhost:8081/search?q=test&format=json"

# 3. 检查返回结果
# - 是否有搜索结果
# - 结果格式是否正确
# - 是否包含标题、链接、摘要
```

**预期结果：**
- ✅ 返回 HTTP 200
- ✅ JSON 格式正确
- ✅ 包含搜索结果（至少 5 条）
- ✅ 每条结果包含 title、url、content

**实际结果：**
- [ ] 通过 / 失败
- 备注：

---

### 测试用例 2：中文搜索

**测试目标：** 验证中文搜索支持

**测试步骤：**
```bash
# 测试中文查询
curl "http://localhost:8081/search?q=人工智能&format=json"
curl "http://localhost:8081/search?q=天气预报&format=json"
curl "http://localhost:8081/search?q=北京美食&format=json"
```

**预期结果：**
- ✅ 返回中文搜索结果
- ✅ 结果相关性高
- ✅ 包含百度/必应中国来源

**实际结果：**
- [ ] 通过 / 失败
- 备注：

---

### 测试用例 3：多引擎支持

**测试目标：** 验证多引擎聚合功能

**测试步骤：**
```bash
# 检查可用引擎
curl "http://localhost:8081/preferences" | grep -o '"name":"[^"]*"'

# 测试特定引擎
curl "http://localhost:8081/search?q=python&engines=baidu&format=json"
curl "http://localhost:8081/search?q=python&engines=bing&format=json"
curl "http://localhost:8081/search?q=python&engines=google&format=json"
```

**预期结果：**
- ✅ 至少支持 3 个搜索引擎
- ✅ 百度/必应中国可用
- ✅ 可以指定引擎搜索

**实际结果：**
- [ ] 通过 / 失败
- 备注：

---

### 测试用例 4：OpenSERP 适配器

**测试目标：** 验证适配器转换功能

**测试步骤：**
```bash
# 1. 启动适配器
cd /root/.openclaw/workspace/openserp-searxng-adapter
node index.js &

# 2. 测试健康检查
curl http://localhost:8765/health

# 3. 测试搜索接口
curl "http://localhost:8765/search?q=OpenClaw&count=10"

# 4. 检查输出格式
# - 是否符合 Brave API 格式
# - 是否包含 query、results、total
```

**预期结果：**
- ✅ 适配器正常启动
- ✅ 健康检查返回 ok
- ✅ 搜索结果格式正确
- ✅ 符合 Brave API 兼容格式

**实际结果：**
- [ ] 通过 / 失败
- 备注：

---

### 测试用例 5：OpenClaw 集成

**测试目标：** 验证在 OpenClaw 中的实际使用

**测试步骤：**
```bash
# 1. 配置 OpenClaw 使用 OpenSERP
# 编辑 ~/.openclaw/openclaw.json 或 models.json
{
  "tools": {
    "web": {
      "search": {
        "provider": "brave",
        "baseUrl": "http://localhost:8765"
      }
    }
  }
}

# 2. 重启 OpenClaw Gateway
openclaw gateway restart

# 3. 在对话中测试搜索
"搜索 OpenClaw 最新功能"
"搜索 AI Agent 发展趋势"
"搜索 2026 年技术热点"
```

**预期结果：**
- ✅ OpenClaw 能正常调用搜索
- ✅ 返回相关结果
- ✅ 结果能用于回答问题

**实际结果：**
- [ ] 通过 / 失败
- 备注：

---

### 测试用例 6：响应时间测试

**测试目标：** 测量搜索响应时间

**测试步骤：**
```bash
# 测试 10 次搜索，记录时间
for i in {1..10}; do
  start=$(date +%s%N)
  curl -s "http://localhost:8081/search?q=test$i&format=json" > /dev/null
  end=$(date +%s%N)
  duration=$(( (end - start) / 1000000 ))
  echo "Request $i: ${duration}ms"
done
```

**预期结果：**
- ✅ 平均响应时间 < 5 秒
- ✅ 最快响应 < 2 秒
- ✅ 最慢响应 < 10 秒

**实际结果：**
- 平均：___ ms
- 最快：___ ms
- 最慢：___ ms
- [ ] 通过 / 失败

---

### 测试用例 7：搜索结果质量

**测试目标：** 评估搜索结果的相关性

**测试查询：**
1. "OpenClaw AI assistant" - 应该返回 OpenClaw 相关信息
2. "SearXNG privacy search" - 应该返回 SearXNG 官方信息
3. "2026 AI trends" - 应该返回最新的 AI 趋势文章
4. "北京天气" - 应该返回北京天气预报

**评分标准：**
- ⭐⭐⭐⭐⭐ 前 3 条结果完全相关
- ⭐⭐⭐⭐ 前 5 条结果大部分相关
- ⭐⭐⭐ 前 10 条结果一半相关
- ⭐⭐ 结果相关性较低
- ⭐ 结果不相关

**实际结果：**
| 查询 | 评分 | 备注 |
|------|------|------|
| OpenClaw AI assistant | ⭐ | |
| SearXNG privacy search | ⭐ | |
| 2026 AI trends | ⭐ | |
| 北京天气 | ⭐ | |

---

### 测试用例 8：错误处理

**测试目标：** 验证错误情况处理

**测试步骤：**
```bash
# 1. 空查询
curl "http://localhost:8081/search?q=&format=json"

# 2. 特殊字符
curl "http://localhost:8081/search?q=<script>alert(1)</script>&format=json"

# 3. 超长查询
curl "http://localhost:8081/search?q=$(python3 -c 'print("a"*10000)')&format=json"

# 4. 服务不可用
# 停止 SearXNG 后测试
curl "http://localhost:8081/search?q=test&format=json"
```

**预期结果：**
- ✅ 空查询返回友好错误
- ✅ 特殊字符被正确处理
- ✅ 超长查询被拒绝或截断
- ✅ 服务不可用时返回明确错误

**实际结果：**
- [ ] 通过 / 失败
- 备注：

---

### 测试用例 9：并发测试

**测试目标：** 测试并发请求处理能力

**测试步骤：**
```bash
# 使用 ab 或 wrk 进行压力测试
# 100 个请求，10 个并发
ab -n 100 -c 10 "http://localhost:8081/search?q=test&format=json"

# 或使用 curl 并发
for i in {1..20}; do
  curl -s "http://localhost:8081/search?q=test$i&format=json" > /dev/null &
done
wait
```

**预期结果：**
- ✅ 支持至少 10 个并发请求
- ✅ 无请求失败
- ✅ 平均响应时间无明显下降

**实际结果：**
- [ ] 通过 / 失败
- 备注：

---

### 测试用例 10：中国大陆网络环境

**测试目标：** 验证在中国大陆的可用性

**测试步骤：**
```bash
# 1. 测试百度引擎
curl "http://localhost:8081/search?q=人工智能&engines=baidu&format=json"

# 2. 测试必应中国
curl "http://localhost:8081/search?q=AI 技术&engines=bing&format=json"

# 3. 测试搜狗（如果配置）
curl "http://localhost:8081/search?q=新闻&engines=sogou&format=json"

# 4. 测试 360 搜索（如果配置）
curl "http://localhost:8081/search?q=百科&engines=360&format=json"
```

**预期结果：**
- ✅ 百度搜索结果正常
- ✅ 必应中国搜索结果正常
- ✅ 响应时间 < 10 秒
- ✅ 无超时错误

**实际结果：**
- [ ] 通过 / 失败
- 备注：

---

## 📊 性能基准

### 响应时间基准

| 场景 | 目标 | 可接受 | 实际 |
|------|------|--------|------|
| 简单查询 | <2s | <5s | ___ |
| 中文查询 | <3s | <8s | ___ |
| 多引擎查询 | <5s | <10s | ___ |
| 复杂查询 | <5s | <15s | ___ |

### 搜索结果数量基准

| 查询类型 | 目标结果数 | 最少可接受 | 实际 |
|----------|-----------|-----------|------|
| 通用查询 | >20 | >10 | ___ |
| 专业查询 | >10 | >5 | ___ |
| 中文查询 | >15 | >8 | ___ |

### 资源消耗基准

| 指标 | 目标 | 可接受 | 实际 |
|------|------|--------|------|
| CPU 使用率 | <50% | <80% | ___ |
| 内存使用 | <500MB | <1GB | ___ |
| 磁盘 IO | 低 | 中 | ___ |

---

## ✅ 验收标准

### 必须通过（P0）

- [ ] 基本搜索功能正常
- [ ] 中文搜索可用
- [ ] OpenSERP 适配器工作正常
- [ ] 响应时间 < 10 秒
- [ ] 无严重错误

### 应该通过（P1）

- [ ] 多引擎支持正常
- [ ] 搜索结果质量高（>⭐⭐⭐⭐）
- [ ] 错误处理完善
- [ ] 并发支持 >10
- [ ] 中国大陆网络可用

### 最好通过（P2）

- [ ] 响应时间 < 5 秒
- [ ] 搜索结果质量极高（>⭐⭐⭐⭐⭐）
- [ ] 缓存功能正常
- [ ] 资源消耗低
- [ ] 监控告警完善

---

## 📝 测试报告模板

```markdown
# SearXNG 技能测试报告

**测试日期：** 2026-03-11  
**测试版本：** v1.0.0  
**测试人：** 小马 🐴

## 总体结果

- 总测试用例：10
- 通过：__
- 失败：__
- 跳过：__
- 通过率：__%

## 性能 summary

- 平均响应时间：___ ms
- 搜索结果质量：⭐⭐⭐⭐
- 并发能力：___ req/s
- 资源消耗：CPU __%, MEM ___MB

## 发现的问题

1. [严重] 问题描述...
2. [中等] 问题描述...
3. [轻微] 问题描述...

## 改进建议

1. ...
2. ...
3. ...

## 发布建议

- [ ] ✅ 可以发布
- [ ] ⚠️ 需要修复后发布
- [ ] ❌ 不建议发布

**理由：** ...
```

---

## 🚀 执行测试

### 准备阶段

```bash
# 1. 检查 SearXNG 服务
docker ps | grep searxng

# 2. 检查适配器服务
ps aux | grep openserp

# 3. 检查 OpenClaw 配置
cat ~/.openclaw/openclaw.json | grep -A5 search
```

### 执行阶段

按顺序执行上述测试用例，记录结果。

### 报告阶段

生成测试报告，决定是否发布。

---

**下一步：** 开始执行测试用例 1-10，记录实际结果。
