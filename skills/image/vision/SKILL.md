---
name: vision
description: "Use this skill whenever the user shares an image (local path, URL, or attachment) and needs it analyzed, described, or recognized. Also trigger when user asks to 'look at this image', 'what's in this picture', 'describe this screenshot', or any image-related question. This skill bridges models without native vision by calling a vision-capable model API."
---

# Vision Skill — Image Recognition

## Overview

Current model has no native vision. When images appear, do NOT use `Read` tool on images. Use `vision.js` instead — it sends image to Qwen VL model, returns text description.

## Trigger

- User shares image path (local or URL)
- Message contains "Saved attachments:" listing image files
- User asks to analyze, describe, or recognize image content
- Any screenshot, photo, or diagram shared

## Usage

```bash
node ~/.claude/skills/vision/vision.js "<image-path>" "Describe this image in detail"
node ~/.claude/skills/vision/vision.js --url "<image-url>" "What's in this picture?"
```

## Rules

1. For EVERY image, run `vision.js` — do NOT skip any image
2. Process images one by one, collect all text descriptions before replying
3. Default prompt: "请详细描述这张图片的内容。" (Chinese) or "Describe this image in detail." (English)
4. If vision.js fails, report the error to user, do NOT attempt Read on image
