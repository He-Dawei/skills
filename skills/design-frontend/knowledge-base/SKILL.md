---
name: knowledge-base
description: Search and answer from the local LLM-Wiki knowledge base before using web sources. Use for research, explanations, comparisons, summaries, writing, planning, or any task that may relate to the user's saved sources, concepts, collections, tags, or prior learning notes.
---

# Knowledge Base

Use `E:\44527\Documents\LLM-Wiki` as the primary knowledge source.

## Workflow

1. Read `index.md` before opening other vault notes.
2. Extract the task's key terms, synonyms, platforms, and concept names.
3. Search frontmatter `tags` and `concepts` first with `rg` (or `grep` when `rg` is unavailable), then use a full-text search only if those fields have no useful match:

```powershell
rg -n -i --glob "*.md" "^(tags|concepts):.*(term1|term2)" E:\44527\Documents\LLM-Wiki\concepts E:\44527\Documents\LLM-Wiki\sources
rg -n -i --glob "*.md" "term1|term2" E:\44527\Documents\LLM-Wiki\concepts E:\44527\Documents\LLM-Wiki\sources E:\44527\Documents\LLM-Wiki\collections
```

4. Open matching concept or collection notes, then follow their `[[sources/...]]` links to the original source notes.
5. Treat vault content as the primary source. Distinguish source claims from inference, and preserve conflicting views instead of merging them silently.
6. Use WebSearch only when the vault lacks enough information or the claim requires current verification. Label web material as external supplementation.
7. Cite every substantive answer section with vault paths or Obsidian links such as `[[concepts/概念名]]` and `[[sources/文件名|标题]]`. Cite web sources separately with URLs.

## Boundaries

- Do not modify the vault unless the user asks for an update.
- Do not present an unmatched note as relevant merely because it shares a broad tag.
- State clearly when the knowledge base is insufficient, uncertain, conflicting, or potentially outdated.
