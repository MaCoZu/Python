"""File I/O utilities."""

from pathlib import Path
from typing import Any

import pandas as pd


def read_csv_auto(filepath: str | Path, **kwargs: Any) -> pd.DataFrame:
    """Read CSV with automatic type inference and cleaning.

    Args:
        filepath: Path to CSV file
        **kwargs: Additional arguments passed to pd.read_csv

    Returns:
        DataFrame with cleaned data

    Example:
        >>> df = read_csv_auto("data/myfile.csv")
    """
    df: pd.DataFrame = pd.read_csv(filepath, **kwargs)

    # Strip whitespace from string columns
    str_cols = df.select_dtypes(include=["object", "string"]).columns
    df[str_cols] = df[str_cols].apply(lambda x: x.str.strip())

    return df


def save_results(
    df: pd.DataFrame,
    filepath: str | Path,
    include_index: bool = False,
) -> None:
    """Save DataFrame with sensible defaults.

    Args:
        df: DataFrame to save
        filepath: Output path
        include_index: Whether to include index in output

    Example:
        >>> df = pd.DataFrame({"a": [1, 2, 3]})
        >>> save_results(df, "output.csv")
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    if filepath.suffix == ".csv":
        df.to_csv(filepath, index=include_index)
    elif filepath.suffix in [".xlsx", ".xls"]:
        df.to_excel(filepath, index=include_index)
    elif filepath.suffix == ".parquet":
        df.to_parquet(filepath, index=include_index)
    else:
        msg = f"Unsupported file format: {filepath.suffix}"
        raise ValueError(msg)
