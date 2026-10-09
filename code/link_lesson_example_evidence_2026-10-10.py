from pathlib import Path

root = Path(__file__).resolve().parents[1]
replacements = {
    "lessons/03_metrics.html": (
        '<p class="meta">代码和结果均未单独执行；依赖版本以 `code/requirements.txt` 为准。</p>',
        '<p class="meta">页面内短片段仍是教学示例；可执行的指标示例已运行并保存于 <a href="../reports/lesson_03_06_examples_2026-10-10.json">验证 JSON</a>，脚本为 <a href="../code/lesson_03_06_examples.py">code/lesson_03_06_examples.py</a>。</p>',
    ),
    "lessons/06_tree_splits.html": (
        '<p class="meta">本节代码尚未单独记录运行结果。</p>',
        '<p class="meta">页面内短片段仍是教学示例；候选切点与 Gini 示例已运行并保存于 <a href="../reports/lesson_03_06_examples_2026-10-10.json">验证 JSON</a>，脚本为 <a href="../code/lesson_03_06_examples.py">code/lesson_03_06_examples.py</a>。</p>',
    ),
}
for relative, (old, new) in replacements.items():
    path = root / relative
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"missing anchor in {relative}")
    path.write_text(text.replace(old, new), encoding="utf-8", newline="")
print("Linked executable lesson example evidence.")
