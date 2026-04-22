"""Tests for plotting utilities."""

import pandas as pd

from SRC.utils.plotting import correlation_heatmap, quick_hist


def test_quick_hist(numeric_series: pd.Series) -> None:
    """Test quick histogram creation."""
    ax = quick_hist(numeric_series, bins=10, title="Test Plot")
    assert ax is not None
    assert ax.get_title() == "Test Plot"
    assert ax.get_xlabel() == "values"


def test_quick_hist_defaults(numeric_series: pd.Series) -> None:
    """Test quick histogram with default parameters."""
    ax = quick_hist(numeric_series)
    assert ax is not None
    assert "Distribution of values" in ax.get_title()


def test_correlation_heatmap(sample_df: pd.DataFrame) -> None:
    """Test correlation heatmap creation."""
    ax = correlation_heatmap(sample_df)
    assert ax is not None
    assert ax.get_title() == "Correlation Heatmap"


def test_correlation_heatmap_custom_size(sample_df: pd.DataFrame) -> None:
    """Test correlation heatmap with custom size."""
    ax = correlation_heatmap(sample_df, figsize=(8, 6))
    assert ax is not None
    fig = ax.get_figure()
    assert fig is not None
    assert fig.get_figwidth() == 8
    assert fig.get_figheight() == 6
