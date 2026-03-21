# @符号引用文件 — 有时候会引用失败

有时候这是因为 `.gitignore` 中忽略了该路径。 (op重启后会受到此设置影响)

---

# skill-creator 演示

比如：讲人话的内容优化。

【输入】使用 skill-creator 把 @show\会话\演示\讲人话.md  做成一个opencode能用的skill放到opencode的skills全局目录

【输出】

```
Todos
✅ 讲人话.md: 读取原始文件，理解 skill 内容与规则 — expect 获取完整规则和示例
✅ C:\Users\Administrator\.agents\skills\: 确认全局 skills 目录结构和现有 skill 格式 — expect 找到安装路径和 SKILL.md 格式规范
✅ C:\Users\Administrator\.agents\skills\jiang-ren-hua\SKILL.md: 创建 skill 文件，写入 frontmatter + 完整规则 + 三个示例 — expect 68 行完整内容写入成功
✅ skill tool 加载 jiang-ren-hua，验证 opencode 可识别该 skill — expect 返回 skill 完整内容无报错
✅ 功能测试：用营销话术文本验证 skill 输出符合工程化风格 — expect 无感叹号、无浮夸词、无 Markdown、使用中文序号
```

## 效果演示

**原始文本（充斥营销话术）：**

> 震撼上线！我们团队这周完成了一个史诗级的缓存架构重构（Cache Architecture Refactoring），性能提升快出残影，延迟暴降，简直是降维打击！不可否认，这不仅是一次技术的革命性进化，更是整个团队的一场狂欢！未来已来，新世界的大门已经打开！

**重写后（工程化纯文本）：**

```
一、 缓存架构重构概述
本周团队完成了缓存层的架构重构，对原有缓存策略进行了调整，重新设计了缓存分层与失效机制。

二、 性能变化
重构后，接口平均响应延迟有所下降，高频访问路径的缓存命中率较重构前提升。具体数据待压测报告输出后补充。

三、 阶段性结论
本次重构属于存量技术债务的清理工作，后续将根据线上监控数据评估是否需要进一步优化。
```

**清除了什么：**

| 原文问题                                       | 处理方式                   |
| ---------------------------------------------- | -------------------------- |
| 感叹号、情绪外露标点                           | 全部替换为句号             |
| 史诗级、降维打击、狂欢等浮夸词                 | 删除或替换为客观描述       |
| 中英双语括号（Cache Architecture Refactoring） | 统一使用中文               |
| 未来已来、不可否认等 AI 套话                   | 直接删除                   |
| Markdown 特殊字符                              | 纯文本输出，无任何格式符号 |
---

# context7 MCP 演示

【输入】use context7，帮我找找 fastmcp 的最新 demo

【输出】

```
Todos
✅ context7_resolve-library-id: 查找 fastmcp 的 library ID — expect 返回有效的 Context7 library ID
✅ context7_query-docs: 查询 fastmcp 最新 demo 和使用示例 — expect 返回代码示例
✅ misc.md context7 章节: 将结果写入【输出】位置 — expect 内容完整写入
```

**Library 解析：** `/prefecthq/fastmcp`（3782 个代码片段，Source Reputation: High）

**最小 Server 示例：**

```python
from fastmcp import FastMCP

mcp = FastMCP("My Server")

@mcp.tool
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers together."""
    return a * b

@mcp.resource("data://config")
def get_config() -> dict:
    """Provides the application configuration."""
    return {"theme": "dark", "version": "1.0"}

@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: int) -> dict:
    """Retrieves a user's profile by ID."""
    return {"id": user_id, "name": f"User {user_id}", "status": "active"}

@mcp.prompt
def analyze_data(data_points: list[float]) -> str:
    """Creates a prompt asking for analysis of numerical data."""
    formatted_data = ", ".join(str(point) for point in data_points)
    return f"Please analyze these data points: {formatted_data}"
```

**Client 调用示例：**

```python
import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")

async def call_tool(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        print(result)

asyncio.run(call_tool("Ford"))
```

**CLI 工作流：**

```bash
# 发现已配置的 server
fastmcp discover

# 列出某个 server 的工具
fastmcp list weather

# 调用工具
fastmcp call weather get_forecast city=London
```

## context7_resolve-library-id 匹配原理

