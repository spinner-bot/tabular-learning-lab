"""Execute lesson 23's ColumnTransformer/Pipeline teaching example."""

from __future__ import annotations

import json
import platform
from pathlib import Path

import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = ROOT / "reports" / "lesson_23_preprocessing_example_2026-10-10.json"
REPORT_MD = ROOT / "reports" / "lesson_23_preprocessing_example_2026-10-10.md"


def main() -> None:
    frame = pd.DataFrame(
        {
            "age": [22, 25, None, 41, 44, 52, 29, None, 37, 48, 33, 56],
            "region": ["north", "south", "north", None, "south", "east", "east", "north", None, "south", "east", "north"],
            "income": [30, 34, 31, 60, None, 72, 38, 35, 55, None, 46, 80],
        }
    )
    target = [0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1]
    numeric = ["age", "income"]
    categorical = ["region"]
    preprocess = ColumnTransformer(
        [
            (
                "num",
                Pipeline(
                    [("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]
                ),
                numeric,
            ),
            (
                "cat",
                Pipeline(
                    [
                        ("impute", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical,
            ),
        ]
    )
    model = Pipeline(
        [("preprocess", preprocess), ("classifier", LogisticRegression(max_iter=500, random_state=42))]
    )
    x_train, x_test, y_train, y_test = train_test_split(
        frame, target, test_size=0.25, random_state=42, stratify=target
    )
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    transformed_shape = model.named_steps["preprocess"].transform(x_test).shape
    assert len(predictions) == len(y_test)
    assert transformed_shape[0] == len(y_test)
    assert transformed_shape[1] > 0
    result = {
        "status": "PASS",
        "rows": len(frame),
        "train_rows": len(x_train),
        "test_rows": len(x_test),
        "transformed_test_shape": list(transformed_shape),
        "missing_values_before_fit": int(frame.isna().sum().sum()),
        "accuracy": float((predictions == y_test).mean()),
        "python": platform.python_version(),
        "pandas": pd.__version__,
        "scikit_learn": sklearn.__version__,
        "seed": 42,
        "note": "Teaching-scale preprocessing path; not a TabPFN or production benchmark.",
    }
    REPORT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        "# 第 23 节预处理代码验证（2026-10-10）\n\n"
        "- 状态：PASS\n"
        f"- 数据：{result['rows']} 行，训练/测试={result['train_rows']}/{result['test_rows']}；原始缺失单元格 {result['missing_values_before_fit']} 个。\n"
        f"- 变换后测试形状：`{result['transformed_test_shape']}`；准确率：`{result['accuracy']:.3f}`。\n"
        f"- 环境：Python {result['python']}、pandas {result['pandas']}、scikit-learn {result['scikit_learn']}。\n"
        "- 证据边界：验证的是教学规模的 `ColumnTransformer`/`Pipeline` 插补、缩放、独热编码和分类器连接；不等于 TabPFN、生产容量或性能基准。\n",
        encoding="utf-8",
    )
    print(f"lesson 23 preprocessing example: PASS (accuracy={result['accuracy']:.3f})")


if __name__ == "__main__":
    main()
