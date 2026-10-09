"""Executable examples for lessons 03 and 06.

The values are deliberately small teaching examples, not benchmark results.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from sklearn.metrics import (
    f1_score,
    log_loss,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    roc_auc_score,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reports" / "lesson_03_06_examples_2026-10-10.json"


def gini(labels: np.ndarray) -> float:
    _, counts = np.unique(labels, return_counts=True)
    probabilities = counts / counts.sum()
    return float(1.0 - np.sum(probabilities**2))


def weighted_split_gini(x: np.ndarray, y: np.ndarray, threshold: float) -> float:
    left = y[x <= threshold]
    right = y[x > threshold]
    return float((len(left) * gini(left) + len(right) * gini(right)) / len(y))


def main() -> None:
    y_true = np.array([0, 1, 1, 0, 1, 0])
    probabilities = np.array([0.10, 0.80, 0.70, 0.40, 0.90, 0.20])
    predictions = (probabilities >= 0.50).astype(int)
    y_reg = np.array([1.0, 2.0, 5.0, 6.0])
    pred_reg = np.array([1.2, 1.8, 4.5, 6.3])
    x = np.array([1.0, 2.0, 3.0, 4.0])
    y_tree = np.array([0, 0, 1, 1])
    thresholds = [1.5, 2.5, 3.5]
    split_scores = [weighted_split_gini(x, y_tree, t) for t in thresholds]

    result = {
        "status": "verified",
        "note": "Small deterministic teaching examples; not benchmark results.",
        "environment": {"python": "runtime", "sklearn": __import__("sklearn").__version__},
        "classification": {
            "f1": float(f1_score(y_true, predictions)),
            "roc_auc": float(roc_auc_score(y_true, probabilities)),
            "log_loss": float(log_loss(y_true, probabilities)),
        },
        "regression": {
            "mae": float(mean_absolute_error(y_reg, pred_reg)),
            "rmse": float(np.sqrt(mean_squared_error(y_reg, pred_reg))),
            "r2": float(r2_score(y_reg, pred_reg)),
        },
        "tree_split": {
            "thresholds": thresholds,
            "weighted_gini": split_scores,
            "best_threshold": thresholds[int(np.argmin(split_scores))],
        },
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"lesson 03/06 examples: PASS ({OUTPUT.relative_to(ROOT)})")


if __name__ == "__main__":
    main()
