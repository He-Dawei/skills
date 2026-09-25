# LLM-Wiki 落盘规范

vault：`E:/44527/Documents/LLM-Wiki/`。规则以 vault 根目录的 `AGENTS.md` 为准，本文是摘要。

**动手前先读 `index.md`。** 不要无目标扫描全库。

## 三个目录各放什么

| 目录 | 放什么 | 谁能写 |
|---|---|---|
| `sources/` | 原始来源笔记 | **禁止人工改写**。只有自动关系引擎和概念提取器可维护其 `concepts` 字段与文末关联区块 |
| `concepts/` | 概念笔记 | 有门槛，见下 |
| `collections/` | 主题合集 | 按主题聚合来源 |

## 蒸馏的落盘策略（重要）

**单本书蒸出的内容不满足 `concepts/` 的门槛。**

`AGENTS.md` 明确规定：同一概念被 **2 个以上独立来源**提及，才允许建概念笔记。
一本《穷爸爸富爸爸》蒸出来的概念是**孤证**，不能进 `concepts/`。

所以蒸馏产物这样落：

1. **来源笔记** `sources/` —— 原材料本身作为一条来源。用 `templates/source-template.md` 的字段。
2. **主题合集** `collections/` —— 按主题聚合，双链指向来源。
3. **概念笔记** `concepts/` —— **仅当该概念已有另一个独立来源支持时**才创建或补充。

宁可少写一步，不要建孤证笔记。孤证笔记后续会污染整个库的可信度。

## frontmatter 字段

**source**（模板见 `templates/source-template.md`）：

```yaml
---
id: ""
type: source
template: book          # 或 article / video / paper
platform: ""            # 来源平台，本机可填 local
source_url: ""
title: "书名"
author: ""
category: "未分类"
tags: [待整理]
created_at: "YYYY-MM-DDTHH:MM:SS"
status: pending          # pending → processed
---
```

**concept**：

```yaml
---
type: "concept"
concept: "概念名"
tags: ["概念名"]
confidence: "medium"     # high | medium | low
source_count: 2          # 必须 ≥2 才允许建
updated_at: "YYYY-MM-DDTHH:MM:SS+00:00"
---
```

**collection**：

```yaml
---
type: "collection"
topic: "主题名"
source_count: 2
updated_at: "YYYY-MM-DDTHH:MM:SS+00:00"
---
```

## confidence 怎么定

- `high` —— 多个可靠来源结论一致
- `medium` —— 证据有限但无明显冲突
- `low` —— 待核验、存在冲突，或来源质量不足

## 双链格式

引用来源必须用 Obsidian 双链：

```
[[sources/文件名]]
[[sources/文件名|显示名]]
```

概念结论必须反向链接对应来源，**不能只写无来源的 AI 判断**。

## 发现矛盾时

**保留不同观点并标注来源，不静默覆盖其中一方。**
这一条对蒸馏尤其重要 —— 蒸馏最容易在压缩过程中把矛盾抹平。

## 收尾

每次新增知识后，**检查并更新 `index.md`**。
