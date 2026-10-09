"""Smoke test for lessons 01-05.

Executed locally on 2026-10-09 with Python 3.13.5,
pandas 3.0.6 and scikit-learn 1.9.1.
"""

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeClassifier


def main() -> None:
    frame = pd.DataFrame(
        {"area": [60, 90], "region": ["A", "B"], "price": [180, 320]}
    )
    assert list(frame.columns) == ["area", "region", "price"]

    features, labels = load_iris(return_X_y=True)
    x_train, x_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.2, random_state=42, stratify=labels
    )
    model = make_pipeline(
        SimpleImputer(), LogisticRegression(max_iter=500)
    )
    model.fit(x_train, y_train)
    score = f1_score(y_test, model.predict(x_test), average="macro")
    assert 0 <= score <= 1

    baseline = DummyClassifier(strategy="most_frequent")
    assert len(cross_val_score(baseline, x_train, y_train, cv=5)) == 5
    DecisionTreeClassifier(max_depth=3, random_state=42).fit(x_train, y_train)
    print(f"foundation batch smoke test: PASS (macro-F1={score:.3f})")


if __name__ == "__main__":
    main()
