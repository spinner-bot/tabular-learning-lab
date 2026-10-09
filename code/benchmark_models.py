"""Reproducible small-data benchmark for the course comparison protocol.

This benchmark intentionally excludes TabPFN because the current Windows
environment cannot import PyTorch. It is a local protocol check, not a claim
about universal model rankings.
"""

from __future__ import annotations

import json
import platform
import time
from importlib.metadata import version
from pathlib import Path

import numpy as np
import pandas as pd
import xgboost as xgb
from catboost import CatBoostClassifier
from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "benchmark" / "initial_results.json"
SEEDS = (7, 42, 101)


def make_models(seed: int) -> dict[str, object]:
    return {
        "dummy": DummyClassifier(strategy="prior"),
        "logistic_regression": make_pipeline(
            StandardScaler(), LogisticRegression(max_iter=500, random_state=seed)
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=80, max_depth=8, random_state=seed, n_jobs=1
        ),
        "hist_gradient_boosting": HistGradientBoostingClassifier(
            max_iter=80, max_leaf_nodes=15, random_state=seed
        ),
        "xgboost": xgb.XGBClassifier(
            n_estimators=80,
            max_depth=4,
            learning_rate=0.08,
            subsample=0.9,
            colsample_bytree=0.9,
            random_state=seed,
            n_jobs=1,
            eval_metric="logloss",
        ),
        "catboost": CatBoostClassifier(
            iterations=80,
            depth=5,
            learning_rate=0.08,
            random_seed=seed,
            verbose=False,
            allow_writing_files=False,
        ),
        "mlp": make_pipeline(
            StandardScaler(),
            MLPClassifier(
                hidden_layer_sizes=(32,),
                early_stopping=True,
                max_iter=200,
                random_state=seed,
            ),
        ),
    }


def run() -> dict[str, object]:
    X, y = make_classification(
        n_samples=900,
        n_features=18,
        n_informative=8,
        n_redundant=4,
        n_classes=2,
        weights=[0.72, 0.28],
        class_sep=0.9,
        random_state=20261009,
    )
    rows: list[dict[str, object]] = []
    for seed in SEEDS:
        x_train, x_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, stratify=y, random_state=seed
        )
        for name, model in make_models(seed).items():
            started = time.perf_counter()
            model.fit(x_train, y_train)
            fit_seconds = time.perf_counter() - started
            probabilities = model.predict_proba(x_test)[:, 1]
            predictions = (probabilities >= 0.5).astype(int)
            rows.append(
                {
                    "seed": seed,
                    "model": name,
                    "accuracy": accuracy_score(y_test, predictions),
                    "balanced_accuracy": balanced_accuracy_score(y_test, predictions),
                    "macro_f1": f1_score(y_test, predictions, average="macro"),
                    "roc_auc": roc_auc_score(y_test, probabilities),
                    "fit_seconds": fit_seconds,
                }
            )
    frame = pd.DataFrame(rows)
    summary = (
        frame.groupby("model", sort=True)[
            ["accuracy", "balanced_accuracy", "macro_f1", "roc_auc", "fit_seconds"]
        ]
        .agg(["mean", "std"])
        .round(6)
    )
    return {
        "protocol": {
            "dataset": "sklearn.make_classification",
            "samples": 900,
            "features": 18,
            "test_size": 0.25,
            "seeds": list(SEEDS),
            "threshold": 0.5,
            "note": "Synthetic protocol check; not a universal ranking and excludes TabPFN.",
        },
        "environment": {
            "python": platform.python_version(),
            "numpy": version("numpy"),
            "pandas": version("pandas"),
            "scikit_learn": version("scikit-learn"),
            "xgboost": version("xgboost"),
            "catboost": version("catboost"),
        },
        "runs": rows,
        "summary": json.loads(summary.to_json()),
    }


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    result = run()
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"benchmark: PASS ({len(result['runs'])} runs, output={OUTPUT.relative_to(ROOT)})")


if __name__ == "__main__":
    main()
