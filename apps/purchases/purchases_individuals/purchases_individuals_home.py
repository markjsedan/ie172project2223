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
        # dbc.DropdownMenu(
        #     children=[
        #         # dbc.DropdownMenuItem("A-Z", href="/purchases/individuals/a-z"),
        #         # dbc.DropdownMenuItem("Z-A", href="/purchases/individuals/z-a"),
        #         dbc.DropdownMenuItem("Latest", href="/purchases/individuals_latest"),
        #     ],
        #     nav=True,
        #     in_navbar=True,
        #     label="Sort by",
        # ),
        dbc.Button("Add a purchase", color="dark", className="me-2", href="/purchases/individuals_profile?mode=add"),
    ],
    brand="",
)

nav_contents = [
    dbc.NavItem(dbc.NavLink("Individuals", href="/purchases/individuals_home", active=True)),
    dbc.NavItem(dbc.NavLink("Institutions", href="/purchases/institutions_home",)),
]
navs = html.Div(dbc.Nav(nav_contents,pills=True,fill=True))

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Label(html.H5("Search"), width=1),
                dbc.Col(
                    dbc.Input(
                        type="text", id="purchases_individuals_filter", placeholder="Enter keyword/s"
                    ),
                    width=5,
                ),
            ],
            className="mb-3"
        ),
        dbc.Card(
            [
                dbc.CardHeader(html.H4("Purchases > Individuals")),
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
                                    "This will contain the table for purchases (individuals)",
                                    id='purchases_individuals_list',
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
        Output('purchases_individuals_list', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('purchases_individuals_filter', 'value'),
    ]
)
def updatepurchases_individuals_list(pathname, searchterm):
    if pathname == '/purchases/individuals_home':
        # 1. query the relevant records, add filter first before query
        sql = """ SELECT pur_ind_id, cust_ind_name, pur_ind_date, pur_ind_amt
                FROM purchases_individuals
                    INNER JOIN customers_individuals on purchases_individuals.cust_ind_id = customers_individuals.cust_ind_id
                WHERE NOT pur_ind_delete_ind
        """
        val = []
        cols = ["Purchase ID", "Customer Name", "Date of Purchase", "Amount"]
        

        if searchterm:
            sql += """ AND cust_ind_name ILIKE %s"""
            val += [f"%{searchterm}%"]

        pur_ind_list = db.querydatafromdatabase(sql,val,cols)
        
        # 2. create the table and add it to the db
        if pur_ind_list.shape[0]:
            buttons = []
            for pur_ind_id in pur_ind_list['Purchase ID']:
                buttons += [
                    html.Div(
                        dbc.Button('View/Edit/Delete', href=f"/purchases/individuals_profile?mode=edit&id={pur_ind_id}",
                            size='sm', color='dark', ),
                            style={'text-align': 'center'}
                    )
                ]
            
            # we add the buttons to the table
            pur_ind_list['Action'] = buttons
            purchases_individuals_table = dbc.Table.from_dataframe(pur_ind_list, striped=True, bordered=True, hover=True, size='sm', dark=False,)

            return [purchases_individuals_table]
        
        else:
            return ["There are no records that match the search term."] 

    else:
        raise PreventUpdate