---
name: video-transcript-jump
description: 生成可点击时间轴跳转的视频字幕播放器。将视频+字幕文件转为交互式 HTML 页面，点击任意字幕行即可跳转到视频对应位置。支持 SRT/VTT/纯文本时间戳。当前播放的字幕行高亮，支持搜索和键盘快捷键。
---

# Video Transcript Jump — 可跳转视频字幕播放器

## 触发条件

- "给这个视频生成可跳转字幕"
- "做一个能点击时间轴的视频播放器"
- "video transcript with clickable timestamps"
- 用户提供视频文件+字幕文件 (SRT/VTT/TXT)
- 用户说"字幕跳转"、"时间轴播放器"

## 工作流

### 1. 确认输入

需要两个文件：
- **视频文件**: 本地路径或 URL（本地路径生成后可直接在浏览器打开）
- **字幕文件**: SRT, WebVTT, 或纯文本 `HH:MM:SS 文本内容` / `MM:SS 文本内容`

如果用户**只有视频没有字幕**，先用 whisper 生成字幕：

```bash
# 用 whisper.cpp 或 openai whisper API 转录
whisper video.mp4 --model medium --output_format srt
```

### 2. 生成播放器

```bash
node ~/.claude/skills/video-transcript-jump/scripts/generate-player.js <视频路径> <字幕路径> [输出路径] [--title "自定义标题"]
```

### 3. 交付

输出一个自包含 HTML 文件，用户用浏览器打开即可。

## 播放器功能

| 功能 | 操作 |
|------|------|
| 点击跳转 | 点任意字幕行 → 视频跳转到对应时间 |
| 高亮跟随 | 当前播放的字幕行自动高亮 + 滚动到可见区域 |
| 搜索字幕 | 顶部搜索框，实时过滤匹配字幕 |
| 键盘控制 | `←→` 跳转上下条, `Space` 暂停, `F` 搜索, `Esc` 清除搜索 |
| 拖放替换 | 拖入新视频/字幕文件实时切换 |
| 响应式 | 桌面左右分栏, 手机上下分栏 |

## 支持的字幕格式

### SRT
```
1
00:00:02,500 --> 00:00:05,000
第一行字幕内容

2
00:00:05,500 --> 00:00:09,000
第二行字幕内容
```

### WebVTT
```
WEBVTT

00:00:02.500 --> 00:00:05.000
第一行字幕内容

00:00:05.500 --> 00:00:09.000
第二行字幕内容
```

### 纯文本时间戳
```
00:00 第一行字幕
00:05 第二行字幕
1:30 也可以这样写
01:02:03 或者带小时的
```

## 示例

```bash
# 基础用法
node ~/.claude/skills/video-transcript-jump/scripts/generate-player.js \
  ~/Videos/lecture.mp4 ~/Videos/lecture.srt \
  --title "机器学习 Lecture 1"

# 输出到桌面
node ~/.claude/skills/video-transcript-jump/scripts/generate-player.js \
  ~/Videos/talk.mp4 ~/Videos/talk.vtt \
  ~/Desktop/talk-player.html
```

## 注意事项

- 视频路径嵌入 HTML 的 `<video src="...">`，**相对路径或绝对路径均可**
- 如果视频是网络 URL，直接把 URL 作为视频路径参数传入
- 生成的 HTML 不依赖任何 CDN，完全离线可用
- 字幕必须包含有效的时间戳格式
