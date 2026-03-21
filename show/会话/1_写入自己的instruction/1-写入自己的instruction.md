```
如果你在windows powershell 环境下（目前就是），请使用powershell方式执行命令

如果你在windows cmd环境下：
1. If you want to run python during debugging ,you MUST run in this format: 
    ```cmd
    cmd /c set PYTHONIOENCODING=utf-8 && python your_script.py
    ```
2. If you want to run cmd command ,you MUST run in this format: 
    ```cmd
    cmd /c chcp 65001 & your_command
    ```
2. always think and answer in simplified Chinese.
3. Never write emojis in codes.
4. 测试文件和debug文件只能写在 MISC/debug_and_test 目录下.
5. 你书写 implementation plan 时必须使用中文.
6.  涉及到 path，需要使用项目的相对把路径，避免复杂的路径拼接.
```
以上是我需要加入到instruction中的内容，请你晚上powershell环境下的命令执行参数 尤其要支持中文输出（可以参考上面cmd的设置）你测试修改上述约束opencode的指令内容后，帮我写入全局指导文件位置：`~/.config/opencode/GUIDE.md`
- 在 `opencode.json` 中配置 `"instructions"` 引用该文件 然后验证。





======
注意 可以与opencode多轮探讨之后优化GUIDE.md的内容 （但是有时op也会忘记）