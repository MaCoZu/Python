"""Tests for statistical utilities."""

import pandas as pd
import pytest

from SRC.utils.stats import describe_numeric, detect_outliers


def test_describe_numeric(df_with_missing: pd.DataFrame) -> None:
    """Test extended numeric description."""
    result = describe_numeric(df_with_missing)
    assert "missing" in result.columns
    assert "missing_pct" in result.columns
    assert result.loc["a", "missing"] == 1
    # Column 'c' has no missing values
    assert result.loc["c", "missing"] == 0
    assert result.loc["a", "missing_pct"] == 25.0


def test_describe_numeric_no_missing(sample_df: pd.DataFrame) -> None:
    """Test description with no missing values."""
    result = describe_numeric(sample_df)
    assert (result["missing"] == 0).all()
    assert (result["missing_pct"] == 0).all()


def test_detect_outliers_iqr(numeric_series: pd.Series) -> None:
    """Test IQR outlier detection."""
    outliers = detect_outliers(numeric_series, method="iqr", threshold=1.5)
    # 100 should be detected as an outlier
    assert outliers.iloc[-1]
    # Other values should not be outliers
    assert outliers.iloc[:-1].sum() == 0


def test_detect_outliers_zscore(numeric_series: pd.Series) -> None:
    """Test z-score outlier detection."""
    outliers = detect_outliers(numeric_series, method="zscore", threshold=2.0)
    # 100 should be detected as an outlier
    assert outliers.iloc[-1]


def test_detect_outliers_invalid_method(numeric_series: pd.Series) -> None:
    """Test that invalid method raises ValueError."""
    with pytest.raises(ValueError, match="Unknown method"):
        detect_outliers(numeric_series, method="invalid")
