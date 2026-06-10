"""Model evaluation utilities."""

import pandas as pd
import numpy as np
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score, 
    precision_recall_curve, f1_score, precision_score, recall_score
)
from loguru import logger
from typing import Dict, Any, Tuple


class ModelEvaluator:
    """Evaluate model performance."""
    
    def __init__(self):
        """Initialize ModelEvaluator."""
        pass
    
    def evaluate(self, y_true: np.ndarray, y_pred: np.ndarray, y_pred_proba: np.ndarray = None) -> Dict[str, Any]:
        """Evaluate model performance.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_pred_proba: Predicted probabilities
            
        Returns:
            Evaluation metrics dictionary
        """
        metrics = {
            "accuracy": float((y_true == y_pred).mean()),
            "precision": float(precision_score(y_true, y_pred, zero_division=0)),
            "recall": float(recall_score(y_true, y_pred, zero_division=0)),
            "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        }
        
        if y_pred_proba is not None:
            metrics["roc_auc"] = float(roc_auc_score(y_true, y_pred_proba))
        
        confusion = confusion_matrix(y_true, y_pred)
        metrics["confusion_matrix"] = confusion.tolist()
        
        logger.info(f"Evaluation metrics: {metrics}")
        return metrics
    
    def find_optimal_threshold(self, y_true: np.ndarray, y_pred_proba: np.ndarray) -> Tuple[float, float]:
        """Find optimal classification threshold.
        
        Args:
            y_true: True labels
            y_pred_proba: Predicted probabilities
            
        Returns:
            Tuple of (optimal_threshold, best_f1_score)
        """
        precisions, recalls, thresholds = precision_recall_curve(y_true, y_pred_proba)
        f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-10)
        
        optimal_idx = np.argmax(f1_scores)
        optimal_threshold = thresholds[optimal_idx]
        best_f1 = f1_scores[optimal_idx]
        
        logger.info(f"Optimal threshold: {optimal_threshold:.4f}, F1 score: {best_f1:.4f}")
        return optimal_threshold, best_f1
