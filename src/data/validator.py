"""Data validation utilities."""

import pandas as pd
from typing import List, Dict, Any
from dataclasses import dataclass
from loguru import logger


@dataclass
class ValidationResult:
    """Results of data validation."""
    is_valid: bool
    missing_columns: List[str]
    duplicate_records: int
    missing_values: Dict[str, int]
    issues: List[str]


class DataValidator:
    """Validate data quality and schema."""
    
    def __init__(self, required_columns: List[str]):
        """Initialize DataValidator.
        
        Args:
            required_columns: List of required column names
        """
        self.required_columns = required_columns
    
    def validate(self, df: pd.DataFrame) -> ValidationResult:
        """Validate DataFrame.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            ValidationResult object
        """
        issues = []
        missing_columns = []
        
        # Check required columns
        actual_columns = set(df.columns)
        required = set(self.required_columns)
        missing_columns = list(required - actual_columns)
        
        if missing_columns:
            issues.append(f"Missing columns: {missing_columns}")
        
        # Check duplicates
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            issues.append(f"Found {duplicates} duplicate records")
        
        # Check missing values
        missing_values = df.isnull().sum().to_dict()
        missing_values = {k: v for k, v in missing_values.items() if v > 0}
        
        if missing_values:
            issues.append(f"Missing values: {missing_values}")
        
        is_valid = len(issues) == 0
        
        result = ValidationResult(
            is_valid=is_valid,
            missing_columns=missing_columns,
            duplicate_records=duplicates,
            missing_values=missing_values,
            issues=issues
        )
        
        if is_valid:
            logger.info("Data validation passed")
        else:
            logger.warning(f"Data validation issues: {issues}")
        
        return result
