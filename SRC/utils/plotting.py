"""Custom plotting utilities."""

from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def quick_hist(
    data: pd.Series,
    bins: int = 30,
    title: str | None = None,
    xlabel: str | None = None,
) -> Any:
    """Create a quick histogram with sensible defaults.

    Args:
        data: Series to plot
        bins: Number of bins
        title: Plot title (defaults to series name)
        xlabel: X-axis label (defaults to series name)

    Returns:
        Matplotlib axes object

    Example:
        >>> import pandas as pd
        >>> data = pd.Series([1, 2, 2, 3, 3, 3])
        >>> ax = quick_hist(data, title="Distribution")
    """
    _fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(data.dropna(), bins=bins, edgecolor="black", alpha=0.7)
    ax.set_title(title or f"Distribution of {data.name}")
    ax.set_xlabel(xlabel or str(data.name))
    ax.set_ylabel("Frequency")
    ax.grid(alpha=0.3)
    return ax


def correlation_heatmap(df: pd.DataFrame, figsize: tuple[int, int] = (12, 10)) -> Any:
    """Create a correlation heatmap for numeric columns.

    Args:
        df: DataFrame with numeric columns
        figsize: Figure size as (width, height)

    Returns:
        Matplotlib axes object

    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({"a": [1, 2, 3], "b": [2, 4, 6]})
        >>> ax = correlation_heatmap(df)
    """
    numeric_df = df.select_dtypes(include=["number"])
    corr = numeric_df.corr()

    _fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        square=True,
        linewidths=1,
        ax=ax,
    )
    ax.set_title("Correlation Heatmap")
    return ax
