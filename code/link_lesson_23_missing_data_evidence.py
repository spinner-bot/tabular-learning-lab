"""Link the Rubin missing-data source and boundary note from lesson 23."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "lessons" / "23_data_processing.html"
LINK = (
    ' 本节预处理代码的实际运行记录见 '
    '<a href="../reports/lesson_23_preprocessing_example_2026-10-10.md">'
    '第 23 节代码验证报告</a>；该记录不等于 TabPFN 或生产 benchmark。'
)


def main() -> None:
    source = PAGE.read_text(encoding="utf-8")
    if "lesson_23_preprocessing_example_2026-10-10.md" not in source:
        start = source.index("<h2>1.")
        marker = "</section>"
        position = source.index(marker, start)
        source = source[:position] + f"<p class=\"meta\">{LINK}</p>" + source[position:]
    source = source.replace(
        "<h2>3. 代码示例（未执行）</h2>",
        "<h2>3. 代码示例与运行证据</h2>",
    ).replace(
        "<p class=\"meta\">应在交叉验证管道内拟合预处理。</p>",
        "<p class=\"meta\">应在交叉验证管道内拟合预处理；教学规模运行结果见上方验证报告。</p>",
    )
    PAGE.write_text(source, encoding="utf-8", newline="")
    print("linked Rubin missing-data evidence")


if __name__ == "__main__":
    main()
