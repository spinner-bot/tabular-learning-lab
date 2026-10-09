"""Audit named headings and interactive roles in every lesson's Edge AX tree."""

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
OUTPUT = ROOT / "reports" / "ax_tree_course_audit_2026-10-10.json"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return


def read_nodes(tree: dict[str, object]) -> list[tuple[str, str]]:
    nodes: list[tuple[str, str]] = []
    for node in tree.get("nodes", []):
        role = str(node.get("role", {}).get("value", ""))
        name = str(node.get("name", {}).get("value", ""))
        if role or name:
            nodes.append((role, name))
    return nodes


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
            page = browser.new_page()
            session = page.context.new_cdp_session(page)
            for path in sorted((ROOT / "lessons").glob("*.html")):
                page.goto(f"{base_url}/lessons/{path.name}", wait_until="networkidle")
                nodes = read_nodes(session.send("Accessibility.getFullAXTree"))
                interactive_roles = {"button", "checkbox", "combobox", "link", "radio", "slider", "spinbutton", "textbox"}
                interactive = [
                    {"role": role, "name": name}
                    for role, name in nodes
                    if role in interactive_roles
                ]
                unnamed = [item for item in interactive if not item["name"].strip()]
                headings = [name for role, name in nodes if role == "heading" and name.strip()]
                assert headings, f"no named heading: {path.name}"
                assert not unnamed, f"unnamed interactive nodes in {path.name}: {unnamed}"
                records.append(
                    {
                        "page": path.name,
                        "named_heading_count": len(headings),
                        "interactive_count": len(interactive),
                        "unnamed_interactive_count": len(unnamed),
                        "interactive_roles": interactive,
                    }
                )
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    OUTPUT.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"course AX tree audit: PASS ({len(records)} lessons, output={OUTPUT.relative_to(ROOT)})")


if __name__ == "__main__":
    raise SystemExit(main())
