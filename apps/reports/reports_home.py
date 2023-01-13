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
from openpyxl import Workbook


layout = html.Div(
    [
        dbc.Card(
            [
                dbc.CardHeader(html.H4("Reports")),
                dbc.CardBody(
                    [
                        html.Button("Download Excel", id="btn_xlsx"),
                        dcc.Download(id="download-dataframe-xlsx"),
                    ]
                ),
            ]
        ),
    ],
)
df = pd.DataFrame({"a": [1, 2, 3, 4], "b": [2, 1, 5, 6], "c": ["x", "x", "y", "y"]})

@app.callback(
    Output("download-dataframe-xlsx", "data"),
    Input("btn_xlsx", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(df.to_excel, "mydf.xlsx", sheet_name="Sheet_name_1")
