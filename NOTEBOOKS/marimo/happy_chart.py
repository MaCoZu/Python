import marimo

__generated_with = "0.23.3"
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
    # Silence logs to prevent the "not found in regex" spam
    logging.getLogger("country_converter").setLevel(logging.ERROR)

    cc = coco.CountryConverter()

    def standardize_and_clean(df, country_col):
        df = df.copy()

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
        is_aggregate = (
            df[country_col].str.contains(r"\(.*\)", na=False)
            | df[country_col].str.contains(
                "income|countries|World|Union|Total", case=False, na=False
            )
            | df[country_col].isin(groups)
            | (df[country_col].str.len() > 35)
        )

        # 3. Process unique valid names only (efficiency)
        valid_candidates = df.loc[~is_aggregate, country_col].unique().tolist()

        if not valid_candidates:
            return pd.DataFrame()  # Or handle empty case as needed

        # 4. Generate Mappings
        # We use not_found=None so we can easily drop failed matches later
        iso3_list = cc.convert(names=valid_candidates, to="ISO3", not_found="not found")
        name_list = cc.convert(names=valid_candidates, to="name_short", not_found="not found")

        # Ensure coco returns lists even for single results
        if isinstance(iso3_list, str):
            iso3_list = [iso3_list]
        if isinstance(name_list, str):
            name_list = [name_list]

        iso_map = dict(zip(valid_candidates, iso3_list))
        name_map = dict(zip(valid_candidates, name_list))

        # 5. Create new columns and filter
        df["Country_Clean"] = df[country_col].map(name_map)
        df["Code_Clean"] = df[country_col].map(iso_map)

        # Drop rows that failed conversion (the aggregates or unrecognized strings)
        df = df.dropna(subset=["Code_Clean"]).reset_index(drop=True)

        # 6. Reorder and Clean Columns
        # Identify original columns to drop (including any 'Code' column if it exists)
        cols_to_drop = [country_col]
        if "Code" in df.columns:
            cols_to_drop.append("Code")

        # Get list of 'other' columns
        other_cols = [
            c for c in df.columns if c not in cols_to_drop + ["Country_Clean", "Code_Clean"]
        ]

        # Final assembly: Clean Country, Clean Code, then everything else
        df = df[["Country_Clean", "Code_Clean"] + other_cols]

        # Optional: Rename back to standard names
        df = df.rename(columns={"Country_Clean": "Country", "Code_Clean": "Code"})

        return df

    return (standardize_and_clean,)


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
def _(happy_c):
    # gdp_gni_c[gdp_gni_c.duplicated(subset=["Country", "Code", "Year"], keep=False)]
    happy_c[happy_c.duplicated(subset=["Country", "Code", "Year"], keep=False)].sort_values(
        by=["Country", "Year"]
    )
    # happy[happy["Country"].isin(["Cyprus", "Somalia"])].sort_values(by=["Country", "Year"])
    # happy[happy["Country"].isin(["Cyprus", "Somalia"])].sort_values(by=["Country", "Year"])
    return


@app.cell
def _(gdp_gni_c, happy_c):
    happy_gdp = happy_c.merge(gdp_gni_c, on=["Country", "Code", "Year"], how="outer")
    return (happy_gdp,)


@app.cell
def _(happy_gdp):
    happy_gdp.duplicated(subset=["Country", "Code", "Year"], keep=False)
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
    # hpi_all_c
    return (hpi_all_c,)


@app.cell
def _(happy_gdp, hpi_all_c):
    happy_hpi = happy_gdp.merge(hpi_all_c, on=["Country", "Code", "Year"], how="inner")
    happy_hpi
    return (happy_hpi,)


@app.cell
def _(happy_hpi, pd, standardize_and_clean):
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
    happy_spi = happy_hpi.merge(spi_all_c, on=["Country", "Code", "Year"], how="inner")
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
def _(happy):
    happy[happy["Country"].isin(["Cyprus"])]
    return


@app.cell
def _():
    return


@app.cell
def _(happy_spi):
    happy_spi_c = happy_spi[
        ~happy_spi["Country"].isin(
            [
                "Africa",
                "Asia",
                "Europe",
                "North America",
                "South America",
                "Oceania",
                "High-income countries",
                "High-income countries",
                "Low-income countries",
                "Low-income countries",
                "Lower-middle-income countries",
                "Lower-middle-income countries",
                "Upper-middle-income countries",
                "Upper-middle-income countries",
            ]
        )
    ]

    happy_spi_c[happy_spi.duplicated(subset=["Country", "Year"], keep=False)]
    return (happy_spi_c,)


