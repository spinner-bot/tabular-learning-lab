"""Playwright smoke test for page load, interaction, and narrow layout."""

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
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    base_url = f"http://127.0.0.1:{server.server_port}"
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                executable_path=str(edge),
                headless=True,
                args=["--disable-gpu", "--no-sandbox"],
            )
            desktop = browser.new_page(
                viewport={"width": 1440, "height": 900}, reduced_motion="reduce"
            )
            desktop.goto(f"{base_url}/index.html", wait_until="networkidle")
            assert desktop.locator("a[href^='lessons/']").count() == 30
            assert desktop.locator("h1").inner_text() == "从表格数据到可复现研究"
            artifact_dir = ROOT / "reports" / "browser_artifacts"
            artifact_dir.mkdir(parents=True, exist_ok=True)
            desktop.screenshot(path=str(artifact_dir / "index_desktop.png"), full_page=True)

            lesson_context = browser.new_context(
                viewport={"width": 390, "height": 844},
                reduced_motion="reduce",
                permissions=["clipboard-read", "clipboard-write"],
            )
            lesson = lesson_context.new_page()
            lesson.goto(f"{base_url}/lessons/05_decision_trees.html", wait_until="networkidle")
            assert lesson.locator("#treeCanvas").count() == 1
            lesson.locator("#depth").fill("3")
            assert "深度 3" in lesson.locator("#demoText").inner_text()
            lesson.locator("#depth").focus()
            lesson.keyboard.press("ArrowDown")
            assert lesson.locator("#depthOut").inner_text() == "2"
            lesson.locator(".copy").click()
            lesson.wait_for_function("document.querySelector('#copyStatus').textContent.length > 0")
            assert lesson.locator("#copyStatus").inner_text() == "代码已复制。"
            assert lesson.evaluate(
                """async () => {
                    const copied = await navigator.clipboard.readText();
                    const expected = document.querySelector('#codeBlock').innerText;
                    return copied.replace(/\\r\\n/g, '\\n') === expected.replace(/\\r\\n/g, '\\n');
                }"""
            )
            assert lesson.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
            assert lesson.locator("details.quiz").count() >= 5
            lesson.screenshot(path=str(artifact_dir / "lesson_05_mobile.png"), full_page=True)

            pages = sorted((ROOT / "lessons").glob("*.html"))
            layout_records: list[dict[str, int | str | bool]] = []
            for page in pages:
                lesson.goto(f"{base_url}/lessons/{page.name}", wait_until="networkidle")
                assert lesson.locator("h1").count() == 1, page.name
                record = lesson.evaluate(
                    """() => ({
                        page: location.pathname.split('/').pop(),
                        title: document.title,
                        h1: document.querySelector('h1').textContent.trim(),
                        viewport_width: window.innerWidth,
                        scroll_width: document.documentElement.scrollWidth,
                        scroll_height: document.documentElement.scrollHeight,
                        horizontal_overflow: document.documentElement.scrollWidth > window.innerWidth
                    })"""
                )
                assert not record["horizontal_overflow"], page.name
                layout_records.append(record)
            (ROOT / "reports" / "browser_full_layout_2026-10-10.json").write_text(
                json.dumps(layout_records, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            lesson_context.close()
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    print("browser smoke test: PASS (30 lessons, keyboard/clipboard interaction, reduced motion, 390px overflow check)")


if __name__ == "__main__":
    main()
