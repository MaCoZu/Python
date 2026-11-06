import marimo

__generated_with = "0.23.3"
app = marimo.App()


@app.cell
def _():
    import numpy as np
    import pandas as pd

    return np, pd


@app.cell
def _(pd):
    hdi = pd.read_csv("../../../../Data/hdi_all_time2.csv", encoding="latin1", sep=";")
    hdi.isnull().sum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Missing Data
    """)
    return


@app.cell
def _(np, pd):
    df_miss = pd.DataFrame({
        "Student_ID": [101, 102, 103, 104, 101, 105, 106, 107, 108],
        "Name": ["Alice", "Bob", "Charlie", "David", "Alice", "Eve", "Frank", "Grace", "Heidi"],
        "Math_Score": [85, 90, np.nan, 70, 85, np.nan, 95, np.nan, 88],
        "Science_Score": [82, np.nan, 78, np.nan, 82, 91, np.nan, 85, 80],
        "Attendance_pct": [95, 80, 75, np.nan, 95, 60, 100, np.nan, 92],
        "Class_Section": ["A", "A", "B", "B", "A", "A", "B", "B", "A"],
    })
    return (df_miss,)


@app.cell
def _(df_miss):
    # Show which rows are repeats
    # df_miss.duplicated()
    # df_miss[df_miss.duplicated(keep="first")]
    # df_miss[df_miss.duplicated(keep=False)]

    # Keep only the first occurrence
    df_miss_clean = df_miss.drop_duplicates()
    df_miss_clean.duplicated()
    return


@app.cell
def _(df_miss):
    df_miss
    return


@app.cell
def _(df_miss):
    # df_miss.dropna()
    # df_miss.dropna(subset=["Math_Score"])
    df_miss
    return


@app.cell
def _(df_miss):
    df_miss["Math_Score"].fillna(0)
    return


@app.cell
def _(df_miss):
    # df_miss["Math_Score"] = df_miss["Math_Score"].fillna(0)
    # df_miss


    # # fill with agg function
    df_miss["Science_Score"] = df_miss["Science_Score"].fillna(df_miss["Science_Score"].mean())
    df_miss["Attendance_pct"] = df_miss["Attendance_pct"].fillna(df_miss["Attendance_pct"].min())
    df_miss
    return


@app.cell
def _(np, pd):
    # Create a range of dates
    dates = pd.date_range(start="2024-01-01", periods=7, freq="D")

    weather = pd.DataFrame({
        "Date": dates,
        "City": ["Berlin"] * 7,
        "Temp_Celsius": [2.1, np.nan, 3.5, np.nan, np.nan, 1.8, 2.0],
    })

    weather
    return (weather,)


@app.cell
def _(weather):
    weather["Temp_Celsius_ffill"] = weather["Temp_Celsius"].ffill()
    weather["Temp_Celsius_bfill"] = weather["Temp_Celsius"].bfill()
    weather["Temp_Celsius_bfill_l"] = weather["Temp_Celsius"].bfill(limit=1)
    weather
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Dates
    """)
    return


@app.cell
def _(pd):
    df_date = pd.DataFrame({
        "Customer_ID": [1, 2, 3, 4, 5],
        "Signup_Date": ["2023-01-15", "15/01/2023", "Jan 20, 2023", "2023.01.25", None],
        "Last_Login": [
            "2024-03-01 14:30:40",
            "2024-03-02 09:15:60",
            "2024-03-05 22:00:10",
            "2024-03-07 12:00:05",
            "2024-03-10 08:00:19",
        ],
        "Birth_Year": [1990, 1985, 2000, 1978, 1995],
    })
    return (df_date,)


@app.cell
def _(df_date):
    df_date.info()
    return


@app.cell
def _(df_date, pd):
    df_date["Last_Login"] = pd.to_datetime(df_date["Last_Login"])
    df_date["Last_Login"]
    return


@app.cell
def _(df_date):
    df_date
    return


@app.cell
def _(df_date, pd):
    df_date["Signup_Date"] = pd.to_datetime(df_date["Signup_Date"], format="mixed")
    return


