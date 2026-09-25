---
name: wiki-curator
description: Maintain the llm-wiki knowledge base using the LLM Wiki pattern. Use for ingesting sources, linting, archiving queries, and keeping the wiki healthy.
---

# Wiki Curator

Maintain the llm-wiki Obsidian knowledge base following Andrej Karpathy's LLM Wiki pattern.

## Trigger

User says "ingest", "lint", "wiki", "整理知识", "入库", or after discovering useful knowledge to persist.

## Ingest Flow

1. Read source material (raw file, URL, conversation, video transcript)
2. Discuss key points with user if needed
3. Create `wiki/sources/<title>.md` with summary
4. Create or update entity/concept pages
5. Update `wiki/index.md`
6. Append `wiki/log.md` entry

## Lint Flow

Check: contradictions, stale claims, orphan pages, missing cross-references, empty directories, outdated counts.

## Query Archive

Save valuable Q&A to `wiki/queries/<short-description>.md`.

## Vault Paths

- Root: `E:\44527\Documents\claude仓库\`
- llm-wiki: `llm-wiki/`
- Schema: `llm-wiki/schema.md`
- Index: `llm-wiki/wiki/index.md`
