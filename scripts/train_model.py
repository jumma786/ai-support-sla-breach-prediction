"""Train the SLA breach prediction pipeline on the API's input features.

Usage:
    python scripts/train_model.py

Saves models/sla_breach_pipeline.joblib (+ .json metadata) so the FastAPI
service can load it at startup.
"""

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import (
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "01_Data" / "processed data" / "model_ready_support_sla_sample.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "sla_breach_pipeline.joblib"

# Must match TicketPredictionRequest in src/api/schemas.py
CATEGORICAL_FEATURES = ["customer_segment", "priority_initial", "issue_category"]
NUMERIC_FEATURES = [
    "agent_queue_length_at_submit",
    "backlog_age_hours",
    "negative_sentiment_flag",
    "message_has_deadline",
]
FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES
TARGET = "sla_breached"


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    df = df.dropna(subset=FEATURES + [TARGET])
    X, y = df[FEATURES], df[TARGET].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    pipeline = Pipeline(
        [
            (
                "preprocess",
                ColumnTransformer(
                    [("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES)],
                    remainder="passthrough",
                ),
            ),
            (
                "model",
                GradientBoostingClassifier(
                    n_estimators=200, learning_rate=0.1, max_depth=4, random_state=42
                ),
            ),
        ]
    )

    pipeline.fit(X_train, y_train)

    proba = pipeline.predict_proba(X_test)[:, 1]
    pred = (proba >= 0.5).astype(int)
    metrics = {
        "precision": round(precision_score(y_test, pred), 4),
        "recall": round(recall_score(y_test, pred), 4),
        "f1": round(f1_score(y_test, pred), 4),
        "roc_auc": round(roc_auc_score(y_test, proba), 4),
    }
    print(f"Test metrics: {metrics}")

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    MODEL_PATH.with_suffix(".json").write_text(
        json.dumps(
            {
                "model_type": "gradient_boosting",
                "feature_names": FEATURES,
                "target": TARGET,
                "metrics": metrics,
                "random_state": 42,
            },
            indent=2,
        )
    )
    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    main()
