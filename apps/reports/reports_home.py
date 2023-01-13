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

card1 = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Top 10 Customers (Individuals)", className="card-title-1"),
            html.P(
                "This report shows the top 10 individuals "
                "that have spent the most in the store.",
                className="card-text-1",
            ),
            dbc.Button("Download Excel Report", id="btn_xlsx_1"),
            dcc.Download(id="download-dataframe-xlsx-1"),
        ],
    ),
    style={"width": "24rem"},
)

card2 = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Top 10 Customers (Institutions)", className="card-title-2"),
            html.P(
                "This report shows the top 10 institutions "
                "that have spent the most in the store.",
                className="card-text-2",
            ),
            dbc.Button("Download Excel Report", id="btn_xlsx_2"),
            dcc.Download(id="download-dataframe-xlsx-2"),
        ],
    ),
    style={"width": "24rem"},
)

card3 = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Top 10 Publishers", className="card-title-3"),
            html.P(
                "This report shows the top 10 publishers "
                "with highest total amount of orders.",
                className="card-text-3",
            ),
            dbc.Button("Download Excel Report", id="btn_xlsx_3"),
            dcc.Download(id="download-dataframe-xlsx-3"),
        ],
    ),
    style={"width": "24rem"},
)


layout = html.Div(
    [
        dbc.Card(
            [
                dbc.CardHeader(html.H4("Reports")),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(card1),
                                dbc.Col(card2),
                                dbc.Col(card3),
                            ]
                        )
                    ]
                ),
            ]
        ),
    ],
)

@app.callback(
    Output("download-dataframe-xlsx-1", "data"),
    Input("btn_xlsx_1", "n_clicks"),
    prevent_initial_call=True,
)
def download_func_1(n_clicks):
    
    # Top 10 Customers (Individuals)
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
    top10_cust_ind = db.querydatafromdatabase(sql,val,cols)

    return dcc.send_data_frame(top10_cust_ind.to_excel, "Top 10 Customers (Individuals).xlsx", sheet_name="Top 10 Customers (Individuals)")


@app.callback(
    Output("download-dataframe-xlsx-2", "data"),
    Input("btn_xlsx_2", "n_clicks"),
    prevent_initial_call=True,
)
def download_func_2(n_clicks):
    
    # Top 10 Customers (Institutions)
    sql = """ SELECT cust_ins_name, COUNT(pur_ins_amt), SUM(pur_ins_amt)
    FROM purchases_institutions
    INNER JOIN customers_institutions on purchases_institutions.cust_ins_id = customers_institutions.cust_ins_id
    WHERE NOT pur_ins_delete_ind
    GROUP BY cust_ins_name
    ORDER BY SUM(pur_ins_amt) DESC
    FETCH FIRST 10 ROWS ONLY
    """
    val = []
    cols = ["Customer", "Number of Purchases","Total Amount"]     
    top10_cust_ins = db.querydatafromdatabase(sql,val,cols)

    return dcc.send_data_frame(top10_cust_ins.to_excel, "Top 10 Customers (Institutions).xlsx", sheet_name="Top 10 Customers (Institutions)")

@app.callback(
    Output("download-dataframe-xlsx-3", "data"),
    Input("btn_xlsx_3", "n_clicks"),
    prevent_initial_call=True,
)
def download_func_3(n_clicks):
    
    # Top 10 Customers (Institutions)
    sql = """ SELECT pub_name, COUNT(pub_order_amt), SUM(pub_order_amt)
    FROM publishers_orders
    INNER JOIN publishers on publishers_orders.pub_id = publishers.pub_id
    WHERE NOT pub_order_delete_ind
    GROUP BY pub_name
    ORDER BY SUM(pub_order_amt) DESC
    FETCH FIRST 10 ROWS ONLY
    """
    val = []
    cols = ["Publisher", "Number of Fulfilled Orders","Total Amount"]     
    top10_pub = db.querydatafromdatabase(sql,val,cols)

    return dcc.send_data_frame(top10_pub.to_excel, "Top 10 Publishers.xlsx", sheet_name="Top 10 Publishers")