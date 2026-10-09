"""Capture every lesson at desktop and mobile viewports for visual review."""

from __future__ import annotations

import functools
import json
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "reports" / "browser_artifacts" / "course_visual_2026-10-10"
REPORT = ROOT / "reports" / "course_visual_capture_2026-10-10.json"
EDGE_CANDIDATES = (
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
)


class QuietHandler(SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return
        super().do_GET()

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> None:
    edge = next((path for path in EDGE_CANDIDATES if path.exists()), None)
    if edge is None:
        raise RuntimeError("Microsoft Edge executable not found")
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
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
            for viewport_name, viewport in (("desktop", {"width": 1440, "height": 1000}), ("mobile", {"width": 390, "height": 844})):
                context = browser.new_context(viewport=viewport, reduced_motion="reduce")
                page = context.new_page()
                for lesson in sorted((ROOT / "lessons").glob("*.html")):
                    console_errors: list[str] = []
                    page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)
                    page.goto(f"{base_url}/lessons/{lesson.name}", wait_until="networkidle")
                    output = ARTIFACTS / f"{lesson.stem}_{viewport_name}.png"
                    page.screenshot(path=str(output), full_page=True)
                    records.append(
                        {
                            "page": lesson.name,
                            "viewport": viewport_name,
                            "width": viewport["width"],
                            "height": viewport["height"],
                            "scroll_width": page.evaluate("document.documentElement.scrollWidth"),
                            "scroll_height": page.evaluate("document.documentElement.scrollHeight"),
                            "console_errors": console_errors,
                            "screenshot": str(output.relative_to(ROOT)),
                        }
                    )
                context.close()
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    REPORT.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"course visual capture: PASS ({len(records)} screenshots, output={REPORT.relative_to(ROOT)})")


if __name__ == "__main__":
    main()
