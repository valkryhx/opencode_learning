### OpenCode + Draw.io 极客配置手册(https://skills.sh/bahayonghang/drawio-skills/drawio)
### 0. repo: https://github.com/bahayonghang/drawio-skills

### 注意配置方式跟官网不太一致
opencode 的mcp 配置  注意 type:local  以及 command 要写到一个数组
"drawio": {
      "type": "local",
      "enabled": true,
      "command": [
        "cmd",
        "/c",
        "npx",
        "--yes",
        "@next-ai-drawio/mcp-server@latest"
      ],
    },


### antigravity 的mcp 配置 没这么刁钻


1. 核心架构：双剑合璧
这套方案通过 逻辑层 (Skill) 与 执行层 (MCP) 分离，实现了“会思考、能动手”的绘图能力：

Skill (大脑): 提供绘图模板、XML 规范及审美逻辑。

MCP Server (肌肉): 提供文件写入、格式转换（PNG/SVG）及浏览器预览的物理接口。

2. 技能安装 (Logic Layer)
通过 npx skills 工具实现全局安装，确保所有项目共享绘图逻辑：

安装命令:

PowerShell
npx skills add https://github.com/bahayonghang/drawio-skills --skill drawio
物理路径: C:\Users\drago\.agents\skills\drawio

关键特性: 支持符号链接 (Symlink)，修改本地 Skill 文件即可全局生效。

3. MCP 服务配置 (Execution Layer)
在 antigravity 的 mcpServers 配置中注入，采用 Cloud-Sync (云端同步) 模式以保持版本领先：

JSON
{
  "mcpServers": {
    "drawio": {
      "type": "stdio",
      "command": "cmd",
      "args": [
        "/c", 
        "npx", 
        "--yes", 
        "--prefer-online", 
        "@next-ai-drawio/mcp-server@latest"
      ]
    }
  }
}
--yes: 自动跳过安装确认。

--prefer-online: 优先检查更新，网络不通时回退本地缓存。

cmd /c: 解决 Windows 环境下 npx 直接调用的路径阻塞问题。

4. 典型工作流
环境预检: AI 通过 find-skills 确认 drawio 技能可用。

内容提取: AI 读取 SESSIONS_LOG.md 或源码，梳理逻辑关系。

图形生成:

Skill 将自然语言转为 .drawio 的 XML 源码。

MCP Server 将源码写入本地文件并导出为图片。

即时反馈: 自动在浏览器打开图形预览，或直接在编辑器内展示图片。

5. 极客调试建议
刷新机制: 若安装后无法识别，在聊天框执行 /reload 或重启客户端。

中文字体: 绘图若乱码，确保 Windows 环境变量 PYTHONIOENCODING=utf-8 已设置。

导出增强: 若需导出 PDF，需在本地安装 draw.io 桌面客户端并添加至系统 PATH。