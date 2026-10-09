"""Playwright smoke test for page load, interaction, and narrow layout."""

from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
EDGE_CANDIDATES = (
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
)


def main() -> None:
    edge = next((path for path in EDGE_CANDIDATES if path.exists()), None)
    if edge is None:
        raise RuntimeError("Microsoft Edge executable not found")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path=str(edge),
            headless=True,
            args=["--disable-gpu", "--no-sandbox"],
        )
        desktop = browser.new_page(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
        desktop.goto((ROOT / "index.html").as_uri(), wait_until="networkidle")
        assert desktop.locator("a[href^='lessons/']").count() == 30
        assert desktop.locator("h1").inner_text() == "从表格数据到可复现研究"
        artifact_dir = ROOT / "reports" / "browser_artifacts"
        artifact_dir.mkdir(parents=True, exist_ok=True)
        desktop.screenshot(path=str(artifact_dir / "index_desktop.png"), full_page=True)

        lesson = browser.new_page(viewport={"width": 390, "height": 844}, reduced_motion="reduce")
        lesson.goto(
            (ROOT / "lessons" / "05_decision_trees.html").as_uri(),
            wait_until="networkidle",
        )
        assert lesson.locator("#treeCanvas").count() == 1
        lesson.locator("#depth").fill("3")
        assert "深度 3" in lesson.locator("#demoText").inner_text()
        lesson.locator("#depth").focus()
        lesson.keyboard.press("ArrowDown")
        assert lesson.locator("#depthOut").inner_text() == "2"
        assert lesson.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
        assert lesson.locator("details.quiz").count() >= 5
        lesson.screenshot(path=str(artifact_dir / "lesson_05_mobile.png"), full_page=True)

        pages = sorted((ROOT / "lessons").glob("*.html"))
        for page in pages:
            lesson.goto(page.as_uri(), wait_until="networkidle")
            assert lesson.locator("h1").count() == 1, page.name
            assert lesson.evaluate("document.documentElement.scrollWidth <= window.innerWidth"), page.name
        browser.close()
    print("browser smoke test: PASS (30 lessons, keyboard interaction, reduced motion, 390px overflow check)")


if __name__ == "__main__":
    main()
