from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

from app import app
from apps import dbconnect as db


layout = html.Div(
    [
        dbc.Card(
            [
                dbc.CardHeader(html.H4("Reports")),
                dbc.CardBody(
                    [
                        html.Div([
                            html.Button("Download Text", id="btn-download-txt"),
                            dcc.Download(id="download-text")
                        ]),
                    ]
                ),
            ]
        ),
    ],
)

@app.callback(
    [
        Output("download-text", "data"),
    ],
    [
        Input("btn-download-txt", "n_clicks")
    ]
)
def func(n_clicks):
    return dict(content="Hello world!", filename="hello.txt")