@app.cell
def _(df_date):
    df_date
    return


@app.cell
def _(df_date):
    # df_date["Signup_Date"].dt.
    df_date["Signup_Date"].dt.day_name()
    return


@app.cell
def _(df_date, pd):
    # How long has it been since they signed up?
    reference_date = pd.Timestamp("2024-04-01")
    df_date["Account_Age"] = reference_date - df_date["Signup_Date"]
    df_date["Account_Age_Days"] = df_date["Account_Age"].dt.days
    df_date
    return


@app.cell
def _(df_date):
    # Calculate difference between logins
    df_date["Inactivity_Period"] = df_date["Last_Login"].diff()  # Difference from the previous row
    df_date
    return


@app.cell
def _(df_date, pd):
    # Keep full timestamp (Datetime)
    df_date["Last_Login_Full"] = pd.to_datetime(df_date["Last_Login"])

    # Extract just the date (Date)
    df_date["Last_Login_Date"] = df_date["Last_Login_Full"].dt.date
    df_date
    return


@app.cell
def _(df_date):
    df_date["Last_Login_Full"].dt.floor("min")
    return


@app.cell
def _():
    # df_date["Signup_Date"] = df_date["Signup_Date"].dt.date
    # df_date["Last_Login"] = df_date["Last_Login"].dt.date
    return


@app.cell
def _(df_date, pd):
    # Convert 1990 (int) to 1990-01-01 (datetime)
    df_date["Birth_Date"] = pd.to_datetime(df_date["Birth_Year"], format="%Y")
    return


@app.cell
def _(df_date):
    df_date["Birth_Date"].dt.date
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Replace
    """)
    return


@app.cell
def _():
    return


@app.cell
def _(pd):
    df_replace = pd.DataFrame({
        "Ticket_ID": [1, 2, 3, 4, 5, 6],
        "Status": ["Open!", "In Progress", "Closed", "None", "Pending", "In Progress"],
        "Phone Number": ["555-1234", "555.5678", "!Unknown", "555-9999", "N/A", "555 0000"],
        "Feedback": ["Great!", "Bad...", "very happy", "Terrible!!!", "Happy", "Excellent service"],
        "Costs": ["$3.28", "$5.5", "$8.41", "$1.2", "$9.76", "4.83"]
    })
    df_replace
    return (df_replace,)


@app.cell
def _(df_replace):
    df_replace["Status"].unique()
    return


@app.cell
def _(df_replace):
    df_replace.replace('!', '', regex=True)
    return


@app.cell
def _(df_replace):
    # Replace specific strings with a standard value
    df_replace["Status"] = df_replace["Status"].replace(["None", "Pending"], "Open")
    df_replace
    return


@app.cell
def _(df_replace):
    df_replace.columns = df_replace.columns.str.replace(' Number', '', regex=False)
    df_replace
    return


@app.cell
def _(df_replace):
    # Using a dictionary for multiple different replacements at once
    df_replace["Status"] = df_replace["Status"].replace({"In Progress": "Active", "Closed": "Resolved"})

    df_replace
    return


@app.cell
def _(df_replace):
    df_replace.replace(
        {
        'Feedback': {'!': '', 'Great': 'Good', "very happy": "Good", "Terrible": "Bad", "Happy": "Good"},
        'Costs': {r'\$': ''},
        },
    regex=True)
    return


@app.cell
def _(df_replace):
    df_replace
    return


@app.cell
def _(df_replace):
    # Standardize "very happy" and "Happy" to "Positive"
    # (?i) is the regex flag for "ignore case"
    df_replace.replace({'Feedback': {r'(?i)happy': 'Good'}}, regex=True)
    return


@app.cell
def _(df_replace):
    # Replace any non-digit (except the start) with a dash
    # This turns 555.5678 and 555 0000 into 555-5678 and 555-0000
    df_replace['Phone'] = df_replace['Phone'].replace(r'[^\d]', '-', regex=True)
    df_replace
    return


@app.cell
def _(df_replace):
    df_replace.columns = df_replace.columns.str.replace(' ', '_')
    df_replace
    return


@app.cell
def _(df_replace):
    # reintroduce 'dirty' NA values just to clean them in the next cell
    df_replace.loc[0, 'Status'] = 'Unknown'
    df_replace.loc[1, 'Phone'] = 'N/A'
    df_replace
    return


@app.cell
def _(df_replace, np):
    # Turn placeholder strings into actual NaN objects
    df_replace.replace(['Unknown', 'N/A', "---", "-------"], np.nan)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Import
    """)
    return


