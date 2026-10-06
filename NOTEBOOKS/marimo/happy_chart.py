import marimo

__generated_with = "0.23.6"
app = marimo.App(width="full")


@app.cell
def _():
    import pandas as pd
    import country_converter as coco
    import logging

    return coco, logging, pd


@app.cell
def _(pd):
    pd.options.display.float_format = "{:.2f}".format
    return


@app.cell
def _(pd):
    # hdi_2023 = pd.read_csv("../../../Data/hdi_2023.csv", encoding="latin1")
    happy = pd.read_csv("../../../Data/happiness_clean.csv")
    # hale = pd.read_csv("../../Data/HALE_clean.csv")
    # co2 = pd.read_csv("../../Data/co2_pc_clean.csv")
    # footprint = pd.read_csv("../../Data/footprint_clean_2019.csv")
    # le = pd.read_csv("../../Data/life_expectancy_clean.csv")
    # sdg = pd.read_csv("../../Data/SDG_from2000_clean.csv")
    gdp_gni = pd.read_csv("../../../Data/GNI_GDP.csv")
    return gdp_gni, happy


@app.function
def entity_to_country(df):
    return df.rename(
        {
            "Entity": "Country",
        },
        axis=1,
        inplace=True,
    )


@app.cell
def _(gdp_gni):
    gdp_gni.rename(
        {
            "Entity": "Country",
            "GNI per capita": "GNI pc",
            "GDP per capita": "GDP pc",
            "World region according to OWID": "World region",
        },
        axis=1,
        inplace=True,
    )

    gdp_gni
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Country Coverter - Clean Country and Codes
    """)
    return


@app.cell
def _(coco, logging, pd):
    # Silence logs
    logging.getLogger("country_converter").setLevel(logging.ERROR)
    cc = coco.CountryConverter()

    def standardize_and_clean(df, country_col):
        df = df.copy()

        # --- NEW: Define Special Cases (OWID & Custom) ---
        special_cases = {
            "Northern Cyprus": {"Code": "OWID_CYN", "Name": "Northern Cyprus"},
            "Somaliland": {"Code": "OWID_SML", "Name": "Somaliland"},
            "Somaliland region": {"Code": "OWID_SML", "Name": "Somaliland"},
        }

        # 1. Define groups to skip
        groups = [
            "Africa",
            "Asia",
            "Europe",
            "North America",
            "South America",
            "Oceania",
            "High-income countries",
            "Low-income countries",
            "Lower-middle-income countries",
            "Upper-middle-income countries",
            "World",
            "European Union",
            "Total",
        ]

        # 2. Identify aggregate rows
        # We exclude our special cases from being accidentally flagged as aggregates
        is_special = df[country_col].isin(special_cases.keys())

        is_aggregate = (
            (
                df[country_col].str.contains(r"\(.*\)", na=False)
                | df[country_col].str.contains(
                    "income|countries|World|Union|Total", case=False, na=False
                )
                | df[country_col].isin(groups)
                | (df[country_col].str.len() > 35)
            )
            & ~is_special  # Don't drop it if it's a special case
        )

        # 3. Process unique valid names
        valid_candidates = df.loc[~is_aggregate, country_col].unique().tolist()

        if not valid_candidates:
            return pd.DataFrame()

        # 4. Generate Mappings
        iso_map = {}
        name_map = {}

        # Split candidates into special and standard for coco
        for name in valid_candidates:
            if name in special_cases:
                iso_map[name] = special_cases[name]["Code"]
                name_map[name] = special_cases[name]["Name"]
            else:
                # Convert standard names via coco
                # We use not_found="not found" to filter out garbage later
                res_iso = cc.convert(names=name, to="ISO3", not_found="not found")
                res_name = cc.convert(names=name, to="name_short", not_found="not found")

                iso_map[name] = res_iso
                name_map[name] = res_name

        # 5. Create new columns and filter
        df["Country_Clean"] = df[country_col].map(name_map)
        df["Code_Clean"] = df[country_col].map(iso_map)

        # Clean up results that coco failed on (marked as "not found")
        df = (
            df[df["Code_Clean"] != "not found"].dropna(subset=["Code_Clean"]).reset_index(drop=True)
        )

        # 6. Reorder and Clean Columns
        cols_to_drop = [country_col]
        if "Code" in df.columns:
            cols_to_drop.append("Code")

        other_cols = [
            c for c in df.columns if c not in cols_to_drop + ["Country_Clean", "Code_Clean"]
        ]
        df = df[["Country_Clean", "Code_Clean"] + other_cols]
        df = df.rename(columns={"Country_Clean": "Country", "Code_Clean": "Code"})

        return df

    return (standardize_and_clean,)


@app.cell
def _(happy):
    # Look for any country name that starts with 'Cyprus' or 'Somalia'
    # or contains common regional keywords.
    keywords = ["Cyprus", "Somalia", "Somaliland", "North", "South"]
    mask = happy["Country"].str.contains("|".join(keywords), case=False, na=False)

    # Display unique names to see what we are dealing with
    print(happy[mask]["Country"].unique())

    # View the actual duplicates
    happy[mask].sort_values(by=["Country", "Year"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""

    """)
    return


