#!/usr/bin/env python3
"""成长：往 skill 的成长日志追加一条。

两道闸门，都不可绕过：
  1. 冲突检查 —— 新条目与已有条目关键词重叠时，先摆出来让人判断
  2. 用户确认 —— 不加 --confirm 只打印预览，不写文件

用法：
    # 预览（不写）
    python growth_append.py --skill "<skill目录>" \
        --situation "..." --gap "..." --fix "..."
    # 确认写入
    python growth_append.py --skill "<skill目录>" \
        --situation "..." --gap "..." --fix "..." --confirm
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

LOG_HEADER = "## 成长日志"
STOPWORDS = {"这个", "那个", "一个", "我们", "可以", "需要", "没有", "就是", "还是", "什么"}


def load_log(text: str) -> tuple[list[str], list[str]]:
    """返回 (表头区行, 数据行)。"""
    if LOG_HEADER not in text:
        raise SystemExit(f"该 skill 没有「{LOG_HEADER}」节。它不含成长功能，先补上再追加。")
    head, _, tail = text.partition(LOG_HEADER)
    lines = tail.split("\n")
    rows = [line for line in lines if line.strip().startswith("|") and "---" not in line]
    return head.split("\n") + [LOG_HEADER], rows


def keywords(text: str) -> set[str]:
    tokens = re.findall(r"[\u4e00-\u9fff]{2,}|[A-Za-z_]{3,}", text)
    return {token for token in tokens if token not in STOPWORDS}


def is_data_row(row: str) -> bool:
    """区分真条目行与表头/空行/分隔行。

    早先只排除 --- 分隔行，结果表头与空占位行也被当成条目，
    导致冲突检查对着表头做比对。
    """
    cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
    if not any(cells):
        return False
    if all(set(cell) <= set("-: ") for cell in cells if cell):
        return False
    if cells and cells[0] in ("日期", "date", "Date"):
        return False
    return True


def find_conflicts(rows: list[str], new_text: str) -> list[tuple[str, set[str]]]:
    new_keys = keywords(new_text)
    conflicts = []
    for row in rows:
        overlap = keywords(row) & new_keys
        if len(overlap) >= 2:
            conflicts.append((row.strip(), overlap))
    return conflicts


def main() -> int:
    parser = argparse.ArgumentParser(description="追加成长日志条目")
    parser.add_argument("--skill", required=True, help="skill 目录")
    parser.add_argument("--situation", required=True, help="遇到的情况")
    parser.add_argument("--gap", required=True, help="原协议哪里不够")
    parser.add_argument("--fix", required=True, help="修正")
    parser.add_argument("--confirm", action="store_true", help="真的写进去；不加只预览")
    args = parser.parse_args()

    skill_dir = Path(args.skill).expanduser()
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        raise SystemExit(f"找不到 {skill_md}")

    text = skill_md.read_text(encoding="utf-8")
    head_lines, rows = load_log(text)
    data_rows = [row for row in rows if is_data_row(row)]

    row = f"| {date.today().isoformat()} | {args.situation} | {args.gap} | {args.fix} |"
    new_keys = keywords(f"{args.situation} {args.gap} {args.fix}")
    conflicts = find_conflicts(data_rows, f"{args.situation} {args.gap} {args.fix}")

    print(f"skill：{skill_dir.name}")
    print(f"现有条目：{len(data_rows)} 条")
    print(f"\n拟追加：\n{row}\n")

    if conflicts:
        print("⚠️ 与已有条目关键词重叠，先确认是不是同一类问题：")
        for old_row, overlap in conflicts:
            print(f"  旧：{old_row}")
            print(f"  重叠词：{'、'.join(sorted(overlap))}\n")
        print("若确认是新问题就照写；若是旧问题的补充，应当改写旧条目而不是新增。")
    else:
        print("未发现冲突。")

    if not args.confirm:
        print("\n（预览模式，未写入。确认后加 --confirm 重跑。）")
        return 0

    if LOG_HEADER in text:
        marker = text.index(LOG_HEADER)
        end = text.find("\n\n", marker)
        insert_at = len(text) if end == -1 else end + 1
        text = text[:insert_at].rstrip("\n") + "\n" + row + "\n" + text[insert_at:].lstrip("\n")
    skill_md.write_text(text, encoding="utf-8")
    print(f"\n已追加到 {skill_md}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
