"""Static HTML structure and local-link checker for the course."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []
        self.meta_names: set[str] = set()
        self.local_links: list[str] = []
        self.external_links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append(tag)
        values = dict(attrs)
        if tag == "meta" and values.get("name"):
            self.meta_names.add(values["name"])
        href = values.get("href")
        if not href:
            return
        parsed = urlparse(href)
        if parsed.scheme or href.startswith("#"):
            self.external_links.append(href)
        else:
            self.local_links.append(href.split("#", 1)[0])


def main() -> None:
    pages = sorted(ROOT.glob("index.html")) + sorted((ROOT / "lessons").glob("*.html"))
    errors: list[str] = []
    total_links = 0
    for page in pages:
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        total_links += len(parser.local_links)
        if "viewport" not in parser.meta_names and page.name != "index.html":
            errors.append(f"{page}: missing viewport meta")
        for link in parser.local_links:
            target = (page.parent / link).resolve()
            if not target.exists():
                errors.append(f"{page}: missing local target {link}")
    if errors:
        for error in errors:
            print("ERROR:", error)
        raise SystemExit(1)
    print(f"HTML structure check: PASS ({len(pages)} pages, {total_links} local links)")


if __name__ == "__main__":
    main()
