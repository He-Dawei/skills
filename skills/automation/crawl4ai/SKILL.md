---
name: crawl4ai
description: Use when you need to crawl, scrape, or extract content from web pages — turn any URL into clean Markdown, structured JSON, or screenshots using a local browser. Triggers: "scrape this page", "crawl this site", "extract content from URL", "screenshot this page", "get data from website", "爬取", "抓取", "网页内容".
---

# Crawl4AI

Local LLM-friendly web crawling. Open-source, no API keys. Uses real browser (Playwright) to render JS-heavy pages. Extracts clean Markdown, structured data, screenshots, and PDFs.

**Installed at:** `C:\Users\44527\AppData\Local\hermes\hermes-agent\venv\Scripts\`
**Python:** `/c/Users/44527/AppData/Local/hermes/hermes-agent/venv/Scripts/python`

## Quick Reference

| Task | Command |
|------|---------|
| Scrape URL to Markdown | `python -m crawl4ai https://example.com` |
| Health check | `python -c "from crawl4ai import ..."` |
| Install/Update | `python -m pip install -U crawl4ai` |

## One-Shot Scraping (For Quick Tasks)

Use `AsyncWebCrawler` for single-page scraping. Always use async context manager.

### Basic scrape — get clean Markdown

```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def scrape(url):
    async with AsyncWebCrawler(verbose=False) as crawler:
        result = await crawler.arun(url=url)
        return result.markdown  # Clean, LLM-ready markdown

md = asyncio.run(scrape("https://example.com"))
print(md[:5000])  # First 5000 chars
```

### Structured extraction with LLM

```python
import asyncio, json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy

async def extract_structured(url, schema, instruction):
    config = CrawlerRunConfig(
        extraction_strategy=LLMExtractionStrategy(
            provider="openai/gpt-4o",  # or "ollama/llama3"
            api_token="YOUR_KEY",
            schema=schema,
            instruction=instruction,
        )
    )
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url, config=config)
        return json.loads(result.extracted_content) if result.extracted_content else None
```

### Screenshot a page

```python
import asyncio, base64
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

async def screenshot(url, output_path):
    config = CrawlerRunConfig(screenshot=True)
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url, config=config)
        if result.screenshot:
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(result.screenshot))
            return output_path

asyncio.run(screenshot("https://example.com", "C:/Users/44527/Desktop/page.png"))
```

### Crawl multiple pages

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

async def crawl_many(urls):
    async with AsyncWebCrawler(verbose=False) as crawler:
        results = []
        for url in urls:
            result = await crawler.arun(url=url)
            results.append({
                "url": url,
                "title": result.metadata.get("title") if result.metadata else url,
                "markdown": result.markdown[:2000],
            })
        return results

data = asyncio.run(crawl_many([
    "https://example.com",
    "https://httpbin.org/html",
]))
for d in data:
    print(d["title"], "|", len(d["markdown"]), "chars")
```

### JavaScript-heavy pages (SPA)

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

async def scrape_spa(url):
    config = CrawlerRunConfig(
        js_code="window.scrollTo(0, document.body.scrollHeight);",
        wait_for="css:.content-loaded",  # Wait for element
        delay_before_return_html=2.0,    # Extra wait after JS
    )
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url, config=config)
        return result.markdown
```

## Common Configuration Options

```
CrawlerRunConfig(
    word_count_threshold=10,          # Skip text blocks < 10 words
    excluded_tags=["nav", "footer"],  # Remove these elements
    exclude_external_links=True,      # Remove external links
    remove_overlay_elements=True,     # Remove popups/modals
    process_iframes=True,             # Process iframe content
    screenshot=True,                  # Capture screenshot
    pdf=True,                         # Export as PDF
    cache_mode="BYPASS",              # or "ENABLED", "DISABLED"
    css_selector="main",              # Only extract this element
    js_code=[                         # Run JS before extraction
        "document.querySelector('.cookie-banner')?.remove()",
    ],
    wait_for="css:.main-content",     # Wait for element before extracting
    delay_before_return_html=1.0,     # Additional wait in seconds
)
```

## Running a Script

Always use the full Python path and write scripts to temp files:

```bash
/c/Users/44527/AppData/Local/hermes/hermes-agent/venv/Scripts/python -c "
import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler(verbose=False) as c:
        r = await c.arun(url='URL_HERE')
        print(r.markdown[:3000])

asyncio.run(main())
"
```

For sensitive pages, use `verbose=False` to suppress logging.

## Common Mistakes

- **Forgetting async context**: Always use `async with AsyncWebCrawler() as crawler:` — never instantiate directly.
- **Running sync**: crawl4ai is async-only. Use `asyncio.run()` to call from sync code.
- **Not waiting for JS**: SPAs need `wait_for` or `delay_before_return_html` — otherwise you get empty content.
- **Large pages without truncating**: Print first N chars of markdown (e.g. `[:3000]`) to avoid context overflow.
- **Wrong Python**: Always use `/c/Users/44527/AppData/Local/hermes/hermes-agent/venv/Scripts/python` — system Python may not have crawl4ai.

## vs Firecrawl

| | Crawl4AI | Firecrawl |
|---|---|---|
| Cost | Free, local | API key + credits |
| JS rendering | ✅ Playwright browser | ✅ |
| Speed | Slower (real browser) | Fast (cloud) |
| Scale | Single machine | Cloud infrastructure |
| Use case | Quick local scrapes | Production/scale |
