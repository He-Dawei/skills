---
name: glm-vision
description: "PRIMARY image recognition — use FIRST whenever user shares any image (local path, URL, attachment, screenshot, photo, diagram). Calls GLM vision models via MCP tool with automatic fallback (GLM-4.6V → GLM-4.1V-Thinking-FlashX → GLM-4.6V-Flash). Only fall back to 'vision' skill if this MCP tool is unavailable or fails. Triggers on: any image file, 'look at this', 'what's in this picture', 'describe this screenshot', 'analyze this image', '识别图片', '看看这张图'."
---

# GLM Vision Skill — 图片识别（第一顺位）

## Priority

**THIS SKILL IS FIRST PRIORITY for all image recognition.** Use it before the `vision` skill. The `vision` skill is the fallback — ONLY use it when `glm-vision` MCP tool is unavailable or returns an error.

## Trigger

Activate ANY time an image is present:

- User shares image path (local or URL)
- Message contains "Saved attachments:" listing image files
- Any screenshot, photo, or diagram attached
- User asks "look at this", "what's in this picture", "describe this image", "识别图片", "看看这张图"

## Usage

### Step 1: Try GLM Vision MCP Tool FIRST

Call the MCP tool `vision_chat` with:
- `image`: The image URL, data URI, or base64 string
- `prompt`: What to analyze. Default: "请详细描述这张图片的内容。"

### Step 2: Fallback to vision skill ONLY if needed

If MCP tool errors, fall back to:

```bash
node ~/.claude/skills/vision/vision.js "<image-path>" "Describe this image in detail"
```

## Image Processing Rules

1. Process EVERY image the user shares
2. For multiple images, process one by one
3. Default prompt (Chinese): "请详细描述这张图片的内容。"
4. Default prompt (English): "Describe this image in detail."
5. Report which model was used (e.g., "_via GLM-4.6V_")
6. If ALL methods fail, tell the user clearly what errors occurred

## Fallback Chain

```
glm-vision (MCP, this skill) → vision (old skill, script) → report error to user
```
