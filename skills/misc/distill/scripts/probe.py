#!/usr/bin/env python3
"""判定：原材料类型 + 可蒸性评估。

纯确定性启发式，不调模型。判断密集的最终决定留给 agent —— 本脚本给证据，
低置信度时明确要求 agent 去问用户，而不是猜。

用法：
    python probe.py --work "<工作目录>"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

MIN_CHARS_TO_DISTILL = 3000
LOW_UNIQUE_RATIO = 0.55          # 去重行占比低于此值 -> 注水嫌疑
CONFIDENCE_MARGIN = 0.25         # 头名与次名的分差低于此值 -> 要问用户

# 每类的特征词。命中即计分，权重按区分度给。
TYPE_MARKERS: dict[str, list[tuple[str, int]]] = {
    "tool-book": [
        # 只认结构化、命令式的标记。泛用词（方法/技巧/示例/如何）区分度太低，
        # 实测会把《富爸爸穷爸爸》这类思想书刷成工具书，故降权到 1 或剔除。
        (r"第[一二三四五六七八九十]+步", 6),
        (r"操作步骤|步骤如下|按以下步骤", 6),
        (r"清单|检查表|核对表|模板", 5),
        (r"注意事项|常见错误|误区", 4),
        (r"练习|作业|自测", 4),
        (r"怎么做|如何做|怎样做", 3),
        (r"方法|技巧", 1),
    ],
    "idea-book": [
        (r"本质上|归根结底|说到底|其实是", 4),
        (r"我(认为|觉得|相信|发现|意识到)", 4),
        (r"价值观|认知|思维方式|心智|观念", 4),
        (r"因为.{0,25}所以", 3),
        (r"哲学|智慧|人性|意义|道理", 3),
        (r"富人|穷人|思维|选择|自由|恐惧|贪婪", 3),
        (r"故事|有一次|记得那|小时候", 2),
        (r"我(?!们)", 1),
    ],
    "paper": [
        (r"摘要|abstract|关键词|keywords", 5),
        (r"参考文献|references|doi|et al", 5),
        (r"实验|样本|数据集|对照组|显著性", 4),
        (r"引言|研究方法|研究结果|讨论|结论", 3),
        (r"图\s*\d|表\s*\d|figure|table", 2),
        (r"本文|本研究|我们提出", 2),
    ],
    "transcript": [
        (r"\[\d{1,2}:\d{2}(:\d{2})?\]", 5),
        (r"\d{1,2}:\d{2}:\d{2}", 3),
        (r"主持人|嘉宾|听众|提问|回答", 4),
        (r"发言人|说话人|speaker", 4),
        (r"你(说的|讲的)|我想问|我补充", 2),
        (r"会议|访谈|对谈|录音", 3),
    ],
    "workflow": [
        (r"复盘|回顾|总结一下", 5),
        (r"环节|阶段|这一步", 4),
        (r"踩(过|了)坑|翻车|踩雷", 5),
        (r"不可省略|必须检查|别忘(了)?", 4),
        (r"下次(遇到|再)|以后(遇到|再)", 4),
    ],
}


TYPE_LABELS = {
    "tool-book": "工具书 -> 蒸方法论",
    "idea-book": "非工具书 -> 蒸作者思维框架",
    "paper": "论文/报告 -> 蒸论证链 + 可复用方法",
    "transcript": "会议纪要/访谈 -> 蒸决策逻辑",
    "workflow": "自己的工作流 -> 蒸成 skill",
}


def _lines(body: str) -> list[str]:
    return [line.strip() for line in body.split("\n") if line.strip()]


def assess_distillability(body: str, meta: dict) -> dict:
    """可蒸性：注水材料蒸出来必然是空话，这里先拦一道。"""
    lines = _lines(body)
    if not lines:
        return {"score": 0, "verdict": "不可蒸", "reasons": ["正文为空"]}

    unique_ratio = len(set(lines)) / len(lines)
    numbers = sum(1 for line in lines if re.search(r"\d", line)) / len(lines)
    headings = len(re.findall(r"^#{1,4}\s+\S", body, re.MULTILINE))
    avg_line = len(body) / len(lines)

    score = 0
    reasons: list[str] = []

    if unique_ratio >= 0.75:
        score += 3
    elif unique_ratio >= LOW_UNIQUE_RATIO:
        score += 2
    else:
        reasons.append(f"去重行占比仅 {unique_ratio:.0%}，重复内容多，注水嫌疑")

    if numbers >= 0.08:
        score += 3
        reasons.append(f"含数字的行占 {numbers:.0%}，有具体依据")
    elif numbers >= 0.03:
        score += 1
    else:
        reasons.append(f"含数字的行仅 {numbers:.0%}，几乎没有具体依据")

    if headings >= 5:
        score += 2
        reasons.append(f"有 {headings} 个章节标题，结构清晰")
    elif headings == 0:
        reasons.append("无章节结构，出处定位会困难")

    if 20 <= avg_line <= 120:
        score += 2
    elif avg_line < 12:
        reasons.append(f"平均行长仅 {avg_line:.0f} 字，可能是碎片或对话稿")

    if meta.get("is_scanned"):
        reasons.append("扫描件，出处精度打折")
    if meta.get("ocr_ratio", 0) and meta["ocr_ratio"] > 0.5:
        reasons.append(f"OCR 占比 {meta['ocr_ratio']:.0%}，转写可能有误")

    if meta.get("char_count", 0) < MIN_CHARS_TO_DISTILL:
        return {
            "score": score,
            "verdict": "不可蒸",
            "reasons": reasons + [f"全文仅 {meta.get('char_count', 0)} 字，材料太短，蒸不出东西"],
        }

    verdict = "可蒸" if score >= 6 else ("勉强可蒸" if score >= 4 else "不可蒸")
    if verdict == "不可蒸" and not any("太短" in r for r in reasons):
        reasons.append("信息密度不足，蒸出来会是一堆正确的废话")
    return {"score": score, "verdict": verdict, "reasons": reasons}


def classify(body: str) -> tuple[dict[str, int], str, float]:
    """返回 (各类得分, 头名, 头名领先幅度)。"""
    sample = body[:200_000]
    scores: dict[str, int] = {}
    for type_name, markers in TYPE_MARKERS.items():
        total = 0
        for pattern, weight in markers:
            total += len(re.findall(pattern, sample, re.IGNORECASE)) * weight
        scores[type_name] = total

    # 按每万字归一。不归一的话，篇幅本身就能决定胜负。
    per_10k = max(len(sample), 1) / 10_000
    scores = {key: round(value / per_10k, 2) for key, value in scores.items()}

    ranked = sorted(scores.values(), reverse=True)
    top = ranked[0] if ranked else 0
    second = ranked[1] if len(ranked) > 1 else 0
    margin = (top - second) / top if top else 0.0
    best = max(scores, key=lambda key: scores[key]) if top else ""
    return scores, best, margin


def probe(work: Path) -> dict:
    source = work / "source.md"
    if not source.is_file():
        raise SystemExit(f"缺 {source}。先跑 ingest.py。")

    body = source.read_text(encoding="utf-8")
    meta_path = work / "source.meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.is_file() else {}

    scores, best, margin = classify(body)
    distillability = assess_distillability(body, meta)
    need_user = margin < CONFIDENCE_MARGIN or best == ""

    result = {
        "work": str(work),
        "title": meta.get("title", ""),
        "char_count": meta.get("char_count", len(body)),
        "detected_type": best,
        "type_label": TYPE_LABELS.get(best, "无法判定"),
        "type_scores": scores,
        "confidence_margin": round(margin, 3),
        "need_user_confirmation": need_user,
        "agent_must_verify": True,
        "distillability": distillability,
        "probed_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    }

    # 关键词启发式只作弱先验。实测会把《富爸爸穷爸爸》误判成工具书，
    # 所以类型必须由真正读过文本的一方拍板，不能直接采信这里的结果。
    result["verify_hint"] = " | ".join([
        "先读 source.md 的目录与前两章，再用下面两条判断，最后决定读哪个 references：",
        "· 有可执行的分步操作、清单、判据 -> 工具书",
        "· 通篇是立场、取舍、反复出现的判断倾向，说不清「学会了什么」-> 非工具书",
        f"启发式倾向：{TYPE_LABELS.get(best, '无法判定')}（仅供参考，可推翻）",
    ])
    if distillability["verdict"] == "不可蒸":
        result["action"] = "可蒸性不达标，向用户说明理由并早退，不要硬蒸。"
    elif need_user:
        result["action"] = "类型置信度不足，先读 source.md 再用上面两条判断，必要时问用户。"
    else:
        result["action"] = f"读 source.md 复核类型；若确认是{best}，读 references/{best}.md 按协议抽取。"

    (work / "classification.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="判定材料类型与可蒸性")
    parser.add_argument("--work", required=True, help="工作目录")
    args = parser.parse_args()

    result = probe(Path(args.work).expanduser())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\n>>> {result['action']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
