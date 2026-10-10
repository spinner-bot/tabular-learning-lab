"""Align lesson labels with existing executable evidence and its limits."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    for relative in ("lessons/03_metrics.html", "lessons/12_mlp.html", "lessons/13_transformer.html"):
        path = ROOT / relative
        source = path.read_text(encoding="utf-8")
        source = source.replace("代码示例（未执行）", "代码示例与运行边界", 1)
        path.write_text(source, encoding="utf-8", newline="")
    path = ROOT / "lessons/22_calibration.html"
    source = path.read_text(encoding="utf-8")
    source = source.replace("代码行未单独执行；同一 calibration API 已由", "页面短片段未单独执行；同一 calibration API 已由", 1)
    path.write_text(source, encoding="utf-8", newline="")
    print("clarified lesson code boundaries")


if __name__ == "__main__":
    main()
