#!/usr/bin/env python3
"""锻造：把蒸馏结果生成 skill 骨架。

默认只写到工作目录下的 build/，不碰 skills-repo。
加了 --install-to 才会落到 skills-repo —— 但那一步是审批闸门，
本脚本只负责写文件，不 commit、不跑 sync-skills.ps1。

用法：
    python scaffold.py --work "<工作目录>" --name my-skill \
        --description "<触发词设计>"
    python scaffold.py --work "<工作目录>" --name my-skill \
        --description "..." --install-to "<skills-repo>/skills"
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
GROWTH_TEMPLATE = SKILL_DIR / "assets" / "growth-section.md"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def build_frontmatter(name: str, description: str) -> str:
    safe = description.replace('"', "'")
    return f'---\nname: {name}\ndescription: "{safe}"\n---\n'


def collect_body(work: Path) -> str:
    distilled = work / "distilled.md"
    if not distilled.is_file():
        raise SystemExit(
            f"缺 {distilled}。Extract 与 Compress 是判断密集型环节，要先产出它。\n"
            "流程：读 references/<类型>.md -> 抽取带出处 -> 压缩到一张 A4 -> 写成 distilled.md"
        )
    body = distilled.read_text(encoding="utf-8").strip()
    if len(body) < 200:
        raise SystemExit(f"distilled.md 只有 {len(body)} 字，太薄，不像压缩到位的结果。")
    return body


def scaffold(work: Path, name: str, description: str, category: str, install_to: Path | None) -> Path:
    if not NAME_RE.match(name):
        raise SystemExit(f"skill 名要 kebab-case：{name}")

    body = collect_body(work)
    growth = GROWTH_TEMPLATE.read_text(encoding="utf-8").strip() if GROWTH_TEMPLATE.is_file() else ""
    content = f"{build_frontmatter(name, description)}\n{body}\n\n---\n\n{growth}\n"

    root = install_to if install_to else work / "build"
    target = root / name if install_to else root / name
    if install_to:
        target = install_to / category / name
    target.mkdir(parents=True, exist_ok=True)
    (target / "SKILL.md").write_text(content, encoding="utf-8")

    # 带上工作目录里的抽取产物作为 references/
    copied = []
    work_refs = work / "references"
    if work_refs.is_dir():
        dest_refs = target / "references"
        dest_refs.mkdir(exist_ok=True)
        for item in sorted(work_refs.glob("*.md")):
            shutil.copy2(item, dest_refs / item.name)
            copied.append(item.name)

    # 把出处证据一起带走。抽取产物留在工作目录的话，skill 一迁移就断了溯源 ——
    # 「每条带出处」这条硬约束就白立了。
    dest_refs = target / "references"
    for name, source_name in (("evidence.json", "extract.json"), ("source-meta.json", "source.meta.json")):
        origin = work / source_name
        if not origin.is_file():
            continue
        dest_refs.mkdir(exist_ok=True)
        shutil.copy2(origin, dest_refs / name)
        copied.append(name)

    if not any(item == "evidence.json" for item in copied):
        print("⚠️  未找到 extract.json，产物不带出处证据。确认 Extract 步骤是否真的产出了它。")

    manifest = {
        "name": name,
        "category": category,
        "target": str(target),
        "installed_to_skills_repo": bool(install_to),
        "references_copied": copied,
        "skill_md_chars": len(content),
        "built_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    (target / "build-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description="生成 skill 骨架")
    parser.add_argument("--work", required=True, help="工作目录")
    parser.add_argument("--name", required=True, help="skill 名（kebab-case）")
    parser.add_argument("--description", required=True, help="frontmatter 的 description，触发词设计")
    parser.add_argument("--category", default="knowledge-management", help="skills-repo 下的分类目录")
    parser.add_argument("--install-to", default="", help="skills-repo 的 skills 目录；留空只写到 build/")
    args = parser.parse_args()

    install_to = Path(args.install_to).expanduser() if args.install_to else None
    if install_to and not install_to.is_dir():
        raise SystemExit(f"--install-to 不是目录：{install_to}")

    target = scaffold(
        Path(args.work).expanduser(), args.name, args.description, args.category, install_to
    )

    print(f"骨架已生成：{target}")
    if not install_to:
        print("（仅写到 build/，未装进 skills-repo）")
    else:
        print("\n⚠️ 审批闸门：请用户确认后再执行同步，不要自动 commit。")
    print("   确认后运行：C:/Users/44527/sync-skills.ps1 -Commit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
