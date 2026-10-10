"""Link executable code evidence from lessons 01 and 02."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    ("lessons/01_tabular_learning_intro.html", "<h2>4."),
    ("lessons/02_ml_workflow.html", "<h2>4."),
]
EVIDENCE = (
    ' 页面片段已执行，逐项记录见 '
    '<a href="../reports/lesson_01_02_code_examples_2026-10-10.md">'
    '01、02 节代码验证报告</a>；这不等于完整数据工作流 benchmark。'
)


def main() -> None:
    for relative, heading in PAGES:
        path = ROOT / relative
        source = path.read_text(encoding="utf-8")
        if "lesson_01_02_code_examples_2026-10-10.md" in source:
            continue
        source = source.replace("代码示例（未执行）", "代码示例与运行证据", 1)
        start = source.index(heading)
        marker = '<p class="meta">'
        position = source.index(marker, start) + len(marker)
        source = source[:position] + EVIDENCE + source[position:]
        path.write_text(source, encoding="utf-8", newline="")
    print("linked lesson 01/02 code evidence")


if __name__ == "__main__":
    main()
