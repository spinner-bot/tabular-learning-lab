"""Audit source declarations and evidence boundaries across all lessons.

The audit is deliberately conservative: it enforces source structure, while
recording (rather than hiding) semantic parity and date-sensitive warnings for
manual review.
"""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF_RE = re.compile(r"\bR\d{2}\b")


class Parser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []
        self.text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        href = dict(attrs).get("href")
        if tag == "a" and href:
            self.hrefs.append(href)

    def handle_data(self, data: str) -> None:
        self.text.append(data)


def source_line(plan: str) -> str:
    for line in plan.splitlines():
        if line.startswith("- 来源："):
            return line
    return ""


def main() -> None:
    errors: list[str] = []
    warnings: list[str] = []
    rows: list[str] = []
    pages = sorted((ROOT / "lessons").glob("*.html"))
    if len(pages) != 30:
        errors.append(f"expected 30 pages, got {len(pages)}")
    for number in range(1, 31):
        key = f"{number:02d}"
        page_path = next((ROOT / "lessons").glob(f"{key}_*.html"))
        plan_path = ROOT / "lesson_plans" / f"lesson_{key}_plan.md"
        plan = plan_path.read_text(encoding="utf-8")
        page_raw = page_path.read_text(encoding="utf-8")
        page_parser = Parser()
        page_parser.feed(page_raw)
        page_text = " ".join(page_parser.text)
        plan_sources = sorted(set(REF_RE.findall(source_line(plan))))
        page_refs = sorted(set(REF_RE.findall(page_text)))
        external = [h for h in page_parser.hrefs if h.startswith(("http://", "https://"))]
        local = [h for h in page_parser.hrefs if not h.startswith(("http://", "https://", "#", "mailto:"))]
        if not source_line(plan):
            errors.append(f"{plan_path.name}: missing source declaration")
        if "来源" not in page_text:
            errors.append(f"{page_path.name}: missing source section")
        if not external:
            errors.append(f"{page_path.name}: missing external source")
        if f"lesson_plans/lesson_{key}_plan.md" not in page_raw:
            errors.append(f"{page_path.name}: missing plan link")
        if plan_sources and not (set(plan_sources) & set(page_refs)):
            warnings.append(f"{key}: plan refs {','.join(plan_sources)} are represented by page URLs/local links rather than visible R IDs")
        if number in (20, 21, 22) and "2026-10-10" not in page_text:
            warnings.append(f"{key}: version-sensitive module has no visible 2026-10-10 snapshot marker")
        boundary = any(marker in page_text for marker in ("未执行", "未验证", "未确认", "不能", "不等于"))
        rows.append(
            f"| {key} | {len(plan_sources)} | {len(page_refs)} | {len(external)} | {len(local)} | {'有' if boundary else '未发现'} |"
        )
    warning_lines = [f"- {warning}" for warning in warnings] if warnings else ["- 无。"]
    report = ROOT / "reports" / "citation_consistency_2026-10-10.md"
    report.write_text(
        "\n".join(
            [
                "# 全课程引用一致性审计（2026-10-10）",
                "",
                "本报告由 `code/citation_consistency_audit.py` 生成。它强制检查来源结构和计划链接，并把 R ID 表达差异、版本日期缺失和边界标记作为人工复核提示；它不把字符串存在性当作语义事实通过。",
                "",
                "| 课次 | 计划 R ID | 页面 R ID | 外部链接 | 本地链接 | 有边界提示 |",
                "|---:|---:|---:|---:|---:|---|",
                *rows,
                "",
                f"结构门禁：{'通过' if not errors else '失败'}。警告数：{len(warnings)}。",
                "",
                "## 警告",
                "",
                *warning_lines,
                "",
                "## 范围限制",
                "",
                "逐句主张是否由来源支持、论文与实现是否混写、动态页面是否仍然最新，仍需研究矩阵和人工核读完成。",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print(f"citation consistency: PASS (30 lessons, {len(warnings)} manual-review warnings)")


if __name__ == "__main__":
    main()
