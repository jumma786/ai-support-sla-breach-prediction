"""Model training utilities."""

import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
import joblib
from pathlib import Path
from loguru import logger
from typing import Tuple, Dict, Any
import json


class ModelTrainer:
    """Train and save ML models."""
    
    def __init__(self, model_type: str = "gradient_boosting", random_state: int = 42):
        """Initialize ModelTrainer.
        
        Args:
            model_type: Type of model to train
            random_state: Random state for reproducibility
        """
        self.model_type = model_type
        self.random_state = random_state
        self.model = None
        self.feature_names = None
    
    def _build_model(self):
        """Build the model based on type."""
        if self.model_type == "gradient_boosting":
            self.model = GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=self.random_state
            )
        elif self.model_type == "random_forest":
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=self.random_state
            )
        elif self.model_type == "logistic_regression":
            self.model = LogisticRegression(random_state=self.random_state)
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def train(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, Any]:
        """Train the model.
        
        Args:
            X: Training features
            y: Training target
            
        Returns:
            Training results dictionary
        """
        self.feature_names = X.columns.tolist()
        self._build_model()
        
        logger.info(f"Training {self.model_type} model with {X.shape[0]} samples...")
        self.model.fit(X, y)
        
        train_score = self.model.score(X, y)
        logger.info(f"Training accuracy: {train_score:.4f}")
        
        return {"train_accuracy": train_score, "model": self.model}
    
    def cross_validate(self, X: pd.DataFrame, y: pd.Series, cv: int = 5) -> Dict[str, Any]:
        """Perform cross-validation.
        
        Args:
            X: Features
            y: Target
            cv: Number of folds
            
        Returns:
            Cross-validation results
        """
        self._build_model()
        
        scores = cross_val_score(self.model, X, y, cv=cv, scoring='f1_weighted')
        
        logger.info(f"Cross-validation scores: {scores}")
        logger.info(f"Mean CV score: {scores.mean():.4f} (+/- {scores.std():.4f})")
        
        return {
            "scores": scores,
            "mean": scores.mean(),
            "std": scores.std()
        }
    
    def save_model(self, filepath: Path) -> None:
        """Save trained model to disk.
        
        Args:
            filepath: Path to save model
        """
        if self.model is None:
            raise ValueError("No model trained yet")
        
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        joblib.dump(self.model, filepath)
        logger.info(f"Model saved to {filepath}")
        
        # Save metadata
        metadata = {
            "model_type": self.model_type,
            "feature_names": self.feature_names,
            "random_state": self.random_state
        }
        metadata_path = filepath.with_suffix('.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        logger.info(f"Metadata saved to {metadata_path}")