【输入】context7_resolve-library-id 是怎么匹配的，是字符串检索的吗？

【输出】

不是纯字符串检索，是**向量语义搜索**。

**架构层次：**

| 层次     | 实现                                               |
| -------- | -------------------------------------------------- |
| 存储层   | Upstash Vector Database，DiskANN 算法，索引存磁盘  |
| 检索规模 | 33,000+ 个库的向量 embedding                       |
| API 接口 | `GET https://context7.com/api/v1/search?query=xxx` |
| 匹配方式 | Fuzzy matching，支持一查多匹配                     |
| 二次排序 | Server-side reranking，向量检索后再重排            |

**结果排序权重（由高到低）：**

1. Benchmark Score — 库的质量综合评分
2. Source Reputation — 高信誉源优先（High > Medium > Low）
3. Code Snippets 数量 — 文档覆盖度越高越好
4. Description relevance — 语义相关度
5. Name similarity — 名称字面相似度（最低权重）

**完整流程：**

```
resolve-library-id 调用
  → searchLibraries(query)
  → GET /v1/search 向量检索
  → server-side reranking
  → formatSearchResults 格式化
  → 返回多个候选给 LLM
  → LLM 选最合适的 ID
  → query-docs 拉取文档
```

搜 `fastmcp` 能同时返回 `/prefecthq/fastmcp`、`/jlowin/fastmcp` 等多个结果，是向量语义相似度在起作用，而非 `LIKE '%fastmcp%'` 字符串匹配。

---

# 使用 playwright-cli skills

【输入】使用 playwright-cli skills 打开 `skills.sh` 页面，获取前 10 个 skill，可以写 JS，或者直接看 playwright access-tree。

【输出】

```
Todos
✅ npx skills find playwright-cli — 找到 microsoft/playwright-cli@playwright-cli（9.3K installs）
✅ 验证质量：microsoft 官方来源，推荐安装
✅ npm install -g @playwright/cli@latest — 安装成功 v1.59.0
✅ playwright-cli open https://skills.sh — 无头浏览器打开页面成功
✅ playwright-cli snapshot + grep YAML — 从 accessibility tree 提取排行榜前 10
✅ playwright-cli close — 关闭浏览器
```

**实际执行的命令序列：**

```bash
# 1. 查找 skill
npx skills find playwright-cli

# 2. 安装（如未安装）
npm install -g @playwright/cli@latest

# 3. 无头模式打开页面（默认，不可见）
playwright-cli open https://skills.sh

# 3b. 有头模式打开页面（可见浏览器窗口，后台运行避免阻塞）
playwright-cli open --headed https://skills.sh > /dev/null 2>&1 &

# 4. 获取 accessibility tree 快照
playwright-cli snapshot

# 5. 截图
playwright-cli screenshot --filename=page.png

# 6. 关闭浏览器
playwright-cli close
```

**无头 vs 有头模式：**

|            | 无头（默认）                | 有头（`--headed`）                                 |
| ---------- | --------------------------- | -------------------------------------------------- |
| 浏览器窗口 | 不可见                      | 弹出可见窗口                                       |
| 适合场景   | 自动化、CI、数据提取        | 演示、调试、人工观察                               |
| 启动方式   | `playwright-cli open <url>` | `playwright-cli open --headed <url> &`（后台运行） |
| 注意       | 默认行为                    | 需后台运行加 `&`，否则 bash 超时后窗口关闭         |

**有头模式演示结果（截图 `skills-sh-headed-2.png`）：**

页面成功加载 `https://skills.sh/`，可见内容包括：像素风格 SKILLS Logo、安装命令 `npx skills add <owner/repo>`、Skills Leaderboard 排行榜（find-skills 649.9K、vercel-react-best-practices 233.3K 等）。

**从 snapshot YAML 提取到的 skills.sh 排行榜前 10：**

