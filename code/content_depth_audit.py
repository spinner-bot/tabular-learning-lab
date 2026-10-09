"""Audit the minimum teaching structure against lesson plans."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Parser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []
        self.text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append(tag)

    def handle_data(self, data: str) -> None:
        self.text.append(data)


def main() -> None:
    errors: list[str] = []
    for number in range(1, 31):
        key = f"{number:02d}"
        page_path = next((ROOT / "lessons").glob(f"{key}_*.html"))
        plan_path = ROOT / "lesson_plans" / f"lesson_{key}_plan.md"
        parser = Parser()
        parser.feed(page_path.read_text(encoding="utf-8"))
        content = " ".join(parser.text)
        plan = plan_path.read_text(encoding="utf-8")
        page_requirements = {
            "学习目标": "学习目标" in content,
            "机制/讲解": len([tag for tag in parser.tags if tag == "h2"]) >= 6,
            "误区": "误区" in content or "易错点" in content,
            "自测": parser.tags.count("details") >= 5,
            "来源": "来源" in content,
            "闭环": "下一节" in content or "课程终点" in content,
        }
        plan_requirements = {
            "目标": "学习目标：" in plan,
            "核心问题": "核心问题：" in plan,
            "知识点": "知识点：" in plan,
            "案例": "案例：" in plan,
            "代码": "代码：" in plan,
            "自测": "自测：" in plan,
            "来源": "来源：" in plan,
        }
        for name, passed in page_requirements.items():
            if not passed:
                errors.append(f"{page_path.name}: page missing {name}")
        for name, passed in plan_requirements.items():
            if not passed:
                errors.append(f"{plan_path.name}: plan missing {name}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("content depth audit: PASS (30 pages and plans meet minimum structure)")


if __name__ == "__main__":
    main()
