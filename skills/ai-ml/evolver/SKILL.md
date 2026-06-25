---
name: evolver
description: AI agent self-evolution engine. Use when user wants to evolve, optimize, or improve an AI agent/project through auditable Genes and Capsules under the GEP protocol.
---

# Evolver — Agent Self-Evolution Engine

## Tool Info

- **CLI**: `evolver` (installed globally, v1.89.17)
- **Package**: `@evomap/evolver`
- **Protocol**: GEP (Genes, Capsules, Events) — auditable evolution assets
- **Research**: [arXiv:2604.15097](https://arxiv.org/abs/2604.15097)

## When to Use

User mentions: evolve agent, optimize prompt, improve performance, self-evolution, 进化, 优化, prompt engineering iteration, agent improvement, GEP, skill evolution.

## Quick Start

```bash
evolver
```

Run in any git repo to start evolution tracking.

## Common Workflows

### Initialize Evolution Tracking
```bash
cd <project-dir>
evolver init
```

### Run Evolution Cycle
```bash
evolver run
```

### View Evolution History
```bash
evolver history
```

### Export Evolution Assets
```bash
evolver export
```

## Key Concepts

- **Genes**: Compact, auditable evolution units (stronger than skill docs per research)
- **Capsules**: Packaged evolution assets for reuse
- **Events**: Immutable audit trail of all changes
- **GEP Protocol**: Standard for agent evolution data exchange

## Integration Notes

1. Works with any LLM-based agent — not tied to a specific framework
2. Evolution assets are git-tracked for auditability
3. Genes can be shared across projects (EvoMap network)
4. CLI Quick Start path is for users who want to evolve agents; Run from Source path is for contributors