@app.cell
def _(np, pd):
    # read_csv() params
    df = pd.read_csv("example.csv",
                     dtype={'Postal_Code': str, 'Score': np.float32}, # assign data types
                     parse_dates=['Year', 'Date'], # declare datetime
                     index_col='Country_Code', # make index
                     skiprows=990, # skip the first x rows
                     converters={'growth': lambda x: float(x.strip('%')) / 100}, # clean columns
                     on_bad_lines='skip', # avoid errors
                     na_values=['..', 'Missing', 'N/A'] # define what is na
                     )
    return


@app.cell
def _(pd):
    df_excel = pd.read_excel("example.xlsx",
            # sheet_name=None,
            sheet_name="Data",
            #  sheet_name=[0, 1, "Data"],
            header=2, # col names in row 3
            usecols="A:C, G", # use col A to C and G
            index_col="Date",
            skipfooter=5
            )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Maddison - Excel Data
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `tail -n 100 data.csv > last_rows.csv`
    """)
    return


@app.cell
def _(pd):
    maddison = pd.read_excel(
        "../../../../Data/maddison2023.xlsx", sheet_name="Full data", dtype={"year": "Int16"}
    )
    maddison
    return (maddison,)


@app.cell
def _(maddison):
    maddison[(maddison["year"] > 1700) & (maddison["country"] == "India")].plot.line(
        x="year", y="gdppc"
    )
    return


@app.cell
def _(maddison):
    (maddison[(maddison["year"] > 1700) & (maddison["country"].isin(["India", "Pakistan"]))])
    return


@app.cell
def _(maddison):
    (
        maddison[
            (maddison["year"] > 1800) & (maddison["country"].isin(["India", "Pakistan", "Afghanistan"]))
        ].pivot(index="year", columns="country", values="gdppc")
    )
    return


@app.cell
def _():
    # (
    #     maddison[
    #         (maddison["year"] > 1700) & (maddison["country"].isin(["India", "Pakistan", "Afghanistan"]))
    #     ]
    #     .pivot(index="year", columns="country", values="gdppc")
    #     .plot.line()
    # )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Footprint
    """)
    return


@app.cell
def _(pd):
    footprint = pd.read_csv("../../../../Data/footprint_clean_2019.csv")
    footprint
    return (footprint,)


@app.cell
def _(footprint, pd):
    footprint["Population (millions)"] = pd.to_numeric(footprint["Population (millions)"])
    return


@app.cell
def _(footprint):
    footprint["Population (millions)"] = (
        footprint["Population (millions)"]
        .replace( ",", "", regex=True)
        .str.strip()
    )
    return


@app.cell
def _(footprint):
    footprint.head()
    return


@app.cell
def _(footprint):
    footprint.rename(columns={"Life Exectancy": "Life Expectancy"}, inplace=True)
    footprint
    return


@app.cell
def _(footprint, pd):
    # footprint["Life Expectancy"].str.strip().astype("Int16")

    footprint["Life Expectancy"] = pd.to_numeric(
        footprint["Life Expectancy"], downcast="integer"
    ).astype("Int16")

    footprint
    return


@app.cell
def _(footprint, pd):
    footprint["HDI"] = pd.to_numeric(footprint["HDI"].str.strip())
    footprint["SDGi"] = pd.to_numeric(footprint["SDGi"].str.strip())
    footprint
    return


if __name__ == "__main__":
    app.run()
