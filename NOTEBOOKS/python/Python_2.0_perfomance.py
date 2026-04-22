"""
PYTHON PERFORMANCE & EFFICIENCY GUIDE
======================================
Key principles for writing fast, resource-efficient Python code.
Focus: Vectorization, avoiding copies, using the right data structures.
"""

import itertools
import time
from concurrent.futures import ThreadPoolExecutor  # pylint: disable=no-name-in-module
from functools import wraps
from multiprocessing import Pool

import numpy as np
import pandas as pd

# =============================================================================
# TIMER WRAPPER
# =============================================================================


def timer(func):
    @wraps(func)  # ← Preserves metadata
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result

    return wrapper


# =============================================================================
# 1. VECTORIZE EVERYTHING - Avoid Python loops for numerical operations
# =============================================================================


# SLOW - Python loop (interpreted, slow)
@timer
def slow_multiply():
    arr = list(range(1000000))
    result = []
    for i in range(len(arr)):
        result.append(arr[i] * 2)
    return result[:2]


slow_multiply()


# FAST - Vectorized NumPy (compiled C code, 10-100x faster)
@timer
def fast_multiply():
    arr = np.arange(1000000)
    result = arr * 2  # Single vectorized operation
    return result[:2]


fast_multiply()


# Pandas vectorized operations - ALWAYS prefer these over loops
def pandas_vectorization_examples(df):
    """Pandas vectorized operations:"""
    # SLOW - Manual loop for percentage change
    # for i in range(1, len(df)):
    #     df.loc[i, 'pct'] = (df.loc[i, 'price'] - df.loc[i-1, 'price']) / df.loc[i-1, 'price']

    # FAST - Built-in vectorized function
    df["pct"] = df["price"].pct_change()

    # FAST - Conditional logic with np.where instead of if/else in loops
    df["category"] = np.where(df["price"] > 100, "expensive", "cheap")

    # FAST - Rolling window operations
    df["rolling_mean"] = df["price"].rolling(window=7).mean()

    # FAST - Boolean indexing instead of filtering with loops
    df[df["price"] > 100]

    return df


# =============================================================================
# 2. AVOID COPYING DATA - Use views and in-place operations
# =============================================================================


def memory_efficient_operations():
    # SLOW - Creates unnecessary copies
    arr = np.arange(1000000)
    arr.copy()  # Full copy in memory

    # FAST - NumPy view (shares memory, no copy)
    arr_view = arr[::2]  # Every second element, just a view
    arr_view[0] = 999  # Modifies original arr too!

    # FAST - In-place operations in Pandas
    df = pd.DataFrame({"a": range(1000), "b": range(1000)})
    df["c"] = df["a"] + df["b"]  # Adds column in-place, no copy

    # FAST - query() is often more efficient than boolean indexing
    df.query("a > 500")  # Less memory overhead

    return arr, df


# =============================================================================
# 3. USE THE RIGHT DATA STRUCTURE
# =============================================================================


def data_structure_performance():
    data = list(range(10000))

    # SLOW - List membership test is O(n)
    # if 5000 in data:  # Scans entire list
    #     pass

    # FAST - Set membership test is O(1)
    data_set = set(data)
    if 5000 in data_set:  # Instant lookup
        pass

    # FAST - Dict for lookups instead of scanning lists
    lookup = {i: f"value_{i}" for i in range(10000)}
    lookup.get(5000)  # O(1) vs O(n) list scan

    # Use NumPy for numerical data (not Python lists)
    np.array(data)  # More memory efficient, faster operations

    # For large datasets: Polars > Pandas (faster, less memory)
    # import polars as pl
    # df_polars = pl.DataFrame({'col': data})


# =============================================================================
# 4. LIST COMPREHENSIONS > LOOPS (but vectorization > both)
# =============================================================================


