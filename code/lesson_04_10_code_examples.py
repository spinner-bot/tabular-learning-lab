"""Execute the executable teaching snippets from lessons 04 and 06-10."""

from __future__ import annotations

import json
import platform
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
import xgboost as xgb
from catboost import CatBoostClassifier
from sklearn.datasets import load_iris
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import GradientBoostingRegressor, RandomForestClassifier
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.tree import DecisionTreeClassifier


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "reports" / "lesson_04_10_code_examples_2026-10-10.json"
MD_PATH = ROOT / "reports" / "lesson_04_10_code_examples_2026-10-10.md"


def main() -> None:
    X, y = load_iris(return_X_y=True)
    x_train, x_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    records: list[dict[str, object]] = []

    baseline = DummyClassifier(strategy="most_frequent")
    baseline_scores = cross_val_score(baseline, x_train, y_train, cv=5)
    records.append({"lesson": 4, "model": "DummyClassifier", "status": "PASS", "cv_folds": len(baseline_scores)})

    tree = DecisionTreeClassifier(criterion="gini", max_depth=3, random_state=42)
    tree.fit(x_train, y_train)
    records.append({"lesson": 6, "model": "DecisionTreeClassifier", "status": "PASS", "predictions": len(tree.predict(x_test))})

    forest = RandomForestClassifier(n_estimators=200, oob_score=True, random_state=42, n_jobs=1)
    forest.fit(x_train, y_train)
    assert forest.oob_score_ is not None
    records.append({"lesson": 7, "model": "RandomForestClassifier", "status": "PASS", "oob_score": float(forest.oob_score_)})

    regression_target = X[:, 0] + 0.5 * X[:, 1]
    reg_train, reg_test, target_train, target_test = train_test_split(
        X, regression_target, test_size=0.2, random_state=42
    )
    gbdt = GradientBoostingRegressor(n_estimators=200, learning_rate=0.05, max_depth=2, random_state=42)
    gbdt.fit(reg_train, target_train)
    records.append({"lesson": 8, "model": "GradientBoostingRegressor", "status": "PASS", "predictions": len(gbdt.predict(reg_test))})

    xgb_model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=1,
        eval_metric="mlogloss",
    )
    xgb_model.fit(x_train, y_train)
    records.append({"lesson": 9, "model": "XGBClassifier", "status": "PASS", "predictions": len(xgb_model.predict(x_test))})

    categorical = pd.DataFrame(
        {"size": np.r_[np.arange(60), np.arange(60) + 1], "region": ["north"] * 60 + ["south"] * 60}
    )
    cat_target = np.r_[np.zeros(60, dtype=int), np.ones(60, dtype=int)]
    cat_model = CatBoostClassifier(
        iterations=200, depth=4, learning_rate=0.05, verbose=False, random_seed=42
    )
    cat_model.fit(categorical, cat_target, cat_features=["region"])
    records.append({"lesson": 10, "model": "CatBoostClassifier", "status": "PASS", "predictions": len(cat_model.predict(categorical))})

    result = {
        "status": "PASS",
        "records": records,
        "python": platform.python_version(),
        "scikit_learn": sklearn.__version__,
        "xgboost": xgb.__version__,
        "catboost": CatBoostClassifier.__module__.split(".")[0],
        "seed": 42,
        "note": "Executable teaching paths only; not a comparative benchmark or a claim of universal model superiority.",
    }
    JSON_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 第 04、06–10 节代码示例验证（2026-10-10）",
        "",
        "- 状态：PASS（6/6 个页面代码路径）",
        f"- 环境：Python {result['python']}、scikit-learn {result['scikit_learn']}、XGBoost {result['xgboost']}。",
        "- 路径：DummyClassifier + 5 折交叉验证、DecisionTree、RandomForest OOB、GradientBoostingRegressor、XGBClassifier、CatBoostClassifier 均完成最小运行。",
        "- 边界：这是页面 API/参数路径验证，不是统一调参 benchmark，也不支持模型普遍优越性结论。",
        "- 逐项 JSON：`reports/lesson_04_10_code_examples_2026-10-10.json`。",
    ]
    MD_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("lesson 04/06-10 code examples: PASS (6/6 paths)")


if __name__ == "__main__":
    main()
