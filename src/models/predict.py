"""Model prediction utilities."""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from loguru import logger
from typing import Tuple, Dict, Any
import json


class ModelPredictor:
    """Make predictions with trained models."""
    
    def __init__(self, model_path: Path, threshold: float = 0.5):
        """Initialize ModelPredictor.
        
        Args:
            model_path: Path to saved model
            threshold: Classification threshold
        """
        self.model_path = Path(model_path)
        self.model = joblib.load(self.model_path)
        self.threshold = threshold
        self.feature_names = self._load_metadata()
        logger.info(f"Model loaded from {self.model_path}")
    
    def _load_metadata(self) -> list:
        """Load model metadata."""
        metadata_path = self.model_path.with_suffix('.json')
        if metadata_path.exists():
            with open(metadata_path) as f:
                metadata = json.load(f)
                return metadata.get('feature_names', [])
        return []
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Get prediction probabilities.
        
        Args:
            X: Input features
            
        Returns:
            Prediction probabilities
        """
        return self.model.predict_proba(X)
    
    def predict(self, X: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Make predictions.
        
        Args:
            X: Input features
            
        Returns:
            Tuple of (predictions, probabilities)
        """
        proba = self.predict_proba(X)
        predictions = (proba[:, 1] >= self.threshold).astype(int)
        return predictions, proba[:, 1]
    
    def predict_single(self, X: pd.DataFrame) -> Dict[str, Any]:
        """Make prediction for single record.
        
        Args:
            X: Single record features
            
        Returns:
            Prediction dictionary
        """
        predictions, probabilities = self.predict(X)
        
        return {
            "prediction": int(predictions[0]),
            "probability": float(probabilities[0]),
            "threshold": self.threshold
        }
