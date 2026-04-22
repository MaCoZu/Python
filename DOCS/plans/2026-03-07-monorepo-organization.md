# Monorepo Organization Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Transform Python learning repository into a professional monorepo with strict tooling, efficient dependency management, and reusable utilities.

**Architecture:** Workspace monorepo with flat topic folders, single utils package, uv for dependencies, ruff/mypy for code quality, pytest for testing, pre-commit hooks and CI/CD for automation.

**Tech Stack:** uv, ruff, mypy, pytest, pre-commit, GitHub Actions

---

## Task 1: Create Directory Structure

**Files:**
- Create: `numpy/`
- Create: `sklearn/`
- Create: `visualization/`
- Create: `statistics/`
- Create: `sql/`
- Create: `utils/`
- Create: `tests/`
- Create: `tests/fixtures/`
- Create: `docs/notes/`
- Create: `.github/workflows/`

**Step 1: Create all required directories**

Run:
```bash
mkdir -p numpy sklearn visualization statistics sql utils tests/fixtures docs/notes .github/workflows
```

Expected: Directories created silently

**Step 2: Verify directory structure**

Run:
```bash
ls -d */ | sort
```

Expected output should include:
```
.github/
Code Challenges/
Misc/
Pandas/
Python/
data/
docs/
images/
numpy/
sklearn/
sql/
statistics/
tests/
utils/
visualization/
```

**Step 3: Commit directory structure**

Run:
```bash
git add numpy/ sklearn/ visualization/ statistics/ sql/ utils/ tests/ docs/notes/ .github/workflows/
git commit -m "feat: create monorepo directory structure

Add topic folders for numpy, sklearn, visualization, statistics, sql
Add utils package and tests directory
Add docs/notes for learning documentation

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

Expected: Commit created successfully

---

## Task 2: Setup pyproject.toml with uv

**Files:**
- Create: `pyproject.toml`

**Step 1: Check if uv is installed**

Run:
```bash
uv --version
```

Expected: Version output like "uv 0.x.x"
If not installed, run: `curl -LsSf https://astral.sh/uv/install.sh | sh`

**Step 2: Initialize uv project**

Run:
```bash
uv init --name python-ds-learning --no-readme
```

Expected: Creates pyproject.toml with basic structure

**Step 3: Replace pyproject.toml with full configuration**

Create file `pyproject.toml`:

```toml
[project]
name = "python-ds-learning"
version = "0.1.0"
description = "Comprehensive Python and Data Science learning repository"
requires-python = ">=3.14"
dependencies = [
    "pandas>=3.0.0",
    "numpy>=2.0.0",
    "scipy>=1.14.0",
    "matplotlib>=3.9.0",
    "seaborn>=0.13.0",
    "jupyter>=1.1.0",
    "ipykernel>=6.29.0",
]

[project.optional-dependencies]
ml = [
    "scikit-learn>=1.5.0",
    "xgboost>=2.1.0",
]

viz = [
    "plotly>=5.24.0",
    "altair>=5.4.0",
]

db = [
    "sqlalchemy>=2.0.0",
    "duckdb>=1.1.0",
]

web = [
    "requests>=2.32.0",
    "beautifulsoup4>=4.12.0",
    "httpx>=0.27.0",
]

dev = [
    "ruff>=0.8.0",
    "mypy>=1.13.0",
    "pytest>=8.3.0",
    "pre-commit>=4.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
target-version = "py314"
line-length = 100

lint.select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # pyflakes
    "I",      # isort (import sorting)
    "N",      # pep8-naming
    "UP",     # pyupgrade (modern Python syntax)
    "B",      # flake8-bugbear (common bugs)
    "C4",     # flake8-comprehensions
    "SIM",    # flake8-simplify
    "PTH",    # flake8-use-pathlib
    "RUF",    # Ruff-specific rules
]

lint.ignore = [
    "E501",   # Line too long (handled by formatter)
]

exclude = [
    ".venv",
    "__pycache__",
    "*.ipynb",
]

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["N802", "F401"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.mypy]
python_version = "3.14"
strict = true
warn_unused_ignores = true
warn_return_any = true
warn_unreachable = true
show_error_codes = true
ignore_missing_imports = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[[tool.mypy.overrides]]
module = "utils.*"
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--strict-markers",
    "--tb=short",
]
```

