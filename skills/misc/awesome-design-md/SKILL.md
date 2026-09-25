---
name: awesome-design-md
description: Apply brand design systems to UI projects using DESIGN.md files from 74+ brands (Apple, Airbnb, Stripe, Claude, Figma, etc). Use when building UI, designing components, or when user asks for a specific brand's look-and-feel.
---

# Awesome DESIGN.md

Collection of DESIGN.md files from 74+ popular brand design systems. Each file contains design tokens, typography, color palettes, spacing, and component patterns extracted from real products.

## When to Use

- User asks for UI matching a specific brand (e.g. "make it look like Stripe", "Apple-style landing page")
- Building frontend components and need a design system reference
- User says "use a design system", "brand styling", "DESIGN.md"
- Vibe-coding UI and need consistent design direction
- User asks "what design systems do you have?"

## Available Brands

74 brands in `design-md/` directory. Key ones:

| Category | Brands |
|----------|--------|
| Big Tech | apple, google, microsoft, meta, amazon, netflix, spotify |
| AI/ML | claude, openai, cohere, elevenlabs, cursor, composio |
| Design Tools | figma, framer, linear, notion, clay, airtable |
| Finance | stripe, coinbase, binance, mercedes-benz |
| Automotive | bugatti, ferrari, porsche, bmw, bmw-m, rivian |
| Social | discord, instagram, snapchat, tiktok, threads |
| Dev Tools | vercel, expo, railway, render, supabase, planetscale |
| Other | nike, sonos, patagonia, dell-1996, and more |

Full list: `ls design-md/`

## How to Use

### 1. List available brands
`ls ~/.claude/skills/awesome-design-md/design-md/`

### 2. Load a DESIGN.md
When user specifies a brand, read:
`~/.claude/skills/awesome-design-md/design-md/{brand}/DESIGN.md`

### 3. Copy to project
Copy the DESIGN.md to user's project root:
`cp ~/.claude/skills/awesome-design-md/design-md/{brand}/DESIGN.md {project}/DESIGN.md`

### 4. Apply the design
After reading DESIGN.md, extract and apply:
- **Colors**: CSS variables, hex values, dark/light variants
- **Typography**: Font stack, sizes, weights, line heights
- **Spacing**: Scale system, component gaps, layout patterns
- **Components**: Button styles, card patterns, input designs
- **Animation**: Easing curves, duration scales, motion patterns
- **Iconography**: Icon style, sizing, usage rules

## Workflow

1. User requests brand X UI
2. Read `design-md/{brand}/DESIGN.md`
3. If brand not found, suggest closest alternatives
4. Extract design tokens from the file
5. Apply tokens to the UI being built
6. Mention which brand's design system is being used

## Notes

- DESIGN.md files are analysis of public brand design systems — use as reference
- Not all brands have complete token coverage — adapt where needed
- Some files contain CSS variables ready to copy-paste
- For brands without DESIGN.md, consider creating one by analyzing their public website
