"""Link the completed R04 reading record from lesson 28."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "lessons" / "28_paper_workshop.html"
LINK = (
    ' 已完成的 R04 主张—证据—边界记录见 '
    '<a href="../reports/paper_reading_R04_tabpfn_original_2026-10-10.md">'
    'R04 精读记录</a>；该记录不替代当前 checkpoint 的运行复现。'
)


def main() -> None:
    source = PAGE.read_text(encoding="utf-8")
    if "paper_reading_R04_tabpfn_original_2026-10-10.md" not in source:
        marker = '<p class="meta">'
        start = source.index("<h2>3.")
        position = source.index(marker, start) + len(marker)
        source = source[:position] + LINK + source[position:]
        PAGE.write_text(source, encoding="utf-8", newline="")
    print("linked R04 reading evidence")


if __name__ == "__main__":
    main()
