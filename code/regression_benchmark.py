"""Run a fixed-seed regression benchmark without copying the source dataset."""

from __future__ import annotations

import json
import math
import platform
import time
import warnings
from importlib.metadata import version
from pathlib import Path

import numpy as np
import pandas as pd
from catboost import CatBoostRegressor
from sklearn.datasets import load_diabetes
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor

ROOT = Path(__file__).resolve().parents[1]
SEEDS = [3, 7, 11, 19, 23, 42, 57, 71, 101, 131]
OUTPUT = ROOT / "data" / "benchmark" / "repeated_10seeds_diabetes_regression.json"
REPORT = ROOT / "reports" / "repeated_benchmark_diabetes_regression_2026-10-10.md"


def make_models(seed: int) -> dict[str, object]:
    return {
        "dummy": DummyRegressor(strategy="mean"),
        "ridge": make_pipeline(StandardScaler(), Ridge(alpha=1.0)),
        "random_forest": RandomForestRegressor(
            n_estimators=200, max_features=1.0, random_state=seed, n_jobs=1
        ),
        "hist_gradient_boosting": HistGradientBoostingRegressor(random_state=seed),
        "xgboost": XGBRegressor(
            n_estimators=200,
            max_depth=3,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.9,
            objective="reg:squarederror",
            eval_metric="rmse",
            random_state=seed,
            n_jobs=1,
            verbosity=0,
        ),
        "catboost": CatBoostRegressor(
            iterations=200,
            depth=6,
            learning_rate=0.05,
            loss_function="RMSE",
            random_seed=seed,
            verbose=False,
            thread_count=1,
        ),
        "mlp": make_pipeline(
            StandardScaler(),
            MLPRegressor(
                hidden_layer_sizes=(64,),
                alpha=1e-4,
                learning_rate_init=0.01,
                max_iter=1000,
                early_stopping=True,
                random_state=seed,
            ),
        ),
    }


def main() -> None:
    dataset = load_diabetes()
    rows: list[dict[str, object]] = []
    for seed in SEEDS:
        x_train, x_test, y_train, y_test = train_test_split(
            dataset.data, dataset.target, test_size=0.25, random_state=seed
        )
        for name, model in make_models(seed).items():
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                started = time.perf_counter()
                model.fit(x_train, y_train)
                fit_seconds = time.perf_counter() - started
            predictions = model.predict(x_test)
            rows.append(
                {
                    "seed": seed,
                    "model": name,
                    "mae": float(mean_absolute_error(y_test, predictions)),
                    "rmse": float(np.sqrt(mean_squared_error(y_test, predictions))),
                    "r2": float(r2_score(y_test, predictions)),
                    "fit_seconds": float(fit_seconds),
                    "warnings": [str(item.message) for item in caught],
                }
            )

    frame = pd.DataFrame(rows)
    metrics = ["mae", "rmse", "r2", "fit_seconds"]
    summary: dict[str, dict[str, dict[str, float]]] = {}
    for model_name, group in frame.groupby("model", sort=True):
        summary[model_name] = {}
        for metric in metrics:
            values = group[metric].astype(float)
            mean = float(values.mean())
            std = float(values.std(ddof=1))
            half_width = 2.262 * std / math.sqrt(len(values))
            summary[model_name][metric] = {
                "mean": round(mean, 6),
                "std": round(std, 6),
                "ci95_low": round(mean - half_width, 6),
                "ci95_high": round(mean + half_width, 6),
            }

    result = {
        "dataset": {
            "name": "Diabetes",
            "loader": "sklearn.datasets.load_diabetes",
            "samples": int(dataset.data.shape[0]),
            "features": int(dataset.data.shape[1]),
            "target": "quantitative disease progression measure",
            "source": "https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_diabetes.html",
            "license": "scikit-learn BSD-3-Clause; dataset provenance follows scikit-learn documentation",
            "license_note": "The repository stores no redistributed raw file.",
        },
        "protocol": {
            "test_size": 0.25,
            "stratified": False,
            "seeds": SEEDS,
            "seed_count": len(SEEDS),
            "interval": "mean ± 2.262 * sample_std / sqrt(10), two-sided t approximation with df=9",
            "metrics": ["MAE", "RMSE", "R2"],
            "note": "Descriptive repeated-split regression comparison; excludes TabPFN and is not a universal ranking.",
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
        "summary": summary,
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Diabetes 回归重复实验",
        "",
        "日期：2026-10-10。使用 `sklearn.datasets.load_diabetes`，仓库不复制原始数据；固定 10 个随机种子、25% 测试集和 7 个模型，共 70 次拟合。",
        "",
        "区间为各固定拆分上的描述性 `mean ± 2.262 × sample_std / sqrt(10)`，不是对所有数据集的普遍推断。TabPFN 未参与，不能从本实验推出 TabPFN 对照结论。",
        "",
        "| 模型 | MAE 均值 | RMSE 均值 | R² 均值 | 拟合时间（秒） |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, values in summary.items():
        lines.append(
            f"| {name} | {values['mae']['mean']:.6f} | {values['rmse']['mean']:.6f} | {values['r2']['mean']:.6f} | {values['fit_seconds']['mean']:.6f} |"
        )
    lines.extend(
        [
            "",
            "原始逐次结果：`data/benchmark/repeated_10seeds_diabetes_regression.json`。数据来源与代码许可证边界见 `data/license_manifest.json`。",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"regression benchmark: PASS ({len(rows)} runs, output={OUTPUT.relative_to(ROOT)})")


if __name__ == "__main__":
    main()
