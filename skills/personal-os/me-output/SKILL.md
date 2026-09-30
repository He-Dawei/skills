---
name: me-output
description: 生成文件的存放位置、桌面清洁规则、格式工具选择。任何要产出文件（docx/pptx/pdf/xlsx/图片/导出/脚本）或临时脚本的任务都适用。触发词：导出、生成文件、存哪、保存、桌面、下载目录、简历 docx、报告文件。
---

# me-output — 文件输出与桌面清洁

## 存放位置

| 产出类型 | 位置 |
|---|---|
| **默认全部**生成/下载的文件 | `E:\claude code生成文件\` |
| **简历 .docx（仅最终版）** | `C:\Users\44527\Desktop\` |
| 构建脚本、`node_modules`、`package.json`、临时文件 | `C:\Users\44527\` 或系统 temp |
| 项目相关产出 | 该项目的目录（如 `E:\claude code生成文件\AI跨境\`） |

**禁止**：把生成文件丢到 `~/Downloads`、`~/Desktop`、当前工作目录 —— 除非用户明确说了放那儿。

## 桌面清洁（硬约束）

`C:\Users\44527\Desktop\` **只能有 .docx 简历文件**。

- 不留 `.js` / `.py` / `node_modules` / `package.json` / 临时文件。
- 流程固定：构建脚本写到 `C:\Users\44527\` 或 temp → 生成 .docx 到 Desktop → **立即清理**脚本和中间产物。
- 交付前自己检查一遍桌面，发现多余文件当场删掉（删除前先看清目标，见 `me-guard`）。

## 格式工具选择

- **Excel / 表格**：Python 3.14 必须用 `xlsxwriter`，**不要** `openpyxl`（有 `Fill()` bug）。
- **Word / 简历**：Node.js 用 `docx` 包。
- **PDF / PPTX**：按对应 skill 走，不要手搓。
- 证件照素材：`C:\Users\44527\Desktop\1寸证件照.jpg`

## 交付前检查清单

1. 文件在正确目录（不是 Desktop、不是 Downloads、不是 cwd）。
2. 文件名能看懂，不含临时后缀（`_v2_final`、`tmp`）。
3. 临时脚本、依赖目录、中间产物已清理。
4. Desktop 上只剩 .docx。
5. 回复里写清每个文件的路径和作用。

## 相关

- `me-guard` — 清理/覆盖文件前的范围与可逆性检查
- `me-index` — 项目专属产出目录
