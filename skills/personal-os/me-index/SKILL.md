---
name: me-index
description: 个人系统的总入口与路由索引。任何非平凡任务开始时先读它——先判断任务主题，再只加载相关的 memory 文件和 skill，不加载全部历史。触发词：你还记得吗、我的偏好、该读什么、索引、路由、memory、个人规则、上次怎么做的。
---

# me-index — 个人索引与最小加载路由

任何非平凡任务（要多步、要动文件、要决策）开始时，**先过一遍这里的路由表**，再动手。

## 三条硬原则

1. **只读相关的。** 不要遍历 memory 目录，不要读整个 Skill 列表。按主题查表，只打开命中的那 1-2 个 memory 文件和 1 个 skill。
2. **索引不等于内容。** memory 目录里的 `MEMORY.md` 是**索引**（每行一句话），先读它再做选择。真正的规则在各自的 `.md` 里。
3. **不背历史。** 过去的对话不在文件里。需要某次决策的来龙去脉时，只去 `E:\44527\Documents\claude仓库\对话记录\` 找那**一篇**摘要，或直接问用户。不要凭空假设项目历史。

## 加载预算

| 情况 | 预算 |
|---|---|
| 单领域任务 | ≤1 个 memory + ≤1 个 skill |
| 跨领域任务 | ≤3 个 memory + ≤2 个 skill |
| 简单问答 | 0 —— 直接答，不查表 |

超预算说明主题判断错了，回去重判，不要靠多读来补。

## 定位

- **memory 目录**：当前会话的项目 memory 目录（本会话为 `C:\Users\44527\.claude\projects\e--claude-code----\memory\`）。**里面的文件才是事实源**，skill 里不复制内容。
- **live skills**：`C:\Users\44527\.claude\skills\`
- **canonical skills**：`C:\Users\44527\.claude\skills-repo\skills\`（Codex 也读这里，改完要两边同步）
- **Obsidian vault**：`E:\44527\Documents\claude仓库\`

## 主题路由表

| 任务主题 | 先读 memory | 再考虑 skill |
|---|---|---|
| 我是谁 / 个人信息 / 偏好 | `user-social-baseline.md` | `me-user` |
| 输出文件放哪 / 桌面清洁 | — | `me-output` |
| 浏览器、抓网页、桌面 GUI | `use-scrapling.md` `use-browser-use.md` `use-chrome-devtools.md` `no-chrome-protocol-dialog.md` | `me-browser` |
| 删除 / 发布 / 付款 / 账号 / 密钥 / 对外发送 | — | `me-guard` |
| 调试 bug / 报错 / 测试失败 | — | `me-guard` → `debugging-methodology` |
| AI 跨境电商 | `ai-crossborder-project.md` `ai-crossborder-labor-split.md` | — |
| 抖音 / 短视频 | `douyin-extract-pipeline.md` `douyin-creator-crawler.md` `douyin-keyword-search.md` `use-douyin-tools.md` | `douyin-creator-crawl` `douyin-obsidian` |
| 小红书 | `use-xiaohongshu-tools.md` | `xhs-*` |
| 炒股 / 投资 | `ai-stock-project.md` | — |
| 健康 / 饮食 | `anti-inflammatory-kitchen.md` | — |
| 社交 / 情感 | `user-social-baseline.md` `emotion-strategist-project.md` | — |
| 求职 / 实习 / 简历 | `fde-career-path.md` | `internship-hunter` `resume-*` |
| 工具安装 / 分类存放 | `tools-organization.md` `tools-skills-organization.md` | — |
| skill 管理 / 同步 Codex | `codex-skills-sync.md` `distill-skill.md` | — |
| token / 上下文压缩 | `compress-token-skills.md` | `ponytail` `caveman-compress` `codegraph` |
| 媒体管线 / 静默失败类 bug | `media-pipeline-bugs.md` | — |
| 新任务要不要先写方案 | `prd-first.md` | — |
| 要不要反驳用户 | `no-pushback.md` | — |

## 执行顺序

1. 用一句话说清任务主题。
2. 查表 → 打开命中的 memory 文件（只读相关段落，不必通读长文件）。
3. 判断有没有 skill 命中 → 有就**完整读它的 `SKILL.md`** 再执行，不靠名字猜用法。
4. 主题命中 `me-guard` 的条件（删除/发布/付款/账号/密钥/对外发送）→ **先读 `me-guard`，过三问，再动手。**
5. 做完有新的、可复用的、非显而易见的知识 → 写入 memory 并在 `MEMORY.md` 加一行索引。

## 相关

- `me-user` — 个人信息与记忆系统的单一事实源
- `me-output` — 生成文件放哪、桌面清洁
- `me-browser` — 浏览器 / Windows 控制的路由决策树
- `me-guard` — 不可逆操作前的安全闸门
