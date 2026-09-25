---
name: internship-hunter
description: Use when user wants to find internships or jobs — searching platforms, verifying listings, tailoring resumes to JDs, generating application Excel trackers. Triggers on: 找实习, 暑期实习, 日常实习, 找工作, 简历匹配, internship, job search, JD匹配, 投递. Covers the full pipeline: multi-source search → strict verification → JD-resume mapping → Excel output → priority-based action plan. NOT for one-off resume edits without search context.
---

# Internship Hunter

## Overview

End-to-end internship search pipeline. Core principle: **every listing must be verified against its source before it enters the Excel**. No verification = deletion. This skill covers search strategy, verification rules, JD-to-resume rewriting, and Excel generation.

## When to Use

- User asks to find internships / jobs with specific filters (city, major, industry, deadline)
- User wants resume tailored to a specific JD
- User needs an Excel tracker of application targets with deadlines
- User says: 找实习, 暑期实习, 日常实习, 帮我找, JD匹配, 投递, 简历改写

**Do NOT use for:**
- Resume formatting without search context → use `docx` skill directly
- General career advice without concrete listings
- Single-resume edits not driven by a JD

## Search Strategy

### Five Channels in Parallel

Always search ALL five. Never stop at one.

| Channel | Query Pattern | Best For |
|---------|-------------|----------|
| 应届生求职网 | `site:yingjiesheng.com [city] 实习 [year]` | Bank/government/institution summer programs |
| 实习僧 | `[city] 实习 [industry] [year] shixiseng.com` | HR/ops/marketing daily internships |
| BOSS直聘 | `[city] 实习 在校生 [year]` + web search | Tech/startup positions, fast apply |
| 51job前程无忧 | `site:51job.com [city] 实习 [year]届` | Foreign companies, traditional enterprises |
| 银行官网 | `[bank name] [city] 暑期实习 [year] 公告` | Bank summer internship official announcements |

### Search Phases

```
Phase 1: Broad sweep → 5 parallel searches with city + "实习" + "2026"
Phase 2: Bank-specific → search each major bank name + city + "暑期实习" + "公告"
Phase 3: Niche/补漏 → search "韩语" / "外语" / "不限专业" variants if relevant
Phase 4: Verification → fetch each listing individually, check: deadline, location, degree requirement
```

## Verification Rules (CRITICAL)

Every position MUST pass these checks before entering Excel. Failure on ANY check = DELETE.

### Mandatory Checks

| Check | Rule | Signal to Delete |
|-------|------|-----------------|
| **Deadline** | Must be > today's date | "3月31日截止" in June = DELETE |
| **Location** | Must contain the target city | "全国" without explicit city mention = SUSPECT |
| **Degree** | Must accept user's current level | "硕士及以上" when user is 本科 = DELETE |
| **Recency** | Posting < 30 days old OR has explicit deadline | "2025年" posting = DELETE |
| **Source** | Must have verifiable source URL or official announcement ID | Third-party reposts without original link = DELETE |

### How to Verify

1. For bank positions: search `[bank name] [city] 暑期实习 公告 2026` → must find official announcement page with matching content
2. For platform positions: open the actual listing URL → check "在招" status, deadline, requirements
3. For 滚动招聘 (rolling): acceptable ONLY if posting refreshed within 30 days

### Red Flags — Delete Immediately

- "3月31日截止" or any deadline < today
- "硕士及以上" when user is 本科在校生
- "需要X年工作经验" for internship position
- Listing page returns 404 or "已下线"
- City column shows wrong location (e.g., "天津" in Dalian search)
- Posting from previous calendar year without refresh

## JD→Resume Rewriting Rules

### Core Principle

Every resume bullet MUST end with an explicit mapping to a JD requirement. The reader must see "this experience = that requirement" without thinking.

### Mapping Pattern

```
JD keyword → project experience reframed → explicit correspondence
```

### Template

```
dot("[JD keyword in Chinese]:", "[user's experience reframed using JD vocabulary] —— [explicit 'matches JD item X' statement]")
```

