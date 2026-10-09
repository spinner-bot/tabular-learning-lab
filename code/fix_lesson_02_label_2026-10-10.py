from pathlib import Path

path = Path(__file__).resolve().parents[1] / "lessons/02_ml_workflow.html"
text = path.read_text(encoding="utf-8")
old = '<input id="leakage-switch" type="checkbox"><label for="leakage-switch">模拟“先整体计算统计量再划分”</label>'
new = '<input id="leakage-switch" type="checkbox" aria-label="模拟先整体计算统计量再划分"><label for="leakage-switch">模拟“先整体计算统计量再划分”</label>'
if old not in text:
    raise RuntimeError("lesson 02 input anchor not found")
path.write_text(text.replace(old, new), encoding="utf-8", newline="")
print("Fixed lesson 02 checkbox label association.")
