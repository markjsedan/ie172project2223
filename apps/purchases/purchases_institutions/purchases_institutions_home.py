from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table
import dash
from dash.exceptions import PreventUpdate
import pandas as pd

from app import app
from apps import dbconnect as db
from dash.dependencies import Input, Output, State


sort_add = dbc.NavbarSimple(
    children=[
        dbc.Button("Add a purchase", color="dark", className="me-2", href="/purchases/institutions_profile?mode=add"),
    ],
    brand="",
)

nav_contents = [
    dbc.NavItem(dbc.NavLink("Individuals", href="/purchases/individuals_home")),
    dbc.NavItem(dbc.NavLink("Institutions", href="/purchases/institutions_home",active=True)),
]
navs = html.Div(dbc.Nav(nav_contents,pills=True,fill=True))

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Label(html.H5("Search"), width=1),
                dbc.Col(
                    dbc.Input(
                        type="text", id="purchases_institutions_filter", placeholder="Enter keyword/s"
                    ),
                    width=5,
                ),
            ],
            className="mb-3"
        ),
        dbc.Card(
            [
                dbc.CardHeader(html.H4("Purchases > Institutions")),
                dbc.CardBody(
                    [
                        dbc.Row(navs, style={'fontWeight':'bold',"color":"dark"}
                        ),
                        html.Hr(),
                        dbc.Row(
                            dbc.Col(sort_add),
                        ),
                        html.Div(
                            [
                                html.Div(
                                    "This will contain the table for purchases_institutions",
                                    id='purchases_institutions_list',
                                    style={'text-align': 'center'}
                                ),
                            ]
                        )
                    ]
                ),
            ]
        )
    ]
)
@app.callback(
    [
        Output('purchases_institutions_list', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('purchases_institutions_filter', 'value'),
    ]
)
def updatepurchases_institutions_list(pathname, searchterm):
    if pathname == '/purchases/institutions_home':
        # 1. query the relevant records, add filter first before query
        
        sql = """ SELECT pur_ins_id, pur_ins_name, pur_ins_date, pur_ins_amt
                FROM purchases_institutions
                WHERE NOT pur_ins_delete_ins
        """
        val = []
        cols = ["Purchase ID", "Purchaser", "Date of Purchase", "Amount"]
        

        if searchterm:
            sql += """ AND pur_ins_name ILIKE %s"""
            val += [f"%{searchterm}%"]


        purchases_institutions = db.querydatafromdatabase(sql,val,cols)
        
        # 2. create the table and add it to the db
        if purchases_institutions.shape[0]:
            buttons = []
            for pur_ins_id in purchases_institutions['Purchase ID']:
                buttons += [
                    html.Div(
                        dbc.Button('View/Edit/Delete', href=f"/purchases/institutions_profile?mode=edit&id={pur_ins_id}",
                            size='sm', color='dark', ),
                            style={'text-align': 'center'}
                    )
                ]
            
            # we add the buttons to the table
            purchases_institutions['Action'] = buttons

            # remove ID col
            # purchases_institutions.drop('puromer ID', axis=1, inplace=True)

            purchases_institutions_table = dbc.Table.from_dataframe(purchases_institutions, striped=True, bordered=True, hover=True, size='sm', dark=False,)

            return [purchases_institutions_table]
        
        else:
            return ["There are no records that match the search term."]

    else:
        raise PreventUpdate