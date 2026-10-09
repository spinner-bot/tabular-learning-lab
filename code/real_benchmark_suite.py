"""Run the same bounded protocol on a second bundled real dataset."""

from __future__ import annotations

import json
import platform
import time
from importlib.metadata import version
from pathlib import Path

import pandas as pd
from sklearn.datasets import load_wine
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split

from benchmark_models import SEEDS, make_models

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "benchmark" / "real_wine_results.json"


def main() -> None:
    dataset = load_wine()
    rows: list[dict[str, object]] = []
    for seed in SEEDS:
        x_train, x_test, y_train, y_test = train_test_split(
            dataset.data,
            dataset.target,
            test_size=0.25,
            stratify=dataset.target,
            random_state=seed,
        )
        for name, model in make_models(seed).items():
            started = time.perf_counter()
            model.fit(x_train, y_train)
            fit_seconds = time.perf_counter() - started
            probabilities = model.predict_proba(x_test)
            predictions = model.predict(x_test)
            rows.append(
                {
                    "seed": seed,
                    "model": name,
                    "accuracy": accuracy_score(y_test, predictions),
                    "balanced_accuracy": balanced_accuracy_score(y_test, predictions),
                    "macro_f1": f1_score(y_test, predictions, average="macro"),
                    "roc_auc_ovr": roc_auc_score(y_test, probabilities, multi_class="ovr"),
                    "fit_seconds": fit_seconds,
                }
            )
    frame = pd.DataFrame(rows)
    summary = (
        frame.groupby("model", sort=True)[
            ["accuracy", "balanced_accuracy", "macro_f1", "roc_auc_ovr", "fit_seconds"]
        ]
        .agg(["mean", "std"])
        .round(6)
    )
    result = {
        "dataset": {
            "name": "Wine",
            "loader": "sklearn.datasets.load_wine",
            "samples": int(dataset.data.shape[0]),
            "features": int(dataset.data.shape[1]),
            "classes": int(len(set(dataset.target))),
            "source": "https://archive.ics.uci.edu/dataset/109/wine",
            "doi": "https://doi.org/10.24432/C5PC7J",
            "license": "CC BY 4.0",
            "license_note": "UCI page states CC BY 4.0; this repository stores no raw file.",
        },
        "protocol": {
            "test_size": 0.25,
            "seeds": list(SEEDS),
            "note": "Bounded multiclass comparison; not a universal ranking and excludes TabPFN.",
        },
        "environment": {
            "python": platform.python_version(),
            "pandas": version("pandas"),
            "scikit_learn": version("scikit-learn"),
            "xgboost": version("xgboost"),
            "catboost": version("catboost"),
        },
        "runs": rows,
        "summary": json.loads(summary.to_json()),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"real wine benchmark: PASS ({len(rows)} runs, output={OUTPUT.relative_to(ROOT)})")


if __name__ == "__main__":
    main()
