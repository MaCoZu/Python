"""Tests for I/O utilities."""

from pathlib import Path

import pandas as pd
import pytest

from SRC.utils.io import read_csv_auto, save_results


def test_save_and_read_csv(tmp_path: Path, sample_df: pd.DataFrame) -> None:
    """Test saving and reading CSV."""
    filepath = tmp_path / "test.csv"
    save_results(sample_df, filepath)

    assert filepath.exists()

    # Read back and verify
    df = pd.read_csv(filepath)
    assert len(df) == len(sample_df)


def test_save_results_creates_directory(tmp_path: Path, sample_df: pd.DataFrame) -> None:
    """Test that save_results creates parent directories."""
    filepath = tmp_path / "subdir" / "test.csv"
    save_results(sample_df, filepath)

    assert filepath.exists()
    assert filepath.parent.exists()


def test_save_results_unsupported_format(tmp_path: Path, sample_df: pd.DataFrame) -> None:
    """Test that unsupported format raises ValueError."""
    filepath = tmp_path / "test.txt"
    with pytest.raises(ValueError, match="Unsupported file format"):
        save_results(sample_df, filepath)


def test_read_csv_auto_strips_whitespace(tmp_path: Path) -> None:
    """Test that read_csv_auto strips whitespace."""
    filepath = tmp_path / "test.csv"
    df = pd.DataFrame({"name": [" Alice ", "  Bob  "], "age": [25, 30]})
    df.to_csv(filepath, index=False)

    result = read_csv_auto(filepath)
    assert result["name"].tolist() == ["Alice", "Bob"]
