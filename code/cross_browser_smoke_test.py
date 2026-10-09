"""Run a lightweight course smoke test in Playwright Chromium, Firefox, and WebKit."""

from __future__ import annotations

import functools
import json
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import BrowserType, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "cross_browser_smoke_2026-10-10.json"
SUMMARY = ROOT / "reports" / "cross_browser_smoke_2026-10-10.md"


class QuietHandler(SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return
        super().do_GET()

    def log_message(self, format: str, *args: object) -> None:
        return


def run_engine(name: str, browser_type: BrowserType, base_url: str) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    browser = browser_type.launch(headless=True)
    try:
        for viewport_name, viewport in (
            ("desktop", {"width": 1440, "height": 1000}),
            ("mobile", {"width": 390, "height": 844}),
        ):
            context = browser.new_context(viewport=viewport, reduced_motion="reduce")
            try:
                for lesson in sorted((ROOT / "lessons").glob("*.html")):
                    errors: list[str] = []
                    page = context.new_page()
                    page.on(
                        "console",
                        lambda message: errors.append(message.text)
                        if message.type == "error"
                        else None,
                    )
                    page.goto(f"{base_url}/lessons/{lesson.name}", wait_until="networkidle")
                    scroll_width = int(page.evaluate("document.documentElement.scrollWidth"))
                    h1_count = int(page.locator("h1").count())
                    records.append(
                        {
                            "engine": name,
                            "viewport": viewport_name,
                            "page": lesson.name,
                            "scroll_width": scroll_width,
                            "viewport_width": viewport["width"],
                            "horizontal_overflow": scroll_width > viewport["width"],
                            "h1_count": h1_count,
                            "console_errors": errors,
                        }
                    )
                    page.close()
            finally:
                context.close()
    finally:
        browser.close()
    return records


def main() -> None:
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_port}"
    records: list[dict[str, object]] = []
    engine_errors: dict[str, str] = {}
    try:
        with sync_playwright() as playwright:
            for name, browser_type in (
                ("chromium", playwright.chromium),
                ("firefox", playwright.firefox),
                ("webkit", playwright.webkit),
            ):
                try:
                    records.extend(run_engine(name, browser_type, base_url))
                except Exception as error:  # preserve missing-browser evidence
                    engine_errors[name] = str(error)
    finally:
        server.shutdown()
        server.server_close()
    REPORT.write_text(
        json.dumps(
            {
                "expected_engines": ["chromium", "firefox", "webkit"],
                "records": records,
                "engine_errors": engine_errors,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    failures = [
        row
        for row in records
        if row["horizontal_overflow"] or row["h1_count"] != 1 or row["console_errors"]
    ]
    engines = sorted({str(row["engine"]) for row in records})
    status = "PASS" if not failures and not engine_errors else "PARTIAL" if not failures else "FAIL"
    SUMMARY.write_text(
        "# 跨浏览器自动 smoke test（2026-10-10）\n\n"
        f"- 状态：{status}\n"
        f"- 可运行引擎：{', '.join(engines) or '无'}\n"
        f"- 页面路径：{len(records)}/180 条（30 节 × 3 引擎 × 桌面/移动）\n"
        f"- 失败记录：{len(failures)}\n\n"
        f"- 缺失/启动失败引擎：{', '.join(engine_errors) or '无'}\n\n"
        "该记录是 Playwright 自动化兼容性证据，不替代真实屏幕阅读器语音审查或人工逐像素视觉检查。\n",
        encoding="utf-8",
    )
    if failures:
        raise SystemExit(f"cross-browser smoke test: FAIL ({len(failures)} failures)")
    print(f"cross-browser smoke test: {status} ({len(records)} records, engines={','.join(engines)})")


if __name__ == "__main__":
    main()
