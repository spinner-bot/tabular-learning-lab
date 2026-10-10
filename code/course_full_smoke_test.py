"""Browser smoke test for the integrated course page."""

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
    records: dict[str, object] = {}
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(executable_path=str(edge), headless=True, args=["--disable-gpu", "--no-sandbox"])
            for width, height, label in ((1440, 900, "desktop"), (390, 844, "mobile")):
                page = browser.new_page(viewport={"width": width, "height": height}, reduced_motion="reduce")
                errors: list[str] = []
                page.on("pageerror", lambda exc: errors.append(str(exc)))
                page.goto(f"http://127.0.0.1:{server.server_port}/course_full.html", wait_until="networkidle")
                assert page.locator("article.full-lesson").count() == 30
                assert page.locator("#course-cover").count() == 1
                assert page.locator("#course-toc").count() == 1
                assert page.locator("#course-conclusion").count() == 1
                page.locator('a[href="#lesson-23"]').first.click()
                page.wait_for_timeout(100)
                assert page.locator("#lesson-23").bounding_box()["y"] < height * 2
                page.locator("#lesson-01-task-demo").select_option("regression")
                assert "回归" in page.locator("#lesson-01-task-result").inner_text()
                page.locator("#lesson-03-threshold-demo").evaluate("(el) => { el.value = '0.8'; el.dispatchEvent(new Event('input', {bubbles:true})); }")
                assert "TP=" in page.locator("#lesson-03-threshold-result").inner_text()
                page.locator("#lesson-05-depth").fill("3")
                assert "3" in page.locator("#lesson-05-demoText").inner_text()
                page.locator("details.quiz").first.locator("summary").click()
                assert page.locator("details.quiz").first.get_attribute("open") is not None
                assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
                assert not errors, errors
                records[label] = {"width": width, "articles": 30, "horizontal_overflow": False, "page_errors": errors}
                page.close()
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    report = ROOT / "reports" / "course_full_smoke_2026-10-10.json"
    report.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print("course full smoke test: PASS (30 lessons, anchors, 4 interactions, desktop/mobile overflow)")


if __name__ == "__main__":
    main()
