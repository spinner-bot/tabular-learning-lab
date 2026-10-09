"""Controlled preprocessing ablation on the two real course datasets.

The comparison asks only whether fitting StandardScaler inside the training
pipeline changes three fixed model families under the same splits. It is not a
general preprocessing recommendation.
"""

from __future__ import annotations

import json
import platform
import time
import warnings
from importlib.metadata import version
from pathlib import Path

import pandas as pd
from sklearn.datasets import load_breast_cancer, load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
SEEDS = [7, 42, 101, 131, 197]
OUTPUT = ROOT / "data" / "benchmark" / "preprocessing_ablation.json"


def make_model(name: str, scaled: bool, seed: int):
    if name == "logistic_regression":
        model = LogisticRegression(max_iter=2000, random_state=seed)
    elif name == "random_forest":
        model = RandomForestClassifier(n_estimators=80, max_depth=8, random_state=seed, n_jobs=1)
    elif name == "mlp":
        model = MLPClassifier(
            hidden_layer_sizes=(32,), early_stopping=True, max_iter=300, random_state=seed
        )
    else:
        raise ValueError(name)
    return make_pipeline(StandardScaler(), model) if scaled else model


def run_dataset(name: str, dataset, multiclass: bool) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for seed in SEEDS:
        x_train, x_test, y_train, y_test = train_test_split(
            dataset.data, dataset.target, test_size=0.25, stratify=dataset.target, random_state=seed
        )
        for model_name in ("logistic_regression", "random_forest", "mlp"):
            for scaled in (False, True):
                model = make_model(model_name, scaled, seed)
                started = time.perf_counter()
                with warnings.catch_warnings(record=True) as captured:
                    warnings.simplefilter("always")
                    model.fit(x_train, y_train)
                fit_seconds = time.perf_counter() - started
                probabilities = model.predict_proba(x_test)
                predictions = model.predict(x_test)
                row: dict[str, object] = {
                    "dataset": name,
                    "seed": seed,
                    "model": model_name,
                    "preprocessing": "standard_scaled" if scaled else "raw",
                    "accuracy": float(accuracy_score(y_test, predictions)),
                    "balanced_accuracy": float(balanced_accuracy_score(y_test, predictions)),
                    "macro_f1": float(f1_score(y_test, predictions, average="macro")),
                    "fit_seconds": float(fit_seconds),
                    "warnings": [str(item.message) for item in captured],
                    "convergence_warning": any(
                        "converg" in str(item.message).lower() for item in captured
                    ),
                }
                row["roc_auc"] = float(
                    roc_auc_score(y_test, probabilities, multi_class="ovr")
                    if multiclass
                    else roc_auc_score(y_test, probabilities[:, 1])
                )
                rows.append(row)
    return rows


def main() -> None:
    jobs = [
        ("Breast Cancer Wisconsin Diagnostic", load_breast_cancer(), False),
        ("Wine", load_wine(), True),
    ]
    rows: list[dict[str, object]] = []
    for name, dataset, multiclass in jobs:
        rows.extend(run_dataset(name, dataset, multiclass))
    frame = pd.DataFrame(rows)
    summary = (
        frame.groupby(["dataset", "model", "preprocessing"], sort=True)[
            ["accuracy", "balanced_accuracy", "macro_f1", "roc_auc", "fit_seconds"]
        ]
        .agg(["mean", "std"])
        .round(6)
    )
    result = {
        "protocol": {
            "datasets": [job[0] for job in jobs],
            "models": ["logistic_regression", "random_forest", "mlp"],
            "preprocessing": ["raw", "standard_scaled"],
            "seeds": SEEDS,
            "test_size": 0.25,
            "stratified": True,
            "note": "Controlled within-pipeline preprocessing ablation; not a universal ranking and excludes TabPFN.",
        },
        "environment": {
            "python": platform.python_version(),
            "pandas": version("pandas"),
            "scikit_learn": version("scikit-learn"),
        },
        "runs": rows,
        "summary": json.loads(summary.to_json()),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"preprocessing ablation: PASS ({len(rows)} runs, output={OUTPUT.relative_to(ROOT)})")


if __name__ == "__main__":
    main()
