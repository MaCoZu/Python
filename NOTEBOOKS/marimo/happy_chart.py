import marimo

__generated_with = "0.23.2"
app = marimo.App(width="full")


@app.cell
def _():
    import pandas as pd

    return (pd,)


@app.cell
def _(pd):
    pd.options.display.float_format = "{:.2f}".format
    return


@app.cell
def _(pd):
    hdi = pd.read_csv("../../Data/hdi_from2000_cleaned.csv")
    happy = pd.read_csv("../../Data/happiness_clean.csv")
    hale = pd.read_csv("../../Data/HALE_clean.csv")
    co2 = pd.read_csv("../../Data/co2_pc_clean.csv")
    footprint = pd.read_csv("../../Data/footprint_clean_2019.csv")
    le = pd.read_csv("../../Data/life_expectancy_clean.csv")
    sdg = pd.read_csv("../../Data/SDG_from2000_clean.csv")
    gdp_gni = pd.read_csv("../../Data/GNI_GDP.csv")
    return gdp_gni, happy, hdi


@app.cell
def _(hdi):
    hdi
    return


@app.cell
def _(hdi):
    hdi_r = hdi.rename(
        columns={
            "country": "Country",
            "iso3": "Code",
            "year": "Year",
            "hdi": "HDI",
            "hdi_rank_2022": "HDIRank2022",
            "region": "Region",
            "hdicode": "HDICode",
            "pop_total": "PopTotal",
        }
    )

    hdi_r
    return (hdi_r,)


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


@app.cell
def _(happy):
    happy
    return


@app.cell
def _(gdp_gni, happy, hdi_r):
    happy_hdi = happy.merge(hdi_r, on=["Country", "Code", "Year"], how="outer")
    happy_gdp = happy_hdi.merge(gdp_gni, on=["Country", "Code", "Year"], how="outer")
    happy_gdp
    return happy_gdp, happy_hdi


@app.cell
def _(pd):
    hpi_all = pd.read_csv("../scraper/happy_planet_index_all.csv")
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
    return (hpi_all,)


@app.cell
def _(hpi_all):
    hpi_all
    return


@app.cell
def _(happy_gdp, hpi_all):
    happy_hpi = happy_gdp.merge(hpi_all, on=["Country", "Year"], how="outer")
    happy_hpi
    return (happy_hpi,)


@app.cell
def _(pd):
    spi_2021 = pd.read_csv("../scraper/social_progress_index_2021.csv")
    spi_2022 = pd.read_csv("../scraper/social_progress_index_2022.csv")
    spi_2024 = pd.read_csv("../scraper/social_progress_index_2024.csv")
    spi_2021["Year"] = 2021
    spi_2022["Year"] = 2022
    spi_2024["Year"] = 2024
    spi_all = pd.concat([spi_2021, spi_2022, spi_2024], ignore_index=True)
    spi_all.rename(
        {"country": "Country", "score": "SPI Score", "rank": "SPI Rank"}, axis=1, inplace=True
    )
    return (spi_all,)


@app.cell
def _(spi_all):
    spi_all_r = spi_all[["Country", "Year", "SPI Score", "SPI Rank"]]
    spi_all_r
    return (spi_all_r,)


@app.cell
def _(happy_hpi, spi_all_r):
    happy_spi = happy_hpi.merge(spi_all_r, on=["Country", "Year"], how="outer")
    happy_spi
    return (happy_spi,)


@app.cell
def _(happy_spi):
    happy_spi.columns
    return


