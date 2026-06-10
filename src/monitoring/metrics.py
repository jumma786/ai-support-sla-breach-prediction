"""Performance monitoring utilities."""

import pandas as pd
from datetime import datetime
from loguru import logger
from typing import Dict, Any
import json


class PerformanceMonitor:
    """Monitor model performance over time."""
    
    def __init__(self):
        """Initialize PerformanceMonitor."""
        self.metrics_history = []
    
    def log_prediction(self, prediction: float, actual: bool, features: dict) -> None:
        """Log a prediction for monitoring.
        
        Args:
            prediction: Model prediction probability
            actual: Actual outcome
            features: Input features
        """
        record = {
            "timestamp": datetime.now().isoformat(),
            "prediction": prediction,
            "actual": actual,
            "error": abs(prediction - int(actual))
        }
        self.metrics_history.append(record)
        logger.debug(f"Logged prediction: {record}")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary.
        
        Returns:
            Performance summary dictionary
        """
        if not self.metrics_history:
            return {"total_predictions": 0}
        
        df = pd.DataFrame(self.metrics_history)
        
        return {
            "total_predictions": len(df),
            "mean_error": float(df["error"].mean()),
            "max_error": float(df["error"].max()),
            "min_error": float(df["error"].min())
        }
