"""Keep the appended TabPFN environment update on its own Markdown heading."""

from pathlib import Path

path = Path(__file__).resolve().parents[1] / "research" / "open_questions.md"
text = path.read_text(encoding="utf-8")
marker = "### 2026-10-10 默认环境复核"
if marker in text:
    text = text.replace(marker, "\n" + marker, 1)
    path.write_text(text, encoding="utf-8", newline="")
print("normalized open questions update")
