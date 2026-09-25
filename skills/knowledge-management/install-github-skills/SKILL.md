---
name: install-github-skills
description: Install Claude Code skills from any GitHub repository. Auto-discovers skill structure, handles diverse repo layouts, rate limits, and logs to Obsidian. Use when user provides a GitHub URL ending with a repo name, asks to install/下载 skills/skills from GitHub, or says "帮我装这个 skill".
---

# Install GitHub Skills

Universal installer for Claude Code agent skills from GitHub repositories.

## When to Use

- User provides a GitHub repo URL: `https://github.com/owner/repo`
- User says: "帮我安装这个 skill", "装这个到用户目录", "install this skill"
- User mentions a GitHub repo by name: `owner/repo`

## Installation Pipeline

### Phase 1: Reconnaissance (2 API calls)

```
GET /repos/{owner}/{repo}         → default_branch, description
GET /repos/{owner}/{repo}/contents?ref={branch}  → root listing
```

Classify the repo type:
- **Skill repo**: has `skills/` dir, or `SKILL.md` at root, or skill dirs at root
- **Plugin repo**: has `.claude-plugin/plugin.json` — check `skills_root` field
- **Python CLI**: has `pyproject.toml` or `setup.py` — pip install, not skill copy

### Phase 2: Locate Skills

Search these paths in order (1 API call each):
1. `skills/` — most common
2. Root `""` — SKILL.md in top-level dirs
3. `dist/claude/skills/` — built repos (PaperSpine pattern)
4. `adapters/claude-code/skills/` — multi-platform repos
5. `plugins/` — marketplace repos (YuanyuanMa03 pattern)
6. `.claude-plugin/plugin.json` → read `skills_root` field

A directory is a skill if it contains `SKILL.md`.

### Phase 3: Download & Install (1 API call)

**Use zipball endpoint** — 1 API call downloads entire repo:

```
GET /repos/{owner}/{repo}/zipball/{branch}
```

Then:
1. Extract zip to temp dir
2. Navigate to discovered skills path
3. For each skill dir with `SKILL.md`:
   - Destination: `~/.claude/skills/{skill-name}/`
   - Skip if `SKILL.md` already exists at destination
   - Copy entire skill directory (preserves references/, scripts/, agents/)
4. Count files installed

### Phase 4: Verify & Log

- Report: skill name, file count
- Grand total of all skills in `~/.claude/skills/`
- Append install summary to Obsidian: `对话记录/YYYY-MM-DD.md`

## Critical Rules

### Branch Detection
- Always check `default_branch` from repo info API
- **Never assume** `main` or `master` — nature-skills uses `main`, others use `master`

### Rate Limiting
- GitHub API: 60 requests/hour unauthenticated
- Budget: ~5 repos per batch, 1.5s delay between repos
- Zipball endpoint saves massive API calls (1 vs N+1)

### Encoding
- Windows: wrap stdout with UTF-8 TextIOWrapper
- All file writes: `encoding="utf-8"`

### Path Handling
- Chinese/Unicode paths: quote properly
- Windows backslash vs forward slash: use `/` in API, `os.path.join()` locally
- Obsidian CLI path: quote `E:\新建文件夹 (2)\obsidian\obsidian` because of parentheses

### Skip Logic
- Check `SKILL.md` exists at destination before copying
- Report `= name (exists)` for skipped skills
- Report `+ name (N files)` for newly installed

## Repo Pattern Reference

| Pattern | Example | Skills Path |
|---------|---------|-------------|
| Standard `skills/` | kepano/obsidian-skills, Yuan1z0825/nature-skills | `skills/` |
| Root-level skill dirs | mikubaka88/CCFA-Skills, dox012/research-skill | `""` (root) |
| Built `dist/claude/skills/` | WUBING2023/PaperSpine | `dist/claude/skills/` |
| Adapter pattern | heyu-233/engineering-figure-agent | `adapters/claude-code/skills/` |
| Plugin marketplace | YuanyuanMa03/academic-research-skills | `plugins/` |
| Single root SKILL.md | Haojae/scipilot-figure-skill | entire repo |
| Python CLI tool | Panniantong/Agent-Reach | pip install, not skill copy |

## Post-Install

After successful install:
1. Append to Obsidian vault `对话记录/YYYY-MM-DD.md`:
   ```
   ## {repo-name}
   - {N} skills: {skill names}
   - {brief description}
   ```
2. Update todo list
3. If user has `system-review` skill, this installation will be picked up in next review

## Error Recovery

| Error | Action |
|-------|--------|
| 404 on path | Try next search path |
| 403 rate limit | Report wait time, ask user to retry |
| Encoding crash | Wrap stdout with UTF-8 TextIOWrapper |
| Empty skill dir | Skip, continue with next |
| ZIP extraction fails | Try individual file download fallback |