**Step 4: Install base dependencies**

Run:
```bash
uv sync
```

Expected: Dependencies installed, uv.lock created

**Step 5: Install dev dependencies**

Run:
```bash
uv sync --extra dev
```

Expected: ruff, mypy, pytest, pre-commit installed

**Step 6: Verify installation**

Run:
```bash
uv run ruff --version && uv run mypy --version && uv run pytest --version
```

Expected: Version outputs for all three tools

**Step 7: Commit configuration**

Run:
```bash
git add pyproject.toml uv.lock
git commit -m "feat: configure uv workspace with dependencies

- Add base dependencies (pandas, numpy, scipy, jupyter)
- Add optional groups (ml, viz, db, web, dev)
- Configure ruff with strict rules
- Configure mypy with strict mode
- Configure pytest

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

Expected: Commit created successfully

---

## Task 3: Create Utils Package

**Files:**
- Create: `utils/__init__.py`
- Create: `utils/cleaning.py`
- Create: `utils/plotting.py`
- Create: `utils/stats.py`
- Create: `utils/io.py`
- Create: `utils/text.py`

**Step 1: Create utils/__init__.py**

Create file `utils/__init__.py`:

```python
"""Reusable utilities for data science workflows."""

from utils.cleaning import clean_columns, clean_text, handle_missing
from utils.plotting import quick_hist, correlation_heatmap
from utils.stats import describe_numeric, detect_outliers
from utils.io import read_csv_auto, save_results

__all__ = [
    # Cleaning
    "clean_columns",
    "clean_text",
    "handle_missing",
    # Plotting
    "quick_hist",
    "correlation_heatmap",
    # Stats
    "describe_numeric",
    "detect_outliers",
    # IO
    "read_csv_auto",
    "save_results",
]
```

**Step 2: Create utils/cleaning.py**

Create file `utils/cleaning.py`:

```python
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
    strategy: Literal["drop", "mean", "median", "mode", "forward_fill"] = "drop",
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
           b
        0  4
        1  5
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
```

**Step 3: Create utils/plotting.py**

Create file `utils/plotting.py`:

```python
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
    fig, ax = plt.subplots(figsize=(10, 6))
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

    fig, ax = plt.subplots(figsize=figsize)
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
```

**Step 4: Create utils/stats.py**

Create file `utils/stats.py`:

```python
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
        z_scores = (data - mean) / std
        return z_scores.abs() > threshold
    else:
        msg = f"Unknown method: {method}"
        raise ValueError(msg)
```

**Step 5: Create utils/io.py**

Create file `utils/io.py`:

```python
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
    df = pd.read_csv(filepath, **kwargs)

    # Strip whitespace from string columns
    str_cols = df.select_dtypes(include=["object"]).columns
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
```

**Step 6: Create utils/text.py**

Create file `utils/text.py`:

```python
"""Text processing utilities."""

import re


def remove_urls(text: str) -> str:
    """Remove URLs from text.

    Args:
        text: Input text

    Returns:
        Text with URLs removed

    Example:
        >>> remove_urls("Check https://example.com for more")
        'Check  for more'
    """
    url_pattern = r"https?://\S+|www\.\S+"
    return re.sub(url_pattern, "", text)


def remove_mentions(text: str) -> str:
    """Remove @mentions from text.

    Args:
        text: Input text

    Returns:
        Text with mentions removed

    Example:
        >>> remove_mentions("Hello @user nice to meet you")
        'Hello  nice to meet you'
    """
    return re.sub(r"@\w+", "", text)


def normalize_whitespace(text: str) -> str:
    """Normalize whitespace in text.

    Args:
        text: Input text

    Returns:
        Text with normalized whitespace

    Example:
        >>> normalize_whitespace("Hello    world\\n\\n  test")
        'Hello world test'
    """
    return re.sub(r"\s+", " ", text).strip()
```

**Step 7: Format utils package with ruff**

Run:
```bash
uv run ruff format utils/
```

Expected: Files formatted

**Step 8: Type check utils package with mypy**

Run:
```bash
uv run mypy utils/
```

Expected: Success: no issues found

**Step 9: Commit utils package**

Run:
```bash
git add utils/
git commit -m "feat: create utils package with typed utilities

