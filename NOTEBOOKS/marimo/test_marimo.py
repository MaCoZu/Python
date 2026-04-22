import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md("""
    # Hello world
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    🚑
    """)
    return


@app.cell
def _(mo):
    text_input = mo.ui.text()
    mo.md(f"Enter some text: {text_input}")
    return


@app.cell
def _():
    # load an example dataset
    from vega_datasets import data

    cars = data.cars()

    # plot the dataset, referencing dataframe column names
    import altair as alt

    (
        alt.Chart(cars)
        .mark_point()
        .encode(x="Horsepower", y="Miles_per_Gallon", color="Origin")
        .interactive()
    )
    return


@app.cell
def _():
    def _():
        # load an example dataset
        from vega_datasets import data

        cars = data.cars()

        # plot the dataset, referencing dataframe column names
        import altair as alt

        return alt.Chart(cars).mark_bar().encode(x=alt.X("Miles_per_Gallon", bin=True), y="count()")

    _()
    return


if __name__ == "__main__":
    app.run()
