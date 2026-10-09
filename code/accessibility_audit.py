"""Static accessibility checks for the course HTML pages."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AccessibilityParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []
        self.ids: set[str] = set()
        self.labels: set[str] = set()
        self.errors: list[str] = []
        self.text_stack: list[list[str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        self.tags.append(tag)
        self.text_stack.append([])
        if values.get("id"):
            self.ids.add(values["id"] or "")
        if tag == "label" and values.get("for"):
            self.labels.add(values["for"] or "")
        if tag == "html" and values.get("lang") != "zh-CN":
            self.errors.append("html lang must be zh-CN")
        if tag in {"canvas", "svg"} and not values.get("aria-label"):
            self.errors.append(f"{tag} missing aria-label")
        if tag == "input":
            input_id = values.get("id")
            if not input_id or (input_id not in self.labels and not values.get("aria-label")):
                self.errors.append("input missing associated label")
        if tag == "img" and not values.get("alt"):
            self.errors.append("img missing alt")

    def handle_data(self, data: str) -> None:
        for bucket in self.text_stack:
            bucket.append(data)

    def handle_endtag(self, tag: str) -> None:
        if not self.text_stack:
            return
        text = "".join(self.text_stack.pop()).strip()
        if tag == "button" and not text:
            self.errors.append("button has no accessible name")
        if tag == "a" and not text:
            self.errors.append("link has no accessible name")
        if self.tags:
            self.tags.pop()


def main() -> None:
    errors: list[str] = []
    pages = sorted((ROOT / "lessons").glob("*.html")) + [ROOT / "index.html"]
    for page in pages:
        parser = AccessibilityParser()
        parser.feed(page.read_text(encoding="utf-8"))
        errors.extend(f"{page.name}: {error}" for error in parser.errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print(f"accessibility audit: PASS ({len(pages)} pages, labels/media/names checked)")


if __name__ == "__main__":
    main()
