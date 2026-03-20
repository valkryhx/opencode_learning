我把opencode 启动成服务 命令是啥 然后在哪里能看到api

Gemini said
启动命令非常简单。你只需要在你的终端里运行：

Bash
opencode serve
如果你想指定运行的端口（比如 4096），并且允许你的 Ciri（假设跑在 8000 端口）跨域调用它，可以带上参数运行：

Bash
### opencode serve --port 4096 --cors http://127.0.0.1:8000
在哪里看 API 文档？
服务成功启动后，OpenCode 已经在本地为你准备好了一份完整且可交互的 OpenAPI (Swagger UI) 文档。

你只需要在浏览器中打开：
###  http://127.0.0.1:4096/doc （请将 4096 替换为你实际指定的端口）

在这个页面里，你可以：

直观地看到所有可用的 HTTP 接口（比如我们前面提到的 POST /session 和 POST /session/{sessionID}/message）。

## 接口很多 也可以直接调但是调用过程比较复杂 建议用sdk

### pip install opencode-ai
Successfully installed opencode-ai-0.1.0a36