Add modules:
- cleaning: column/text cleaning, missing value handling
- plotting: quick histograms, correlation heatmaps
- stats: extended descriptions, outlier detection
- io: CSV reading/writing with defaults
- text: URL/mention removal, whitespace normalization

All functions include type hints, docstrings, and examples

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

Expected: Commit created successfully

---

## Task 4: Create Tests for Utils Package

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/conftest.py`
- Create: `tests/test_cleaning.py`
- Create: `tests/test_plotting.py`
- Create: `tests/test_stats.py`
- Create: `tests/test_io.py`
- Create: `tests/test_text.py`

**Step 1: Create tests/__init__.py**

Create empty file `tests/__init__.py`:

```python
"""Tests for utils package."""
```

**Step 2: Create tests/conftest.py**

Create file `tests/conftest.py`:

```python
"""Shared pytest fixtures."""

import pandas as pd
import pytest


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """Sample DataFrame for testing."""
    return pd.DataFrame(
        {
            "First Name": ["Alice", "Bob", "Charlie"],
            "Last-Name": ["Smith", "Jones", "Brown"],
            " Age ": [25, 30, 35],
            "Score": [85.5, 90.0, 88.5],
        }
    )


@pytest.fixture
def df_with_missing() -> pd.DataFrame:
    """DataFrame with missing values."""
    return pd.DataFrame(
        {
            "a": [1.0, 2.0, None, 4.0],
            "b": [None, None, None, None],  # All missing
            "c": [5.0, 6.0, 7.0, 8.0],
        }
    )


@pytest.fixture
def numeric_series() -> pd.Series:
    """Numeric series for testing."""
    return pd.Series([1, 2, 2, 3, 3, 3, 4, 100], name="values")
```

**Step 3: Create tests/test_cleaning.py**

Create file `tests/test_cleaning.py`:

```python
"""Tests for cleaning utilities."""

import pandas as pd
import pytest

from utils.cleaning import clean_columns, clean_text, handle_missing


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
```

**Step 4: Create tests/test_plotting.py**

Create file `tests/test_plotting.py`:

```python
"""Tests for plotting utilities."""

import pandas as pd
import pytest

from utils.plotting import correlation_heatmap, quick_hist


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
```

**Step 5: Create tests/test_stats.py**

Create file `tests/test_stats.py`:

```python
"""Tests for statistical utilities."""

import pandas as pd
import pytest

from utils.stats import describe_numeric, detect_outliers


def test_describe_numeric(df_with_missing: pd.DataFrame) -> None:
    """Test extended numeric description."""
    result = describe_numeric(df_with_missing)
    assert "missing" in result.columns
    assert "missing_pct" in result.columns
    assert result.loc["a", "missing"] == 1
    assert result.loc["b", "missing"] == 4
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
    assert outliers.iloc[-1] is True
    # Other values should not be outliers
    assert outliers.iloc[:-1].sum() == 0


def test_detect_outliers_zscore(numeric_series: pd.Series) -> None:
    """Test z-score outlier detection."""
    outliers = detect_outliers(numeric_series, method="zscore", threshold=2.0)
    # 100 should be detected as an outlier
    assert outliers.iloc[-1] is True


def test_detect_outliers_invalid_method(numeric_series: pd.Series) -> None:
    """Test that invalid method raises ValueError."""
    with pytest.raises(ValueError, match="Unknown method"):
        detect_outliers(numeric_series, method="invalid")
```

**Step 6: Create tests/test_io.py**

Create file `tests/test_io.py`:

```python
"""Tests for I/O utilities."""

from pathlib import Path

import pandas as pd
import pytest

from utils.io import read_csv_auto, save_results


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
```

**Step 7: Create tests/test_text.py**

Create file `tests/test_text.py`:

```python
"""Tests for text processing utilities."""

from utils.text import normalize_whitespace, remove_mentions, remove_urls


def test_remove_urls() -> None:
    """Test URL removal."""
    text = "Check https://example.com and www.test.com for more"
    result = remove_urls(text)
    assert "https://example.com" not in result
    assert "www.test.com" not in result
    assert "Check" in result
    assert "for more" in result


def test_remove_mentions() -> None:
    """Test mention removal."""
    text = "Hello @user and @another nice to meet you"
    result = remove_mentions(text)
    assert "@user" not in result
    assert "@another" not in result
    assert "Hello" in result
    assert "nice to meet you" in result


