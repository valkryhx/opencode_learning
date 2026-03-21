# 全局指导文件

## Windows 环境注意事项

### Bash 环境（opencode bash 工具）
**重要**：opencode 的 bash 工具底层运行在 bash 下，必须使用 bash 语法：

1. **Python 执行**：必须设置环境变量
   ```bash
   export PYTHONIOENCODING=utf-8; python your_script.py
   ```
   或在一行内：
   ```bash
   PYTHONIOENCODING=utf-8 python your_script.py
   ```

2. **中文输出**：确保终端编码为 UTF-8
   ```bash
   export LANG=en_US.UTF-8
   ```

3. **文件路径**：使用正斜杠 `/`，Windows 路径自动转换
   ```bash
   cd /d/git_repos/project  # /d/ 代表 D: 盘
   ```

4. **Windows 路径转换规则**：
   - `D:\path\to\file` → `/d/path/to/file`
   - `C:\Users\name` → `/c/Users/name`

### PowerShell 环境
**重要**：以下规则在 PowerShell 环境下必须严格遵守：

#### 1. Python 执行
- 如果需要在调试时运行 Python，必须使用以下格式以确保中文输出正常：
  ```powershell
  $env:PYTHONIOENCODING="utf-8"; python your_script.py
  ```
- 如果需要传递参数给 Python 脚本：
  ```powershell
  $env:PYTHONIOENCODING="utf-8"; python your_script.py --arg1 value1
  ```
- 如果脚本需要读取中文文件，确保使用正确的编码读取：
  ```powershell
  python -c "import sys; sys.stdout.reconfigure(encoding='utf-8')"
  ```

#### 2. 命令执行
- PowerShell 命令直接执行，默认支持 UTF-8
- 如果命令输出中文出现乱码，检查终端编码设置：
  ```powershell
  [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
  ```
- 避免在命令中使用可能导致编码问题的特殊字符

#### 3. 文件路径
- Windows 路径分隔符使用反斜杠 `\` 或正斜杠 `/`（PowerShell 均支持）
- 包含空格的路径需要用引号包裹
- 建议使用 `$PWD` 获取当前目录

#### 4. 编码相关
- PowerShell 默认输出编码可能不是 UTF-8
- 重要输出建议显式指定编码：
  ```powershell
  "中文内容" | Out-File -FilePath "output.txt" -Encoding utf8
  ```



### CMD 环境
1. 如果需要在调试时运行 Python，必须使用以下格式：
   ```cmd
   cmd /c set PYTHONIOENCODING=utf-8 && python your_script.py
   ```
2. 如果需要运行 CMD 命令，必须使用以下格式：
   ```cmd
   cmd /c chcp 65001 & your_command
   ```

## 其他规则

3. 始终使用简体中文思考和回答。
4. 代码中不要写表情符号（emojis）。
5. 测试文件和 debug 文件只能写在 `MISC/debug_and_test` 目录下。
6. 书写 implementation plan 时必须使用中文。
7. 涉及到 path，需要使用项目的相对路径，避免复杂的路径拼接。
