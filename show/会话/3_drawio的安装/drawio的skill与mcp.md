
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

配置命令与项目主页不是完全一致  配置之后重启op 在右侧能看到drawio的mcp服务 连接
配置之后能让op交互式作图  会在http://localhost:6002/启动