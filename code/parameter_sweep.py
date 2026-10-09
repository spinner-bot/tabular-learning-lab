"""Predeclared XGBoost/CatBoost parameter sweep on two real datasets."""

from __future__ import annotations

import json
import platform
import time
from importlib.metadata import version
from pathlib import Path

import pandas as pd
import xgboost as xgb
from catboost import CatBoostClassifier
from sklearn.datasets import load_breast_cancer, load_wine
from sklearn.metrics import balanced_accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split

from benchmark_models import SEEDS

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "benchmark" / "parameter_sweep_results.json"

CONFIGS = {
    "xgb_small": ("xgboost", {"n_estimators": 50, "max_depth": 3, "learning_rate": 0.1}),
    "xgb_regular": ("xgboost", {"n_estimators": 100, "max_depth": 4, "learning_rate": 0.08}),
    "xgb_deeper": ("xgboost", {"n_estimators": 150, "max_depth": 6, "learning_rate": 0.05}),
    "cat_small": ("catboost", {"iterations": 50, "depth": 4, "learning_rate": 0.1}),
    "cat_regular": ("catboost", {"iterations": 100, "depth": 6, "learning_rate": 0.08}),
    "cat_deeper": ("catboost", {"iterations": 150, "depth": 8, "learning_rate": 0.05}),
}


def make_model(name: str, params: dict[str, float | int], seed: int, multiclass: bool) -> object:
    if name == "xgboost":
        return xgb.XGBClassifier(
            **params,
            subsample=0.9,
            colsample_bytree=0.9,
            random_state=seed,
            n_jobs=1,
            eval_metric="mlogloss" if multiclass else "logloss",
        )
    return CatBoostClassifier(
        **params,
        random_seed=seed,
        verbose=False,
        allow_writing_files=False,
        loss_function="MultiClass" if multiclass else "Logloss",
    )


def main() -> None:
    datasets = {
        "breast_cancer": load_breast_cancer(),
        "wine": load_wine(),
    }
    rows: list[dict[str, object]] = []
    for dataset_name, dataset in datasets.items():
        multiclass = len(set(dataset.target)) > 2
        for seed in SEEDS:
            x_train, x_test, y_train, y_test = train_test_split(
                dataset.data,
                dataset.target,
                test_size=0.25,
                stratify=dataset.target,
                random_state=seed,
            )
            for config_name, (model_name, params) in CONFIGS.items():
                model = make_model(model_name, params, seed, multiclass)
                started = time.perf_counter()
                model.fit(x_train, y_train)
                fit_seconds = time.perf_counter() - started
                probabilities = model.predict_proba(x_test)
                predictions = model.predict(x_test)
                if multiclass:
                    auc = roc_auc_score(y_test, probabilities, multi_class="ovr")
                else:
                    auc = roc_auc_score(y_test, probabilities[:, 1])
                rows.append(
                    {
                        "dataset": dataset_name,
                        "seed": seed,
                        "config": config_name,
                        "model_family": model_name,
                        "balanced_accuracy": balanced_accuracy_score(y_test, predictions),
                        "macro_f1": f1_score(y_test, predictions, average="macro"),
                        "roc_auc_ovr": auc,
                        "fit_seconds": fit_seconds,
                    }
                )
    frame = pd.DataFrame(rows)
    summary = frame.groupby(["dataset", "config"], sort=True)[
        ["balanced_accuracy", "macro_f1", "roc_auc_ovr", "fit_seconds"]
    ].agg(["mean", "std"]).round(6)
    result = {
        "protocol": {
            "datasets": list(datasets),
            "seeds": list(SEEDS),
            "test_size": 0.25,
            "configs": CONFIGS,
            "selection": "Predeclared configurations; no test-set-driven selection.",
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
    print(f"parameter sweep: PASS ({len(rows)} runs, output={OUTPUT.relative_to(ROOT)})")


if __name__ == "__main__":
    main()
