"""Measure representative resource behavior at two larger synthetic scales."""

from __future__ import annotations

import gc
import json
import os
import platform
import threading
import time
from importlib.metadata import version
from pathlib import Path

import psutil
from catboost import CatBoostClassifier
from sklearn.datasets import make_classification
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "benchmark" / "stress_resource_profile.json"
REPORT = ROOT / "reports" / "stress_resource_profile_2026-10-10.md"
SIZES = ((5_000, 50), (15_000, 50))


def make_models(seed: int) -> dict[str, object]:
    return {
        "logistic_regression": make_pipeline(
            StandardScaler(), LogisticRegression(max_iter=500, random_state=seed)
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=100, max_depth=12, random_state=seed, n_jobs=1
        ),
        "hist_gradient_boosting": HistGradientBoostingClassifier(
            max_iter=100, max_leaf_nodes=31, random_state=seed
        ),
        "xgboost": XGBClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.08,
            subsample=0.9,
            colsample_bytree=0.9,
            random_state=seed,
            n_jobs=1,
            eval_metric="logloss",
            verbosity=0,
        ),
        "catboost": CatBoostClassifier(
            iterations=100,
            depth=6,
            learning_rate=0.08,
            random_seed=seed,
            verbose=False,
            thread_count=1,
            allow_writing_files=False,
        ),
        "mlp": make_pipeline(
            StandardScaler(),
            MLPClassifier(
                hidden_layer_sizes=(64,),
                early_stopping=True,
                max_iter=300,
                random_state=seed,
            ),
        ),
    }


def profile(model: object, x_train, y_train) -> dict[str, float]:
    process = psutil.Process(os.getpid())
    baseline = process.memory_info().rss
    peak = baseline
    stop = threading.Event()

    def sample() -> None:
        nonlocal peak
        while not stop.is_set():
            peak = max(peak, process.memory_info().rss)
            stop.wait(0.01)

    worker = threading.Thread(target=sample, daemon=True)
    started = time.perf_counter()
    worker.start()
    model.fit(x_train, y_train)
    stop.set()
    worker.join(timeout=1)
    elapsed = time.perf_counter() - started
    peak = max(peak, process.memory_info().rss)
    return {
        "fit_seconds": round(elapsed, 6),
        "baseline_rss_mb": round(baseline / (1024 * 1024), 3),
        "peak_rss_mb": round(peak / (1024 * 1024), 3),
        "delta_peak_rss_mb": round((peak - baseline) / (1024 * 1024), 3),
    }


def main() -> None:
    rows: list[dict[str, object]] = []
    for samples, features in SIZES:
        x, y = make_classification(
            n_samples=samples,
            n_features=features,
            n_informative=20,
            n_redundant=10,
            weights=[0.7, 0.3],
            class_sep=0.9,
            random_state=20261010 + samples,
        )
        split = int(samples * 0.75)
        x_train, y_train = x[:split], y[:split]
        for name, model in make_models(42).items():
            rows.append(
                {
                    "samples": samples,
                    "features": features,
                    "model": name,
                    **profile(model, x_train, y_train),
                }
            )
            del model
            gc.collect()
        del x, y, x_train, y_train
        gc.collect()

    result = {
        "protocol": {
            "dataset": "sklearn.datasets.make_classification",
            "sizes": [{"samples": n, "features": p} for n, p in SIZES],
            "train_fraction": 0.75,
            "seed": 42,
            "models": list(make_models(42)),
            "rss_sampling_interval_seconds": 0.01,
            "note": "Synthetic stress profile; absolute RSS is process/environment dependent and is not a universal complexity claim. TabPFN is excluded because its runtime environment is unavailable.",
        },
        "environment": {
            "python": platform.python_version(),
            "psutil": version("psutil"),
            "scikit_learn": version("scikit-learn"),
            "xgboost": version("xgboost"),
            "catboost": version("catboost"),
        },
        "runs": rows,
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# 更大规模资源压力剖析",
        "",
        "日期：2026-10-10。使用 `make_classification` 生成 5,000×50 与 15,000×50 两档合成表格数据，按 75/25 顺序切分，在固定 seed=42 下运行 6 个模型，共 12 次拟合。",
        "",
        "RSS 是当前单进程环境中的绝对观测值；`delta_peak_rss_mb` 是拟合相对该次拟合开始时的进程 RSS 增量。结果用于压力边界记录，不支持跨硬件复杂度结论。",
        "",
        "| 样本数 | 模型 | 拟合秒数 | 基线 RSS MB | 峰值 RSS MB | 峰值增量 MB |",
        "|---:|---|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['samples']} | {row['model']} | {row['fit_seconds']:.6f} | {row['baseline_rss_mb']:.3f} | {row['peak_rss_mb']:.3f} | {row['delta_peak_rss_mb']:.3f} |"
        )
    lines.extend(
        [
            "",
            "逐次结果：`data/benchmark/stress_resource_profile.json`。这不是 TabPFN 对照，也不替代生产规模容量测试。",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"stress resource profile: PASS ({len(rows)} fits, output={OUTPUT.relative_to(ROOT)})")


if __name__ == "__main__":
    main()
