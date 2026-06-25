---
name: agent-browser
description: Browser automation for AI agents. Use when user wants to automate browser tasks, scrape websites, fill forms, take screenshots, or control a browser programmatically.
---

# Agent Browser — Browser Automation CLI

## Tool Info

- **CLI**: `agent-browser` (installed globally, v0.28.0)
- **Package**: `agent-browser`
- **Capability**: Headless browser automation designed for AI agent use

## When to Use

User mentions: browser automation, scrape website, fill web form, take screenshot, headless browser, web automation, 浏览器自动化, 网页抓取.

## Quick Start

```bash
agent-browser
```

## Common Workflows

### Open a URL
```bash
agent-browser open <url>
```

### Take Screenshot
```bash
agent-browser screenshot <url> -o screenshot.png
```

### Extract Page Content
```bash
agent-browser scrape <url>
```

### Fill and Submit Form
```bash
agent-browser fill <url> --data '{"field": "value"}'
```

## Features

- Headless Chrome/Chromium based
- JavaScript execution support
- Screenshot and PDF export
- Form interaction and submission
- Cookie and session management

## Notes

- Designed for AI agent programmatic use — runs headless by default
- Can run in visible mode for debugging
- Supports proxy configuration
