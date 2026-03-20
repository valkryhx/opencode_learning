
## 各种skills /  插件  / json配置 的安装和配置  尤其是skills.sh的用法 和skills 放置的位置  ，现在已经不用放在指定位置了
## 模型切换 /  模式切换 /  session切换 / 会话 share / 配色






# Opencode 演示 - 会话汇总

## 演示日期
2026年3月10日

## 涉及技术栈
- FastMCP (Python Model Context Protocol 框架)
- FastMCP Server/Client 构建
- Opencode 全局开发指导文件创建

## 用户指令汇总

### 第一部分：FastMCP Server/Client 演示

#### 指令1：使用 context7 搜索 fastmcp 库
用户要求使用 context7 搜索 fastmcp 序，了解如何编写简单的 MCP Server 和 Client。

#### 指令2：创建 MCP Server 和 Client 示例
用户要求创建简单的 MCP Server 和 Client 示例，并写入到：
`D:\git_codes\google_adk_helloworld_git\MISC\testpencil\`

#### 指令3：演示运行
用户要求演示 Server 和 Client 的实际运行过程。

#### 实现结果
✅ 成功创建：
- `mcp_server.py` - 包含 add、greet 工具和 config 资源
- `mcp_client.py` - 客户端调用示例
- 成功演示 Server 和 Client 通信，输出正确

---

### 第二部分：Opencode 全局开发指导文件

#### 指令4：创建 Opencode 全局开发指导文件
用户要求创建类似 gemini.md 的 Opencode 全局开发指导文件。

#### 指令5：指定全局位置
用户询问全局指导文件应该写在哪里。

#### 指令6：基于文档创建指导文件
用户提供了详细的规范要求，包括：
- 全部使用中文思考和回答
- Windows 命令执行规范
- Python 编码规范
- Git 提交规范
- PR 提交规范
- 其他禁止事项

#### 实现结果
✅ 成功创建：
- 全局指导文件位置：`~/.config/opencode/GUIDE.md`
- 在 `opencode.json` 中配置了 `"instructions"` 引用该文件
- 文件包含完整的开发规范

---

### 第三部分：规范执行证明

#### 指令7：要求证明规范执行
用户要求证明我确实按照指导进行操作。

#### 实现结果
✅ 提供了文件创建和修改的证明：
- 显示了创建的 GUIDE.md 文件内容
- 显示了 opencode.json 的 instructions 配置
- 展示了代码创建过程中遵循的规范

---

## 技术要点总结

### FastMCP 演示
```python
# Server 创建方式
from fastmcp import FastMCP
mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Client 创建方式
import asyncio
from fastmcp import Client

async def main():
    async with Client("path/to/server.py") as client:
        result = await client.call_tool("add", {"a": 5, "b": 3})
```

### Opencode 指令配置
```json
{
  "instructions": ["C:/Users/drago/.config/opencode/GUIDE.md"]
}
```

### Windows 命令执行规范
```
# 正确的 UTF-8 代码页切换
cmd /c chcp 65001 > NUL && python script.py

# Python 命令规范
cmd /c chcp 65001 > NUL && python -X utf8 script.py
```

## 演示价值
1. **MCP Server/Client 实践**：展示了 Python 中构建 Model Context Protocol 服务的完整流程
2. **全局配置管理**：演示了如何在 Opencode 中设置全局开发规范
3. **规范执行证明**：提供了完整的操作轨迹和结果验证
4. **跨技术栈整合**：结合了 MCP 技术和 Opencode 配置，展示了现代 AI 开发工作流

## 团队分享要点
- FastMCP 是构建 MCP 服务的现代化 Python 框架
- Opencode 支持全局指令配置，可统一团队开发规范
- Windows 环境下需要特别注意 UTF-8 和命令执行规范
- 通过规范配置可以确保团队开发的一致性和质量