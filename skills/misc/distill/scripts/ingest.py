#!/usr/bin/env python3
"""摄取：原材料 -> 规范化 markdown。

只做搬运与清洗，不做理解。产出 source.md + source.meta.json。

用法：
    python ingest.py --input "<文件路径>" --work "<工作目录>"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

REPEAT_HEADER_MAX = 0.08      # 同一行重复出现比例超过此值，视为页眉页脚
SCANNED_CHARS_PER_PAGE = 200  # 每页字符数低于此值，判为扫描件


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


# --------------------------------------------------------------------- 各格式抽取


def from_pdf(path: Path) -> tuple[str, str, int, int]:
    """返回 (正文, 用的解析器, 页数, 字符数)。"""
    try:
        import fitz  # pymupdf
    except ImportError:
        raise RuntimeError("未安装 pymupdf，无法解析 pdf。pip install pymupdf")

    doc = fitz.open(str(path))
    pages = []
    for index, page in enumerate(doc, start=1):
        text = page.get_text("text").strip()
        if text:
            # 保留页码标记 —— 抽取阶段要靠它标出处
            pages.append(f"\n<!-- page:{index} -->\n\n{text}")
    doc.close()
    body = "\n".join(pages)
    return body, "pymupdf", len(pages), len(body)


def from_epub(path: Path) -> tuple[str, str, int, int]:
    try:
        import ebooklib
        from ebooklib import epub
        from bs4 import BeautifulSoup
    except ImportError:
        raise RuntimeError("未安装 ebooklib/beautifulsoup4。pip install ebooklib beautifulsoup4")

    book = epub.read_epub(str(path))
    sections = []
    # 按 spine 阅读顺序取。get_items_of_type 不保证顺序，会让出处错位。
    for idref, _linear in book.spine:
        item = book.get_item_with_id(idref)
        if item is None or item.get_type() != ebooklib.ITEM_DOCUMENT:
            continue
        soup = BeautifulSoup(item.get_content(), "html.parser")
        heading = ""
        for tag in soup.find_all(["h1", "h2", "h3", "title"]):
            candidate = tag.get_text(" ", strip=True)
            if candidate:
                heading = candidate[:80]
                break
        text = soup.get_text("\n").strip()
        if len(text) < 20:          # 封面、版权页这类碎片
            continue
        sections.append((heading, text))

    parts = []
    for index, (heading, text) in enumerate(sections, start=1):
        label = heading or f"第 {index} 节"
        parts.append(f"\n## {label}\n\n{text}")
    body = "\n".join(parts)
    return body, "ebooklib", len(sections), len(body)


def from_docx(path: Path) -> tuple[str, str, int, int]:
    try:
        from docx import Document
    except ImportError:
        raise RuntimeError("未安装 python-docx。pip install python-docx")

    document = Document(str(path))
    lines = []
    for para in document.paragraphs:
        text = para.text.strip()
        if text:
            style = (para.style.name or "").lower()
            lines.append(f"## {text}" if "heading" in style else text)
    body = "\n\n".join(lines)
    return body, "python-docx", len(lines), len(body)


def from_text(path: Path) -> tuple[str, str, int, int]:
    body = path.read_text(encoding="utf-8", errors="replace")
    return body, "direct", body.count("\n") + 1, len(body)


EXTRACTORS = {
    ".pdf": from_pdf,
    ".epub": from_epub,
    ".docx": from_docx,
    ".txt": from_text,
    ".md": from_text,
    ".markdown": from_text,
}


# --------------------------------------------------------------------- 清洗


def strip_repeated_lines(body: str) -> tuple[str, int]:
    """剔除页眉页脚：短行反复出现即视为噪声，返回 (清洗后正文, 剔除行数)。"""
    lines = body.split("\n")
    counts: dict[str, int] = {}
    for line in lines:
        stripped = line.strip()
        if 0 < len(stripped) <= 40:
            counts[stripped] = counts.get(stripped, 0) + 1

    threshold = max(3, int(len(lines) * REPEAT_HEADER_MAX))
    noise = {line for line, count in counts.items() if count >= threshold}
    kept = [line for line in lines if line.strip() not in noise]
    return "\n".join(kept), len(lines) - len(kept)



# 脚注规则：全用字符类写法，避免任何反斜杠转义（本机 heredoc 会吃掉一层）
_FOOTNOTE_RULE = re.compile("^[—=_-]{10,}[ 	]*$")
_MARKER_ONLY = re.compile("^[ 	]*[(][0-9]{1,3}[)][ 	]*$")
_SENTENCE_END = ("。", "！", "？", "：", "”", "）", "」", "』", "!", "?", ".")


def strip_footnotes(body: str) -> tuple[str, int]:
    """剥离脚注。epub 转出来的脚注会把句子劈成两截："

        「连八年级 / (1) / 都没能念完」

    两处都要处理：正文中间的 (N) 标记，以及章末分隔线之后那一整块脚注正文。
    不处理的话，抽取阶段读到的是断句，出处也就跟着错位。
    """
    kept: list[str] = []
    dropped = 0
    pending_join = False
    in_footnote_block = False

    for line in body.split(chr(10)):
        if line.startswith("## "):
            in_footnote_block = False
            pending_join = False
            kept.append(line)
            continue

        if _FOOTNOTE_RULE.match(line):
            in_footnote_block = True
            dropped += 1
            continue

        if in_footnote_block:
            dropped += 1
            continue

        if _MARKER_ONLY.match(line):
            pending_join = True
            dropped += 1
            continue

        if pending_join:
            if not line.strip():
                continue                      # 标记后面的空行，吞掉
            # 注意：标记前面已经入栈了空行，kept[-1] 是空的。
            # 必须先回退尾部空行，否则永远取不到上一段文字，接不回去。
            while kept and not kept[-1].strip():
                kept.pop()
            # 接上的两种情形，缺一不可：
            #   1) 上一行没写完一句
            #   2) 下一行以标点开头（引号收尾的术语被拆开时就长这样：
            #      「“所得等级攀升”」换行「。这时…」）
            # 只看情形 1 会漏掉 2 —— 引号 `”` 同时是句末和句中，判不出来。
            continues = bool(line.strip()) and line.strip()[0] in _SENTENCE_END
            unfinished = bool(kept) and not kept[-1].rstrip().endswith(_SENTENCE_END)
            if kept and (unfinished or continues):
                kept[-1] = kept[-1].rstrip() + line.strip()
                pending_join = False
                continue
            pending_join = False

        kept.append(line)

    # 折叠连续空行（手写循环，不用正向则表达式，规避转义问题）
    out: list[str] = []
    blanks = 0
    for line in kept:
        if line.strip():
            blanks = 0
            out.append(line)
        else:
            blanks += 1
            if blanks <= 1:
                out.append("")
    return chr(10).join(out), dropped


_SKIP_TITLE = re.compile(
    r"^(目\s*录|contents?|版权|copyright|cover|扉页|书名页|出版|图书在版)",
    re.IGNORECASE,
)


def slice_body(body: str, from_re: str, to_re: str) -> tuple[str, str]:
    """按章节标题切片。套装/合集里只取目标那一本 —— 不切会让多本书混在一起蒸。

    返回 (切出的正文, 用作标题的章节名)。
    """
    start, title = 0, ""
    if from_re:
        match = re.search(rf"^##\s+.*{from_re}.*$", body, re.MULTILINE)
        if not match:
            raise SystemExit(f"--from-heading 没匹配到任何章节：{from_re}")
        start, title = match.start(), match.group(0).lstrip("# ").strip()
    end = len(body)
    if to_re:
        match = re.search(rf"^##\s+.*{to_re}.*$", body, re.MULTILINE)
        if not match:
            raise SystemExit(f"--to-heading 没匹配到任何章节：{to_re}")
        end = match.start()
    if end <= start:
        raise SystemExit("切片范围为空：--to-heading 落在 --from-heading 之前")
    return body[start:end], title


def guess_title(body: str, fallback: str) -> str:
    """取首个像书名的行。跳过目录页与版权页 —— 否则标题会变成「目 录」。"""
    for line in body.splitlines()[:120]:
        stripped = line.strip().lstrip('#').strip()
        if not 2 <= len(stripped) <= 80:
            continue
        if _SKIP_TITLE.match(stripped):
            continue
        return stripped
    return fallback


# --------------------------------------------------------------------- 主流程


def ingest(input_path: Path, work: Path, from_heading: str = "", to_heading: str = "") -> dict:
    if not input_path.is_file():
        raise SystemExit(f"输入文件不存在：{input_path}")

    suffix = input_path.suffix.lower()
    if suffix not in EXTRACTORS:
        raise SystemExit(f"不支持的格式：{suffix}（支持 {'/'.join(EXTRACTORS)}）")

    body, extractor, units, _raw_len = EXTRACTORS[suffix](input_path)
    body, removed = strip_repeated_lines(body)
    body, footnotes = strip_footnotes(body)

    slice_title = ""
    if from_heading or to_heading:
        body, slice_title = slice_body(body, from_heading, to_heading)

    if len(body.strip()) < 200:
        raise SystemExit(
            f"抽取到的正文只有 {len(body.strip())} 字，基本是空的。\n"
            "不接受残缺输入 —— 它会静默污染后面所有环节。\n"
            "若是扫描版 PDF，请改用 OCR 路径（mineru 或 vision.js）重新摄取。"
        )

    units = max(units, 1)
    chars_per_unit = len(body) / units
    is_scanned = suffix == ".pdf" and chars_per_unit < SCANNED_CHARS_PER_PAGE

    work.mkdir(parents=True, exist_ok=True)
    (work / "source.md").write_text(body, encoding="utf-8")

    meta = {
        "input_path": str(input_path),
        "format": suffix.lstrip("."),
        "extractor": extractor,
        "title": slice_title or guess_title(body, input_path.stem),
        "author": "",
        "char_count": len(body),
        "section_count": len(re.findall(r"^#{1,4}\s+\S", body, re.MULTILINE)) or units,
        "page_count": units if suffix == ".pdf" else 0,
        "is_scanned": is_scanned,
        "ocr_ratio": 0.0,
        "chars_per_unit": round(chars_per_unit, 1),
        "removed_noise_lines": removed,
        "removed_footnote_lines": footnotes,
        "language": "zh" if _is_chinese(body) else "en",
        "sliced_from": from_heading,
        "sliced_to": to_heading,
        "ingested_at": _now(),
    }
    (work / "source.meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return meta


def _is_chinese(body: str) -> bool:
    sample = body[:20000]
    if not sample:
        return False
    han = sum(1 for char in sample if "\u4e00" <= char <= "\u9fff")
    return han / len(sample) > 0.15


def main() -> int:
    parser = argparse.ArgumentParser(description="摄取原材料为规范化 markdown")
    parser.add_argument("--input", required=True, help="原材料路径")
    parser.add_argument("--work", required=True, help="工作目录（输出 source.md 等）")
    parser.add_argument("--from-heading", default="", help="只取匹配此正则的章节起（含）。套装/合集用")
    parser.add_argument("--to-heading", default="", help="取到匹配此正则的章节止（不含）")
    args = parser.parse_args()

    meta = ingest(
        Path(args.input).expanduser(),
        Path(args.work).expanduser(),
        args.from_heading,
        args.to_heading,
    )
    print(json.dumps(meta, ensure_ascii=False, indent=2))
    print(f"\n下一步：python probe.py --work \"{args.work}\"")
    if meta["is_scanned"]:
        print("⚠️ 判定为扫描件，出处精度会打折，产物里要注明。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
