---
name: yt-dlp
description: Video/audio downloader. Use when user wants to download videos, extract audio, get subtitles, or list formats from YouTube and 1000+ sites.
---

# yt-dlp — Video & Audio Downloader

## Tool Info

- **CLI**: `yt-dlp` (installed via winget, v2026.06.09)
- **Location**: `C:\Users\44527\AppData\Local\Microsoft\WinGet\Links\yt-dlp.exe`
- **FFmpeg**: Available for format conversion

## When to Use

User mentions: download video, download audio, 下载视频, 下载音频, extract audio/mp3, get subtitles, YouTube/B站 download, 下载字幕.

## Quick Commands

### Download Video (best quality)
```bash
yt-dlp -o "E:\claude code生成文件\%(title)s.%(ext)s" <URL>
```

### Download Audio Only (mp3)
```bash
yt-dlp -x --audio-format mp3 -o "E:\claude code生成文件\%(title)s.%(ext)s" <URL>
```

### Download with Subtitles
```bash
yt-dlp --write-subs --sub-langs all -o "E:\claude code生成文件\%(title)s.%(ext)s" <URL>
```

### List Available Formats
```bash
yt-dlp -F <URL>
```

### Download Specific Format
```bash
yt-dlp -f <format-code>+bestaudio -o "E:\claude code生成文件\%(title)s.%(ext)s" <URL>
```

### Playlist Download
```bash
yt-dlp -o "E:\claude code生成文件\%(playlist)s\%(playlist_index)s - %(title)s.%(ext)s" <URL>
```

## Output Directory Rule

All downloads go to `E:\claude code生成文件\` unless user specifies otherwise.
