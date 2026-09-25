---
name: douyin-obsidian-sync
description: Sync Douyin (抖音) favorites to Obsidian vault — download, transcribe, analyze, and generate structured notes. Use when user mentions 抖音收藏, Douyin favorites, syncing videos to notes, or wants to process Douyin bookmarks.
---

# Douyin → Obsidian Sync Pipeline

Sync Douyin (抖音) favorite videos to Obsidian vault as structured Markdown notes.

## Pipeline Location

```
C:\Users\44527\Documents\codex\2026-07-24\codex-reconnecting-codex-env-3\outputs\douyin-obsidian-pipeline\
```

## Pipeline Steps

1. Read Douyin video URLs from `data/favorites.txt` (one URL per line, tab-separated title optional)
2. Download video via yt-dlp (with browser cookies for auth)
3. Extract audio via FFmpeg (16kHz mono WAV)
4. Transcribe via VibeVoice (or skip with `provider = "none"`)
5. Analyze transcript → summary, key points, auto-tags
6. Write structured Markdown to `E:\44527\Documents\claude仓库\Douyin Favorites\`

## Quick Reference

| Action | Command |
|--------|---------|
| Run once | `.\run.ps1 -ConfigPath .\config.toml` |
| Dry run | `python src/pipeline.py --config config.toml --dry-run` |
| Install daily task (02:00) | `.\install_task.ps1 -ConfigPath .\config.toml -Time 02:00` |
| Diagnose | `.\diagnose.ps1 -ConfigPath .\config.toml` |
| Add new favorite | Append URL to `data/favorites.txt` (tab-separated: `URL\tTitle\tDate`) |

## Configuration (`config.toml`)

Key settings:
- `obsidian.vault_path` — Obsidian vault path
- `obsidian.notes_subdir` — subdirectory for notes (default: "Douyin Favorites")
- `source.type` — data source: `links_file`, `json_file`, `download_dir`, `collector_command`
- `transcription.provider` — `vibevoice_cli`, `vibeasr_cpp`, or `none`
- `download.enabled` — whether to download videos

## Output Format

Each note has YAML frontmatter with tags, source URL, creation date, then sections:
- 核心内容 (summary)
- 关键观点 (key points)
- 自动标签 (auto tags)
- 原始转写 (transcript)
- 处理信息 (metadata)

## State & Dedup

Processed URLs tracked in `state/processed.json`. Same URL won't process twice.
Status `pending_transcription` items auto-retry when transcription provider is configured.

## How to Add Favorites

User gives you a Douyin URL → append to `data/favorites.txt`:
```
https://www.douyin.com/video/123456	视频标题	2026-07-26
```

Then run: `.\run.ps1 -ConfigPath .\config.toml`

## Troubleshooting

- Download fails → check cookies: set `cookies_from_browser = "edge"` or provide `cookies_file`
- FFmpeg not found → set `tools.ffmpeg_path` to full path
- Transcription skipped → set `transcription.provider = "vibevoice_cli"` or configure wrapper
- Browser collector not working → run `init_douyin_browser_profile.ps1` to set up auth profile
