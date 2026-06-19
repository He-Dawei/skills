---
name: side-hustle-korean
description: Use when a Korean-major student in China wants to make money online, monetize Korean skills, find side hustles, or set up freelancing pipelines. Triggers on 副业, 赚钱, 韩语翻译, 微任务, 闲鱼, Fiverr, platform monetization, or setting up income streams. Covers platform database, pricing formulas, listing templates, and anti-scam rules.
---

# Side Hustle for Korean Majors in China

## Overview

Monetization pipeline optimized for Korean language students in China. Core insight: Korean skills = 2-3x premium over generic micro-tasks. Stack quick-win platforms (same-day cash) with long-term freelancing (recurring income).

## Decision Tree

```
New monetization request
├─ Need money TODAY (<24h)?
│  ├─ At computer? → 腾讯搜活帮 (WeChat) + 蚂蚁微客 (Alipay)
│  ├─ Going outside? → 友活来了 (store photo tasks, 20-40 RMB)
│  └─ Have 2+ hours? → Combo: 搜活帮 (30min) + 微客 (20min) + 友活 (walk-by)
├─ Building long-term pipeline?
│  ├─ Korean translation → Fiverr Gig + 闲鱼 listing
│  ├─ AI training → Mercor ($12-25/hr) + 百度众测
│  └─ Digital products → 闲鱼 (TOPIK materials, templates)
└─ Already have clients?
   └─ Use translate_helper.py for pricing + batch prep
```

## Platform Quick Reference

| Platform | Access | Pay Speed | Best For | Est. RMB/hr |
|----------|--------|-----------|----------|-------------|
| 腾讯搜活帮 | WeChat mini-program | Instant (1 RMB min) | Voice→text, image classify | 15-40 |
| 蚂蚁微客 | Alipay mini-program | 10 RMB min | Data annotation | 15-30 |
| 友活来了 | Alipay mini-program | Instant | Store photo verification | 20-40 |
| 阿里众包 | Alipay service window | 10 RMB min | Image/text checking | 15-25 |
| 百度众测 | test.baidu.com | Periodic | Data annotation, search eval | 15-30 |
| Fiverr | fiverr.com | Per order ($5 min) | Korean translation gigs | $15-25 |
| Mercor | work.mercor.com/explore | Weekly (Stripe/Wise) | AI training, translation eval | $12-25 |
| 闲鱼 | App | Per order | Translation services, study materials | 30-80/order |

Full platform details: [platforms.md](platforms.md)

## Pricing: Korean Translation

```
Base rates:
  韩→中: 50 RMB/1000 chars (harder to find native Chinese translators)
  中→韩: 80 RMB/1000 chars (rarer skill, charge more)
  Minimum: 30 RMB/order
  Rush fee: +50% (<2hr delivery)

Fiverr (global market pricing):
  Basic: $5/100 words
  Standard: $15/500 words
  Premium: $30/1000 words + express delivery
  
Tool: python tools/translate_helper.py quote <chars> [--rush]
```

Full pricing strategy: [pricing.md](pricing.md)

## Templates

Copy-paste ready. Edit bracketed fields, publish immediately.

- **Fiverr Gigs** (2 variants): [fiverr-gigs.md](fiverr-gigs.md)
- **闲鱼 Listings** (3 service types): [xianyu-listings.md](xianyu-listings.md)
- **Mercor Resume** (English): [mercor-guide.md](mercor-guide.md)

## Anti-Scam Rules (Non-Negotiable)

1. **Never pay upfront fees** — real platforms don't charge deposits
2. **No 刷单 (fake orders)** — illegal, will get your account frozen
3. **No renting out accounts** — WeChat/Alipay accounts used for money laundering = criminal liability
4. **Stick to big-tech platforms** — Tencent, Alibaba, Baidu, ByteDance-backed only
5. **Test withdrawal first** — withdraw 1 RMB before committing hours
6. **"500 RMB/day" promises** — all scams. Realistic: 40-80 RMB/day from micro-tasks

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Only doing micro-tasks, no long-term pipe | Stack: micro-tasks (today) + Fiverr (this week) + Mercor (this month) |
| Pricing too low on Fiverr | Start $5 to get reviews, raise to $15+ after 5 orders |
| Generic Gig description | Use templates — they're battle-tested |
| Not mentioning TOPIK | TOPIK = trust signal. Put it in every listing title |
| Waiting for clients | Post on 闲鱼 + Fiverr + 小红书 simultaneously |

## Tool: translate_helper.py

```
python tools/translate_helper.py count <file>    # Word count
python tools/translate_helper.py quote <chars>   # Price quote
python tools/translate_helper.py batch <dir>     # Batch directory stats
python tools/translate_helper.py bilingual \     # Generate side-by-side
  --ko ko.txt --zh zh.txt --output out.md
```

## Skill Maintenance

- **Platform database** (platforms.md): Update when platforms die/emerge. Most volatile file.
- **Templates**: Update when platform policies change (e.g., Fiverr fee structure).
- **Pricing**: Adjust quarterly based on demand. Check Fiverr "Korean translation" search results for market rate.
- **Tool**: Keep translate_helper.py compatible with Python 3.11+.