@app.cell
def _(gdp_gni, happy, standardize_and_clean):
    gdp_gni_c = standardize_and_clean(gdp_gni, "Country")
    happy_c = standardize_and_clean(happy, "Country")
    return gdp_gni_c, happy_c


@app.cell
def _(gdp_gni_c):
    gdp_gni_c[gdp_gni_c.duplicated(subset=["Country", "Code", "Year"], keep=False)]
    # happy_c[happy_c.duplicated(subset=["Country", "Code", "Year"], keep=False)].sort_values(
    #     by=["Country", "Year"]
    # )
    # happy[happy["Country"].isin(["Cyprus", "Somalia"])].sort_values(by=["Country", "Year"])
    # happy[happy["Country"].isin(["Cyprus", "Somalia"])].sort_values(by=["Country", "Year"])
    return


@app.cell
def _(gdp_gni_c, happy_c):
    happy_gdp = happy_c.merge(gdp_gni_c, on=["Country", "Code", "Year"], how="outer")
    return (happy_gdp,)


@app.cell
def _(happy_gdp):
    happy_gdp[happy_gdp.duplicated(subset=["Country", "Code", "Year"], keep=False)]
    return


@app.cell
def _(happy_c):
    # happy_c.query("Code == CYP")
    happy_c[happy_c["Country"] == "Cyprus"]
    return


@app.cell
def _(pd, standardize_and_clean):
    hpi_all = pd.read_csv("../../../Data/happy_planet_index/happy_planet_index_all.csv")

    hpi_all.rename(
        {
            "country": "Country",
            "year": "Year",
            "life_expectancy": "HPI Life Expectancy",
            "wellbeing": "HPI Wellbeing",
            "carbon_footprint": "HPI Footprint",
            "hpi_score": "HPI",
            "rank": "HPI Rank",
            "change": "HPI Change",
        },
        axis=1,
        inplace=True,
    )

    # hpi_all
    hpi_all_c = standardize_and_clean(hpi_all, "Country")
    return (hpi_all_c,)


@app.cell
def _(hpi_all_c):
    hpi_all_c[hpi_all_c.duplicated(subset=["Country", "Code", "Year"], keep=False)]
    return


@app.cell
def _(happy_gdp, hpi_all_c):
    happy_hpi = happy_gdp.merge(hpi_all_c, on=["Country", "Code", "Year"], how="outer")
    happy_hpi
    return (happy_hpi,)


@app.cell
def _(pd, standardize_and_clean):
    spi_2021 = pd.read_csv("../../../Data/social_progress_index/social_progress_index_2021.csv")
    spi_2022 = pd.read_csv("../../../Data/social_progress_index/social_progress_index_2022.csv")
    spi_2024 = pd.read_csv("../../../Data/social_progress_index/social_progress_index_2024.csv")
    spi_2021["Year"] = 2021
    spi_2022["Year"] = 2022
    spi_2024["Year"] = 2024
    spi_all = pd.concat([spi_2021, spi_2022, spi_2024], ignore_index=True)
    spi_all.rename(
        {"country": "Country", "score": "SPI Score", "rank": "SPI Rank"}, axis=1, inplace=True
    )

    spi_all_c = standardize_and_clean(spi_all, "Country")
    spi_all_c[spi_all_c.duplicated(subset=["Country", "Code", "Year"], keep=False)]
    return (spi_all_c,)


