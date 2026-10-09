"""Requirement-oriented audit for the 30 lesson HTML files."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AuditParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []
        self.text: list[str] = []
        self.hrefs: list[str] = []
        self.meta_names: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append(tag)
        values = dict(attrs)
        if tag == "meta" and values.get("name"):
            self.meta_names.add(values["name"])
        if values.get("href"):
            self.hrefs.append(values["href"] or "")

    def handle_data(self, data: str) -> None:
        self.text.append(data)


def main() -> None:
    lessons = sorted((ROOT / "lessons").glob("*.html"))
    errors: list[str] = []
    warnings: list[str] = []
    for page in lessons:
        parser = AuditParser()
        parser.feed(page.read_text(encoding="utf-8"))
        content = " ".join(parser.text)
        required = {
            "h1": parser.tags.count("h1") == 1,
            "viewport": "viewport" in parser.meta_names,
            "svg_or_canvas": "svg" in parser.tags or "canvas" in parser.tags,
            "code_or_operation": "pre" in parser.tags or "svg" in parser.tags or "canvas" in parser.tags,
            "five_quizzes": parser.tags.count("details") >= 5,
            "navigation": "nav" in parser.tags,
            "misconceptions": "易错点" in content or "误区" in content,
            "sources": "来源" in content,
        }
        for name, passed in required.items():
            if not passed:
                errors.append(f"{page.name}: missing {name}")
        for href in parser.hrefs:
            if not href or href.startswith("#") or "://" in href or href.startswith("mailto:"):
                continue
            target = (page.parent / href.split("#", 1)[0]).resolve()
            if not target.exists():
                errors.append(f"{page.name}: broken local link {href}")
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    linked = sum(f"lessons/{p.name}" in index for p in lessons)
    if linked != 30:
        errors.append(f"index.html links {linked}/30 lesson files")
    if warnings:
        for warning in warnings:
            print("WARNING:", warning)
    if errors:
        for error in errors:
            print("ERROR:", error)
        raise SystemExit(1)
    print(f"lesson audit: PASS ({len(lessons)} lessons, index links {linked}/30)")


if __name__ == "__main__":
    main()
