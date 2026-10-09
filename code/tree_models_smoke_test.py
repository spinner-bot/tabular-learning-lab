"""Smoke test for lessons 06-10.

Executed locally on 2026-10-09 with Python 3.13.5,
scikit-learn 1.9.1, xgboost 3.4.1 and catboost 1.2.10.
"""

import numpy as np
import pandas as pd
import xgboost as xgb
from catboost import CatBoostClassifier
from sklearn.datasets import load_iris
from sklearn.ensemble import GradientBoostingRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


def main() -> None:
    X, y = load_iris(return_X_y=True)
    x_train, x_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    models = [
        DecisionTreeClassifier(max_depth=3, random_state=42),
        RandomForestClassifier(n_estimators=20, random_state=42, n_jobs=1),
        xgb.XGBClassifier(
            n_estimators=20,
            max_depth=3,
            learning_rate=0.1,
            random_state=42,
            n_jobs=1,
            eval_metric="mlogloss",
        ),
    ]
    for model in models:
        model.fit(x_train, y_train)
        assert model.predict(x_test).shape == y_test.shape

    regression = GradientBoostingRegressor(
        n_estimators=20, max_depth=2, random_state=42
    )
    regression.fit(x_train, y_train.astype(float))
    assert regression.predict(x_test).shape == y_test.shape

    frame = pd.DataFrame(
        {
            "size": np.r_[np.arange(60), np.arange(60) + 1],
            "region": ["north"] * 60 + ["south"] * 60,
        }
    )
    labels = np.r_[np.zeros(60, dtype=int), np.ones(60, dtype=int)]
    cat = CatBoostClassifier(
        iterations=20, depth=3, learning_rate=0.1, verbose=False, random_seed=42
    )
    cat.fit(frame, labels, cat_features=["region"])
    assert cat.predict(frame).shape[0] == len(frame)
    print("tree models smoke test: PASS")


if __name__ == "__main__":
    main()
