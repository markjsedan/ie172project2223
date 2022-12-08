import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.exceptions import PreventUpdate
import pandas as pd

from app import app

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                        "Search", color="dark", className="ms-2", n_clicks=0
                    ),
                    width="auto",
                ),
                dbc.Col(dbc.Input(type="search", placeholder="Enter keyword/s")),
            ],
            className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
            align="center",
        )
    ]
)