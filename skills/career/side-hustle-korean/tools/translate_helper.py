"""
韩语翻译接单效率工具
功能: 字数统计 + 报价计算 + 格式转换 + 批量处理
用法: python translate_helper.py
"""
import re
import os
import sys
from pathlib import Path

# === 配置 ===
OUTPUT_DIR = r"E:\claude code生成文件"
PRICING = {
    "ko_to_zh": 50,   # 韩→中: 50元/千字
    "zh_to_ko": 80,   # 中→韩: 80元/千字
    "rush_fee": 1.5,  # 急单加50%
}

def count_chars(text):
    """统计中韩文字数(去掉空格和标点)"""
    # 韩文 + 中文 + 英文单词
    korean = len(re.findall(r'[가-힣]', text))
    chinese = len(re.findall(r'[一-鿿]', text))
    english_words = len(re.findall(r'[a-zA-Z]+', text))
    return korean + chinese + english_words

def count_chars_file(filepath):
    """统计文件字数"""
    path = Path(filepath)
    if not path.exists():
        return f"文件不存在: {filepath}"

    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    chars = count_chars(text)
    return {
        "file": path.name,
        "chars": chars,
        "ko_chars": len(re.findall(r'[가-힣]', text)),
        "zh_chars": len(re.findall(r'[一-鿿]', text)),
    }

def quote_price(chars, direction="ko_to_zh", rush=False):
    """计算报价"""
    rate = PRICING[direction]
    base = max(30, round(chars / 1000 * rate))  # 最低30元
    total = base * PRICING["rush_fee"] if rush else base
    return {
        "base_price": base,
        "rush": rush,
        "total": total,
        "estimate_time": f"{max(0.5, chars/500):.1f}小时",
    }

def batch_translate_prep(input_dir):
    """批量翻译预处理: 生成翻译包"""
    input_path = Path(input_dir)
    files = list(input_path.glob("*.txt")) + list(input_path.glob("*.md"))

    report = []
    total_chars = 0

    for f in files:
        info = count_chars_file(str(f))
        total_chars += info["chars"]
        report.append(f"  {info['file']}: {info['chars']}字 "
                      f"(韩{info['ko_chars']}/中{info['zh_chars']})")

    print(f"\n[翻译批次统计]")
    print(f"文件数: {len(files)}")
    print(f"总字数: {total_chars}")
    print(f"预估报价: {quote_price(total_chars)['total']}元")
    print(f"\n明细:")
    for r in report:
        print(r)

    return {"files": len(files), "total_chars": total_chars}

def format_bilingual(ko_text, zh_text):
    """生成双语对照文档"""
    ko_lines = ko_text.strip().split('\n')
    zh_lines = zh_text.strip().split('\n')

    output = []
    output.append("# 韩中双语对照\n")
    output.append("| 韩语 | 中文 |")
    output.append("|------|------|")

    max_lines = max(len(ko_lines), len(zh_lines))
    for i in range(max_lines):
        ko = ko_lines[i].strip() if i < len(ko_lines) else ""
        zh = zh_lines[i].strip() if i < len(zh_lines) else ""
        if ko or zh:
            output.append(f"| {ko} | {zh} |")

    return '\n'.join(output)

# === CLI ===
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="韩语翻译效率工具")
    sub = parser.add_subparsers(dest="cmd")

    # count
    p_count = sub.add_parser("count", help="统计文件字数")
    p_count.add_argument("file", help="文件路径")

    # quote
    p_quote = sub.add_parser("quote", help="报价")
    p_quote.add_argument("chars", type=int, help="字数")
    p_quote.add_argument("--direction", default="ko_to_zh",
                         choices=["ko_to_zh", "zh_to_ko"])
    p_quote.add_argument("--rush", action="store_true", help="急单")

    # batch
    p_batch = sub.add_parser("batch", help="批量统计目录")
    p_batch.add_argument("dir", help="目录路径")

    # bilingual
    p_bi = sub.add_parser("bilingual", help="生成双语对照")
    p_bi.add_argument("--ko", required=True, help="韩语文件")
    p_bi.add_argument("--zh", required=True, help="中文文件")
    p_bi.add_argument("--output", help="输出文件路径")

    args = parser.parse_args()

    if args.cmd == "count":
        result = count_chars_file(args.file)
        if isinstance(result, str):
            print(result)
        else:
            print(f"文件: {result['file']}")
            print(f"总字数: {result['chars']}")
            print(f"  韩文: {result['ko_chars']}")
            print(f"  中文: {result['zh_chars']}")
            q = quote_price(result['chars'])
            print(f"报价: RMB{q['total']} ({'急单' if q['rush'] else '常规'})")

    elif args.cmd == "quote":
        q = quote_price(args.chars, args.direction, args.rush)
        print(f"字数: {args.chars}")
        print(f"基础价: RMB{q['base_price']}")
        print(f"最终价: RMB{q['total']}")
        print(f"预估时间: {q['estimate_time']}")

    elif args.cmd == "batch":
        batch_translate_prep(args.dir)

    elif args.cmd == "bilingual":
        with open(args.ko, 'r', encoding='utf-8') as f:
            ko_text = f.read()
        with open(args.zh, 'r', encoding='utf-8') as f:
            zh_text = f.read()
        result = format_bilingual(ko_text, zh_text)
        output_path = args.output or os.path.join(
            OUTPUT_DIR, f"bilingual_{Path(args.ko).stem}.md")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"双语对照已生成: {output_path}")

    else:
        parser.print_help()
        print("\n[示例]:")
        print("  python translate_helper.py count 韩语文档.txt")
        print("  python translate_helper.py quote 1500 --rush")
        print("  python translate_helper.py batch ./待翻译/")
        print("  python translate_helper.py bilingual --ko ko.txt --zh zh.txt")
