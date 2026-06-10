"""Feature engineering utilities."""

import pandas as pd
import numpy as np
from typing import List
from loguru import logger


class FeatureEngineer:
    """Feature engineering and transformation."""
    
    def __init__(self):
        """Initialize FeatureEngineer."""
        pass
    
    def create_temporal_features(self, df: pd.DataFrame, datetime_col: str) -> pd.DataFrame:
        """Create temporal features from datetime column.
        
        Args:
            df: Input DataFrame
            datetime_col: Column name containing datetime values
            
        Returns:
            DataFrame with temporal features
        """
        df = df.copy()
        dt = pd.to_datetime(df[datetime_col])
        
        df['submitted_hour'] = dt.dt.hour
        df['submitted_dayofweek_num'] = dt.dt.dayofweek
        df['submitted_month'] = dt.dt.month
        df['is_weekend'] = dt.dt.dayofweek.isin([5, 6]).astype(int)
        
        logger.info(f"Created temporal features from {datetime_col}")
        return df
    
    def create_operational_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create operational risk features.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with operational features
        """
        df = df.copy()
        
        # Queue pressure
        if 'agent_queue_length_at_submit' in df.columns:
            df['queue_pressure'] = df['agent_queue_length_at_submit'] / df['agent_queue_length_at_submit'].max()
        
        # High backlog flag
        if 'backlog_age_hours' in df.columns:
            df['high_backlog_flag'] = (df['backlog_age_hours'] > df['backlog_age_hours'].quantile(0.75)).astype(int)
        
        logger.info("Created operational features")
        return df
    
    def create_text_features(self, df: pd.DataFrame, text_col: str) -> pd.DataFrame:
        """Create text-based features.
        
        Args:
            df: Input DataFrame
            text_col: Column name containing text
            
        Returns:
            DataFrame with text features
        """
        df = df.copy()
        
        # Word count
        df['message_word_count'] = df[text_col].str.split().str.len()
        
        # Deadline detection
        deadline_keywords = ['deadline', 'urgent', 'asap', 'immediately', 'critical']
        pattern = '|'.join(deadline_keywords)
        df['message_has_deadline'] = df[text_col].str.lower().str.contains(pattern, na=False).astype(int)
        
        logger.info(f"Created text features from {text_col}")
        return df
    
    def create_log_transforms(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Apply log transformation to specified columns.
        
        Args:
            df: Input DataFrame
            columns: Columns to transform
            
        Returns:
            DataFrame with log-transformed features
        """
        df = df.copy()
        
        for col in columns:
            if col in df.columns:
                df[f'{col}_log1p'] = np.log1p(df[col])
        
        logger.info(f"Created log transformations for {len(columns)} features")
        return df
