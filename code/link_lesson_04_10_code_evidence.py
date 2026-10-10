"""Link shared executable evidence from lessons 04 and 06-10."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    ("lessons/04_bias_variance.html", "<h2>4."),
    ("lessons/06_tree_splits.html", "<h2>4."),
    ("lessons/07_random_forest.html", "<h2>3."),
    ("lessons/08_gbdt.html", "<h2>3."),
    ("lessons/09_xgboost.html", "<h2>3."),
    ("lessons/10_catboost.html", "<h2>3."),
]
EVIDENCE = (
    ' 共享代码路径已执行，逐项记录见 '
    '<a href="../reports/lesson_04_10_code_examples_2026-10-10.md">'
    '04、06–10 节代码验证报告</a>；这不等于统一调参 benchmark。'
)


def main() -> None:
    for relative, section_heading in PAGES:
        path = ROOT / relative
        source = path.read_text(encoding="utf-8")
        if "lesson_04_10_code_examples_2026-10-10.md" in source:
            continue
        source = source.replace("代码示例（未执行）", "代码示例与运行证据", 1)
        start = source.index(section_heading)
        marker = '<p class="meta">'
        position = source.index(marker, start) + len(marker)
        source = source[:position] + EVIDENCE + source[position:]
        path.write_text(source, encoding="utf-8", newline="")
    print("linked lesson 04/06-10 code evidence")


if __name__ == "__main__":
    main()
