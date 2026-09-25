---
name: firecrawl
description: Use when you need to scrape web pages, crawl websites, search the web, or extract structured data from URLs — turn any web page into clean Markdown or structured JSON for LLM consumption. Triggers include: "scrape this page", "extract content from URL", "crawl this site", "search the web for X and get full content", "turn this webpage into markdown", "get data from this website".
---

# Firecrawl

Web scraping/crawling API. Turn any URL into clean Markdown, structured JSON, or screenshots. Search the web and get full page content from results. LLM-ready output.

## Quick Reference

| Task | CLI | API Endpoint |
|------|-----|-------------|
| Scrape one URL | `firecrawl scrape <url>` | `POST /v2/scrape` |
| Search web + get content | `firecrawl search "<query>"` | `POST /v2/search` |
| Crawl entire site | `firecrawl crawl <url>` | `POST /v2/crawl` |
| List all site URLs | `firecrawl map <url>` | `POST /v2/map` |
| Batch scrape many URLs | — | `POST /v2/batch/scrape` |
| Scrape + interact (click/scroll) | — | `POST /v2/interact` |
| Autonomous data gathering | — | `POST /v2/agent` |

## Setup

**Cloud API** (fastest path):
```bash
# Get API key at https://firecrawl.dev
export FIRECRAWL_API_KEY="fc-YOUR_KEY"
```

**Python SDK:**
```bash
pip install firecrawl-py
```

**Node.js SDK:**
```bash
npm install firecrawl
```

**CLI:**
```bash
npm install -g firecrawl-cli
firecrawl login  # then paste API key
```

**Self-host** (Docker, no API key needed):
```bash
git clone https://github.com/firecrawl/firecrawl.git
cd firecrawl
# Copy .env.example, fill in required vars
docker compose up -d
# Then set FIRECRAWL_API_URL=http://localhost:3002
```

## Common Usage Patterns

### Scrape one page to Markdown

```python
from firecrawl import Firecrawl
app = Firecrawl(api_key="fc-YOUR_KEY")
result = app.scrape("https://example.com")
print(result["markdown"])
```

```bash
# CLI — simplest path
firecrawl scrape https://example.com
firecrawl https://example.com --only-main-content
```

### Search web + get full content of results

```python
results = app.search("latest AI research papers 2026", limit=5)
for r in results:
    print(r["url"], "-", r["title"])
    # Each result includes full markdown content
```

### Extract structured JSON from a page

```python
# Define exactly what you want
schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "price": {"type": "number"},
        "reviews": {"type": "array", "items": {"type": "string"}}
    }
}
result = app.scrape("https://example.com/product", {
    "formats": ["extract"],
    "extract": {"schema": schema}
})
```

### Crawl an entire site

```python
result = app.crawl("https://docs.example.com", {
    "limit": 100,  # max pages
    "includePaths": ["/docs/*"],  # only these paths
    "excludePaths": ["/blog/*"]   # skip these
})
```

### Scrape JS-heavy pages (SPA, dynamic content)

CLI handles JS rendering automatically. In API/SDK:
```python
result = app.scrape("https://spa-site.com", {
    "actions": [
        {"type": "wait", "milliseconds": 2000},
        {"type": "click", "selector": "button.load-more"},
        {"type": "wait", "milliseconds": 1000}
    ]
})
```

### Self-hosted usage

```python
app = Firecrawl(
    api_url="http://localhost:3002",
    api_key=""  # empty for self-hosted
)
```

## MCP Integration

Connect Firecrawl to any MCP client:
```bash
npx firecrawl-mcp
```
Then in Claude Code settings add the MCP server for direct web scraping in conversations.

## Common Mistakes

- **Forgetting JS rendering**: Static fetch won't work on SPAs. Use `actions` with `wait` for JS-heavy pages.
- **No rate limiting on self-hosted**: Self-hosted instances need manual rate limiting — set `MAX_REQUESTS_PER_MINUTE` in env.
- **Scraping without `--only-main-content`**: CLI default includes nav/footer noise. Add `--only-main-content` for clean LLM input.
- **Ignoring `excludePaths` on crawls**: Without path filters, crawl follows every link — can hit your limit fast.

## Format Options

Every endpoint supports these output formats:
- `markdown` — clean, LLM-ready (default)
- `html` — raw HTML
- `rawHtml` — original unprocessed HTML
- `screenshot` — full-page PNG
- `extract` — structured JSON via schema
- `links` — all links on page
- `images` — all image URLs
