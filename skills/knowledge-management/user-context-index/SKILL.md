---
name: user-context-index
description: Route user-specific memory and workflow rules to the smallest relevant Skill. Use at the start of tasks that may depend on this user's profile, output paths, Obsidian logging, browser/computer routing, Douyin workflow, internship verification, or persistent preferences.
---

# User Context Index

This is a lightweight router, not a second memory store.

## Source of truth

- Personal facts stay in `C:\Users\44527\.claude\projects\c--Users-44527--claude-skills\memory\user-profile.md`.
- Other durable facts stay in the same memory directory, one topic per file.
- Current task instructions and the current `AGENTS.md` have priority over memory.
- Do not copy secrets, API keys, cookies, passwords, or full personal records into Skills.

## Routing

Read only the matched Skill and memory file. Do not load the entire memory directory for an unrelated task.

| Task signal | Route |
|---|---|
| User identity, language, career goals | `memory/user-profile.md` |
| Output location, Desktop cleanliness, task logging | `automation/user-workflow-rules` |
| Browser, website, Windows app, CDP, screenshots | `automation/windows-browser-routing` plus the relevant browser/computer Skill |
| Coding plan, debugging, deletion, external side effects | `thinking/user-execution-guardrails` |
| Douyin creator crawl | `social-media/douyin-creator-crawl` |
| Douyin favorites to Obsidian | `social-media/douyin-obsidian-sync` |
| Douyin analysis | `dy-note` |
| Internship search or listing verification | `career/internship-hunter` plus the internship memory rule |
| Spreadsheet work | `automation/spreadsheets` plus `memory/xlsxwriter-not-openpyxl.md` |
| Obsidian notes or vault organization | the relevant Obsidian Skill plus the current vault path in `AGENTS.md` |

## Per-task behavior

1. Perform a lightweight applicability check at the start of every task.
2. Load the smallest matching route; do not treat this index as permission to perform extra work.
3. Preserve existing user data and ask before irreversible deletion, publishing, payments, credential changes, or broad cleanup.
4. At the end of a substantive task, save a concise summary to the configured Obsidian `对话记录` directory.
