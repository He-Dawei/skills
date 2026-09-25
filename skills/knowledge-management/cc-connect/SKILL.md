---
name: cc-connect
description: Bridge AI agents to messaging platforms. Use when user wants to connect Claude Code to Feishu/DingTalk/Slack/Telegram/Discord/LINE/WeChat Work.
---

# CC Connect — AI Agent Messaging Bridge

## Tool Info

- **CLI**: `cc-connect` (installed globally, v1.3.3-beta.4)
- **Package**: `cc-connect`
- **Platforms**: Feishu, DingTalk, Slack, Telegram, Discord, LINE, WeChat Work

## When to Use

User mentions: connect Claude to messaging, bridge to Feishu/DingTalk/Slack/Telegram/Discord, AI agent in chat, 飞书机器人, 钉钉机器人, 企业微信机器人.

## Quick Start

```bash
cc-connect
```

## Setup

```bash
cc-connect init
```

Then configure the messaging platform credentials.

## Supported Platforms

- Feishu (飞书)
- DingTalk (钉钉)
- Slack
- Telegram
- Discord
- LINE
- WeChat Work (企业微信)

## How It Works

1. cc-connect runs as a bridge between local Claude Code and messaging platform
2. Messages from the platform are forwarded to Claude Code
3. Claude's responses are sent back to the platform
4. Supports multiple platforms simultaneously

## Notes

- Requires bot/API credentials from target messaging platform
- Each platform has its own configuration in the cc-connect config file
