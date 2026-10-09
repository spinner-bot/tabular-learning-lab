"""Inspect Chromium's accessibility tree for the entry page and sample lesson."""

from __future__ import annotations

import functools
import json
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
OUTPUT = ROOT / "reports" / "accessibility_ax_tree.json"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return


def node_names(tree: dict[str, object]) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    for node in tree.get("nodes", []):
        role = node.get("role", {}).get("value", "")
        name = node.get("name", {}).get("value", "")
        if role or name:
            result.append((str(role), str(name)))
    return result


def require_named(nodes: list[tuple[str, str]], role: str, name_part: str) -> None:
    if not any(node_role == role and name_part in name for node_role, name in nodes):
        raise AssertionError(f"missing accessible {role} named {name_part!r}")


def main() -> None:
    if not EDGE.exists():
        raise RuntimeError("Microsoft Edge executable not found")
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_port}"
    snapshots: dict[str, list[tuple[str, str]]] = {}
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(executable_path=str(EDGE), headless=True, args=["--disable-gpu"])
            page = browser.new_page()
            page.goto(f"{base_url}/index.html", wait_until="networkidle")
            session = page.context.new_cdp_session(page)
            index_nodes = node_names(session.send("Accessibility.getFullAXTree"))
            require_named(index_nodes, "heading", "从表格数据到可复现研究")
            require_named(index_nodes, "link", "表格学习是什么")
            snapshots["index"] = index_nodes
            page.goto(f"{base_url}/lessons/05_decision_trees.html", wait_until="networkidle")
            lesson_nodes = node_names(session.send("Accessibility.getFullAXTree"))
            require_named(lesson_nodes, "slider", "树深度")
            require_named(lesson_nodes, "slider", "面积阈值")
            require_named(lesson_nodes, "button", "复制代码")
            require_named(lesson_nodes, "Canvas", "二维模拟数据的决策区域图")
            snapshots["lesson_05"] = lesson_nodes
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    OUTPUT.write_text(json.dumps(snapshots, ensure_ascii=False, indent=2), encoding="utf-8")
    print("AX tree audit: PASS (entry and sample lesson named controls verified)")


if __name__ == "__main__":
    main()
