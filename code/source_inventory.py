"""Build a reproducible inventory of sources cited by all lesson pages.

This is an evidence inventory, not a semantic fact checker: URL reachability
and claim-by-claim correctness are tracked by separate reports.
"""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.hrefs.append(href)


def classify(href: str) -> str:
    if href.startswith("http://") or href.startswith("https://"):
        host = urlparse(href).netloc
        return f"external ({host})"
    return "local"


def main() -> None:
    lessons = sorted((ROOT / "lessons").glob("*.html"))
    lines = [
        "# 逐课来源清单（2026-10-10）",
        "",
        "本清单由 `code/source_inventory.py` 生成。它只记录课件链接结构，不判断链接内容是否逐句支持主张；可达性见 `reports/external_link_validation.md`，事实核验见 `research/fact_check_matrix.md`。",
        "",
        "| 课件 | 外部来源数 | 本地来源数 | 外部来源 |",
        "|---|---:|---:|---|",
    ]
    total_external = 0
    total_local = 0
    errors: list[str] = []
    for page in lessons:
        parser = LinkParser()
        parser.feed(page.read_text(encoding="utf-8"))
        external = [h for h in parser.hrefs if classify(h).startswith("external")]
        local = [h for h in parser.hrefs if classify(h) == "local" and not h.startswith("#")]
        total_external += len(external)
        total_local += len(local)
        if not external:
            errors.append(f"{page.name}: no external source")
        rendered = "<br>".join(f"`{h}`" for h in external) or "—"
        lines.append(f"| `{page.name}` | {len(external)} | {len(local)} | {rendered} |")
    lines.extend([
        "",
        f"合计：{len(lessons)} 个课件，{total_external} 个外部链接，{total_local} 个本地链接。",
        "",
        "## 判定",
        "",
        "- 结构门禁：每个课件至少含一个外部来源：" + ("通过。" if not errors else "未通过。"),
        "- 语义事实、链接可达性、版本日期和运行实测不由本脚本代替。",
    ])
    if errors:
        lines.extend(["", "## 错误", "", *[f"- {error}" for error in errors]])
        raise SystemExit("source inventory failed: " + "; ".join(errors))
    report = ROOT / "reports" / "lesson_source_inventory_2026-10-10.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"source inventory: PASS ({len(lessons)} lessons, {total_external} external, {total_local} local links)")


if __name__ == "__main__":
    main()
