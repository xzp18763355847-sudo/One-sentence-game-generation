#!/usr/bin/env python3
"""
将 Excel/TSV 表格内容格式化为 prompt_builder.py 中 OFFCIAL_GAME_PROMPT 的条目格式。

默认按 scripts.xlsx 的列格式读取 .xlsx；TSV 使用 --format tsv 或仅支持无表头时的列顺序。

用法:
  python excel_to_prompt_format.py scripts.xlsx
  python excel_to_prompt_format.py scripts.xlsx -o out.txt --start-id 3
  python excel_to_prompt_format.py data.tsv --format tsv --no-header

scripts.xlsx 列布局（与项目内 scripts.xlsx 一致，0-based 列索引）:
  0: 分类(不参与输出)  1: 剧本名称(中文)  2: 剧本名称(英文)
  3: 欢迎语/游戏规则/游戏简介(中文)  4: (英文)
  5: 故事背景/开场(中文)  6: (英文)
  7: 角色设定/角色卡(中文)  8: (英文)
  9: 规则补充(中文)  10: (英文)
  11,12: 预填回复(不写入)  13: 故事背景和人物设定修改(不写入)
  14: 扮演NPC名称(role)  15: 玩法(type)
"""

import argparse
import csv
import sys
from pathlib import Path

# scripts.xlsx 列索引（0-based，与 Excel 第 A 列=0 对应）
COLS_XLSX = {
    "name_cn": 1,
    "name_en": 2,
    "rule_cn": 3,
    "rule_en": 4,
    "background_cn": 5,
    "background_en": 6,
    "role_setting_cn": 7,
    "role_setting_en": 8,
    "rule_extra_cn": 9,
    "rule_extra_en": 10,
    "role": 14,
    "type": 15,
}

# TSV 无表头时的列顺序（0-based）
COLS_TSV = {
    "name_cn": 0,
    "name_en": 1,
    "rule_cn": 2,
    "rule_en": 3,
    "background_cn": 4,
    "background_en": 5,
    "role_setting_cn": 6,
    "role_setting_en": 7,
    "rule_extra_cn": 8,
    "rule_extra_en": 9,
    "role": 13,
    "type": 14,
}


def _strip(s: str) -> str:
    if s is None:
        return ""
    return str(s).strip().strip('"').strip("'")


def _escape(s: str) -> str:
    """用于 Python 源码中的字符串：保留三引号块内的换行与引号转义。"""
    if not s:
        return '""'
    # 三引号块内只需转义 """ 为 \"""
    if "\n" in s or '"""' in s:
        return '"""' + s.replace("\\", "\\\\").replace('"""', r'\"\"\"') + '"""'
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def row_to_entry(row: list, entry_id: str, cols: dict[str, int]) -> dict:
    """将一行（列表）转为 OFFCIAL_GAME_PROMPT 单条目的结构。cols 为列名到 0-based 索引的映射。"""
    def col(key: str) -> str:
        i = cols.get(key, -1)
        return _strip(row[i]) if 0 <= i < len(row) else ""

    name_cn = col("name_cn")
    name_en = col("name_en")
    type_val = col("type") or "story_based"
    role = col("role") or ""

    return {
        entry_id: {
            "cn": {
                "name": name_cn,
                "type": type_val,
                "rule": col("rule_cn"),
                "rule_extra": col("rule_extra_cn"),
                "background": col("background_cn"),
                "role": role,
                "role_setting": col("role_setting_cn"),
            },
            "en": {
                "name": name_en,
                "type": type_val,
                "rule": col("rule_en"),
                "rule_extra": col("rule_extra_en"),
                "background": col("background_en"),
                "role": role,
                "role_setting": col("role_setting_en"),
            },
        }
    }


def format_entry_python(entry: dict, indent: str = "    ") -> str:
    """将单条条目格式化为可粘贴到 prompt_builder.py 的 Python 源码。"""
    lines = []
    (entry_id, body) = next(iter(entry.items()))
    lines.append(f'{indent}"{entry_id}"' + ": {")
    for lang in ("cn", "en"):
        lines.append(f'{indent}    "{lang}"' + ": {")
        for key in ("name", "type", "rule", "rule_extra", "background", "role", "role_setting"):
            val = body[lang].get(key, "")
            lines.append(f'{indent}        "{key}": {_escape(val)},')
        lines.append(f'{indent}    }},')
    lines.append(f'{indent}}},')
    return "\n".join(lines)


def read_tsv(path: Path) -> list[list]:
    """读取 TSV；支持 Excel 导出的带引号、含换行的字段。"""
    rows = []
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            row = ["" if c is None else str(c).strip().strip('"') for c in row]
            if any(row):
                rows.append(row)
    return rows


def read_xlsx(path: Path) -> list[list]:
    """读取 xlsx 第一个 sheet 的所有行。"""
    try:
        import openpyxl
    except ImportError:
        raise SystemExit("读取 Excel 需要: pip install openpyxl")
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    rows = []
    for row in ws.iter_rows(values_only=True):
        row = ["" if v is None else str(v).strip() for v in row]
        if any(row):
            rows.append(row)
    wb.close()
    return rows


def main():
    parser = argparse.ArgumentParser(description="将 Excel/TSV 转为 OFFCIAL_GAME_PROMPT 格式（默认按 scripts.xlsx 列布局读 xlsx）")
    parser.add_argument("input", type=Path, help="输入文件，如 scripts.xlsx 或 .tsv")
    parser.add_argument("--id-prefix", default="og", help="条目 ID 前缀，如 og")
    parser.add_argument("--start-id", type=int, default=1, help="起始编号")
    parser.add_argument("--no-header", action="store_true", help="TSV 时：无表头，第一行即为数据；xlsx 时忽略（始终视首行为表头）")
    parser.add_argument("--format", choices=("auto", "tsv", "xlsx"), default="auto", help="列布局：auto 按扩展名，tsv/xlsx 强制指定")
    parser.add_argument("-o", "--output", type=Path, help="写入文件；不指定则打印到 stdout")
    args = parser.parse_args()

    path = args.input
    if not path.exists():
        print(f"文件不存在: {path}", file=sys.stderr)
        sys.exit(1)

    suffix = path.suffix.lower()
    if suffix in (".xlsx", ".xls"):
        rows = read_xlsx(path)
        cols = COLS_XLSX
        has_header = True  # scripts.xlsx 首行为表头
    elif suffix == ".tsv" or suffix == ".txt":
        rows = read_tsv(path)
        fmt = args.format
        if fmt == "xlsx":
            cols = COLS_XLSX
        else:
            cols = COLS_TSV
        has_header = not args.no_header
    else:
        print("仅支持 .tsv / .txt / .xlsx", file=sys.stderr)
        sys.exit(1)

    if not rows:
        print("没有数据行", file=sys.stderr)
        sys.exit(1)

    start = 0 if (not has_header) else 1
    data_rows = rows[start:]

    out_lines = []
    for i, row in enumerate(data_rows):
        num = args.start_id + i
        entry_id = f"{args.id_prefix}{num:03d}"
        entry = row_to_entry(row, entry_id, cols)
        out_lines.append(format_entry_python(entry))

    result = "\n".join(out_lines)
    if args.output:
        args.output.write_text(result, encoding="utf-8")
        print(f"已写入: {args.output}", file=sys.stderr)
    else:
        try:
            if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
                sys.stdout.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass
        print(result)


if __name__ == "__main__":
    main()
