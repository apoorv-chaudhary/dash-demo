from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template
import flask

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np


dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

df = pd.read_csv("./no_energy.csv")
hydro_sum = df["Hydro"].sum()
thermal_sum = df["Thermal"].sum()
wind_sum = df["Wind"].sum()
new_df = pd.DataFrame({"energy_type": ["Hydro", "Thermal", "Wind"], "energy_produced": [hydro_sum, thermal_sum, wind_sum]})
new_df.head()

load_figure_template("cyborg")


app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG, dbc_css])

server = app.server

app.layout = html.Div(
    [
        dcc.Tabs(
            id="tabs",
            children=[
                dcc.Tab(
                    label="Yearly Energy Production",
                    value="tab1",
                    children = [
        html.H2(id="Header Text"),
        html.Hr(),
        html.P("Select a source of energy below: ", id='instructions'),
        dcc.Dropdown(
            options=["Hydro", "Thermal", "Wind"],
            value="Hydro",
            id="State Dropdown",
            className="dbc"
        ),
        dcc.Graph(id="Revenue Line"),
        html.P("Data: Courtesy of Statistics Norway", style={"fontsize": 8})
]
                ),
                dcc.Tab(
                    label="Total Energy Poduced",
                    value="tab2",
                    children=[html.H2(f"Energy Production breakdown over past 20 years"),
                              dcc.Graph(figure = px.pie(new_df,
                                     values="energy_produced",
                                     names="energy_type",
                                     hole=0.7,
                                     category_orders={"energy_type": ["Hydro", "Wind", "Thermal"]},
                                     color_discrete_sequence=px.colors.qualitative.T10,
                                     title = "Hydro v/s Thermal v/s Wind Energy"
                                    ))
                             ]
                )
            ]
        )
    ]
)

@app.callback(
    Output("Header Text", "children"),
    Output("Revenue Line", "figure"),
    Input("State Dropdown", "value")
)

def plot_bar_clar(energy):
    if not energy:
        raise PreventUpdate
    #df=pd.read_csv("../Data/no_energy.csv")
    fig=px.line(df,x="Year", y=energy)

    fig.update_yaxes(title=f"{energy} energy produced in GWh")

    title = f"Energy production over last 20 years by {energy.title()}"
    return title, fig

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
