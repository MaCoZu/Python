import marimo

__generated_with = "0.23.1"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MaCoZu/Python/blob/main/pandas/ReDi/01_ReDi_Intro_to_Pandas.ipynb)
    """)
    return


@app.cell
def _():
    import pandas as pd

    return (pd,)


@app.cell
def _(pd):
    df = pd.read_csv("data_admin.csv")
    df
    return (df,)


@app.cell
def _(df, pd):
    df["date_of_birth"] = pd.to_datetime(df["date_of_birth"], format="%Y-%m-%d", errors="coerce")
    df["age"] = (pd.Timestamp("2010-01-01") - df["date_of_birth"]).dt.days / 365.25
    return


@app.cell
def _(df):
    df["score"] = 0
    # df.drop(columns=["score"], inplace=True)
    df
    return


@app.cell
def _(df):
    df.describe()
    # df.describe().round(3)
    return


@app.cell
def _(df, pd):
    df.replace(99999.000000, pd.NA, inplace=True)
    return


@app.cell
def _(df):
    df["avg_math_score"] = (df["grade_math_t1"] + df["grade_math_t2"]) / 2
    df[df["avg_math_score"] > 8]
    return


@app.cell
def _(df):
    df.isna()
    # df.isna().sum()
    # df.isna().sum().sum()

    # df["student_id"].isna().sum()
    # df["student_id"].isna().any()
    return


@app.cell
def _(df):
    df.notna()
    # df.notna().sum()
    # df.notna().sum().sum()

    # df["student_id"].notna().sum()
    # df["student_id"].notna().any()
    return


@app.cell
def _(df):
    df.isna().sum()
    # df["grade_language_t2"] = df["grade_language_t2"].fillna(0)
    # df.isna().sum()
    return


@app.cell
def _(df):
    df["sex"].unique()
    df["gender"] = df["sex"].map({1: "f", 2: "m"})
    # df[["sex", "gender"]]
    return


@app.cell
def _(df):
    # np.where - assign values based on a condition
    import numpy as np

    df["math_level"] = np.where(df["avg_math_score"] > 7, "high", "not high")
    df[["avg_math_score", "math_level"]]
    return (np,)


@app.cell
def _(df):
    df["avg_math_score"].mean()
    return


@app.cell
def _(df, np):
    df["math_level"] = np.select(
        [df["avg_math_score"] > 9, df["avg_math_score"] > 8, df["avg_math_score"] > 6.8],
        ["very high", "high", "above avg"],
        default="below avg",
    )

    df[["avg_math_score", "math_level"]]
    return


@app.cell
def _(df):
    # where - keep values where condition is True, otherwise set to 0
    df["avg_math_score"].where(df["avg_math_score"] > 7, 7)

    # mask - mask values where condition is true, keep oter values intact
    df["avg_math_score"].mask(df["avg_math_score"] <= 7, 7)
    return


@app.cell
def _(df):
    df["avg_math_score"]
    return


@app.cell
def _(df, pd):
    # apply - apply a function along an axis of the DataFrame

    def weighted_average(row):
        "Calculate a weighted average of math scores, giving more weight to the second term if it's below 7."
        if pd.isna(row["grade_math_t2"]):
            return 0
        if row["grade_math_t2"] < 7:  # condition
            # adjuted average, capped at 10:
            return min((row["grade_math_t1"] + row["grade_math_t2"] * 1.5) / 2, 10)
        else:
            return (row["grade_math_t1"] + row["grade_math_t2"]) / 2

    df["weighted_math_score"] = df.apply(weighted_average, axis=1)
    df[["avg_math_score", "weighted_math_score"]]
    return


@app.cell
def _(df):
    df.groupby("gender")["grade_math_t1"].mean()

    df.groupby("gender")["grade_math_t1"].agg(["min", "max", "mean"])

    df.groupby("gender").agg({"grade_math_t1": ["median", "max"], "age": ["min", "std"]})
    return


@app.cell
def _(df):
    df["sex"].value_counts()
    df["sex"].value_counts().plot(kind="bar")
    return


@app.cell
def _(df, pd):
    pd.cut(
        df["grade_math_t1"],
        bins=[0, 2, 5, 7, 10],
        # include_lowest=True,
    ).value_counts()

    # pd.cut(df["grade_math_t1"], bins=[0, 2, 5, 7, 10]).value_counts().plot(kind="bar")
    return


@app.cell
def _(df):
    # df[df["grade_math_t2"]<=10].plot(x="grade_math_t1", y="grade_math_t2", kind="scatter", c="lightblue")
    df[df["grade_math_t2"] <= 10].plot.scatter(
        x="grade_math_t1", y="grade_math_t2", c="treatment", colormap="viridis", s=4
    )
    return


@app.cell
def _(df):
    import seaborn as sns

    sns.scatterplot(
        data=df[df["grade_math_t2"] <= 10],
        x="grade_math_t1",
        y="grade_math_t2",
        hue="treatment",
        palette=["coral", "teal"],
        s=20,
        alpha=0.3,
    )
    return (sns,)


@app.cell
def _(df):
    import altair as alt

    alt.Chart(df[df["grade_math_t2"] <= 10], width=600, height=400, padding=20).mark_circle(
        size=60, opacity=0.9
    ).encode(
        x="grade_math_t1",
        y="grade_math_t2",
        color=alt.Color("treatment:N", scale=alt.Scale(range=["coral", "teal"])),
    )
    return


@app.cell
def _(df, sns):
    import matplotlib.pyplot as plt

    def plot_scatter(df):
        dfc = df[df["grade_math_t2"] <= 10]
        # define a function for recurring tasks
        plt.figure(figsize=(8, 6))
        sns.scatterplot(
            data=dfc,
            x="grade_math_t1",
            y="grade_math_t2",
            hue="treatment",
            palette=["coral", "teal"],
            s=20,
            alpha=0.3,
        )  # data cleaning
        plt.title("Math Grade Comparison")
        plt.tight_layout()
        plt.show()

    plot_scatter(
        df
    )  # Assigning to a variable is optional if you just want to show it  # add a title  # This renders the plot cleanly
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Exercises

    1. tweak the csv_read() function ensuring the date_of_birth column is recognized as a date.

    2. write a boolean index for nationality = 1

    3. find the average grade_math_t1 specifically for female ('F') students.

    3. find all rows where 'grade_math_t1 and grade_science_t2 > 9.5

    4. find all students born after 1997-01-01

    5. create a new column called avg_math which contains the average math scores per student (grade_math_t1 + grade_math_t2)/2

    6. find outliers.

    7. use the .query() method to find all **female** students in grade 6.

    8. calculate the median score for grade_science_t2 and compare it to the mean. What does this suggest about the distribution?

    9. find the average grade_math_t1 scores for all students with treatment = 1 and average grade_math_t1 scores with treatment = 0 and compare.

    10. create a histogram of grade_math_t1 with 100 bins.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Pandas Reference

    ## pd.read_csv()
    The primary way to load data. Think of this as defining your source table.

    **sep**:

    Defines the character used to separate columns. Defaults to `,`.

    `df = pd.read_csv("data.csv", sep=";")`

    **encoding**:

    If you see weird symbols or "UnicodeDecodeErrors," try 'utf-8', 'latin1', or 'cp1252'.

    `df = pd.read_csv("data.csv", encoding='latin1')`

    **parse_dates**:

    Pass a list of columns to convert them to datetime objects immediately.

    `df = pd.read_csv("data.csv", parse_dates=["date_of_birth"])`

    ---

    ## Column Selection
    In SQL, this is your `SELECT` clause.

    **Single column**:

    `df['grade']`

    Returns a **Series** (a single column of data).

    **Multiple columns**:

    Returns a **DataFrame**. Note the double brackets.

    `df[['student_id', 'grade']]`

    **Slicing**:

    Selects a range of rows by position index.

    `df[0:10]` (Returns the first 10 rows).

    ---

    ## Row Selection (Filtering)
    In SQL, these are your `WHERE` clauses.

    **Boolean Indexing**

    Filtering the dataframe based on a logical condition. You may use `==, <, >, <=, >=, !=, ~`

    `df[df['grade'] > 9]`

    `df[~df['grade'] > 9]` ~ is a logical NOT, so it amounts to `df['grade'] < 9`

    The inner condition (`df['grade'] > 10`) returns a Series of **True/False** values. Wrapping it in `df[]` returns only the **True** rows.

    **df.query()**

    Allows you to filter using a string expression. Very similar to SQL syntax.

    `df.query("grade > 10 and sex == 'F'")`

    **df.loc[]**

    Label-based selection. Best for selecting specific rows and columns at the same time.

    `df.loc[df['grade'] > 10, ['student_id', 'sex']]`

    *(The first part filters rows; the second part selects columns).*

    **df.sample()**

    Returns a random subset of rows. Useful for a quick data audit.

    `df.sample(n=5)`

    ---

    ### Values & Counts
    In SQL, these are your `COUNT(col)`, `DISTINCT`, and `GROUP BY col, COUNT(*)` operations.

    **count()**:

    Counts the number of non-null values in a column.

    `df['nationality'].count()`

    **unique()**:

    Returns an array of all unique values in a column. Similar to `SELECT DISTINCT`.

    `df['grade'].unique()`

    **nunique()**:

    Returns the **number** of unique values. Similar to `COUNT(DISTINCT col)`.

    `df['school_id'].nunique()`

    **value_counts()**:

    Returns a list of all unique values and how many times they appear. This is the pandas shortcut for `GROUP BY` and `COUNT` and reveals the distribution of your categories.

    `df['sex'].value_counts()`

    ---

    ## Aggregations & Visualizations

    **Basic Statistics**

    Quickly summarize numerical data.

    `df['grade_math_t1'].mean()` (Average)

    `df.describe()` (Summary statistics for all columns)

    **Simple Plotting**

    Pandas has built-in integration with Matplotlib.

    `df['grade_math_t1'].hist()` (Histogram)

    `df.plot.scatter(x='grade_math_t1', y='grade_science_t1')` (Scatter plot)

    **Pandas plot**
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html

    **Color maps**
    https://matplotlib.org/stable/users/explain/colors/colormaps.html

    ---

    **Cheat Sheet**
    https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf

    **Official Documentation:**
    [pandas.read_csv](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html) | [Indexing and Selecting Data](https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html)
    """)
    return


if __name__ == "__main__":
    app.run()
