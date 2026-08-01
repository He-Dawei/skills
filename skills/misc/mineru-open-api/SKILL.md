---
name: mineru-open-api
description: Document to Markdown converter. Use when user wants to convert PDF/DOCX/PPTX to Markdown, extract text from documents, or parse document content for AI processing.
---

# MinerU Open API — Document to Markdown

## Tool Info

- **CLI**: `mineru-open-api` (installed globally, v0.5.9)
- **Package**: `mineru-open-api`
- **Purpose**: One command to turn documents into Markdown

## When to Use

User mentions: convert PDF to markdown, extract text from document, document to markdown, PDF parsing, DOCX to text, 文档转markdown, 提取文档内容.

## Quick Start

```bash
mineru-open-api <file-path>
```

## Common Workflows

### Convert PDF to Markdown
```bash
mineru-open-api document.pdf
```

### Convert with Specific Output
```bash
mineru-open-api document.pdf -o output.md
```

### Batch Convert
```bash
mineru-open-api *.pdf
```

## Supported Formats

- PDF (.pdf)
- Word (.docx)
- PowerPoint (.pptx)
- Images with text (OCR)

## Output

Clean Markdown with preserved structure:
- Headings hierarchy
- Tables
- Lists
- Images (extracted to separate files)
- Mathematical formulas

## Notes

- Requires MinerU API key set via environment variable
- Cloud-based processing — document is uploaded for parsing
- Best for documents that need to be fed into AI/LLM context