@app.cell
def _(pd):
    working_hours = pd.read_csv("../../../Data/annual-working-hours-per-worker.csv")
    working_hours.rename(columns={"Entity": "Country"}, inplace=True)
    working_hours.sort_values("Year")
    return (working_hours,)


@app.cell
def _(happy_spi_c, working_hours):
    happy_work = happy_spi_c.merge(working_hours, on=["Country", "Year"], how="outer")
    happy_work[["Country", "Code_x", "Code_y"]]
    return (happy_work,)


@app.cell
def _(happy_work):
    happy_work["Code_x"] = happy_work["Code_x"].combine_first(happy_work["Code_y"])
    happy_work[["Country", "Code_x", "Code_y"]].isna().sum()
    happy_work[["Country", "Year"]].duplicated().sum()
    return


@app.cell
def _(happy_work):
    # happy_work.drop(columns="Code_y", inplace=True)
    # happy_work.rename(columns={"Code_x": "Code"}, inplace=True)
    # happy_work.columns = happy_work.columns.str.replace("HPI", "Happy Planet Index")
    happy_work.columns = happy_work.columns.str.replace(
        "Global Social Progress Index", "Social Progress Index"
    )
    return


@app.cell
def _(happy_work):
    happy_work.columns
    return


@app.cell
def _(pd):
    hdi_all = pd.read_csv("../../../Data/HDI_all_time.csv", encoding="latin1", sep=";")
    hdi_all
    return (hdi_all,)


@app.cell
def _(happy_work, hdi_all):
    hdi_work = hdi_all.merge(happy_work, on=["Country", "Year", "Code"], how="outer")
    hdi_work
    return (hdi_work,)