@app.cell
def _(happy_hpi, spi_all_c):
    happy_spi = happy_hpi.merge(spi_all_c, on=["Country", "Code", "Year"], how="outer")
    happy_spi
    return (happy_spi,)


@app.cell
def _(happy_spi):
    happy_spi_s = happy_spi[
        [
            "Country",
            "Code",
            "Population",
            "World region",
            "Year",
            "Happiness Score",
            "GNI pc",
            "GDP pc",
            "HPI",
            "HPI Rank",
            "HPI Life Expectancy",
            "HPI Wellbeing",
            "HPI Footprint",
            "HPI Change",
            "SPI Score",
            "SPI Rank",
        ]
    ]

    happy_spi_s
    return (happy_spi_s,)


@app.cell
def _(happy_spi_s):
    happy_spi_s[["Year", "HPI Rank", "SPI Rank"]] = happy_spi_s[
        ["Year", "HPI Rank", "SPI Rank"]
    ].astype("Int32")
    happy_spi_s.info()
    return


@app.cell
def _(happy_spi_s):
    happy_spi_s[happy_spi_s.duplicated(subset=["Country", "Year"], keep=False)]
    return


@app.cell
def _(happy_spi_s):
    happy_spi_s.reindex
    return


@app.cell
def _(pd):
    working_hours = pd.read_csv("../../../Data/annual-working-hours-per-worker.csv")
    working_hours.rename(columns={"Entity": "Country"}, inplace=True)
    working_hours.sort_values("Year")
    return (working_hours,)


@app.function
def duplicated_rows(df, subset_cols=["Country", "Code", "Year"]):
    return df[df.duplicated(subset=subset_cols, keep=False)].sort_values(by=subset_cols)


@app.cell
def _(standardize_and_clean, working_hours):
    working_hours_c = standardize_and_clean(working_hours, "Country")
    duplicated_rows(working_hours_c)
    return (working_hours_c,)


@app.cell
def _(happy_spi_s, working_hours_c):
    happy_work = happy_spi_s.merge(working_hours_c, on=["Country", "Code", "Year"], how="outer")
    happy_work
    return (happy_work,)


@app.cell
def _(happy_work):
    happy_work[["Country", "Year"]].duplicated().sum()
    return


@app.cell
def _(pd, standardize_and_clean):
    hdi_all = pd.read_csv("../../../Data/HDI_all_time.csv", encoding="latin1", sep=";")
    hdi_all_c = standardize_and_clean(hdi_all, "Country")
    duplicated_rows(hdi_all_c)
    return (hdi_all_c,)


@app.cell
def _(hdi_all_c):
    hdi_all_c
    return


@app.cell
def _(happy_work, hdi_all_c):
    hdi_work = hdi_all_c.merge(happy_work, on=["Country", "Year", "Code"], how="outer")
    hdi_work
    return (hdi_work,)