def test_normalize_whitespace() -> None:
    """Test whitespace normalization."""
    text = "Hello    world\n\n  test   "
    result = normalize_whitespace(text)
    assert result == "Hello world test"


def test_normalize_whitespace_empty() -> None:
    """Test normalizing empty text."""
    assert normalize_whitespace("") == ""
    assert normalize_whitespace("   ") == ""
```

**Step 8: Run all tests**

Run:
```bash
uv run pytest tests/ -v
```

Expected: All tests pass

**Step 9: Format tests with ruff**

Run:
```bash
uv run ruff format tests/
```

Expected: Files formatted

**Step 10: Commit tests**

Run:
```bash
git add tests/
git commit -m "test: add comprehensive tests for utils package

Add tests for all utils modules:
- test_cleaning: column cleaning, text cleaning, missing values
- test_plotting: histograms, heatmaps
- test_stats: descriptions, outlier detection
- test_io: CSV reading/writing
- test_text: URL/mention removal, whitespace

Include pytest fixtures for reusable test data

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

Expected: Commit created successfully

---

## Task 5: Create Makefile

**Files:**
- Create: `Makefile`

**Step 1: Create Makefile**

Create file `Makefile`:

```makefile
.PHONY: help install install-dev format lint type test clean all pre-commit-setup

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install all dependencies
	uv sync --all-extras

install-dev:  ## Install base + dev dependencies only
	uv sync --extra dev

format:  ## Format code with ruff
	uv run ruff format .
	uv run ruff check --fix .

lint:  ## Check code with ruff (no fixes)
	uv run ruff check .

type:  ## Run mypy type checking
	uv run mypy utils/ tests/

test:  ## Run pytest tests
	uv run pytest tests/ -v

clean:  ## Remove cache and temp files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

all: format lint type test  ## Run all checks

pre-commit-setup:  ## Install pre-commit hooks
	uv run pre-commit install
```

**Step 2: Test Makefile help command**

Run:
```bash
make help
```

Expected: Shows all available commands with descriptions

**Step 3: Test make all**

Run:
```bash
make all
```

Expected: Runs format, lint, type, test successfully

**Step 4: Commit Makefile**

Run:
```bash
git add Makefile
git commit -m "feat: add Makefile for common tasks

Commands:
- make install: install all dependencies
- make format: format code
- make lint: check code
- make type: type check
- make test: run tests
- make all: run all checks
- make clean: remove caches

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

Expected: Commit created successfully

---

## Task 6: Setup Pre-commit Hooks

**Files:**
- Create: `.pre-commit-config.yaml`

**Step 1: Create pre-commit configuration**

Create file `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.4
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: [--maxkb=1000]
      - id: check-merge-conflict

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all, pandas-stubs]
        files: ^(utils|tests)/.*\.py$
```

**Step 2: Install pre-commit hooks**

Run:
```bash
make pre-commit-setup
```

Expected: Pre-commit installed to .git/hooks/pre-commit

**Step 3: Test pre-commit on all files**

Run:
```bash
uv run pre-commit run --all-files
```

Expected: All hooks pass

**Step 4: Commit pre-commit config**

Run:
```bash
git add .pre-commit-config.yaml
git commit -m "feat: add pre-commit hooks configuration

Hooks:
- ruff format and linting
- trailing whitespace removal
- end of file fixer
- yaml validation
- large file check
- mypy type checking for utils and tests

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

Expected: Pre-commit hooks run and commit succeeds

---

## Task 7: Setup GitHub Actions CI

**Files:**
- Create: `.github/workflows/ci.yml`

**Step 1: Create CI workflow**

Create file `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Set up Python
        run: uv python install 3.14

      - name: Install dependencies
        run: uv sync --all-extras

      - name: Run ruff format check
        run: uv run ruff format --check .

      - name: Run ruff linting
        run: uv run ruff check .

      - name: Run mypy type checking
        run: uv run mypy utils/ tests/

      - name: Run tests
        run: uv run pytest tests/ -v --tb=short
```

**Step 2: Validate workflow file**

Run:
```bash
cat .github/workflows/ci.yml
```

Expected: YAML is properly formatted

**Step 3: Commit CI workflow**

