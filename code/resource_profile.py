"""Profile fit time and process RSS peak for the fixed comparison protocol."""

from __future__ import annotations

import json
import os
import platform
import threading
import time
from importlib.metadata import version
from pathlib import Path

import psutil
from sklearn.datasets import load_breast_cancer, load_wine
from sklearn.model_selection import train_test_split

from benchmark_models import make_models

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "benchmark" / "resource_profile.json"


def profile_fit(model, x_train, y_train) -> dict[str, float]:
    process = psutil.Process(os.getpid())
    peak = process.memory_info().rss
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
    return {"fit_seconds": round(elapsed, 6), "peak_rss_mb": round(peak / (1024 * 1024), 3)}


def main() -> None:
    rows: list[dict[str, object]] = []
    for name, loader in (
        ("Breast Cancer Wisconsin Diagnostic", load_breast_cancer),
        ("Wine", load_wine),
    ):
        dataset = loader()
        x_train, x_test, y_train, y_test = train_test_split(
            dataset.data, dataset.target, test_size=0.25, stratify=dataset.target, random_state=42
        )
        del x_test, y_test
        for model_name, model in make_models(42).items():
            metrics = profile_fit(model, x_train, y_train)
            rows.append({"dataset": name, "model": model_name, **metrics})
    result = {
        "protocol": {
            "datasets": ["Breast Cancer Wisconsin Diagnostic", "Wine"],
            "seed": 42,
            "test_size": 0.25,
            "models": list(make_models(42)),
            "rss_sampling_interval_seconds": 0.01,
            "note": "Single-process representative profile; RSS includes interpreter and loaded libraries and is not a hardware-independent complexity measure.",
        },
        "environment": {
            "python": platform.python_version(),
            "psutil": version("psutil"),
        },
        "runs": rows,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"resource profile: PASS ({len(rows)} fits, output={OUTPUT.relative_to(ROOT)})")


if __name__ == "__main__":
    main()
