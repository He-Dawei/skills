---
name: system-review
description: Periodic self-review and knowledge consolidation. Reviews conversation patterns, extracts user preferences and domain knowledge, updates memory files and user profile. Use when triggered by cron, when user says "复盘", "review", "总结经验", "自我进化", or at the start of sessions for context refresh.
---

# System Review — Self-Evolution Engine

## Purpose

Periodically review all accumulated data (memory files, Obsidian notes, conversation patterns) to:
1. Extract new facts about the user (role, preferences, domain, tools)
2. Consolidate scattered observations into structured knowledge
3. Prune outdated or contradicted memories
4. Update CLAUDE.md with refined instructions
5. Save an audit trail to Obsidian

## Data Sources (read in order)

1. `~/.claude/projects/*/memory/MEMORY.md` — index of all memories
2. `~/.claude/projects/*/memory/*.md` — individual memory files
3. `~/.claude/CLAUDE.md` — current user instructions
4. `~/.claude/settings.json` — current hooks/config
5. Obsidian vault `对话记录/` — recent conversation logs
6. `~/.claude/skills/` — installed skills (count + categories)

## Review Process

### Phase 1: Scan
Read all memory files and recent Obsidian notes. Build a map of what's known.

### Phase 2: Categorize
Group findings into:
- **User Identity**: role, industry, company, title, expertise
- **Preferences**: tools, workflows, communication style, language
- **Recurring Tasks**: patterns of requests, frequent operations
- **Domain Knowledge**: business context, technical stack, projects
- **Config State**: installed skills, hooks, settings
- **Gaps**: things the user asked about but aren't captured

### Phase 3: Consolidate
- Merge related memories into single files
- Remove duplicates
- Mark outdated facts
- Create new memories for gaps

### Phase 4: Update
- Write/update memory files with `[[cross-references]]`
- Update CLAUDE.md if new patterns emerge
- Save review summary to Obsidian `系统复盘/YYYY-MM-DD.md`

### Phase 5: Report
Output a structured review report with:
- New facts discovered
- Memories consolidated
- Gaps identified
- Recommendations for automation

## Output Locations

| Content | Destination |
|---------|-------------|
| New user facts | `~/.claude/projects/*/memory/{slug}.md` |
| Updated memories | Edit existing memory files |
| Workflow improvements | `~/.claude/CLAUDE.md` (append if needed) |
| Review summary | Obsidian `系统复盘/YYYY-MM-DD.md` |
| Action items | Obsidian `系统复盘/待办.md` |

## Frequency

- **Quick review**: every session start (lightweight: scan MEMORY.md index, note changes)
- **Deep review**: triggered by cron daily or user says "复盘"

## Guidelines

- Be conservative: don't overwrite user data without clear evidence
- Cross-reference: always link related memories with `[[name]]`
- Prune ruthlessly: if two memories say the same thing, merge them
- Track provenance: note where each fact came from (which conversation/date)
- Never remove user's explicit instructions from CLAUDE.md
