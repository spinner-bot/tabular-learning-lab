"""Link the Rubin missing-data source and boundary note from lesson 23."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "lessons" / "23_data_processing.html"
LINK = (
    ' 本节 MCAR/MAR/MNAR 的原始来源与边界见 '
    '<a href="https://dash.harvard.edu/entities/publication/73120378-8764-6bd4-e053-0100007fdf3b">'
    'Rubin (1976)</a>；这里采用操作性定义，不把机制假设当作可由观测数据自动证明的事实。'
)


def main() -> None:
    source = PAGE.read_text(encoding="utf-8")
    if "dash.harvard.edu/entities/publication/73120378-8764-6bd4-e053-0100007fdf3b" not in source:
        start = source.index("<h2>1.")
        marker = "</section>"
        position = source.index(marker, start)
        source = source[:position] + f"<p class=\"meta\">{LINK}</p>" + source[position:]
        PAGE.write_text(source, encoding="utf-8", newline="")
    print("linked Rubin missing-data evidence")


if __name__ == "__main__":
    main()