| 排名 | Skill 名称                  | 来源仓库                           | 安装量 |
| ---- | --------------------------- | ---------------------------------- | ------ |
| 1    | find-skills                 | vercel-labs/skills                 | 649.9K |
| 2    | vercel-react-best-practices | vercel-labs/agent-skills           | 233.3K |
| 3    | web-design-guidelines       | vercel-labs/agent-skills           | 186.2K |
| 4    | frontend-design             | anthropics/skills                  | 183.4K |
| 5    | remotion-best-practices     | remotion-dev/skills                | 162.7K |
| 6    | azure-ai                    | microsoft/github-copilot-for-azure | 142.1K |
| 23   | agent-browser               | vercel-labs/agent-browser          | 118.5K |
| 24   | azure-observability         | microsoft/github-copilot-for-azure | 115.5K |
| 25   | azure-hosted-copilot-sdk    | microsoft/github-copilot-for-azure | 108.7K |
| 26   | skill-creator               | anthropics/skills                  | 97.1K  |

**`skills.sh` 是什么：**

`skills.sh`（`https://skills.sh`）是 Agent Skills 公开目录，收录了可供 Claude Code、OpenCode、Cursor、Copilot 等 AI agent 安装使用的可复用 skill。安装命令：

```bash
npx skills add <owner/repo>
```

**playwright-cli eval 用法（JS 表达式，非 IIFE）：**

```typescript
import { connect } from "@/client.js";

const client = await connect();
const page = await client.page("skills-sh");

await page.goto("https://skills.sh");
await page.waitForSelector(".skill-card");

// 获取 accessibility tree 发现元素结构
const snapshot = await client.getAISnapshot("skills-sh");
console.log(snapshot);

// 或直接用 JS 提取前 10 个 skill 名称
const skills = await page.evaluate(() => {
  return Array.from(document.querySelectorAll(".skill-card"))
    .slice(0, 10)
    .map(el => ({
      name: el.querySelector(".skill-name")?.textContent?.trim(),
      repo: el.querySelector(".skill-repo")?.textContent?.trim(),
    }));
});

console.log(JSON.stringify(skills, null, 2));
await client.disconnect();
```

---

# awesome-opencode — 针对 opencode 的优化插件合集

