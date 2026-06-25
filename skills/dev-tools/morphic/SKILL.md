---
name: morphic
description: AI-powered search engine with generative UI. Use when user wants to run morphic, search with AI, or needs help configuring the morphic search app.
---

# Morphic — AI Search Engine

## Tool Info

- **Location**: `C:\Users\44527\morphic\`
- **Framework**: Next.js 16 (Turbopack), React 19, Tailwind CSS
- **Stack**: Supabase Auth, PostgreSQL, Vercel AI SDK
- **Search Providers**: Tavily, SearXNG, Brave, Exa

## When to Use

User mentions: morphic search, AI search, 智能搜索, start morphic, configure search, morphic setup, search engine.

## Quick Start

```bash
cd C:\Users\44527\morphic
npm run dev
```

## Configuration

Create `.env.local` in `C:\Users\44527\morphic\`:

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# AI Provider (at least one)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_GENERATIVE_AI_API_KEY=

# Search Provider (at least one)
TAVILY_API_KEY=
SEARXNG_URL=
BRAVE_API_KEY=
EXA_API_KEY=

# Optional: Langfuse for telemetry
LANGFUSE_PUBLIC_KEY=
LANGFUSE_SECRET_KEY=
LANGFUSE_BASEURL=

# Optional: Upstash Redis for rate limiting
UPSTASH_REDIS_REST_URL=
UPSTASH_REDIS_REST_TOKEN=
```

## Build (Production)

```bash
cd C:\Users\44527\morphic
npm run build
npm start
```

## Docker Alternative

```bash
docker pull ghcr.io/miurla/morphic:latest
# See repo for docker-compose.yml
```

## Features

- AI-powered search with cited answers
- Generative UI (rich inline components)
- Quick and Adaptive search modes
- Multiple AI providers (OpenAI, Anthropic, Google, Ollama)
- File upload support
- Shareable search results
- Supabase Auth + Guest mode