### Example

**JD says:** "整理与分析辖区内上市公司研报"

**Bad bullet:**
```
dot("数据分析：", "运用Excel处理200+条中韩数据，完成清洗与统计分析。")
```

**Good bullet:**
```
dot("市场研究与数据分析：", "收集处理中韩数据200+条，运用Excel完成清洗、分类汇总与统计分析，数据准确率100%。此能力可直接应用于上市公司研报整理与行业市场数据分析。")
```

### What to Always Match

1. Every JD line → find one resume bullet that maps to it
2. Use JD's own vocabulary in the bullet text
3. End each bullet with the transferability statement
4. Quantify everything (numbers, pages, frequency, accuracy)

## Excel Output Specification

### Required Sheets

| Sheet | Content |
|-------|---------|
| 银行暑期实习 | Bank positions only, sorted by deadline ASC |
| 人力行政猎头 | HR/recruiter/admin positions |
| 其他实习 | Operations, marketing, IT, other |
| 外企实习 | Foreign company positions (if applicable) |
| 投递优先级 | Single table sorted by deadline, with action column |
| 今天行动清单 | Step-by-step what to do TODAY |

### Style Rules

- Use `xlsxwriter` (NOT `openpyxl` — has Python 3.14 Fill() bug)
- Three color tiers: `urgent` (#FFD7D7) for deadline ≤ 2 days, `top` (#E2EFDA) for this week, `green` (#C6EFCE) for rolling
- Freeze top row on every sheet
- All cells: 10pt Microsoft YaHei, border, text_wrap
- Row height: 40-55 depending on content density
- Column widths: content-aware (company name 22, JD description 38-42, others 10-18)

### Column Template

```
["序号","公司","岗位","地点","薪资","要求","学历","亮点","投递渠道","截止时间","核实状态"]
```

Always include "核实状态" column — shows ✅ with verification source.

### Critical Rule

After generating Excel, run:
```
start "" "path/to/file.xlsx"
```
Open it immediately so user can verify.

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Listing "全国" positions as "大连" | Only include if explicitly confirmed for target city |
| Including 恒隆地产 after March | Always check deadline against current date |
| Including 大商所 for undergrad | Always check degree requirement |
| Mixing expired and current listings | Separate sheet for "已过期(参考)" if user wants history |
| Using openpyxl with Python 3.14 | Use xlsxwriter exclusively |
| Forgetting to verify source URL | Every listing must have clickable URL or official announcement ID |
| Not filtering v4 before regenerating | When asked to "更新", remove EXPIRED items FIRST, then add new |

## Quick Reference

### Bank Summer Internship Deadlines (2026 Dalian Reference)

| Bank | Program | Typical Deadline | URL Pattern |
|------|---------|-----------------|-------------|
| 工商银行 | 星令营 | Mid-June | job.icbc.com.cn |
| 建设银行 | 建习生 | Late June | job.ccb.com |
| 农业银行 | 暑期实习生 | Late June | career.abchina.com.cn |
| 兴业银行 | 雏雁计划 | Late June | job.cib.com.cn |
| 招商银行 | 梦工场 | Early-Mid June | career.cmbchina.com |

### Search Keywords Map

```
Bank:        "[city] [bank] 暑期实习 公告 2026"
HR/猎头:     "[city] 猎头 实习 OR [city] 人力资源 实习"
General:     "[city] 实习 不限专业 在校生"
Foreign:     "[city] 外企 实习 OR [city] BPO 实习"
Korean:      "[city] 韩语 实习 OR [city] 朝鲜语 实习"
```

## Implementation Notes

- Always search 5 channels in parallel using WebSearch tool
- Fetch listing detail pages with WebFetch when available
- Generate Excel with xlsxwriter (not openpyxl)
- Generate tailored resume with docx (Node.js `docx` package)
- Clean up temp files (.js scripts, node_modules) from Desktop — only keep .docx output
- Present results as concise summary table, then open the Excel file
