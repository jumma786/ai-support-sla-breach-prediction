"""Tests for data loading and preprocessing."""

import numpy as np
import pandas as pd

from src.data.preprocessor import DataPreprocessor
from src.data.validator import DataValidator


class TestDataValidator:
    def test_valid_data(self):
        df = pd.DataFrame({"id": [1, 2, 3], "value": [10.5, 20.5, 30.5]})
        result = DataValidator(required_columns=["id", "value"]).validate(df)
        assert result.is_valid is True
        assert result.duplicate_records == 0

    def test_missing_columns(self):
        df = pd.DataFrame({"id": [1, 2, 3]})
        result = DataValidator(required_columns=["id", "value"]).validate(df)
        assert result.is_valid is False
        assert "value" in result.missing_columns


class TestDataPreprocessor:
    def test_remove_duplicates(self):
        df = pd.DataFrame({"id": [1, 2, 2, 3], "value": [10, 20, 20, 30]})
        assert len(DataPreprocessor().remove_duplicates(df)) == 3

    def test_handle_missing_values(self):
        df = pd.DataFrame({"a": [1.0, 2.0, np.nan], "b": [10, 20, 30]})
        cleaned = DataPreprocessor().handle_missing_values(df, strategy="mean")
        assert cleaned.isnull().sum().sum() == 0