def comprehension_vs_loop():
    data = range(10000)

    # SLOW - Append in loop
    result = []
    for x in data:
        result.append(x * 2)

    # FASTER - List comprehension (optimized in CPython)
    result = [x * 2 for x in data]

    # FASTEST - Vectorized for numerical data
    result = np.array(list(data)) * 2

    return result


# =============================================================================
# 5. AVOID REPEATED ATTRIBUTE LOOKUPS
# =============================================================================


def optimize_attribute_access():
    result = []
    large_list = range(100000)

    # SLOW - Looks up .append every iteration
    # for item in large_list:
    #     result.append(item)

    # FASTER - Cache the method reference
    append = result.append
    for item in large_list:
        append(item)

    # BEST - Use list comprehension or vectorization when possible
    result = list(large_list)


# =============================================================================
# 6. USE BUILT-IN FUNCTIONS (implemented in C, very fast)
# =============================================================================


def use_builtins():
    data = range(10000)

    # SLOW - Manual loop
    # total = 0
    # for x in data:
    #     total += x

    # FAST - Built-in function in C
    sum(data)
    max(data)
    min(data)

    # any() and all() short-circuit (stop early when possible)
    any(x < 0 for x in data)
    all(x >= 0 for x in data)

    # itertools for efficient iteration patterns
    from itertools import islice

    list(islice(data, 100))  # More efficient than data[:100] for iterators


# =============================================================================
# 7. PANDAS-SPECIFIC OPTIMIZATIONS
# =============================================================================


def pandas_optimizations():
    df = pd.DataFrame(
        {
            "a": range(10000),
            "b": range(10000),
            "category": ["cat1", "cat2", "cat1", "cat2"] * 2500,
        }
    )

    # SLOW - iterrows (never use this if you can avoid it)
    # for idx, row in df.iterrows():
    #     df.loc[idx, 'new'] = row['a'] + row['b']

    # FAST - Vectorized operation
    df["new"] = df["a"] + df["b"]

    # Use .apply() only when vectorization is impossible
    # df['complex'] = df.apply(lambda row: complex_function(row), axis=1)

    # MEMORY OPTIMIZATION - Category dtype for repeated strings
    df["category"] = df["category"].astype("category")  # Saves significant memory

    # Use appropriate numeric dtypes
    df["a"] = df["a"].astype("int32")  # vs default int64, saves 50% memory

    # Read CSV efficiently
    # df = pd.read_csv('file.csv', usecols=['col1', 'col2'])  # Only load needed columns
    # df = pd.read_csv('file.csv', dtype={'col1': 'int32'})   # Specify dtypes upfront

    return df


# =============================================================================
# 8. PARALLELISM - Use when appropriate
# =============================================================================


def expensive_cpu_function(x):
    """Simulate CPU-intensive work"""
    return sum(i * i for i in range(x))


def io_bound_function(url):
    """Simulate I/O-bound work (API call, file read)"""
    import time

    time.sleep(0.1)  # Simulates network delay
    return f"Data from {url}"


def parallel_processing_examples():
    data = [1000, 2000, 3000, 4000]
    urls = ["url1", "url2", "url3", "url4"]

    # CPU-BOUND tasks - Use multiprocessing (bypasses GIL)
    with Pool(processes=4) as pool:
        cpu_results = pool.map(expensive_cpu_function, data)

    # I/O-BOUND tasks - Use threading (GIL released during I/O)
    with ThreadPoolExecutor(max_workers=4) as executor:
        io_results = list(executor.map(io_bound_function, urls))

    # Pandas parallel operations (requires pandarallel package)
    # from pandarallel import pandarallel
    # pandarallel.initialize()
    # df['result'] = df.parallel_apply(expensive_function, axis=1)

    return cpu_results, io_results


# =============================================================================
# 9. GENERATORS FOR MEMORY EFFICIENCY - Don't load everything at once
# =============================================================================


