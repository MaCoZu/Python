import marimo

__generated_with = "0.23.3"
app = marimo.App()


@app.cell
def _():
    import numpy as np
    import pandas as pd
    from scipy import stats

    return np, pd, stats


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Finding Stealth Null Values in Pandas

    To find "stealth" null values without knowing their names beforehand, you have to look for **statistical outliers** and **frequency anomalies**.

    If you don't know the "mask" the data is wearing, you look for the behavior of the data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Example DataFrame with Stealth Nulls

    Let's create a sample dataset with various types of stealth null values to demonstrate the detection techniques.
    """)
    return


@app.cell
def _(pd):
    data = {
        "country": [
            "USA",
            "Canada",
            "...",
            "Germany",
            "N/A",
            "France",
            "..",
            "Italy",
            "Unknown",
            "Spain",
        ],
        "life_expectancy": [78.5, 82.1, 99999.999, 81.0, -1, 79.8, 99999.999, 80.5, 77.0, 82.0],
        "population": [331000000, 38000000, 0, 83000000, 0, 67000000, 0, 60000000, 0, 99947000000],
        "happiness_change": [0.1, -0.2, 0, 0.3, 0, -0.1, 0, 0.2, 0, 0.15],
        "notes": [
            "  ",
            "good",
            " ",
            "stable",
            "N/A",
            "improving",
            " ",
            "good",
            "Unknown",
            "stable",
        ],
    }
    df = pd.DataFrame(data)
    df
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1. The Frequency Hunt (Categorical/String Data)

    Stealth nulls like `N/A`, `Unknown`, or `None` often show up as suspiciously frequent values in columns that should have high variety.
    """)
    return


@app.cell
def _(df):
    # Check the top 10 most common values for every object column
    for col1 in df.select_dtypes(exclude=["number"]):
        print(f"--- {col1} ---")
        print(df[col1].value_counts().head(10))
        print("\n")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2. The Outlier Hunt (Numerical Data)

    Values like `99999.999` or `-1` are classic "sentinel values." They are used because they are technically numbers (so they don't break old systems), but they are physically impossible.
    """)
    return


@app.cell
def _(df):
    # Look at the min and max for every numeric column
    df.describe().round()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3. The "Zero" Scan

    The number `0` is the most dangerous stealth null because it is often a valid number. You have to decide if `0` makes sense in context.
    """)
    return


@app.cell
def _(df):
    # See what percentage of each column is exactly 0
    zeros = (df == 0).sum() / len(df) * 100
    zeros
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4. The "Length" Check (Hidden Whitespace)

    Sometimes a cell looks empty but contains a space `" "`. This won't show up in `isna()`.
    """)
    return


@app.cell
def _(df):
    # Find strings that are just whitespace or very short
    for col in df.select_dtypes(exclude="number"):
        short_strings = df[df[col].str.len() <= 2][col].unique()
        print(f"{col} short values: {short_strings}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 5. Automated Detection (The "Z-Score" Trick)

    For large datasets where you can't look at every column, you can use a Z-score to find values that are "too far away" from the average to be real.
    """)
    return


@app.cell
def _(df, np, stats):
    from typing import cast

    numeric_df = df.select_dtypes(include=[np.number])

    data_array = numeric_df.fillna(0).values
    z_scores = np.abs(np.asarray(stats.zscore(data_array)))  # type: ignore

    # 3. Find where Z > 5
    outliers = np.where(z_scores > 5)

    print("Outlier locations (row, col):")
    # outliers[0] are the row indices, outliers[1] are the column indices
    for row, col_idx in zip(outliers[0], outliers[1]):
        col_name = numeric_df.columns[col_idx]
        value = numeric_df.iloc[row, col_idx]
        print(f"  Row {row}, Column '{col_name}': {value}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This will point you to cells like 99999.999
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6. The "Clean Sweep" Solution

    Once you identify these "villains," you should convert them all to true `NaN` objects so your imputation functions (like the one we built earlier) can actually see them.
    """)
    return


@app.cell
def _(df, np):
    # A list of everything suspicious we found
    bad_values = ["N/A", "Unknown", "..", "...", 99999.999, -1, " ", "  "]

    # Replace them all globally
    df_cleaned = df.replace(bad_values, np.nan)
    df_cleaned
    return (df_cleaned,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Check the result - stealth nulls are now proper NaN values
    """)
    return


@app.cell
def _(df_cleaned):
    print("Null values after cleaning:")
    print(df_cleaned.isnull().sum())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Peer Tip:** If you see `999` in your Maddison or HDI data, it's almost always a placeholder for "No Data Collected."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    | Technique | Best For | Example Values |
    |-----------|----------|----------------|
    | Frequency Hunt | Categorical/string data | "N/A", "Unknown", "..." |
    | Outlier Hunt | Numerical data | 99999.999, -1 |
    | Zero Scan | Context-dependent numbers | 0 in population data |
    | Length Check | Hidden whitespace | " ", "  " |
    | Z-Score | Large datasets, automation | Statistical outliers |

    Remember: Always convert stealth nulls to `NaN` before using imputation functions!
    """)
    return


if __name__ == "__main__":
    app.run()
