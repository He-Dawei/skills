---
name: conversation-extractor
description: Extract reusable knowledge from conversation records into llm-wiki. Use after saving conversation summaries to capture bug patterns, tool configs, user preferences, and new concepts.
---

# Conversation Extractor

Scan conversation records and extract reusable knowledge into llm-wiki.

## Trigger

After saving `对话记录/`, user says "extract"/"提取"/"归档", or weekly lint scan.

## Criteria

Extract when conversation has: new bug pattern + fix, tool install/config change, new user preference/rule, wiki-uncovered topic, reusable diagnostic method.

## Flow

1. Read recent conversation record
2. Check criteria
3. Create/update `wiki/sources/` page
4. Update entity/concept pages with new knowledge
5. Update `wiki/index.md` + `wiki/log.md`
6. Archive high-value Q&A to `wiki/queries/`

## Vault

Root: `E:\44527\Documents\claude仓库\`
