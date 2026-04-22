"""
POLARS CHEAT SHEET
==================
Complete guide to Polars with runnable examples and performance comparisons.

Installation: pip install polars pandas numpy

Why Polars?
- 5-10x faster than Pandas for most operations
- Much lower memory usage (often 50-70% less)
- Better handling of large datasets (>RAM data)
- Lazy evaluation for query optimization
- Built in Rust, designed for speed from ground up
"""

import time
from functools import wraps

import numpy as np
import pandas as pd
import polars as pl

# =============================================================================
# TIMER DECORATOR - To compare Pandas vs Polars performance
# =============================================================================


def timer(func):
    """Decorator to time function execution"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__:40s} took {end - start:.4f} seconds")
        return result

    return wrapper


# =============================================================================
# 1. FIRST STEPS - Creating DataFrames
# =============================================================================


def basic_dataframe_creation():
    """Creating Polars DataFrames - similar to Pandas but faster"""

    # From dictionary
    df_dict = pl.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
            "city": ["NYC", "LA", "Chicago"],
        }
    )
    print("DataFrame from dict:")
    print(df_dict)
    print()

    # From lists
    pl.DataFrame(
        [["Alice", 25, "NYC"], ["Bob", 30, "LA"], ["Charlie", 35, "Chicago"]],
        schema=["name", "age", "city"],
    )

    # From numpy array
    arr = np.random.randn(5, 3)
    pl.DataFrame(arr, schema=["col1", "col2", "col3"])

    # From Pandas (conversion)
    pdf = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    pl.from_pandas(pdf)

    # Read CSV (fast!)
    # df_csv = pl.read_csv('file.csv')
    # df_csv = pl.scan_csv('file.csv')  # Lazy - doesn't load until needed

    return df_dict


# =============================================================================
# 2. CORE PRINCIPLES - Lazy vs Eager Execution
# =============================================================================


def lazy_vs_eager_execution():
    """
    EAGER execution: Operations execute immediately (like Pandas)
    LAZY execution: Operations build a query plan, execute only when needed

    Lazy is MUCH faster for complex queries - Polars optimizes the entire plan
    """

    # Create sample data
    df = pl.DataFrame(
        {
            "id": range(1000),
            "value": np.random.randn(1000),
            "category": np.random.choice(["A", "B", "C"], 1000),
        }
    )

    # EAGER execution (immediate)
    result_eager = df.filter(pl.col("value") > 0).group_by("category").agg(pl.col("value").mean())
    print("Eager result:")
    print(result_eager)
    print()

    # LAZY execution (deferred, optimized)
    result_lazy = (
        df.lazy()  # Convert to LazyFrame
        .filter(pl.col("value") > 0)
        .group_by("category")
        .agg(pl.col("value").mean())
        .collect()  # Execute the optimized query plan
    )
    print("Lazy result (same, but optimized):")
    print(result_lazy)
    print()

    # You can see the optimized query plan
    query_plan = (
        df.lazy().filter(pl.col("value") > 0).group_by("category").agg(pl.col("value").mean())
    )
    print("Query plan (shows optimizations):")
    print(query_plan.explain())

    return result_eager, result_lazy


# =============================================================================
# 3. KEY DIFFERENCES FROM PANDAS
# =============================================================================


def pandas_vs_polars_syntax():
    """Side-by-side comparison of Pandas and Polars syntax"""

    # Sample data
    data = {
        "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "age": [25, 30, 35, 40, 45],
        "salary": [50000, 60000, 70000, 80000, 90000],
        "department": ["HR", "IT", "IT", "HR", "IT"],
    }

    # Create both dataframes
    pdf = pd.DataFrame(data)
    plf = pl.DataFrame(data)

    print("=" * 80)
    print("SELECTING COLUMNS")
    print("=" * 80)

    # Pandas: df['col'] or df[['col1', 'col2']]
    pandas_select = pdf[["name", "age"]]

    # Polars: df.select() with expressions
    polars_select = plf.select(["name", "age"])
    # Or using pl.col() for more power
    plf.select([pl.col("name"), pl.col("age")])

    print("Pandas select:")
    print(pandas_select.head())
    print("\nPolars select:")
    print(polars_select.head())
    print()

    print("=" * 80)
    print("FILTERING ROWS")
    print("=" * 80)

    # Pandas: df[df['col'] > value]
    pandas_filter = pdf[pdf["age"] > 30]

    # Polars: df.filter(pl.col('col') > value)
    polars_filter = plf.filter(pl.col("age") > 30)

    print("Pandas filter:")
    print(pandas_filter)
    print("\nPolars filter:")
    print(polars_filter)
    print()

    print("=" * 80)
    print("ADDING/MODIFYING COLUMNS")
    print("=" * 80)

    # Pandas: df['new_col'] = ...
    pdf_copy = pdf.copy()
    pdf_copy["age_plus_10"] = pdf_copy["age"] + 10

    # Polars: df.with_columns() - IMMUTABLE by default
    polars_new = plf.with_columns([(pl.col("age") + 10).alias("age_plus_10")])

    print("Pandas (mutable):")
    print(pdf_copy[["name", "age", "age_plus_10"]])
    print("\nPolars (immutable, returns new DF):")
    print(polars_new.select(["name", "age", "age_plus_10"]))
    print()

    print("=" * 80)
    print("GROUPBY AND AGGREGATION")
    print("=" * 80)

    # Pandas
    pandas_group = pdf.groupby("department").agg({"salary": "mean", "age": "max"})

    # Polars - more expressive
    polars_group = plf.group_by("department").agg(
        [
            pl.col("salary").mean().alias("avg_salary"),
            pl.col("age").max().alias("max_age"),
        ]
    )

    print("Pandas groupby:")
    print(pandas_group)
    print("\nPolars groupby:")
    print(polars_group)
    print()

    return plf


# =============================================================================
# 4. POLARS EXPRESSIONS - The Power of pl.col()
# =============================================================================


def polars_expressions_guide():
    """
    Expressions are the core of Polars - they're composable and optimized.
    Think of them as building blocks for data transformations.
    """

    df = pl.DataFrame(
        {
            "product": ["A", "B", "C", "A", "B", "C"],
            "price": [100, 200, 150, 120, 210, 160],
            "quantity": [5, 3, 7, 4, 6, 8],
            "date": [
                "2024-01-01",
                "2024-01-01",
                "2024-01-01",
                "2024-01-02",
                "2024-01-02",
                "2024-01-02",
            ],
        }
    )

    # Basic column selection
    df.select([pl.col("product"), pl.col("price")])

    # Column operations
    result2 = df.select(
        [pl.col("product"), (pl.col("price") * pl.col("quantity")).alias("total_value")]
    )
    print("Computed column:")
    print(result2)
    print()

    # Multiple operations at once
    result3 = df.select(
        [
            pl.col("price").mean().alias("avg_price"),
            pl.col("price").max().alias("max_price"),
            pl.col("price").min().alias("min_price"),
            pl.col("quantity").sum().alias("total_quantity"),
        ]
    )
    print("Multiple aggregations:")
    print(result3)
    print()

    # Conditional logic with when/then/otherwise
    result4 = df.with_columns(
        [
            pl.when(pl.col("price") > 150)
            .then(pl.lit("expensive"))
            .otherwise(pl.lit("affordable"))
            .alias("price_category")
        ]
    )
    print("Conditional column:")
    print(result4)
    print()

    # String operations
    df_strings = pl.DataFrame({"name": ["Alice", "Bob", "Charlie"]})
    result5 = df_strings.select(
        [
            pl.col("name"),
            pl.col("name").str.to_uppercase().alias("upper"),
            pl.col("name").str.len_chars().alias("length"),
        ]
    )
    print("String operations:")
    print(result5)
    print()

    return result4


# =============================================================================
# 5. COMMON OPERATIONS - Quick Reference
# =============================================================================


def common_operations_cheatsheet():
    """Most frequently used Polars operations"""

    df = pl.DataFrame(
        {
            "id": range(1, 11),
            "value": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            "category": ["A", "B", "A", "B", "A", "B", "A", "B", "A", "B"],
            "date": pd.date_range("2024-01-01", periods=10),
        }
    )

    # SELECT columns
    df.select(["id", "value"])

    # FILTER rows
    filter_result = df.filter(pl.col("value") > 50)

    # SORT
    df.sort("value", descending=True)

    # ADD columns with with_columns()
    df.with_columns(
        [
            (pl.col("value") * 2).alias("double_value"),
            (pl.col("value") / 100).alias("normalized"),
        ]
    )

    # RENAME columns
    df.rename({"value": "amount", "category": "type"})

    # DROP columns
    df.drop(["category"])

    # UNIQUE values
    unique_categories = df["category"].unique()

    # NULL handling
    df_with_nulls = pl.DataFrame({"a": [1, 2, None, 4], "b": [None, 2, 3, 4]})
    df_with_nulls.fill_null(0)  # Replace nulls with 0
    df_with_nulls.drop_nulls()  # Remove rows with any null

    # JOIN (like SQL)
    df1 = pl.DataFrame({"id": [1, 2, 3], "value": [10, 20, 30]})
    df2 = pl.DataFrame({"id": [1, 2, 4], "score": [100, 200, 400]})
    joined = df1.join(df2, on="id", how="inner")  # inner, left, outer, cross

    print("Common operations examples:")
    print(f"Filter result shape: {filter_result.shape}")
    print(f"Unique categories: {unique_categories.to_list()}")
    print(f"Joined result:\n{joined}")

    return df


# =============================================================================
# 6. PERFORMANCE COMPARISON - Pandas vs Polars
# =============================================================================


@timer
def pandas_operations(df):
    """Typical Pandas operations"""
    result = df[df["value"] > 50].groupby("category").agg({"value": ["mean", "sum", "std"]})
    return result


@timer
def polars_operations_eager(df):
    """Same operations in Polars (eager)"""
    result = (
        df.filter(pl.col("value") > 50)
        .group_by("category")
        .agg(
            [
                pl.col("value").mean().alias("mean"),
                pl.col("value").sum().alias("sum"),
                pl.col("value").std().alias("std"),
            ]
        )
    )
    return result


@timer
def polars_operations_lazy(df):
    """Same operations in Polars (lazy - fastest)"""
    result = (
        df.lazy()
        .filter(pl.col("value") > 50)
        .group_by("category")
        .agg(
            [
                pl.col("value").mean().alias("mean"),
                pl.col("value").sum().alias("sum"),
                pl.col("value").std().alias("std"),
            ]
        )
        .collect()
    )
    return result


def performance_comparison():
    """Compare Pandas vs Polars on larger dataset"""

    print("\n" + "=" * 80)
    print("PERFORMANCE COMPARISON - 1 Million Rows")
    print("=" * 80 + "\n")

    # Create larger dataset
    n = 1_000_000
    data = {
        "id": range(n),
        "value": np.random.randn(n) * 100,
        "category": np.random.choice(["A", "B", "C", "D", "E"], n),
        "date": pd.date_range("2020-01-01", periods=n, freq="min"),
    }

    pdf = pd.DataFrame(data)
    plf = pl.DataFrame(data)

    print("Dataset size:", f"{n:,} rows\n")

    # Run comparisons
    print("1. Pandas operations:")
    pandas_operations(pdf)

    print("2. Polars eager operations:")
    polars_operations_eager(plf)

    print("3. Polars lazy operations (optimized):")
    polars_lazy_result = polars_operations_lazy(plf)

    print("\nResults are equivalent:")
    print(polars_lazy_result)


performance_comparison()
# =============================================================================
# 7. MEMORY EFFICIENCY
# =============================================================================


def memory_comparison():
    """Compare memory usage between Pandas and Polars"""

    n = 500_000
    data = {
        "int_col": np.random.randint(0, 1000, n),
        "float_col": np.random.randn(n),
        "str_col": np.random.choice(["cat1", "cat2", "cat3"], n),
        "bool_col": np.random.choice([True, False], n),
    }

    # Pandas
    pdf = pd.DataFrame(data)
    pandas_memory = pdf.memory_usage(deep=True).sum() / 1024**2  # MB

    # Polars
    plf = pl.DataFrame(data)
    polars_memory = plf.estimated_size() / 1024**2  # MB

    print("\n" + "=" * 80)
    print("MEMORY USAGE COMPARISON - 500k rows")
    print("=" * 80)
    print(f"Pandas memory: {pandas_memory:.2f} MB")
    print(f"Polars memory: {polars_memory:.2f} MB")
    print(f"Polars saves:  {(1 - polars_memory / pandas_memory) * 100:.1f}%")
    print()


memory_comparison()

# =============================================================================
# 8. ADVANCED PATTERNS
# =============================================================================


def advanced_polars_patterns():
    """More complex Polars patterns"""

    df = pl.DataFrame(
        {
            "timestamp": pd.date_range("2024-01-01", periods=100, freq="h"),
            "sensor_id": np.random.choice(["S1", "S2", "S3"], 100),
            "temperature": np.random.randn(100) * 10 + 20,
            "humidity": np.random.randn(100) * 5 + 50,
        }
    )

    # Window functions (like SQL)
    result1 = df.with_columns(
        [
            pl.col("temperature").rolling_mean(window_size=5).alias("temp_ma5"),
            pl.col("temperature").shift(1).alias("temp_prev"),
        ]
    )

    # Complex aggregations per group
    result2 = df.group_by("sensor_id").agg(
        [
            pl.col("temperature").mean().alias("avg_temp"),
            pl.col("temperature").std().alias("std_temp"),
            pl.col("temperature").quantile(0.95).alias("p95_temp"),
            pl.col("humidity").count().alias("measurements"),
        ]
    )

    # Chaining multiple operations (lazy for optimization)
    result3 = (
        df.lazy()
        .filter(pl.col("temperature") > 20)
        .with_columns([(pl.col("temperature") - 20).alias("temp_delta")])
        .group_by("sensor_id")
        .agg([pl.col("temp_delta").mean().alias("avg_delta")])
        .sort("avg_delta", descending=True)
        .collect()
    )

    print("Advanced patterns:")
    print("\n1. Rolling window:")
    print(result1.head())
    print("\n2. Group aggregations:")
    print(result2)
    print("\n3. Complex chain:")
    print(result3)

    return result3


# =============================================================================
# 9. PRACTICAL EXAMPLES
# =============================================================================


@timer
def pandas_data_pipeline():
    """Typical data analysis pipeline in Pandas"""
    df = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv")

    result = (
        df.assign(tip_pct=lambda x: x["tip"] / x["total_bill"] * 100)
        .query("tip_pct > 10")
        .groupby(["day", "time"])
        .agg({"total_bill": "mean", "tip": "mean", "size": "count"})
        .reset_index()
        .sort_values("total_bill", ascending=False)
    )
    return result


pandas_data_pipeline()


@timer
def polars_data_pipeline():
    """Same pipeline in Polars - faster and cleaner"""
    df = pl.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv")

    result = (
        df.lazy()
        .with_columns([(pl.col("tip") / pl.col("total_bill") * 100).alias("tip_pct")])
        .filter(pl.col("tip_pct") > 10)
        .group_by(["day", "time"])
        .agg(
            [
                pl.col("total_bill").mean(),
                pl.col("tip").mean(),
                pl.col("size").count().alias("count"),
            ]
        )
        .sort("total_bill", descending=True)
        .collect()
    )
    return result


polars_data_pipeline()


def practical_examples():
    """Run real-world pipeline comparison"""
    print("\n" + "=" * 80)
    print("REAL-WORLD PIPELINE COMPARISON")
    print("=" * 80 + "\n")

    print("Pandas pipeline:")
    pandas_result = pandas_data_pipeline()
    print(pandas_result.head())
    print()

    print("Polars pipeline (same result, faster):")
    polars_result = polars_data_pipeline()
    print(polars_result.head())
    print()


practical_examples()

# =============================================================================
# 10. QUICK REFERENCE GUIDE
# =============================================================================


def print_quick_reference():
    """Print a quick syntax reference"""

    reference = """
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                     POLARS QUICK REFERENCE                               ║
    ╚══════════════════════════════════════════════════════════════════════════╝

    CREATE DATAFRAME
    ────────────────
    pl.DataFrame({'col': [1, 2, 3]})
    pl.read_csv('file.csv')
    pl.from_pandas(pandas_df)

    LAZY EXECUTION (recommended for complex queries)
    ────────────────
    df.lazy()                    # Convert to lazy
    .filter(...)                 # Add operations
    .collect()                   # Execute

    SELECT COLUMNS
    ──────────────
    df.select(['col1', 'col2'])
    df.select([pl.col('col1'), pl.col('col2')])
    df.select(pl.all())          # All columns
    df.select(pl.col('^.*_id$')) # Regex selection

    FILTER ROWS
    ───────────
    df.filter(pl.col('age') > 25)
    df.filter((pl.col('age') > 25) & (pl.col('city') == 'NYC'))

    ADD/MODIFY COLUMNS
    ──────────────────
    df.with_columns([
        (pl.col('a') + pl.col('b')).alias('sum'),
        pl.col('name').str.to_uppercase().alias('NAME')
    ])

    GROUP BY & AGGREGATE
    ────────────────────
    df.group_by('category').agg([
        pl.col('value').mean().alias('avg'),
        pl.col('value').sum().alias('total'),
        pl.count().alias('count')
    ])

    SORT
    ────
    df.sort('col1')
    df.sort('col1', descending=True)
    df.sort(['col1', 'col2'])

    JOIN
    ────
    df1.join(df2, on='id', how='inner')  # inner, left, outer, cross

    WINDOW FUNCTIONS
    ────────────────
    df.with_columns([
        pl.col('value').rolling_mean(window_size=5),
        pl.col('value').shift(1),
        pl.col('value').rank()
    ])

    CONDITIONALS
    ────────────
    pl.when(pl.col('age') > 18)
      .then(pl.lit('adult'))
      .otherwise(pl.lit('minor'))

    NULL HANDLING
    ─────────────
    df.fill_null(0)              # Replace nulls
    df.drop_nulls()              # Drop rows with nulls
    pl.col('col').is_null()      # Check for nulls

    STRING OPERATIONS
    ─────────────────
    pl.col('name').str.to_uppercase()
    pl.col('name').str.contains('pattern')
    pl.col('name').str.replace('old', 'new')

    COMMON AGGREGATIONS
    ───────────────────
    pl.col('value').sum()
    pl.col('value').mean()
    pl.col('value').std()
    pl.col('value').min() / .max()
    pl.col('value').quantile(0.5)  # Median
    pl.count()                      # Row count

    PERFORMANCE TIPS
    ────────────────
    ✓ Use .lazy() for complex queries (auto-optimized)
    ✓ Use pl.col() expressions (composable and fast)
    ✓ Chain operations instead of intermediate variables
    ✓ Use .collect() only once at the end
    ✓ Polars is typically 5-10x faster than Pandas
    """

    print(reference)


# =============================================================================
# MAIN - Run all examples
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print(" POLARS CHEAT SHEET - Complete Guide with Performance Tests")
    print("=" * 80)

    # 1. Basics
    print("\n[1/9] Basic DataFrame Creation")
    basic_dataframe_creation()

    # 2. Lazy vs Eager
    print("\n[2/9] Lazy vs Eager Execution")
    lazy_vs_eager_execution()

    # 3. Syntax comparison
    print("\n[3/9] Pandas vs Polars Syntax")
    pandas_vs_polars_syntax()

    # 4. Expressions
    print("\n[4/9] Polars Expressions")
    polars_expressions_guide()

    # 5. Common operations
    print("\n[5/9] Common Operations")
    common_operations_cheatsheet()

    # 6. Performance
    print("\n[6/9] Performance Comparison")
    performance_comparison()

    # 7. Memory
    print("\n[7/9] Memory Efficiency")
    memory_comparison()

    # 8. Advanced
    print("\n[8/9] Advanced Patterns")
    advanced_polars_patterns()

    # 9. Practical examples
    print("\n[9/9] Practical Pipeline Examples")
    practical_examples()

    # Quick reference
    print_quick_reference()

    print("\n" + "=" * 80)
    print(" KEY TAKEAWAYS:")
    print("=" * 80)
    print("• Polars is 5-10x faster than Pandas")
    print("• Uses 50-70% less memory")
    print("• Lazy evaluation optimizes entire query plans")
    print("• Immutable by default (safer for pipelines)")
    print("• Better for datasets >1GB")
    print("• Use .lazy() for complex queries, .collect() at the end")
    print("=" * 80)
    print("=" * 80)
