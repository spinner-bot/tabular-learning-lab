"""Execute the small code snippets embedded in lessons 01 and 02."""

from __future__ import annotations

import json
import platform
from pathlib import Path

import pandas as pd
import sklearn
from sklearn.datasets import load_iris
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "reports" / "lesson_01_02_code_examples_2026-10-10.json"
MD_PATH = ROOT / "reports" / "lesson_01_02_code_examples_2026-10-10.md"


def main() -> None:
    frame = pd.DataFrame(
        {"area": [60, 90], "region": ["A", "B"], "price": [180, 320]}
    )
    dtypes = [str(value) for value in frame.dtypes]
    assert dtypes == ["int64", "str", "int64"]

    X, y = load_iris(return_X_y=True)
    x_train, x_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    model = make_pipeline(SimpleImputer(), LogisticRegression(max_iter=500, random_state=42))
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    assert len(predictions) == len(y_test)
    result = {
        "status": "PASS",
        "lesson_01": {"rows": len(frame), "columns": list(frame.columns), "dtypes": dtypes},
        "lesson_02": {"train_rows": len(x_train), "test_rows": len(x_test), "predictions": len(predictions)},
        "python": platform.python_version(),
        "pandas": pd.__version__,
        "scikit_learn": sklearn.__version__,
        "seed": 42,
        "note": "Teaching snippet execution only; not a benchmark or a complete data workflow audit.",
    }
    JSON_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    MD_PATH.write_text(
        "# 第 01、02 节代码示例验证（2026-10-10）\n\n"
        "- 状态：PASS（2/2 个页面代码路径）。\n"
        f"- 第 01 节：创建 {result['lesson_01']['rows']} 行 DataFrame 并核对列名/类型。\n"
        f"- 第 02 节：`SimpleImputer + LogisticRegression` 管道训练并完成 {result['lesson_02']['predictions']} 个测试预测。\n"
        f"- 环境：Python {result['python']}、pandas {result['pandas']}、scikit-learn {result['scikit_learn']}。\n"
        "- 边界：验证页面片段可执行，不替代完整数据泄漏审计、调参实验或生产建议。\n",
        encoding="utf-8",
    )
    print("lesson 01/02 code examples: PASS (2/2 paths)")


if __name__ == "__main__":
    main()
