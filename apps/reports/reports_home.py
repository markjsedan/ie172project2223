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
                        dbc.Col("Top 10 Customers"),
                        dbc.Button("Download Excel", id="btn_xlsx"),
                        dcc.Download(id="download-dataframe-xlsx"),
                    ]
                ),
            ]
        ),
    ],
)

@app.callback(
    Output("download-dataframe-xlsx", "data"),
    Input("btn_xlsx", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks,n_clicks):
    # df = pd.DataFrame({"a": [1, 2, 3, 4], "b": [2, 1, 5, 6], "c": ["x", "x", "y", "y"]})
    
    sql = """ SELECT cust_ind_name, COUNT(pur_ind_amt), SUM(pur_ind_amt)
    FROM purchases_individuals
    INNER JOIN customers_individuals on purchases_individuals.cust_ind_id = customers_individuals.cust_ind_id
    WHERE NOT pur_ind_delete_ind
    GROUP BY cust_ind_name
    ORDER BY SUM(pur_ind_amt) DESC
    FETCH FIRST 10 ROWS ONLY
    """
    val = []
    cols = ["Customer", "Number of Purchases","Total Amount"]
        
    top10_cust = db.querydatafromdatabase(sql,val,cols)


    return dcc.send_data_frame(top10_cust.to_excel, "Top 10 Customers.xlsx", sheet_name="Top 10 Customers")
