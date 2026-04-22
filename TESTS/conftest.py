"""Shared pytest fixtures."""

import sys
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pandas as pd
import pytest

# Add SRC to path for imports
_src = Path(__file__).parent.parent / "SRC"
if str(_src) not in sys.path:
    sys.path.insert(0, str(_src))


@pytest.fixture
def sample_df() -> Iterator[pd.DataFrame]:
    """Sample DataFrame for testing."""
    yield pd.DataFrame(
        {
            "First Name": ["Alice", "Bob", "Charlie"],
            "Last-Name": ["Smith", "Jones", "Brown"],
            " Age ": [25, 30, 35],
            "Score": [85.5, 90.0, 88.5],
        }
    )


@pytest.fixture
def df_with_missing() -> Iterator[pd.DataFrame]:
    """DataFrame with missing values."""
    yield pd.DataFrame(
        {
            "a": [1.0, 2.0, None, 4.0],
            "b": [None, None, None, None],  # All missing
            "c": [5.0, 6.0, 7.0, 8.0],
        }
    )


@pytest.fixture
def numeric_series() -> Iterator[pd.Series[Any]]:
    """Numeric series for testing."""
    yield pd.Series([1, 2, 2, 3, 3, 3, 4, 100], name="values")
