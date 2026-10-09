"""Link the executable lesson 12/13 evidence without rewriting page content."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = (
    ' 最小可运行路径见 <a href="../code/lesson_12_13_examples.py">'
    'code/lesson_12_13_examples.py</a> 与 <a href="../reports/lesson_12_13_examples_2026-10-10.json">'
    '验证 JSON</a>；这不代表完整训练实验。'
)


def add_link(relative: str) -> None:
    path = ROOT / relative
    source = path.read_text(encoding="utf-8")
    start = source.index("<h2>3.")
    marker = '<p class="meta">'
    position = source.index(marker, start) + len(marker)
    if "lesson_12_13_examples.py" in source:
        return
    path.write_text(source[:position] + EVIDENCE + source[position:], encoding="utf-8", newline="")


def main() -> None:
    add_link("lessons/12_mlp.html")
    add_link("lessons/13_transformer.html")
    print("linked lesson 12/13 executable evidence")


if __name__ == "__main__":
    main()
