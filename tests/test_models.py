"""Tests for model training and evaluation."""

import numpy as np
import pandas as pd
import pytest
from sklearn.datasets import make_classification

from src.models.evaluate import ModelEvaluator
from src.models.train import ModelTrainer


@pytest.fixture
def sample_data():
    X, y = make_classification(n_samples=100, n_features=10, n_classes=2, random_state=42)
    return pd.DataFrame(X, columns=[f"feature_{i}" for i in range(10)]), pd.Series(y)


class TestModelTrainer:
    def test_training(self, sample_data):
        X, y = sample_data
        trainer = ModelTrainer(model_type="gradient_boosting")
        results = trainer.train(X, y)
        assert trainer.model is not None
        assert results["train_accuracy"] > 0.5

    def test_cross_validation(self, sample_data):
        X, y = sample_data
        cv = ModelTrainer(model_type="random_forest").cross_validate(X, y, cv=3)
        assert len(cv["scores"]) == 3


class TestModelEvaluator:
    def test_metrics(self):
        y_true = np.array([0, 1, 1, 0, 1, 0, 1, 1])
        y_pred = np.array([0, 1, 0, 0, 1, 1, 1, 1])
        y_proba = np.array([0.1, 0.9, 0.4, 0.2, 0.8, 0.6, 0.7, 0.95])
        metrics = ModelEvaluator().evaluate(y_true, y_pred, y_proba)
        for key in ("accuracy", "precision", "recall", "f1", "roc_auc"):
            assert key in metrics

    def test_optimal_threshold(self):
        y_true = np.array([0, 0, 0, 1, 1, 1])
        y_proba = np.array([0.1, 0.2, 0.3, 0.7, 0.8, 0.9])
        threshold, f1 = ModelEvaluator().find_optimal_threshold(y_true, y_proba)
        assert 0.0 <= threshold <= 1.0
        assert 0.0 <= f1 <= 1.0
