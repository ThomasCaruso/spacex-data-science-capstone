"""Interactive Plotly Dash dashboard for Falcon 9 launch outcomes."""

from __future__ import annotations

from dash import Dash, Input, Output, dcc, html
import pandas as pd
import plotly.express as px

from common import load_csv


DATA = load_csv("spacex_launch_dash.csv")

SITE_COLUMN = "Launch Site"
CLASS_COLUMN = "class"
PAYLOAD_COLUMN = "Payload Mass (kg)"

required_columns = {SITE_COLUMN, CLASS_COLUMN, PAYLOAD_COLUMN}
missing_columns = required_columns.difference(DATA.columns)
if missing_columns:
    raise ValueError(
        f"spacex_launch_dash.csv is missing columns: {sorted(missing_columns)}"
    )

sites = sorted(DATA[SITE_COLUMN].dropna().unique())
minimum_payload = int(DATA[PAYLOAD_COLUMN].min())
maximum_payload = int(DATA[PAYLOAD_COLUMN].max())

app = Dash(__name__)
app.title = "SpaceX Launch Dashboard"

app.layout = html.Div(
    [
        html.H1(
            "SpaceX Falcon 9 Launch Dashboard",
            style={"textAlign": "center", "marginBottom": "8px"},
        ),
        html.P(
            "Explore landing success by launch site and payload mass.",
            style={"textAlign": "center", "marginBottom": "24px"},
        ),
        html.Div(
            [
                html.Label("Launch site"),
                dcc.Dropdown(
                    id="site-dropdown",
                    options=[{"label": "All sites", "value": "ALL"}]
                    + [{"label": site, "value": site} for site in sites],
                    value="ALL",
                    clearable=False,
                ),
            ],
            style={"maxWidth": "700px", "margin": "0 auto 24px auto"},
        ),
        dcc.Graph(id="success-pie-chart"),
        html.Div(
            [
                html.Label("Payload range (kg)"),
                dcc.RangeSlider(
                    id="payload-slider",
                    min=minimum_payload,
                    max=maximum_payload,
                    step=100,
                    value=[minimum_payload, maximum_payload],
                    marks={
                        minimum_payload: str(minimum_payload),
                        maximum_payload: str(maximum_payload),
                    },
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
            ],
            style={"maxWidth": "900px", "margin": "20px auto 10px auto"},
        ),
        dcc.Graph(id="payload-scatter-chart"),
    ],
    style={
        "fontFamily": "Arial, sans-serif",
        "maxWidth": "1200px",
        "margin": "0 auto",
        "padding": "24px",
    },
)


@app.callback(
    Output("success-pie-chart", "figure"),
    Input("site-dropdown", "value"),
)
def update_success_chart(selected_site: str):
    if selected_site == "ALL":
        site_success = (
            DATA.groupby(SITE_COLUMN, as_index=False)[CLASS_COLUMN]
            .mean()
            .assign(success_rate=lambda frame: frame[CLASS_COLUMN] * 100)
        )
        return px.bar(
            site_success,
            x=SITE_COLUMN,
            y="success_rate",
            title="Landing Success Rate by Launch Site",
            labels={"success_rate": "Success rate (%)"},
            range_y=[0, 100],
        )

    filtered = DATA[DATA[SITE_COLUMN] == selected_site]
    outcomes = (
        filtered[CLASS_COLUMN]
        .map({1: "Success", 0: "Failure"})
        .value_counts()
        .rename_axis("Outcome")
        .reset_index(name="Launches")
    )
    return px.pie(
        outcomes,
        values="Launches",
        names="Outcome",
        title=f"Landing Outcomes at {selected_site}",
        hole=0.35,
    )


@app.callback(
    Output("payload-scatter-chart", "figure"),
    [
        Input("site-dropdown", "value"),
        Input("payload-slider", "value"),
    ],
)
def update_payload_chart(selected_site: str, payload_range: list[int]):
    low, high = payload_range
    filtered = DATA[DATA[PAYLOAD_COLUMN].between(low, high)].copy()
    if selected_site != "ALL":
        filtered = filtered[filtered[SITE_COLUMN] == selected_site]

    filtered["Landing Outcome"] = filtered[CLASS_COLUMN].map(
        {1: "Success", 0: "Failure"}
    )
    flight_column = (
        "Flight Number" if "Flight Number" in filtered.columns else filtered.index.name
    )
    if flight_column is None:
        filtered = filtered.reset_index(names="Flight Number")
        flight_column = "Flight Number"

    return px.scatter(
        filtered,
        x=PAYLOAD_COLUMN,
        y=flight_column,
        color="Landing Outcome",
        symbol=SITE_COLUMN,
        hover_data=[SITE_COLUMN],
        title=f"Payload and Landing Outcomes from {low:,} to {high:,} kg",
        labels={flight_column: "Flight number"},
    )


if __name__ == "__main__":
    app.run(debug=True)
