"""Exercise common interactive paths on every lesson in Edge headless."""

from __future__ import annotations

import functools
import json
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
EDGE_CANDIDATES = (
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
)
REPORT = ROOT / "reports" / "browser_interaction_audit_2026-10-10.json"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> None:
    edge = next((path for path in EDGE_CANDIDATES if path.exists()), None)
    if edge is None:
        raise RuntimeError("Microsoft Edge executable not found")
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_port}"
    records: list[dict[str, object]] = []
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                executable_path=str(edge), headless=True, args=["--disable-gpu", "--no-sandbox"]
            )
            context = browser.new_context(
                viewport={"width": 390, "height": 844},
                reduced_motion="reduce",
                permissions=["clipboard-read", "clipboard-write"],
            )
            page = context.new_page()
            for path in sorted((ROOT / "lessons").glob("*.html")):
                console_errors: list[str] = []
                response_errors: list[str] = []
                page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)
                page.on(
                    "response",
                    lambda response: response_errors.append(f"{response.status} {response.url}")
                    if response.status >= 400 and not response.url.endswith("/favicon.ico")
                    else None,
                )
                page.goto(f"{base_url}/lessons/{path.name}", wait_until="networkidle")
                quiz = page.locator("details.quiz")
                quiz_count = quiz.count()
                for index in range(quiz_count):
                    item = quiz.nth(index)
                    item.locator("summary").click()
                    assert item.get_attribute("open") is not None, f"quiz did not open: {path.name}#{index}"
                ranges = page.locator("input[type='range']")
                range_count = ranges.count()
                for index in range(range_count):
                    control = ranges.nth(index)
                    minimum = control.get_attribute("min") or "0"
                    control.fill(minimum)
                    control.press("ArrowRight")
                copies = page.locator("button.copy")
                copy_count = copies.count()
                for index in range(copy_count):
                    copies.nth(index).click()
                canvas_count = page.locator("canvas").count()
                for index in range(canvas_count):
                    box = page.locator("canvas").nth(index).bounding_box()
                    assert box and box["width"] > 0 and box["height"] > 0, f"canvas has no layout: {path.name}"
                scroll_width = page.evaluate("document.documentElement.scrollWidth")
                assert scroll_width <= 390, f"horizontal overflow: {path.name} ({scroll_width})"
                assert not response_errors, f"HTTP resource errors in {path.name}: {response_errors}"
                # Chromium reports the favicon 404 as a console error without its URL;
                # response_errors above is the URL-bearing resource gate.
                records.append(
                    {
                        "page": path.name,
                        "quiz_count": quiz_count,
                        "range_count": range_count,
                        "copy_button_count": copy_count,
                        "canvas_count": canvas_count,
                        "scroll_width": scroll_width,
                        "console_errors": console_errors,
                        "http_errors": response_errors,
                    }
                )
            context.close()
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    REPORT.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"browser interaction audit: PASS ({len(records)} lessons, output={REPORT.relative_to(ROOT)})")


if __name__ == "__main__":
    main()