@app.cell
def _(hdi_work):
    hdi_work.to_csv("../../../Data/social_indicies_combined/social_indicies_master_7.csv")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Fix missing Values
    """)
    return


@app.cell
def _(pd):
    master2 = pd.read_csv("../../../Data/social_indicies_combined/social_indicies_master_7.csv")
    master2
    return (master2,)


@app.cell
def _(master2, pd):
    def find_best_data_year(df, target_col):
        results = []
        years = sorted(df["Year"].unique())

        for year in years:
            year_data = df[df["Year"] == year]
            total_rows = len(year_data)
            null_count = year_data[target_col].isna().sum()

            # Calculate percentage of missing data
            null_percentage = (null_count / total_rows) * 100 if total_rows > 0 else 100

            results.append(
                {
                    "Year": year,
                    "Missing_Values": null_count,
                    "Total_Rows": total_rows,
                    "Percent_Missing": round(null_percentage, 2),
                }
            )

        table = pd.DataFrame(results)

        # Now find the year with the lowest PERCENTAGE of missing values
        # We also filter for Percent_Missing < 100 to ignore years where the column doesn't exist at all
        valid_years = table[table["Percent_Missing"] < 100]

        if valid_years.empty:
            return table, "No years found with any data for this column."

        best_years = valid_years[
            valid_years["Percent_Missing"] == valid_years["Percent_Missing"].min()
        ]

        return table.sort_values("Percent_Missing"), best_years

    find_best_data_year(master2, "Happiness Score")
    return


@app.cell
def _(master):
    master_2024 = master[master["Year"] == 2024]
    master_2024.isna().sum()
    return


@app.cell
def _(pd):
    def impute_closest_year(df, target_year, columns_to_fix):
        df = df.copy()  # Avoid SettingWithCopy warnings

        # --- FIX 1: Filter out existing audit columns to prevent doubling ---
        actual_cols = [c for c in columns_to_fix if not c.endswith(" Source Year")]

        # 1. Setup Audit Columns
        for col in actual_cols:
            audit_col = f"{col} Source Year"
            if audit_col not in df.columns:
                # Initialize with the original year
                df[audit_col] = df["Year"]

        # Identify countries with missing data in the target year
        df_target = df[df["Year"] == target_year]
        missing_mask = df_target[actual_cols].isna().any(axis=1)
        countries_with_holes = df_target[missing_mask]["Country"].unique()

        for country in countries_with_holes:
            # Optimization: Get country data once
            country_data = df[df["Country"] == country]

            for col in actual_cols:
                val_mask = (df["Country"] == country) & (df["Year"] == target_year)

                # Check if row exists and is NaN
                current_val = df.loc[val_mask, col].values
                if len(current_val) > 0 and pd.isna(current_val[0]):
                    # Find available data for this specific column
                    available_data = country_data[country_data[col].notna()].copy()

                    if not available_data.empty:
                        # Calculate distance
                        available_data["dist"] = (available_data["Year"] - target_year).abs()

                        # Get the closest year's data
                        best_match = available_data.sort_values("dist").iloc[0]

                        # Apply the fix to the dataframe
                        df.loc[val_mask, col] = best_match[col]
                        df.loc[val_mask, f"{col} Source Year"] = best_match["Year"]

        # Return only the target year, filtered to requested columns + their audit columns
        # We use actual_cols to ensure we don't return the "Source Year Source Year" mess
        return df[df["Year"] == target_year]

    return (impute_closest_year,)


@app.cell
def _(impute_closest_year, master2):
    happiness_imputed_2024 = impute_closest_year(
        master2,
        2024,
        [
            "HDI",
            "Population",
            "Happiness Score",
            "GNI pc",
            "GDP pc",
            "HPI",
            "HPI Rank",
            "HPI Life Expectancy",
            "HPI Wellbeing",
            "HPI Footprint",
            "HPI Change",
            "SPI Score",
            "SPI Rank",
            "Working hours per worker",
        ],
    )
    return (happiness_imputed_2024,)


@app.cell
def _(happiness_imputed_2024):
    happiness_imputed_2024.columns
    return


@app.cell
def _(happiness_imputed_2024):
    # happiness_imputed_2024["Happiness Score"].isna().sum()
    happiness_imputed_2024.to_csv(
        "../../../Data/social_indicies_combined/happiness_imputed_2024.csv"
    )
    return


@app.cell
def _(happiness_imputed_2024):
    # happiness_imputed_2024[~happiness_imputed_2024["Happiness Score"].isna()].isna().sum()
    # (happiness_imputed_2024[~happiness_imputed_2024["Happiness Score"]
    #                     .isna()][happiness_imputed_2024["HDI"]
    #                                 .isna()].Country.tolist())
    happiness_imputed_2024[happiness_imputed_2024["Code"].isna()]
    happiness_imputed_2024[happiness_imputed_2024["HDI"].isna()]
    happiness_imputed_2024[happiness_imputed_2024["Happiness Score"].isna()]

    happiness_imputed_2024_d = happiness_imputed_2024[
        ~happiness_imputed_2024["Happiness Score"].isna()
    ]
    return (happiness_imputed_2024_d,)


@app.cell
def _(pd):
    # df_d.to_csv("../../../Data/social_indicies_combined/social_indicies_master_imputed.csv")
    df_2023 = pd.read_csv(
        "../../../Data/social_indicies_combined/social_indicies_master_imputed.csv"
    )
    return


@app.cell
def _(happiness_imputed_2024_d):
    happiness_imputed_2024_d.columns
    return


@app.cell
def _(happiness_imputed_2024_d):
    import altair as alt

    df = happiness_imputed_2024_d

    hover = alt.selection_point(on="mouseover", nearest=True, fields=["Country"], empty=False)
    column_options = [
        "HDI",
        "GNI pc",
        "GDP pc",
        "HPI",
        "HPI Life Expectancy",
        "HPI Wellbeing",
        "HPI Footprint",
        "SPI Score",
        "SPI Rank",
        "Working hours per worker",
    ]
    dropdown = alt.binding_select(
        options=column_options, name="Choose an index to plot against vs. the Happiness Score: "
    )
    select_var = alt.selection_point(
        fields=["column"],
        bind=dropdown,
        value=[{"column": column_options[0]}],
        name="Selection",
        toggle=False,
    )
    df_d_clean = df.dropna(subset=column_options)
    chart = (
        alt.Chart(df_d_clean)
        .transform_fold(column_options, as_=["column", "value"])
        .transform_filter("isValid(datum.value)")
        .transform_filter(select_var)
        .mark_point(filled=True, size=100)
        .encode(
            y=alt.Y(
                "Happiness Score:Q",
                axis=alt.Axis(format=".1f", tickCount=5, labelFontSize=14, titleFontSize=16),
                scale=alt.Scale(zero=False),
            ),
            x=alt.X(
                "value:Q",
                scale=alt.Scale(zero=False, padding=5),
                title="Wealth Metric",
                axis=alt.Axis(
                    tickCount=5,
                    labelFontSize=14,
                    titleFontSize=16,
                    format="$.0s",
                    titleAnchor="middle",
                    domainColor="#CBD5E1",
                    tickColor="#CBD5E1",
                    labelColor="#64748B",
                    tickSize=5,
                    domainWidth=1,
                ),
            ),
            color=alt.Color(
                "Happiness Score:Q",
                scale=alt.Scale(scheme="redyellowgreen"),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("Country:N"),
                alt.Tooltip("World region:N"),
                alt.Tooltip("Population:Q"),
                alt.Tooltip("Life Expectancy:Q"),
                alt.Tooltip("GDP pc:Q", format="$.3s", title="GDP pc."),
                alt.Tooltip("GNI pc:Q", format="$.3s", title="GNI pc."),
                alt.Tooltip("HDI:Q", title="HDI"),
                # alt.Tooltip("HDICode:N", title="HDI Code"),
                alt.Tooltip("Wellbeing:Q", title="Wellbeing"),
                alt.Tooltip("Carbon Footprint:Q", title="Carbon Footprint"),
                alt.Tooltip("HPI score:Q", title="HPI Score"),
                alt.Tooltip("SPI Score:Q", title="SPI Score"),
                alt.Tooltip("Happiness Score:Q", format=".2f"),
            ],
            size=alt.Size(
                "value:Q",  # Use the folded value (the metric chosen in dropdown)
                scale=alt.Scale(range=[10, 200]),  # Adjusted range for better visibility
                title="Measure Value",
                legend=alt.Legend(
                    orient="none",
                    legendX=30,
                    legendY=20,
                    fillColor="white",
                    padding=10,
                    cornerRadius=5,
                ),
            ),
        )
        .add_params(select_var)
        .properties(
            width=800,
            height=500,
            title={
                "text": "Wealth vs Happiness",
                "subtitle": ["GDP pc & GNI pc  "],
                "anchor": "start",
                "offset": 30,
            },
        )
        .configure_axis(
            gridColor="gray",
            gridOpacity=0.1,
            labelColor="gray",
            titleColor="black",
        )
        .configure_title(fontSize=22, subtitleFontSize=18, subtitleColor="gray")
        .add_params(hover)
        .configure_view(strokeOpacity=0.2)
    )

    chart
    return (chart,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Export
    """)
    return


@app.cell
def _(chart):
    import json

    chart.save("../../../Websites/MaCoZu/src/components/Charts/HappinessVega/chart_spec.json")
    return


@app.cell
def _():
    return


@app.cell
def _():
    # stable_cols = ["Code", "World region"]

    # happy_spi_sorted = happy_spi_s.sort_values(["Country", "Year"])
    # happy_spi_sorted[stable_cols] = happy_spi_sorted.groupby("Country")[stable_cols].ffill().bfill()
    # happy_spi_sorted
    return


if __name__ == "__main__":
    app.run()
