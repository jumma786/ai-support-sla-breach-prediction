"""Data loading utilities."""

import pandas as pd
from pathlib import Path
from typing import Optional, Union
from loguru import logger


class DataLoader:
    """Load and cache data from various sources."""
    
    def __init__(self, cache_enabled: bool = True):
        """Initialize DataLoader.
        
        Args:
            cache_enabled: Whether to cache loaded data in memory
        """
        self.cache_enabled = cache_enabled
        self._cache = {}
    
    def load_csv(self, filepath: Union[str, Path]) -> pd.DataFrame:
        """Load CSV file into DataFrame.
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            Loaded DataFrame
        """
        filepath = Path(filepath)
        cache_key = str(filepath)
        
        if self.cache_enabled and cache_key in self._cache:
            logger.info(f"Loaded from cache: {filepath.name}")
            return self._cache[cache_key].copy()
        
        logger.info(f"Loading CSV: {filepath}")
        df = pd.read_csv(filepath)
        
        if self.cache_enabled:
            self._cache[cache_key] = df.copy()
        
        logger.info(f"Loaded {len(df)} records from {filepath.name}")
        return df
    
    def load_parquet(self, filepath: Union[str, Path]) -> pd.DataFrame:
        """Load Parquet file into DataFrame.
        
        Args:
            filepath: Path to Parquet file
            
        Returns:
            Loaded DataFrame
        """
        filepath = Path(filepath)
        cache_key = str(filepath)
        
        if self.cache_enabled and cache_key in self._cache:
            logger.info(f"Loaded from cache: {filepath.name}")
            return self._cache[cache_key].copy()
        
        logger.info(f"Loading Parquet: {filepath}")
        df = pd.read_parquet(filepath)
        
        if self.cache_enabled:
            self._cache[cache_key] = df.copy()
        
        logger.info(f"Loaded {len(df)} records from {filepath.name}")
        return df
    
    def clear_cache(self):
        """Clear in-memory cache."""
        self._cache.clear()
        logger.info("Cache cleared")
