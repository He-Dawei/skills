---
name: user-workflow-rules
description: "Apply this user's durable workflow preferences: Chinese concise communication, E-drive outputs, Desktop cleanliness, Obsidian task summaries, and conservative file handling."
---

# User Workflow Rules

- Reply in simplified Chinese. Keep wording concise and technically precise.
- Put generated or downloaded artifacts in `E:\claude code生成文件` unless the user explicitly chooses another location.
- Keep `C:\Users\44527\Desktop` limited to `.docx` resume files. Build scripts, `node_modules`, package files, and temporary artifacts belong in a temp folder or `C:\Users\44527\`.
- For substantive tasks, save a brief summary to `E:\44527\Documents\claude仓库\对话记录\YYYY-MM-DD HHmm.md`.
- Before changing or deleting files, enumerate the exact scope. Do not infer that an old, large, generated, or duplicate file is disposable.
- Preserve user projects, source code, dependencies, backups, credentials, and data unless the user identifies the exact disposable scope.
- Personal identity and private facts remain in the memory directory; do not duplicate them into every Skill.
- If a current task instruction conflicts with an old memory note, follow the current task and record the change only when it is durable.
