"""Data preprocessing utilities."""

import pandas as pd
import numpy as np
from typing import Tuple, Optional
from sklearn.preprocessing import StandardScaler
from loguru import logger


class DataPreprocessor:
    """Handle data preprocessing tasks."""
    
    def __init__(self):
        """Initialize DataPreprocessor."""
        self.scaler = StandardScaler()
        self._fitted = False
    
    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate records.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with duplicates removed
        """
        initial_count = len(df)
        df = df.drop_duplicates()
        removed = initial_count - len(df)
        
        logger.info(f"Removed {removed} duplicate records")
        return df
    
    def handle_missing_values(self, df: pd.DataFrame, strategy: str = "mean") -> pd.DataFrame:
        """Handle missing values.
        
        Args:
            df: Input DataFrame
            strategy: Strategy for handling missing values (mean, median, drop)
            
        Returns:
            DataFrame with missing values handled
        """
        missing_count = df.isnull().sum().sum()
        
        if missing_count == 0:
            logger.info("No missing values found")
            return df
        
        if strategy == "mean":
            df = df.fillna(df.mean(numeric_only=True))
        elif strategy == "median":
            df = df.fillna(df.median(numeric_only=True))
        elif strategy == "drop":
            df = df.dropna()
        
        logger.info(f"Handled {missing_count} missing values using {strategy} strategy")
        return df
    
    def scale_features(self, X: pd.DataFrame, fit: bool = False) -> pd.DataFrame:
        """Scale numerical features.
        
        Args:
            X: Input features
            fit: Whether to fit the scaler
            
        Returns:
            Scaled features
        """
        if fit:
            X_scaled = self.scaler.fit_transform(X)
            self._fitted = True
        else:
            if not self._fitted:
                raise ValueError("Scaler not fitted. Call with fit=True first.")
            X_scaled = self.scaler.transform(X)
        
        logger.info(f"Scaled {X.shape[1]} features")
        return pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
