---
name: freellmapi
description: Use when setting up or using the FreeLLMAPI proxy — aggregates 28 free LLM provider tiers (~4B tokens/month) behind one OpenAI-compatible /v1 endpoint. Also use when configuring Claude Code to use free models via the Anthropic Messages API shim, when setting up fallback chains across free providers, or when troubleshooting provider rate limits and failover. Triggers: "use free models", "aggregate free LLM APIs", "set up LLM proxy", "Claude Code with free models", "Anthropic API alternative", "free inference".
---

# FreeLLMAPI

OpenAI-compatible proxy aggregating 28 free LLM providers (~4B tokens/month) behind one `/v1` endpoint. Includes Anthropic Messages API shim — Claude Code can run against your free pool.

Runs on Windows/macOS/Linux, ~40 MB RAM idle.

## Quick Reference

| Task | Command / Config |
|------|-----------------|
| One-liner install (Docker) | `curl -fsSL https://freellmapi.co/install.sh \| bash` |
| Windows install | Download `.exe` from [Releases](https://github.com/tashfeenahmed/freellmapi/releases/latest) |
| Manual Docker | `git clone` → `docker compose up -d` |
| Dashboard | `http://localhost:3001` |
| OpenAI endpoint | `http://localhost:3001/v1` |
| Anthropic endpoint | `http://localhost:3001/v1/messages` |

## Supported Providers

Google (Gemini), Groq (Llama 4, Qwen3), Cerebras (Qwen3 235B), Mistral, OpenRouter (21 free models), GitHub Models (GPT-4.1, GPT-4o), Cloudflare (Kimi K2, GLM-4.7), Cohere, NVIDIA, HuggingFace, Z.ai (GLM-4.5/4.7), Ollama Cloud, Kilo, Pollinations, LLM7, OVH, AI Horde, NaraRouter, Aion Labs, Requesty, NavyAI, Agnes AI, Reka, SiliconFlow, Routeway, BazaarLink, AINative Studio, SEA-LION — plus any custom OpenAI-compatible endpoint.

Full live list: [freellmapi.co/models](https://freellmapi.co/models.html)

## Setup

### Option A: Docker (recommended)

```bash
git clone https://github.com/tashfeenahmed/freellmapi.git
cd freellmapi
ENCRYPTION_KEY="$(openssl rand -hex 32)"
printf "ENCRYPTION_KEY=%s\nPORT=3001\n" "$ENCRYPTION_KEY" > .env
docker compose up -d
```

Open `http://localhost:3001`, create account (email + password), add provider keys on **Keys** page, grab unified API key from Keys header.

### Option B: Windows desktop

Download `.exe` from [GitHub Releases](https://github.com/tashfeenahmed/freellmapi/releases/latest). System-tray app — one click to start/stop.

### Option C: npm

```bash
npm install -g freellmapi
freellmapi
```

## Using with Claude Code

FreeLLMAPI speaks Anthropic Messages API at `/v1/messages`. Point Claude Code at it:

```bash
# Set in Claude Code session or settings
export ANTHROPIC_BASE_URL="http://localhost:3001/v1"
export ANTHROPIC_API_KEY="freellmapi-YOUR_UNIFIED_KEY"
```

Claude model families auto-map: `opus` / `sonnet` / `haiku` / `default` → `auto` or your pinned model on the Keys page. The router transparently falls over across providers when one is rate-limited.

**Important**: Response quality varies by underlying model. For coding tasks, point `sonnet` to Groq (Llama 4) or GitHub Models (GPT-4o). For long context, use Gemini models.

## Using with Any OpenAI-Compatible Client

Change `base_url` and use unified key:

```python
from openai import OpenAI
client = OpenAI(
    base_url="http://localhost:3001/v1",
    api_key="freellmapi-YOUR_UNIFIED_KEY"
)
# All models from all providers available
models = client.models.list()
```

```bash
curl http://localhost:3001/v1/chat/completions \
  -H "Authorization: Bearer freellmapi-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"auto","messages":[{"role":"user","content":"Hello"}]}'
```

## Routing & Fallback Strategy

Six strategies, selectable on dashboard **Fallback Chain** page:

| Strategy | Behavior |
|----------|----------|
| `priority` | Your manual order — strict top-to-bottom |
| `balanced` | Weighted mix of speed + capability + reliability |
| `smartest` | Highest-capability model first |
| `fastest` | Lowest-latency model first |
| `reliable` | Best uptime/availability first |
| `custom` | Your own weight mix (speed/capability/headroom/errors) |

Each request: router picks best available model, skips rate-limited keys (429/5xx go on cooldown), retries up to 20 attempts within wall-clock budget. Dead key rotates to siblings.

**Sticky sessions**: Multi-turn conversations stay on same model for 30 min to avoid hallucination from mid-conversation switches.

## Fusion — Multi-Model Synthesis

Request model `fusion` and router fans your prompt to N diverse models in parallel, then a judge model synthesizes one answer:

```python
# Normal call, just change model name
response = client.chat.completions.create(
    model="fusion",
    messages=[{"role": "user", "content": "Explain quantum computing"}]
)
```

Configure panel size, judge model, and strategy on dashboard **Fusion** page.

## MCP Server

Exposes router state to MCP-capable agents at `POST /mcp`:
- List usable free models with per-model `supported_parameters`
- Check provider/key health and cooldowns
- Read usage stats and cache hit rates
- Switch routing strategy mid-session

Add to Claude Code MCP config:
```json
{
  "mcpServers": {
    "freellmapi": {
      "type": "http",
      "url": "http://localhost:3001/mcp",
      "headers": { "Authorization": "Bearer freellmapi-YOUR_KEY" }
    }
  }
}
```

## Model Profiles

Save named fallback-chain presets on dashboard:
- **Coding chain**: Groq (Llama 4) → GitHub Models (GPT-4o) → Gemini (Flash)
- **Long-context**: Gemini (2M ctx) → Mistral (128K) → Qwen3 (128K)
- **Vision**: Gemini → GPT-4o → GLM-4.7
- **Fast/cheap**: Groq → Cerebras → Pollinations

Switch active profile on dashboard or via MCP.

## Custom Providers

Add any OpenAI-compatible endpoint as a custom provider from Keys page:
- Local Ollama: `http://localhost:11434/v1`
- LM Studio: `http://localhost:1234/v1`
- Remote vLLM/llama.cpp gateway
- Any `/v1` endpoint

Routes through same fallback chain as cloud providers.

## Analytics & Monitoring

Dashboard shows per-provider/per-model/per-key:
- Request latency (p50, p95), TTFT for streams
- Token counts, success rate, estimated savings
- Windows: 24h to 90d

Health checks periodically mark keys: `healthy`, `rate_limited`, `invalid`, `error`.

## Security Notes

- API keys encrypted AES-256-GCM in SQLite before storage
- Decryption in-memory just before request
- Unified API key (`freellmapi-…`) — never expose upstream keys to apps
- Dashboard gated behind scrypt-hashed email+password login
- Optional encrypted DB backups (`FREEAPI_DB_BACKUP_*` env vars)

## Common Mistakes

- **Expecting same quality as paid APIs**: Free tiers have lower rate limits and weaker models. Use `smartest` strategy + fusion for best results.
- **Not adding enough provider keys**: 1-2 providers = frequent rate limiting. Add 5+ for smooth failover.
- **Forgetting sticky sessions**: Long conversations may switch models if session expires (30min). Restart conversation or pin specific model.
- **Using free tiers in production**: FreeLLMAPI is for personal experimentation. Free tiers have unpredictable availability.
- **Not enabling context handoff**: Set `FREELLMAPI_CONTEXT_HANDOFF=on_model_switch` so the new model knows it's continuing a task after failover.
