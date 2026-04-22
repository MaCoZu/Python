"""Statistical utilities."""

import pandas as pd


def describe_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """Extended description of numeric columns including missing values.

    Args:
        df: Input DataFrame

    Returns:
        DataFrame with statistics for each numeric column

    Example:
        >>> df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, None]})
        >>> describe_numeric(df)
                  a    b
        count   3.0  2.0
        mean    2.0  4.5
        ...
    """
    numeric_df = df.select_dtypes(include=["number"])
    stats = numeric_df.describe().T

    # Add missing count and percentage
    stats["missing"] = numeric_df.isnull().sum()
    stats["missing_pct"] = (stats["missing"] / len(df)) * 100

    return stats


def detect_outliers(
    data: pd.Series,
    method: str = "iqr",
    threshold: float = 1.5,
) -> pd.Series:
    """Detect outliers in a numeric series.

    Args:
        data: Numeric series to check
        method: Method to use ('iqr' or 'zscore')
        threshold: Threshold for outlier detection (IQR multiplier or z-score)

    Returns:
        Boolean series indicating outliers

    Example:
        >>> data = pd.Series([1, 2, 2, 3, 100])
        >>> detect_outliers(data)
        0    False
        1    False
        2    False
        3    False
        4     True
        dtype: bool
    """
    if not pd.api.types.is_numeric_dtype(data):
        raise TypeError(f"Data must be numeric, got {data.dtype}")

    if method == "iqr":
        q1 = data.quantile(0.25)
        q3 = data.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - threshold * iqr
        upper_bound = q3 + threshold * iqr
        return (data < lower_bound) | (data > upper_bound)
    elif method == "zscore":
        mean = data.mean()
        std = data.std()
        if std == 0:
            return pd.Series([False] * len(data), index=data.index)
        z_scores = (data - mean) / std
        return z_scores.abs() > threshold
    else:
        msg = f"Unknown method: {method}"
        raise ValueError(msg)
