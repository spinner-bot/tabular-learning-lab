"""Smoke test for sklearn-based lessons 11-12, 22-24."""

from sklearn.calibration import calibration_curve
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import brier_score_loss
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def main() -> None:
    X, y = load_breast_cancer(return_X_y=True)
    x_train, x_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    model = make_pipeline(
        StandardScaler(),
        MLPClassifier(
            hidden_layer_sizes=(32,),
            early_stopping=True,
            max_iter=100,
            random_state=42,
        ),
    )
    model.fit(x_train, y_train)
    probabilities = model.predict_proba(x_test)[:, 1]
    fraction, mean = calibration_curve(y_test, probabilities, n_bins=5)
    assert len(fraction) == len(mean)
    assert 0 <= brier_score_loss(y_test, probabilities) <= 1
    print("deep/calibration smoke test: PASS")


if __name__ == "__main__":
    main()
