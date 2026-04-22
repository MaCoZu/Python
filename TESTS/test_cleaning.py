"""Tests for cleaning utilities."""

import pandas as pd

from SRC.utils.cleaning import clean_columns, clean_text, handle_missing


def test_clean_columns(sample_df: pd.DataFrame) -> None:
    """Test column name cleaning."""
    result = clean_columns(sample_df)
    expected = ["first_name", "last_name", "age", "score"]
    assert result.columns.tolist() == expected


def test_clean_columns_does_not_modify_original(sample_df: pd.DataFrame) -> None:
    """Test that clean_columns returns a copy."""
    original_columns = sample_df.columns.tolist()
    clean_columns(sample_df)
    assert sample_df.columns.tolist() == original_columns


def test_clean_text() -> None:
    """Test text cleaning."""
    text = "Hello, World! 123  Extra   Spaces"
    result = clean_text(text)
    assert result == "hello world 123 extra spaces"


def test_clean_text_empty() -> None:
    """Test cleaning empty text."""
    assert clean_text("") == ""


def test_handle_missing_drop(df_with_missing: pd.DataFrame) -> None:
    """Test dropping missing values."""
    result = handle_missing(df_with_missing, strategy="drop", threshold=0.5)
    # Column 'b' should be dropped (100% missing)
    assert "b" not in result.columns
    # Rows with missing 'a' should be dropped
    assert len(result) == 3
    assert result["a"].tolist() == [1.0, 2.0, 4.0]


def test_handle_missing_mean(df_with_missing: pd.DataFrame) -> None:
    """Test filling with mean."""
    result = handle_missing(df_with_missing, strategy="mean")
    # Mean of [1, 2, 4] is 2.333...
    assert result["a"].isna().sum() == 0
    assert abs(result["a"].iloc[2] - 2.333) < 0.01


def test_handle_missing_median(df_with_missing: pd.DataFrame) -> None:
    """Test filling with median."""
    result = handle_missing(df_with_missing, strategy="median")
    # Median of [1, 2, 4] is 2
    assert result["a"].isna().sum() == 0
    assert result["a"].iloc[2] == 2.0


def test_handle_missing_forward_fill() -> None:
    """Test forward fill strategy."""
    df = pd.DataFrame({"x": [1.0, None, None, 4.0]})
    result = handle_missing(df, strategy="forward_fill")
    assert result["x"].tolist() == [1.0, 1.0, 1.0, 4.0]
