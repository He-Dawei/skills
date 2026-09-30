---
name: me-user
description: 何大伟的个人信息与记忆系统的单一事实源说明。当任务需要"我是谁"、个人偏好、背景、长期约束，或需要新增/更新/查找记忆时使用。触发词：我的信息、我的偏好、你的记忆、记住这个、更新记忆、忘记这个、memory 怎么用。
---

# me-user — 用户上下文与记忆的单一事实源

## 核心规则：个人信息只存在一个地方

**所有关于本人的事实，只写在 memory 目录的 `.md` 文件里。**

Skill 里**不复制**个人信息。Skill 只做两件事：说明记忆系统怎么用；指向具体文件。理由——Skill 会被同步、被 Codex 读、被复制到多个位置；个人信息一旦复制就有多份会不同步的副本。记忆只有一个源。

同理，**密码、Token、Cookie、API Key、验证码、账号口令一律不写入任何 Skill、记忆文件、日志或对话正文**（详见 `me-guard` 的密钥卫生段）。

## 记忆系统结构

- **目录**：当前会话的项目 memory 目录（本会话 `C:\Users\44527\.claude\projects\e--claude-code----\memory\`）。
- **索引文件 `MEMORY.md`**：每行一条指针 `- [标题](文件名.md) — 一句话钩子`。**先读它，再决定打开哪个文件。**
- **记忆文件**：一份文件 = 一个事实/规则，带 frontmatter。

```markdown
---
name: <kebab-case-slug>
description: <一句话，用于召回时判断相关性>
metadata:
  type: user | feedback | project | reference
---

<事实正文。feedback / project 类型补 **Why:** 和 **How to apply:** 两行。>
用 [[另一个记忆的 name]] 互链。
```

类型含义：`user` 关于本人（角色、专长、偏好）；`feedback` 用户给的工作方式指导（含 why）；`project` 进行中的工作、目标、约束（相对时间要转成绝对日期）；`reference` 外部资源指针。

## 已有记忆的分组（按主题，不按时间）

个人信息与社交基线：`user-social-baseline.md`
工作方式与规则：`prd-first.md` `no-pushback.md` `tools-organization.md` `tools-skills-organization.md` `compress-token-skills.md`
技术路由：`use-scrapling.md` `use-browser-use.md` `use-chrome-devtools.md` `no-chrome-protocol-dialog.md` `use-douyin-tools.md` `use-xiaohongshu-tools.md`
进行中的项目：`ai-crossborder-project.md` `ai-crossborder-labor-split.md` `ai-stock-project.md` `anti-inflammatory-kitchen.md` `emotion-strategist-project.md` `fde-career-path.md`
管线与工具内部：`douyin-extract-pipeline.md` `douyin-creator-crawler.md` `douyin-keyword-search.md` `media-pipeline-bugs.md` `distill-skill.md` `codex-skills-sync.md`

## 读写流程

**读**：任务需要个人信息或既有决策 → 读 `MEMORY.md` → 只打开命中的文件 → 只取相关段落。

**写**：任务中出现新的、可复用的、**非显而易见**的事实 → 新建/更新一个记忆文件 → 在 `MEMORY.md` 加一行。更新优先于新建（先查有没有已覆盖同一件事的文件）。

**不写**：仓库里已有的（代码结构、已修复的 bug、git 历史）、只对本次对话有意义的、能从文件直接读出来的。

**矛盾处理**：发现某条记忆与现状冲突 → **以更新的那条为准**，并在回复里点出冲突，写进下次 lint。

## 已知问题

1. **两套 memory 目录并存（未处理，动它需用户确认）**：本项目用 `...projects\e--claude-code----\memory\`，而 `C:\Users\44527\.codex\AGENTS.md` 指向 `...projects\c--Users-44527--claude-skills\memory\`。Codex 侧可能读不到这份记忆。
2. **Chrome / msedge 分歧（2026-09-29 已解决）**：`no-chrome-protocol-dialog.md` 曾写"本机没装 Chrome，一律用 msedge"——**前提是错的**，实测 Chrome 装着且在跑（见该记忆的更正段）。弹窗真因是 `chrome:` scheme 无注册处理程序，与是否安装无关。浏览器选择见 `me-browser` 的对照表：CDP 自动化 → Chrome；要默认浏览器行为 → Edge。

## 相关

- `me-index` — 按主题查该读哪份记忆
- `me-guard` — 密钥卫生、不可逆操作闸门
