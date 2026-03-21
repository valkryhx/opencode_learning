# @符号引用文件 — 有时候会引用失败

有时候这是因为 `.gitignore` 中忽略了该路径。

---

# skill-creator 演示

比如：讲人话的内容优化。

---

# context7 MCP 演示

---

# 使用 playwright-cli skills

打开 `skills.sh`，让它获取前 10 个 skill，可以写 JS，或者直接看 playwright access-tree。

---

# awesome-opencode — 针对 opencode 的优化插件合集

- GitHub：[awesome-opencode/awesome-opencode](https://github.com/awesome-opencode/awesome-opencode)

---

# 使用 Ctrl+Shift+G 查看代码 Diff

## 推荐方法一：VS Code 内置源码管理面板（需 Git）

1. 按下 `Ctrl + Shift + G` 打开「源码管理」面板。
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

## 方法二：编辑器内置实时 Diff（无需 Git）

即使不使用 Git，VS Code 也能实时显示文件变更：

1. **行号左侧色块**：
   - 绿色：新增行
   - 蓝色：修改行
   - 红色：删除行
2. 点击行号左侧的色块，会弹出浮窗显示具体 Diff。
3. 未保存的文件在资源管理器中会显示为黄色（或其他高亮颜色）。

## 方法三：时间轴视图（Timeline）

1. 在左侧资源管理器（Explorer）最底部，找到「时间轴（Timeline）」面板。
2. 点击历史记录即可查看文件在各个时间点的变更。

## 不推荐：GitLens 插件（付费）

如果需要更强大的 Git 功能，可以安装 GitLens 插件，但需付费：

- **插件名称**：GitLens — Git supercharged
- **功能**：提供行级 Blame、强大的 Git 面板、实时文件变更监控等。

---

# cc-switch 演示

配合 cc 使用。

---

# opencode 内置 session_search 和 read

`session_search` 和 `read` 非常好用，能查询和复制历史会话内容。