def generator_examples():
    # SLOW - Loads entire file into memory
    # with open('large_file.txt') as f:
    #     lines = f.readlines()  # All lines in memory
    #     for line in lines:
    #         process(line)

    # FAST - Generator, processes one line at a time
    def process_large_file(filename):
        with open(filename) as f:
            for line in f:  # Yields one line at a time
                yield line.strip().upper()

    # Generator expressions (like list comprehension but lazy)
    # Memory efficient for large datasets
    large_data = range(1000000)
    squared = (x * x for x in large_data)  # Generator, not list
    # Only computes values when needed
    list(itertools.islice(squared, 100))


# =============================================================================
# 10. PROFILING - Measure before optimizing
# =============================================================================


def profile_code():
    """
    Use these tools to find bottlenecks:

    # Command line profiling
    python -m cProfile -s cumulative my_script.py

    # In code
    import cProfile
    cProfile.run('my_function()')

    # Jupyter notebook line profiling
    %load_ext line_profiler
    %lprun -f my_function my_function()

    # Memory profiling
    from memory_profiler import profile
    @profile
    def my_function():
        pass

    # Timing single operations
    import timeit
    timeit.timeit('sum(range(100))', number=10000)
    """
    pass


# =============================================================================
# QUICK REFERENCE CHECKLIST
# =============================================================================
"""
PERFORMANCE CHECKLIST (in priority order):

1. ✓ Is it vectorizable?
   → Use NumPy/Pandas operations instead of loops

2. ✓ Are you iterating in Python?
   → Replace with vectorized operations or built-in functions

3. ✓ Large dataset (>1GB)?
   → Consider Polars instead of Pandas

4. ✓ Copying data unnecessarily?
   → Use views, in-place operations, or generators

5. ✓ Using wrong data structure?
   → Sets for membership, dicts for lookups, NumPy for numbers

6. ✓ Still too slow?
   → Profile first, then consider parallelization

GOLDEN RULE: One vectorized operation beats 1000 lines of optimized Python loops.

ANTI-PATTERNS TO AVOID:
✗ iterrows() in Pandas
✗ Growing lists in loops (use comprehensions or pre-allocate)
✗ Repeatedly accessing same attribute in loop
✗ Using lists for numerical data (use NumPy)
✗ Full table scans when you need lookups (use sets/dicts)
✗ Loading entire files when you can stream
"""


# =============================================================================
# EXAMPLE: Putting it all together
# =============================================================================


def efficient_data_pipeline_example():
    """Complete example showing multiple optimizations"""

    # 1. Read CSV efficiently - only needed columns, correct dtypes
    df = pd.read_csv(
        "data.csv",
        usecols=["date", "price", "volume", "category"],
        dtype={"category": "category", "volume": "int32"},
        parse_dates=["date"],
    )

    # 2. Vectorized calculations (no loops!)
    df["returns"] = df["price"].pct_change()
    df["moving_avg"] = df["price"].rolling(window=20).mean()
    df["high_volume"] = df["volume"] > df["volume"].quantile(0.75)

    # 3. Efficient filtering with boolean indexing
    df[df["returns"] > 0.02]

    # 4. Group operations (optimized internally)
    category_stats = df.groupby("category").agg({"price": ["mean", "std"], "volume": "sum"})

    # 5. Avoid unnecessary copies - work in-place when possible
    df["normalized"] = (df["price"] - df["price"].mean()) / df["price"].std()

    return df, category_stats


if __name__ == "__main__":
    print("Python Performance Guide - Run individual functions to see examples")
    print("Key takeaway: Vectorize operations, avoid copies, use right data structures")


### Timing
### time perfomance counter

# more accurate than time.time, for timing your code
start = time.perf_counter()
time.sleep(1)
end = time.perf_counter()
print(end - start)

#### PyInstrument
# PyInstrument is a Python profiler that helps you identifing where most of the execution time is spent, allowing you to focus on improving those areas.
# from pyinstrument import Profiler

profiler = Profiler()
profiler.start()
# code you want to measure
profiler.stop()
print(profiler.output_text(unicode=True, color=True))
print(profiler.output_text(unicode=True, color=True))
