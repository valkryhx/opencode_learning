作用 方便的给code agent 导入skills
地址: https://skills.sh/


例如 Rank#1 find-skills  
演示安装命令 npx skills add https://github.com/vercel-labs/skills --skill find-skills

安装过程中会让你选择是全局还是项目级别安装 并且也让其他ide能感知
全局安装在 C:\Users\Administrator\.agents\skills 路径下的find-skills目录 
需要重启op才能感知

使用：1.直接让op使用find-skills 找 pdf skill
      2. /skills/find-skills pdf skill

【自动化】npx skills add anthropics/skills@pdf -g -y    
-g 全局安装 -y 自动确认

特殊-[draw.io 画图]
npx skills add bahayonghang/drawio-skills@drawio -g -y

此时虽然能用 但是只能cli中看无法调整 因此还需要在opencode.json 中配置 mcp
参考但不能完全参考 https://github.com/bahayonghang/drawio-skills 主页
  [终端下注意换行的问题 最好写入文件 让op读取]

 "mcp": {
    "drawio": {
      "type": "local",
      "command": [
        "cmd",
        "/c",
        "npx",
        "--yes",
        "@next-ai-drawio/mcp-server@latest"
      ]
    }
  }

配置之后能交互式作图 会在http://localhost:6002/启动



C:\Users\Administrator>npx skills add https://github.com/vercel-labs/skills --skill find-skills
Need to install the following packages:
skills@1.4.5
Ok to proceed? (y) y


███████╗██╗  ██╗██╗██╗     ██╗     ███████╗
██╔════╝██║ ██╔╝██║██║     ██║     ██╔════╝
███████╗█████╔╝ ██║██║     ██║     ███████╗
╚════██║██╔═██╗ ██║██║     ██║     ╚════██║
███████║██║  ██╗██║███████╗███████╗███████║
╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝

T   skills
|
o  Source: https://github.com/vercel-labs/skills.git
|
o  Repository cloned
|
o  Found 1 skill
|
•  Selected 1 skill: find-skills
|
o  42 agents
◆  Which agents do you want to install to?
│
│  ── Universal (.agents/skills) ── always included ────────────
│    • Amp
│    • Cline
│    • Codex
◇  Which agents do you want to install to?
│  Amp, Cline, Codex, Cursor, Gemini CLI, GitHub Copilot, Kimi Code CLI, OpenCode, Warp
|
o  Installation scope
|  Global

|
o  Installation Summary -----------------------------------+
|                                                          |
|  ~\.agents\skills\find-skills                            |
|    copy → Amp, Cline, Codex, Cursor, Gemini CLI +4 more  |
|                                                          |
+----------------------------------------------------------+
|
o  Security Risk Assessments ---------------------------------+
|                                                             |
|               Gen               Socket            Snyk      |
|  find-skills  Safe              0 alerts          Med Risk  |
|                                                             |
|  Details: https://skills.sh/vercel-labs/skills              |
|                                                             |
+-------------------------------------------------------------+
|
*  Proceed with installation?
|  > Yes /   No
—
