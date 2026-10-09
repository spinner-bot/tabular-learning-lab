"""Run a larger, fixed-seed comparison on the two bundled real datasets.

This extends (without overwriting) the original three-seed benchmark. The
reported 95% intervals are descriptive intervals over the chosen random
splits, not claims about a population of datasets.
"""

from __future__ import annotations

import json
import math
import platform
import time
from importlib.metadata import version
from pathlib import Path

import pandas as pd
from sklearn.datasets import load_breast_cancer, load_wine
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split

from benchmark_models import make_models

ROOT = Path(__file__).resolve().parents[1]
SEEDS = [3, 7, 11, 19, 23, 42, 57, 71, 101, 131]


def run_dataset(name: str, dataset, multiclass: bool) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    for seed in SEEDS:
        x_train, x_test, y_train, y_test = train_test_split(
            dataset.data,
            dataset.target,
            test_size=0.25,
            stratify=dataset.target,
            random_state=seed,
        )
        for model_name, model in make_models(seed).items():
            started = time.perf_counter()
            model.fit(x_train, y_train)
            fit_seconds = time.perf_counter() - started
            probabilities = model.predict_proba(x_test)
            predictions = model.predict(x_test)
            row: dict[str, object] = {
                "seed": seed,
                "model": model_name,
                "accuracy": float(accuracy_score(y_test, predictions)),
                "balanced_accuracy": float(balanced_accuracy_score(y_test, predictions)),
                "macro_f1": float(f1_score(y_test, predictions, average="macro")),
                "fit_seconds": float(fit_seconds),
            }
            if multiclass:
                row["roc_auc_ovr"] = float(roc_auc_score(y_test, probabilities, multi_class="ovr"))
            else:
                row["roc_auc"] = float(roc_auc_score(y_test, probabilities[:, 1]))
            rows.append(row)

    frame = pd.DataFrame(rows)
    metric_names = ["accuracy", "balanced_accuracy", "macro_f1"]
    metric_names.append("roc_auc_ovr" if multiclass else "roc_auc")
    metric_names.append("fit_seconds")
    summary: dict[str, dict[str, dict[str, float]]] = {}
    for model_name, group in frame.groupby("model", sort=True):
        summary[model_name] = {}
        for metric in metric_names:
            values = group[metric].astype(float)
            mean = float(values.mean())
            std = float(values.std(ddof=1))
            # n=10 repeated splits: use the two-sided t critical value for df=9.
            half_width = 2.262 * std / math.sqrt(len(values))
            summary[model_name][metric] = {
                "mean": round(mean, 6),
                "std": round(std, 6),
                "ci95_low": round(mean - half_width, 6),
                "ci95_high": round(mean + half_width, 6),
            }
    return {
        "dataset": {
            "name": name,
            "samples": int(dataset.data.shape[0]),
            "features": int(dataset.data.shape[1]),
            "classes": int(len(set(dataset.target))),
        },
        "protocol": {
            "test_size": 0.25,
            "stratified": True,
            "seeds": SEEDS,
            "seed_count": len(SEEDS),
            "interval": "mean ± 2.262 * sample_std / sqrt(10), two-sided t approximation with df=9",
            "note": "Descriptive repeated-split comparison; excludes TabPFN and is not a universal ranking.",
        },
        "environment": {
            "python": platform.python_version(),
            "pandas": version("pandas"),
            "scikit_learn": version("scikit-learn"),
            "xgboost": version("xgboost"),
            "catboost": version("catboost"),
        },
        "runs": rows,
        "summary": summary,
    }


def main() -> None:
    jobs = [
        ("Breast Cancer Wisconsin Diagnostic", load_breast_cancer(), False, "repeated_10seeds_breast_cancer.json"),
        ("Wine", load_wine(), True, "repeated_10seeds_wine.json"),
    ]
    for name, dataset, multiclass, filename in jobs:
        result = run_dataset(name, dataset, multiclass)
        output = ROOT / "data" / "benchmark" / filename
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"repeated benchmark: PASS ({name}, {len(result['runs'])} runs, output={output.relative_to(ROOT)})")


if __name__ == "__main__":
    main()
