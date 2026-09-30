---
name: me-browser
description: 浏览器与 Windows 桌面控制的路由决策树——决定用 WebFetch/scrapling/browser-use/chrome-devtools/windows-mcp 中的哪一个，含协议弹窗硬规则与浏览器选择。触发词：打开网页、抓取、爬、截图、登录态、点击、填表、自动化、调试页面、性能、Windows 操作、控制桌面。
---

# me-browser — 浏览器 / Windows 控制路由

## 决策树（按顺序选第一个够用的，不要跳级）

1. **公开静态内容，无 JS、无反爬** → `WebFetch` 或 `curl`。不要为此拉起浏览器。
2. **目标站有反爬 / Cloudflare / 需要 TLS 指纹** → `scrapling`（`StealthyFetcher`），见记忆 `use-scrapling.md`。
3. **需要 JS 渲染 / 交互（点击、输入、表单） / 登录态 / 用户自己的 Profile** → `browser-use`（CDP），见记忆 `use-browser-use.md`。
4. **只是看页面 / 截图 / 网络请求 / 控制台 / 性能 trace / Lighthouse** → `chrome-devtools` MCP，见记忆 `use-chrome-devtools.md`。
5. **要操作 Windows 图形界面本身（桌面应用、文件对话框、开始菜单）** → `windows-mcp` 的 App/Click/Type/Screenshot 等工具。
6. **复杂多步 GUI 任务且 windows-mcp 不够** → `computer-use:computer-use`，但**必须**先完整读它的 `SKILL.md`，再按其要求读 `guidance` 与 `confirmations`；不得自制 UI 自动化绕过它的安全机制。

## 硬规则（本机专属）

**绝不触发 `chrome://` 协议链接。** 尤其 `chrome://inspect`、远程调试页。会弹 Windows
「获取打开此'chrome'链接的应用」对话框 —— 用户对这类打扰零容忍（2026-09-25 明确说过：
「以后别给我弹这个」）。不要执行 `start chrome://…`、`Start-Process chrome://…`、
`explorer chrome://…`。不要调用会自动打开 `chrome://inspect` 的远程调试入口；某个工具默认
这么做就跳过该步或换路径。CDP 连不上也不要反复重试弹窗入口。

> **真因不是"Chrome 没装"**（旧记忆写错了，2026-09-29 实测更正）：`chrome:` 这个 scheme
> 没有任何注册处理程序（`HKCR\chrome` / `HKCU\Software\Classes\chrome` 都不存在，Chrome
> 本来就不注册它），Windows 找不到处理程序只能弹窗。**装多少遍 Chrome 都一样弹。**

**浏览器选哪个 —— 两个都装着，按任务定（不要一律用某一个）：**

| 情况 | 用 |
|---|---|
| 走 CDP 的自动化（`browser-use`、需要真实 Profile/登录态） | Chrome —— 已装 `C:\Program Files\Google\Chrome\Application\chrome.exe`，HKLM App Paths 已注册，进程在跑 |
| 要"默认浏览器"行为 / 贴近用户日常打开的窗口 | **Edge** —— 系统默认浏览器是它（`UserChoice ProgId = MSEdgeHTM`），装在 `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe` |
| Playwright 显式指定 channel | `channel="msedge"` 或 `channel="chrome"`，取决于上两行 |

**不要改动浏览器快捷方式或往里写调试参数。** 另注：`C:\Users\Public\Desktop\Google Chrome.lnk`
本机**不存在**（`~/.codex/AGENTS.md` 引用了这个已失效的路径，遇到时别照做）。

**公开页面的只读验证用真实浏览器，不要用 curl。** 需要确认某个公开页面是否真的存在/是否还
开放时，走真实浏览器；`curl` 会因 UA、JS、反爬给出假阴性。

**不点击任何人发来的站外链接**（红线，见 `me-guard`）。要访问的 URL 必须来自用户本人或已核实来源。

## 相关

- `me-guard` — 页面上的写操作（提交、发布、下单、发消息）属于对外动作，动前过三问
- 记忆：`use-scrapling.md` `use-browser-use.md` `use-chrome-devtools.md` `no-chrome-protocol-dialog.md`