Run:
```bash
git add .github/workflows/ci.yml
git commit -m "feat: add GitHub Actions CI workflow

Runs on push and PR to main:
- Checkout code
- Install uv and Python 3.14
- Install dependencies
- Check formatting
- Run linting
- Run type checking
- Run tests

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

Expected: Commit created successfully

---

## Task 8: Reorganize Existing Files

**Files:**
- Move: `Pandas/*.ipynb` → `pandas/*.ipynb`
- Move: `Python/*.py` → `python/*.py`
- Move: `Misc/toolbox.py` → delete (already integrated into utils)
- Move: `Misc/Polars_cheatsheet.py` → `pandas/polars_cheatsheet.py`
- Keep: `Code Challenges/` as is for now
- Keep: `data/` as is

**Step 1: Move Pandas notebooks (lowercase)**

Run:
```bash
mv Pandas pandas_temp && mv pandas_temp pandas
```

Expected: Directory renamed to lowercase

**Step 2: Move Python scripts (lowercase)**

Run:
```bash
mv Python python_temp && mv python_temp python
```

Expected: Directory renamed to lowercase

**Step 3: Move Polars cheatsheet**

Run:
```bash
mv Misc/Polars_cheatsheet.py pandas/polars_cheatsheet.py
```

Expected: File moved

**Step 4: Remove old toolbox (now in utils)**

Run:
```bash
rm Misc/toolbox.py
```

Expected: File removed

**Step 5: Remove Misc directory if empty**

Run:
```bash
rmdir Misc 2>/dev/null || echo "Misc directory not empty, keeping it"
```

Expected: Directory removed if empty

**Step 6: Rename Code Challenges directory**

Run:
```bash
mv "Code Challenges" challenges
```

Expected: Directory renamed

**Step 7: Commit reorganization**

Run:
```bash
git add -A
git commit -m "refactor: reorganize directory structure

Changes:
- Rename Pandas → pandas (lowercase)
- Rename Python → python (lowercase)
- Move Polars_cheatsheet.py to pandas/
- Remove Misc/toolbox.py (integrated into utils/)
- Rename 'Code Challenges' → challenges

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

Expected: Commit created successfully

---

## Task 9: Update Documentation

**Files:**
- Modify: `README.md`
- Create: `docs/notes/README.md`

**Step 1: Update root README.md**

Replace content of `README.md`:

```markdown
# Python & Data Science Learning Repository

A comprehensive monorepo for learning Python and data science, organized for efficiency and best practices.

## Structure

- **pandas/** - DataFrame manipulation and analysis
- **numpy/** - Array computing and numerical operations
- **python/** - Core Python language features
- **sklearn/** - Machine learning with scikit-learn
- **visualization/** - Plotting libraries (matplotlib, seaborn, plotly)
- **statistics/** - Statistical methods and theory
- **sql/** - SQL and database interactions
- **utils/** - Reusable utilities package
- **tests/** - Unit tests for utils package
- **docs/** - Documentation and learning notes
- **data/** - Datasets (gitignored)
- **challenges/** - Coding challenges

## Quick Start

```bash
# Install dependencies
make install

# Install pre-commit hooks
make pre-commit-setup

# Run all checks
make all
```

## Development Workflow

```bash
# Format code
make format

# Run linting
make lint

# Type check
make type

# Run tests
make test
```

## Utils Package

Reusable utilities for DRY code:

```python
from utils.cleaning import clean_columns, handle_missing
from utils.plotting import quick_hist
from utils.stats import describe_numeric

df = clean_columns(df)
df = handle_missing(df, strategy="median")
quick_hist(df['age'])
```

## Adding Dependencies

```bash
# Core dependency
uv add package-name

# Optional group
uv add --optional-group ml tensorflow

# Install with extras
uv sync --extra ml
uv sync --all-extras
```

## Tools

- **uv** - Fast dependency management
- **ruff** - Linting and formatting
- **mypy** - Type checking
- **pytest** - Testing framework
- **pre-commit** - Git hooks
- **GitHub Actions** - CI/CD

## Data

Datasets are stored in `data/` (gitignored). Download from:
https://drive.google.com/drive/folders/1UzgxrOvtdJwKui7gbKhzohp5e_WQihSP?usp=sharing
```

**Step 2: Create docs/notes/README.md**

Create file `docs/notes/README.md`:

```markdown
# Learning Notes

Organized notes and references for data science topics.

## Suggested Structure

- **learning-paths.md** - Suggested topic progressions
- **best-practices.md** - Coding patterns and conventions
- **resources.md** - External resources and references
- **snippets.md** - Useful code snippets

## Topics

Create topic-specific markdown files as you learn:
- pandas-tips.md
- numpy-patterns.md
- sklearn-workflows.md
- visualization-recipes.md
- etc.
```

**Step 3: Commit documentation updates**

Run:
```bash
git add README.md docs/notes/README.md
git commit -m "docs: update README and add notes structure

- Update README with new structure
- Add quick start guide
- Add utils package examples
- Add development workflow
- Create docs/notes/README with learning notes structure

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

Expected: Commit created successfully

---

## Task 10: Update .gitignore

**Files:**
- Modify: `.gitignore`

**Step 1: Review current .gitignore**

Run:
```bash
cat .gitignore | head -20
```

Expected: See current gitignore contents

**Step 2: Add additional entries**

Append to `.gitignore`:

```
# UV
uv.lock

# Ruff
.ruff_cache/

# Jupyter checkpoints
.ipynb_checkpoints/

# Data files
data/
*.csv
*.xlsx
*.parquet

# But keep test fixtures
!tests/fixtures/*.csv

# Logs
*.log

# OS
.DS_Store
```

**Step 3: Commit .gitignore updates**

Run:
```bash
git add .gitignore
git commit -m "chore: update .gitignore for new tooling

Add ignores for:
- uv.lock
- .ruff_cache/
- Jupyter checkpoints
- Data files (but keep test fixtures)
- Log files

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

Expected: Commit created successfully

---

## Task 11: Remove Old Configuration

**Files:**
- Remove: `mypy.ini` (now in pyproject.toml)

**Step 1: Remove old mypy.ini**

Run:
```bash
git rm mypy.ini
```

Expected: File removed from git

**Step 2: Remove old .venv if using uv**

Run:
```bash
echo "Consider removing .venv if you want to use uv's managed environments"
```

Expected: Informational message

**Step 3: Commit cleanup**

Run:
```bash
git commit -m "chore: remove old configuration files

Remove mypy.ini (now configured in pyproject.toml)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

Expected: Commit created successfully

---

## Task 12: Verification and Final Check

**Files:**
- None (verification only)

**Step 1: Verify directory structure**

Run:
```bash
ls -1 | grep -E "^(pandas|numpy|python|sklearn|visualization|statistics|sql|utils|tests|docs|data|challenges)$"
```

Expected: All topic directories exist

**Step 2: Verify utils imports work**

Run:
```bash
uv run python -c "from utils.cleaning import clean_columns; from utils.plotting import quick_hist; print('Imports successful')"
```

Expected: "Imports successful"

**Step 3: Run all checks**

Run:
```bash
make all
```

Expected: All checks pass (format, lint, type, test)

**Step 4: Verify pre-commit works**

Run:
```bash
uv run pre-commit run --all-files
```

Expected: All hooks pass

**Step 5: Check git status**

Run:
```bash
git status
```

Expected: Working directory clean

**Step 6: View commit history**

Run:
```bash
git log --oneline -15
```

Expected: See all commits from this implementation

---

## Success Criteria Checklist

- [ ] Directory structure created with all topic folders
- [ ] pyproject.toml configured with uv, ruff, mypy, pytest
- [ ] Utils package created with typed functions
- [ ] Tests created for all utils modules
- [ ] All tests passing
- [ ] Makefile commands working
- [ ] Pre-commit hooks installed and passing
- [ ] GitHub Actions CI workflow configured
- [ ] Existing files reorganized (lowercase directories)
- [ ] Documentation updated (README, docs/notes)
- [ ] Old config files removed
- [ ] All checks passing (make all)
- [ ] Git history clean with descriptive commits

## Next Steps

After completing this plan:

1. **Explore notebooks** - Start working in topic folders, extracting utilities
2. **Expand utils** - Add more functions as you discover patterns
3. **Add more tests** - Test coverage for new utils functions
4. **Create learning notes** - Document patterns in docs/notes/
5. **Add optional dependencies** - Install ML, viz, db, web extras as needed
6. **Push to GitHub** - Ensure CI runs successfully
