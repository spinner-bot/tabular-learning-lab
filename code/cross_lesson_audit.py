"""Cross-check lesson plans and lesson HTML artifacts."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN_RE = re.compile(r"^# 第 (\d{2}) 节计划：(.+)$", re.MULTILINE)
H1_RE = re.compile(r"<h1>(.*?)</h1>", re.DOTALL)


def main() -> None:
    errors: list[str] = []
    plans = sorted((ROOT / "lesson_plans").glob("lesson_*_plan.md"))
    pages = sorted((ROOT / "lessons").glob("*.html"))
    if len(plans) != 30 or len(pages) != 30:
        errors.append(f"expected 30 plans/pages, got {len(plans)}/{len(pages)}")
    for number in range(1, 31):
        key = f"{number:02d}"
        plan_path = ROOT / "lesson_plans" / f"lesson_{key}_plan.md"
        page_path = ROOT / "lessons" / next(
            page.name for page in pages if page.name.startswith(f"{key}_")
        )
        plan = plan_path.read_text(encoding="utf-8")
        page = page_path.read_text(encoding="utf-8")
        match = PLAN_RE.search(plan)
        if not match or match.group(1) != key:
            errors.append(f"{plan_path.name}: invalid plan heading")
        if f"lesson_plans/lesson_{key}_plan.md" not in page:
            errors.append(f"{page_path.name}: missing self plan link")
        if "来源" not in plan:
            errors.append(f"{plan_path.name}: missing source field")
        if "先修" not in page or "后续" not in page:
            errors.append(f"{page_path.name}: missing prerequisite/follow-up metadata")
        if len(H1_RE.findall(page)) != 1:
            errors.append(f"{page_path.name}: expected one h1")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("cross-lesson audit: PASS (30 plans linked to 30 pages)")


if __name__ == "__main__":
    main()
