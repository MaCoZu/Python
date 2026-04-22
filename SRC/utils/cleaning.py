"""Data cleaning utilities."""

import re
from typing import Literal

import pandas as pd


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Clean column names: lowercase, strip, replace spaces/hyphens with underscores.

    Args:
        df: Input DataFrame

    Returns:
        DataFrame with cleaned column names

    Example:
        >>> df = pd.DataFrame({"First Name": [1], "Last-Name": [2]})
        >>> clean_columns(df).columns.tolist()
        ['first_name', 'last_name']
    """
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    return df


def clean_text(text: str) -> str:
    """Clean text: lowercase, remove non-alphanumeric, normalize whitespace.

    Args:
        text: Input text string

    Returns:
        Cleaned text string

    Example:
        >>> clean_text("Hello, World!")
        'hello world'
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def handle_missing(
    df: pd.DataFrame,
    strategy: Literal["drop", "mean", "median", "forward_fill"] = "drop",
    threshold: float = 0.5,
) -> pd.DataFrame:
    """Handle missing values with various strategies.

    Args:
        df: Input DataFrame
        strategy: How to handle missing values
        threshold: For 'drop' strategy, drop columns with >threshold proportion missing

    Returns:
        DataFrame with missing values handled

    Example:
        >>> df = pd.DataFrame({"a": [1, 2, None], "b": [4, 5, 6]})
        >>> handle_missing(df, strategy="drop")
           a    b
        0  1.0  4
        1  2.0  5
    """
    df = df.copy()

    if strategy == "drop":
        # Drop columns with too many missing values
        missing_prop = df.isnull().mean()
        cols_to_keep = missing_prop[missing_prop <= threshold].index
        df = df[cols_to_keep]
        # Drop remaining rows with any missing
        df = df.dropna()
    elif strategy == "mean":
        numeric_cols = df.select_dtypes(include=["number"]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    elif strategy == "median":
        numeric_cols = df.select_dtypes(include=["number"]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    elif strategy == "forward_fill":
        df = df.ffill()

    return df