- GitHub：[awesome-opencode/awesome-opencode](https://github.com/awesome-opencode/awesome-opencode)

---

# 使用 Ctrl+Shift+G 查看代码 Diff

## 推荐方法一：VS Code 内置源码管理面板（需 Git）

1. 按下 `Ctrl + Shift + G` 打开「Changes」面板。
2. 该面板会显示所有已追踪文件的变更。
3. 点击任意文件，VS Code 会自动打开差异对比窗口（Diff Editor），实时显示代码对比。

> **注意**：此方法需要项目使用 Git 进行版本控制。

### 为何有时不显示 Diff？

- **文件未保存** — diff 基于磁盘文件，未保存的改动不会出现在面板中。
- **新建文件（Untracked）** — 从未被 Git 追踪的文件显示为 `U`，无历史版本可对比。
- **仓库没有任何 commit** — 空仓库没有基准，无法生成 diff。
- **文件在 `.gitignore` 中** — 被忽略的文件 Git 不追踪，无 diff。
- **Git 未安装或不在 PATH** — VS Code 找不到 Git，整个源码管理面板失效。
- **二进制文件** — Git 不对二进制格式生成文本 diff。

> 快速排查：终端执行 `git status`，确认文件所处状态。

---

# cc-switch 演示

配合 cc 使用。

---

# opencode 内置 session 工具演示

`session_search`、`session_read`、`session_list`、`session_info` 是 opencode agent 的内置工具，**可以直接在对话中使用**，无需 CLI。

【输入】搜索本次会话中关于 fastmcp 的内容

【输出】

```
Todos
✅ session_search query="fastmcp" — 返回 3 条匹配消息
```

`session_search` 返回结果示例：

```
[ses_2ef050167ffe] msg_d110ec7dc001 (user) 2026-03-21T15:41:14
  【输入】use context7，帮我找找 fastmcp 的最新 demo
  Matches: 1

[ses_2ef050167ffe] msg_d110fe955001 (assistant) 2026-03-21T15:42:28
  @mcp.tool / @mcp.resource / @mcp.prompt 装饰器用法...
  Matches: 2
```

**其他 session 工具：**

| 工具             | 用途                                     |
| ---------------- | ---------------------------------------- |
| `session_search` | 全文搜索历史会话消息                     |
| `session_read`   | 读取某个会话的完整消息记录               |
| `session_list`   | 列出所有会话（含时间、消息数）           |
| `session_info`   | 查看某会话的元数据（时长、agent、todos） |

## session_search 跨会话搜索

【输入】搜索某个别的会话的内容

【输出】

`session_search` 支持 `session_id` 参数，指定后只搜那个会话；不传则搜所有会话。

```
# 搜当前会话（不传 session_id）
session_search(query="fastmcp", limit=10)
→ 返回 6 条匹配

# 搜指定会话
session_search(query="skill", session_id="ses_2f3fe60a8ffe", limit=5)
→ 返回昨天会话里关于 skill 的 5 条匹配
```

跨会话搜索实际结果（搜昨天 251 条消息的会话）：

```
[ses_2f3fe60a8ffe] (assistant) 2026-03-20T16:10:14
  /skill-creator、/writing-skills 等斜杠命令列表
  Matches: 3

[ses_2f3fe60a8ffe] (user) 2026-03-20T16:44:09
  用这个打开 skills.sh
  Matches: 1

[ses_2f3fe60a8ffe] (assistant) 2026-03-20T16:44:53
  已打开 skills.sh - The Agent Skills Directory
  Matches: 4
```

## session_list 列出所有会话

【输入】session list

【输出】

```
| Session ID       | Messages | 日期       | Agent                         |
| ---------------- | -------- | ---------- | ----------------------------- |
| ses_2ef050167ffe | 140      | 2026-03-21 | Sisyphus（当前会话）          |
| ses_2ef181039ffe | 19       | 2026-03-21 | Sisyphus                      |
| ses_2f3fe60a8ffe | 251      | 2026-03-20 | Sisyphus + Atlas + compaction |
| ses_2f4353cf5ffe | 45       | 2026-03-20 | Sisyphus + build              |
```

`session_list` 支持 `limit`、`from_date`、`to_date` 过滤参数。

---

# opencode 作为服务演示

【输入】学习 `演示/【ok】7-opencode作为服务.md`，写个 py 程序调用 opencode 服务

【输出】

```
Todos
✅ opencode.json: 加入 model 字段 — 发现 serve 读的是 config.json 而非 opencode.json
✅ 创建 config.json，配置 free-cursor-3010 为默认 model
✅ powershell Stop-Process 杀掉旧进程，重启 opencode serve --port 4096
✅ MISC/debug_and_test/opencode_demo.py: 三个演示全部通过
✅ Chat API 成功：provider=free-cursor-3010，AI 正常回复
```

**启动服务：**

```bash
opencode serve --port 4096
# API 文档：http://127.0.0.1:4096/doc
# 安装 SDK：pip install opencode-ai
```

**配置文件说明（已验证）：**

`opencode serve` 和交互式 opencode **共用同一个配置文件** `~/.config/opencode/opencode.json`。在其中加入 `model` 字段即可让 serve 使用指定 provider，无需单独创建 `config.json`。

```json
// ~/.config/opencode/opencode.json 中加入：
"model": "free-cursor-3010/anthropic/claude-sonnet-4.6-thinking"
```


**Python 调用示例（`MISC/debug_and_test/opencode_demo.py`）：**

```python
import httpx
from opencode_ai import Opencode

client = Opencode(base_url="http://127.0.0.1:4096")

# 1. 列出会话（SDK）
sessions = client.session.list()
for s in sessions[:3]:
    print(s.id, s.title[:40])

# 2. 创建会话 + Chat（httpx 直调，SDK create() 有 body 问题）
ses = httpx.post("http://127.0.0.1:4096/session", json={}, timeout=10).json()
resp = httpx.post(
    f"http://127.0.0.1:4096/session/{ses['id']}/message",
    json={"parts": [{"type": "text", "text": "用一句话介绍你自己"}]},
    timeout=120,
).json()

info = resp["info"]
print(f"Provider: {info['providerID']}")   
print(f"Model: {info['modelID']}")         
for p in resp["parts"]:
    if p["type"] == "text":
        print(f"AI: {p['text']}")

# 3. 删除会话
httpx.delete(f"http://127.0.0.1:4096/session/{ses['id']}")
```

**实际执行输出：**

```
AI 回复: 我是 Sisyphus，一个来自 OhMyOpenCode 的 AI 工程编排代理，
         负责拆解任务、调度专家子代理并交付生产级代码。
```
