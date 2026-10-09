"""Run the minimal executable examples referenced by lessons 12 and 13."""

from __future__ import annotations

import json
from pathlib import Path

from sklearn.datasets import load_breast_cancer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "lesson_12_13_examples_2026-10-10.json"


def run_mlp() -> dict[str, object]:
    data = load_breast_cancer()
    x_train, x_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.25, stratify=data.target, random_state=42
    )
    model = make_pipeline(
        StandardScaler(),
        MLPClassifier(
            hidden_layer_sizes=(32, 16),
            early_stopping=True,
            validation_fraction=0.2,
            max_iter=500,
            random_state=42,
        ),
    )
    model.fit(x_train, y_train)
    accuracy = float(accuracy_score(y_test, model.predict(x_test)))
    return {
        "library": "scikit-learn",
        "version": __import__("sklearn").__version__,
        "dataset": "Breast Cancer Wisconsin Diagnostic",
        "protocol": "stratified 75/25 split, random_state=42, StandardScaler in pipeline",
        "accuracy": accuracy,
        "early_stopping": True,
    }


def run_attention() -> dict[str, object]:
    import torch

    torch.manual_seed(42)
    layer = torch.nn.MultiheadAttention(embed_dim=8, num_heads=2, batch_first=True)
    inputs = torch.randn(4, 5, 8)
    with torch.no_grad():
        outputs, weights = layer(inputs, inputs, inputs)
    if not bool(torch.isfinite(outputs).all()) or not bool(torch.isfinite(weights).all()):
        raise RuntimeError("attention output contains non-finite values")
    return {
        "library": "torch",
        "version": torch.__version__,
        "input_shape": list(inputs.shape),
        "output_shape": list(outputs.shape),
        "attention_shape": list(weights.shape),
        "finite_output": True,
        "seed": 42,
    }


def main() -> None:
    result = {"lesson_12_mlp": run_mlp(), "lesson_13_attention": run_attention()}
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"lesson 12/13 examples: PASS (output={REPORT.relative_to(ROOT)})")


if __name__ == "__main__":
    main()
