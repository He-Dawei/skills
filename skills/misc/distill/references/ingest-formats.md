# 摄取：各格式的处理与降级链

目标：把任意原材料转成一份规范化 markdown，供后续抽取使用。

## 各格式的路径

| 输入 | 首选 | 降级 |
|---|---|---|
| `.pdf`（文本版） | pymupdf 直接抽文本 | markitdown |
| `.pdf`（扫描件） | mineru 解析 | vision.js 逐页 OCR |
| `.epub` | ebooklib 按 spine 顺序抽 | pandoc 转 md |
| `.docx` | markitdown | python-docx 逐段抽 |
| `.txt` / `.md` | 直读 | — |
| 音频 / 视频 | ffmpeg 抽音频 → funasr SenseVoiceSmall | 已有链路见 `douyin-extract-pipeline` |

判定是否扫描件：抽出来的文本长度 / 页数 < 200 字/页 → 基本是扫描件，走 OCR 路径。

## 规范化要求

产出的 `source.md` 必须满足：

1. **保留章节层级** —— 标题层级是后续定位出处的唯一依据
2. **保留页码或位置标记** —— 抽取环节要标出处，没有位置标记就标不出
3. **剔除页眉页脚与重复页码**
4. **不要做任何内容改写** —— 摄取只做搬运和清洗，不做理解

## source.meta.json 字段

```json
{
  "input_path": "<原始文件路径>",
  "format": "epub",
  "extractor": "ebooklib",
  "title": "<书名>",
  "author": "<作者>",
  "char_count": 123456,
  "section_count": 42,
  "page_count": 210,
  "is_scanned": false,
  "ocr_ratio": 0.0,
  "language": "zh",
  "ingested_at": "YYYY-MM-DDTHH:MM:SS+08:00"
}
```

`ocr_ratio` = 经 OCR 得到的字符占比。> 0.5 时，抽取阶段的出处精度要打折扣并在产物里注明。

## 转写稿的特殊处理

音频 / 视频转写的稿子，**必须过一遍静音闸门**。
SenseVoice 遇静音段会幻觉（实测 14 秒纯 BGM 转出过不存在的句子）。

闸门：静音段占比 > 30%，或转写结果里有明显重复循环 → 标 `转写可疑`，
在产物里注明本次抽取基于可疑转写，需要人工复核。

## 失败处理

- 某种格式的首选解析器抛错 → 自动降级到备选，记录实际用了哪个
- 全部路径失败 → 明确报错，**不要产出一份残缺的 source.md**
  残缺的输入会静默污染后面所有环节，这是最坏的失败方式
