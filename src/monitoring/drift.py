"""Data drift detection utilities."""

import pandas as pd
import numpy as np
from scipy.stats import ks_2samp, chi2_contingency
from loguru import logger
from typing import Dict, Any


class DriftDetector:
    """Detect data drift between datasets."""
    
    def __init__(self, threshold: float = 0.05):
        """Initialize DriftDetector.
        
        Args:
            threshold: P-value threshold for drift detection
        """
        self.threshold = threshold
    
    def detect_psi(self, expected: pd.Series, actual: pd.Series, bins: int = 10) -> float:
        """Detect drift using Population Stability Index (PSI).
        
        Args:
            expected: Expected distribution
            actual: Actual distribution
            bins: Number of bins
            
        Returns:
            PSI value
        """
        expected_prop, bin_edges = np.histogram(expected, bins=bins)
        expected_prop = expected_prop / expected_prop.sum()
        
        actual_prop, _ = np.histogram(actual, bins=bin_edges)
        actual_prop = actual_prop / actual_prop.sum()
        
        psi = np.sum((actual_prop - expected_prop) * np.log(actual_prop / (expected_prop + 1e-10)))
        return float(psi)
    
    def detect_ks(self, expected: pd.Series, actual: pd.Series) -> Tuple[float, float]:
        """Detect drift using Kolmogorov-Smirnov test.
        
        Args:
            expected: Expected distribution
            actual: Actual distribution
            
        Returns:
            Tuple of (statistic, p_value)
        """
        statistic, p_value = ks_2samp(expected, actual)
        return float(statistic), float(p_value)
    
    def check_drift(self, expected: pd.DataFrame, actual: pd.DataFrame) -> Dict[str, Any]:
        """Check for drift across multiple features.
        
        Args:
            expected: Expected data
            actual: Actual data
            
        Returns:
            Drift detection results
        """
        results = {"drift_detected": False, "features": {}}
        
        for col in expected.columns:
            if col not in actual.columns:
                continue
            
            if expected[col].dtype in ['float64', 'int64']:
                stat, p_value = self.detect_ks(expected[col], actual[col])
                drifted = p_value < self.threshold
                results["features"][col] = {
                    "type": "numerical",
                    "ks_statistic": stat,
                    "p_value": p_value,
                    "drifted": drifted
                }
                if drifted:
                    results["drift_detected"] = True
        
        if results["drift_detected"]:
            logger.warning(f"Drift detected in features: {[f for f, d in results['features'].items() if d['drifted']]}")
        else:
            logger.info("No drift detected")
        
        return results