@app.cell
def _(happy_spi):
    happy_spi_s = happy_spi[
        [
            "Country",
            "Code",
            "Population",
            "PopTotal",
            "World region",
            "Region",
            "Year",
            "Happiness Score",
            "HDI",
            "HDICode",
            "HDIRank2022",
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
    return (happy_spi_s,)


@app.cell
def _(happy_spi_s):
    happy_spi_s.columns
    return


@app.cell
def _(happy_spi_s):
    happy_spi_s
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Sandwich fill stable columns
    """)
    return


@app.cell
def _(happy_spi_s):
    stable_cols = ["Code", "World region", "Region"]

    happy_spi_sorted = happy_spi_s.sort_values(["Country", "Year"])
    happy_spi_sorted[stable_cols] = happy_spi_sorted.groupby("Country")[stable_cols].ffill().bfill()
    happy_spi_sorted
    return


@app.cell
def _(happy_gni_n):
    happy_gni_n["Year"] = happy_gni_n["Year"].astype(int)
    return


@app.cell
def _(happy_hdi):
    happy_hdi_2021 = happy_hdi[happy_hdi["Year"] == 2021]
    happy_hdi_2021
    return


@app.cell
def _(hpi_2021):
    hpi_2021
    return


@app.cell
def _(happy_hpi_2021, spi):
    happy_spi_2021 = happy_hpi_2021.merge(spi, on="Country", how="outer")
    happy_spi_2021
    return (happy_spi_2021,)


@app.cell
def _(happy_spi_2021):
    happy_spi_2021.columns
    return


@app.cell
def _(happy_spi_2021):
    happy_spi_2021_c = happy_spi_2021[
        [
            "Country",
            "Code",
            "Population",
            "World region",
            "Year",
            "GDP pc",
            "GNI pc",
            "HDI",
            "HDICode",
            "Life expectancy",
            "Wellbeing",
            "Carbon footprint",
            "HPI",
            "SPI Score",
            "Happiness Score",
        ]
    ]

    happy_spi_2021_c.to_csv("../../Data/happy_spi_2021.csv", index=False)
    return


@app.cell
def _(pd):
    # happy_spi_2021.to_csv("../../Data/happy_spi_2021.csv", index=False)
    happy_spi_2021_n = pd.read_csv("../../Data/happy_spi_2021.csv")
    happy_spi_2021_n.isna().sum()
    return


@app.cell
def _(pd):
    happy_spi_2021_1 = pd.read_csv("../../Data/happy_spi_2021.csv")
    happy_spi_2021_1
    return (happy_spi_2021_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## fixing nan
    """)
    return


@app.cell
def _(happy_spi_2021_1):
    happy_spi_2021_1[happy_spi_2021_1["Country"].str.startswith("Central African")]
    return


@app.cell
def _(hdi):
    hdi.head()
    return


@app.cell
def _(hdi):
    hdi[hdi["country"] == "Angola"]
    return


@app.cell
def _(happy_spi_2021_1):
    # happy_spi_2021_1["Year"] = 2021
    happy_spi_2021_1[happy_spi_2021_1["Code"].isna()]
    return


@app.cell
def _(happy_spi_2021_1):
    happy_spi_2021_1.isna().sum()
    return


@app.cell
def _(happy_spi_2021_1):
    happy_spi_2021_2 = happy_spi_2021_1.copy()
    happy_spi_2021_2 = happy_spi_2021_2.fillna(0)
    return (happy_spi_2021_2,)


@app.cell
def _(happy_spi_2021_2):
    import altair as alt

    hover = alt.selection_point(on="mouseover", nearest=True, fields=["Country"], empty=False)
    column_options = [
        "GDP pc",
        "GNI pc",
        "HDI",
        "HDICode",
        "Life Expectancy",
        "Wellbeing",
        "Carbon Footprint",
        "HPI score",
        "SPI Score",
    ]
    dropdown = alt.binding_select(options=column_options, name="Choose Wealth Metric: ")
    select_var = alt.selection_point(
        fields=["column"],
        bind=dropdown,
        value=[{"column": column_options[0]}],
        name="Selection",
        toggle=False,
    )
    chart = (
        alt.Chart(happy_spi_2021_2)
        .transform_fold(column_options, as_=["column", "value"])
        .transform_filter("datum.value > 0")
        .transform_filter(select_var)
        .mark_point(filled=True, size=100)
        .encode(
            x=alt.X(
                "Happiness Score:Q",
                axis=alt.Axis(format=".1f", tickCount=5, labelFontSize=14, titleFontSize=16),
                scale=alt.Scale(zero=False),
            ),
            y=alt.Y(
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
    # 1. Define the variables you want to switch between
    # 2. Create the dropdown menu
    # 3. Create the parameter that tracks the selection
    # 'value' sets the default starting position
    # 4. Build the chart
    # chart.save('chart_spec.json')
    chart  # "Fold" (melt) these columns  # into two new columns: 'column' (name) and 'value' (number)  # Removes any rows where the metric is missing/zero  # Filter the data to show only the selected "column"  # color='Happiness Score:Q',  # 1. This is the "detach" command  # 2. X position (pixels from left)  # 3. Y position (pixels from top)  # 4. Makes the box visible  # strokeColor='gray',  # labelBaseline='top',  # Makes it a bit wider/readable  # Main title size  # Subtitle size
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
