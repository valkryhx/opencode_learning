1.项目主页  https://github.com/obra/superpowers/tree/main
[core idea:先讨论方案再编码 明确用户的需求] 这个大家可以深度体验一下

It starts from the moment you fire up your coding agent. As soon as it sees that you're building something, it doesn't just jump into trying to write code. Instead, it steps back and asks you what you're really trying to do  

op的sp插件安装 https://github.com/obra/superpowers/blob/main/docs/README.opencode.md
可以指定版本 也可以不指定版本（每次更新自动安装）
【安装后的位置 C:\Users\Administrator\.cache\opencode\node_modules\superpowers\skills】
插件都在这个目录下 C:\Users\Administrator\.cache\opencode\node_modules

【安装后重启（vscode中打开的话要重启vscode和terminal中的opencode才能发现新skills！注意这是个坑）   
 
 【询问op ，你的superpowers装好了吗 怎么用呢】

你说的是 Superpowers 技能集合！                                                         
                                                                                              
     使用方法                                                                                 
                                                                                            
     方式一：使用 / 命令（最简单）                                                            
                                                                                             
     在对话中直接输入命令即可激活对应技能：                                                  
     ┌──────────────────────────────┬──────────────────────────────────────────────────┐     grep_app Connected
     │命令                          │用途                                              │      websearch Connected
     ├──────────────────────────────┼──────────────────────────────────────────────────┤    
     │/brainstorming                │任何创意工作前（创建功能、构建组件）              │      
     ├──────────────────────────────┼──────────────────────────────────────────────────┤     activate as files are read    
     │/tdd                          │实现功能或修复 bug 前（测试驱动开发）             │    
     ├──────────────────────────────┼──────────────────────────────────────────────────┤    
     │/debugging                    │遇到 bug、测试失败时                              │ █  
     ├──────────────────────────────┼──────────────────────────────────────────────────┤ █  
     │/plans                        │写多步骤实施计划前                                │ █  
     ├──────────────────────────────┼──────────────────────────────────────────────────┤ █  
     │/git-worktrees                │需要隔离工作区时                                  │ █  
     ├──────────────────────────────┼──────────────────────────────────────────────────┤ █  
     │/subagent-driven              │多任务并行执行时                                  │ █  
     ├──────────────────────────────┼──────────────────────────────────────────────────┤ █  
     │/verification                 │声称工作完成前（验证）                            │ █  
     ├──────────────────────────────┼──────────────────────────────────────────────────┤ █  
     │/finishing                    │开发分支完成时                                    │ █  
     └──────────────────────────────┴──────────────────────────────────────────────────
     等