@app.cell
def _(hdi_work):
    hdi_work.to_csv("../../../Data/social_indicies_combined/social_indicies_master_6.csv")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Fix missing Values
    """)
    return


@app.cell
def _(pd):
    master = pd.read_csv("../../../Data/social_indicies_combined/social_indicies_master_6.csv")
    master
    return (master,)


@app.cell
def _(master, pd):
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

    find_best_data_year(master, "Happiness Score")
    return


@app.cell
def _(master):
    master_2024 = master[master["Year"] == 2024]
    master_2024.isna().sum()
    return


@app.cell
def _(master):
    master.columns
    return


@app.cell
def _(pd):
    def impute_closest_year(df, target_year, columns_to_fix):
        # 1. Setup Audit Columns
        for col in columns_to_fix:
            audit_col = f"{col} Source Year"
            if audit_col not in df.columns:
                df[audit_col] = df["Year"]

        # Identify countries with missing data in the target year
        df_target = df[df["Year"] == target_year]
        missing_mask = df_target[columns_to_fix].isna().any(axis=1)
        countries_with_holes = df_target[missing_mask]["Country"].unique()

        for country in countries_with_holes:
            # Get all data for this country once to save time
            country_data = df[df["Country"] == country]

            for col in columns_to_fix:
                val_mask = (df["Country"] == country) & (df["Year"] == target_year)

                # Only proceed if the value is actually NaN
                if pd.isna(df.loc[val_mask, col].values[0]):
                    # Find all years where this specific column is NOT null
                    available_data = country_data[country_data[col].notna()].copy()

                    if not available_data.empty:
                        # CALCULATE DISTANCE: |Year - Target|
                        available_data["dist"] = (available_data["Year"] - target_year).abs()

                        # Sort by distance (closest first)
                        # If distance is equal (e.g., 2020 and 2022), it picks the first one
                        best_match = available_data.sort_values("dist").iloc[0]

                        # Apply the fix
                        df.loc[val_mask, col] = best_match[col]
                        df.loc[val_mask, f"{col} Source Year"] = best_match["Year"]

        return df[df["Year"] == target_year]

    return (impute_closest_year,)


@app.cell
def _(impute_closest_year, master):
    happiness_imputed_2024 = impute_closest_year(
        master,
        2024,
        [
            "Happiness Score",
            "GNI pc",
            "GDP pc",
            "Population",
            "World region",
            "Happy Planet Index Rank",
            "Happy Planet Index Life Expectancy",
            "Happy Planet Index Wellbeing",
            "Happy Planet Index Footprint",
            "Happy Planet Index",
            "Happy Planet Index Change",
            "Social Progress Index Score",
            "Social Progress Index Rank",
            "Working hours per worker",
        ],
    )
    return (happiness_imputed_2024,)


@app.cell
def _(happiness_imputed_2024):
    # happiness_imputed_2024["Happiness Score"].isna().sum()
    happiness_imputed_2024.to_csv(
        "../../../Data/social_indicies_combined/happiness_imputed_2023.csv"
    )
    return


@app.cell
def _(happiness_imputed_2024):
    # happiness_imputed_2024[~happiness_imputed_2024["Happiness Score"].isna()].isna().sum()
    # (happiness_imputed_2024[~happiness_imputed_2024["Happiness Score"]
    #                     .isna()][happiness_imputed_2024["HDI"]
    #                                 .isna()].Country.tolist())
    happiness_imputed_2024[happiness_imputed_2024["Happiness Score"].isna()]
    happiness_imputed_2024[happiness_imputed_2024["HDI"].isna()]
    happiness_imputed_2024[happiness_imputed_2024["Code"].isna()]
    return


@app.cell
def _():
    continents = [
        "Africa",
        "Asia",
        "Europe",
        "North America",
        "South America",
        "Oceania",
        "High-income countries",
        "High-income countries",
        "Low-income countries",
        "Low-income countries",
        "Lower-middle-income countries",
        "Lower-middle-income countries",
        "Upper-middle-income countries",
        "Upper-middle-income countries",
        #   "Bolivia",
        #   "Cote d'Ivoire",
        # "Democratic Republic of Congo",
        #   "Eswatini",
        #   "Hong Kong",
        #   "Iran",
        #   "Kosovo",
        #   "Laos",
        #   "Moldova",
        #   "Palestine",
        #   "Puerto Rico",
        #   "Russia",
        #   "South Korea",
        #   "Syria",
        #   "Taiwan",
        #   "Tanzania",
        #   "Turkey",
        #   "Venezuela",
        #   "Vietnam"
    ]
    return (continents,)


@app.cell
def _(master_2):
    master_2[master_2["Country"] == "Bahamas"]
    return


@app.cell
def _(continents, happiness_imputed_2023):
    df_wc = happiness_imputed_2023[~happiness_imputed_2023["Country"].isin(continents)]
    # df_wc.isna().sum()
    df_wc[["Country", "Happiness Score"]]
    return (df_wc,)


@app.cell
def _(df_wc):
    df_d = df_wc.dropna(subset="Happiness Score")
    df_d.isna().sum()
    return (df_d,)


@app.cell
def _(pd):
    # df_d.to_csv("../../../Data/social_indicies_combined/social_indicies_master_imputed.csv")
    df_2023 = pd.read_csv(
        "../../../Data/social_indicies_combined/social_indicies_master_imputed.csv"
    )
    return (df_2023,)


@app.cell
def _(df_2023):
    df_2023
    return


@app.cell
def _(df_2023):
    # df_2023.loc[df_2023["Country"] == "Syria", "Region"] = "AS"
    # df_2023.loc[df_2023["Country"] == "Syria", "World region"] = "Asia"
    # df_2023.loc[df_2023["Country"] == "Syria"]
    # df_2023.isna().sum()
    df_2023[df_2023["HDI"].isna()]["Country"].to_list()
    # df_2023[df_2023["Country"]=="Spain"]
    return


@app.cell
def _(df_2023):
    df_2023[df_2023["Country"].str.contains("Türkiye")]
    return


@app.cell
def _(df_d):
    import seaborn as sns

    sns.jointplot(df_d, x="HPI Life Expectancy", y="Happiness Score", color="#4CB391")
    # df_d.plot(kind="scatter", x="GDP pc", y="Happiness Score")
    return


@app.cell
def _(df_d):
    df_d.columns
    return


@app.cell
def _(df_d):
    import altair as alt

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
    df_d_clean = df_d.dropna(subset=column_options)
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
                alt.Tooltip("HDICode:N", title="HDI Code"),
                alt.Tooltip("Wellbeing:Q", title="Wellbeing"),
                alt.Tooltip("Carbon Footprint:Q", title="Carbon Footprint"),
                alt.Tooltip("HPI score:Q", title="HPI Score"),
                alt.Tooltip("SPI Score:Q", title="SPI Score"),
                alt.Tooltip("Happiness Score:Q", format=".2f"),
            ],
            size=alt.condition(
                hover,
                alt.value(400),
                alt.Size(
                    "Happiness Score:Q",
                    scale=alt.Scale(range=[10, 200]),
                    title="HDI",
                    legend=alt.Legend(
                        orient="none",
                        legendX=30,
                        legendY=20,
                        fillColor="white",
                        padding=10,
                        cornerRadius=5,
                        direction="vertical",
                        labelAlign="center",
                        labelOffset=20,
                        titleOrient="top",
                        gradientLength=200,
                    ),
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
