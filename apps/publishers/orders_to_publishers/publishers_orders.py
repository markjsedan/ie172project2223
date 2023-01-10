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
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("A-Z", href="/publishers/allpublishers/a-z"),
                dbc.DropdownMenuItem("Z-A", href="/publishers/allpublishers/z-a"),
                dbc.DropdownMenuItem("Latest", href="/publishers/allpublishers/latest"),
            ],
            nav=True,
            in_navbar=True,
            label="Sort by",
        ),
        dbc.Button("Add a publisher", color="dark", className="me-2", href="/publishers/publishers_orders_profile?mode=add"),
    ],
    brand="",

)

nav_contents = [
    dbc.NavItem(dbc.NavLink("All Publishers", href="/publishers/publishers_home")),
    dbc.NavItem(dbc.NavLink("Orders to Publishers", href="/publishers/publishers_orders", active=True)),
]
navs = html.Div(dbc.Nav(nav_contents,pills=True,fill=True))

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Label(html.H5("Search"), width=1),
                dbc.Col(
                    dbc.Input(
                        type="text", id="publishers_orders_filter", placeholder="Enter keyword/s"
                    ),
                    width=5,
                ),
            ],
            className="mb-3"
        ),
        dbc.Card(
            [
                dbc.CardHeader(html.H4("Publishers > Orders to Publishers")),
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
                                    "This will contain the table for orders to publishers",
                                    id='publishers_orders_list',
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
        Output('publishers_orders_list', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('publishers_orders_filter', 'value'),
    ]
)
def updatepublishers_orders_list(pathname, searchterm):
    if pathname == '/publishers/publishers_orders':
        # 1. query the relevant records, add filter first before query
        
        sql = """ SELECT pub_order_id, pub_order_name, pub_order_date,pub_order_amt
                FROM publishers_orders
                WHERE NOT pub_order_delete_ind
        """
        val = []
        cols = ["Order ID", "Publisher Name", "Date Received", "Amount"]
        

        if searchterm:
            sql += """ AND pub_order_id ILIKE %s"""
            val += [f"%{searchterm}%"]


        publishers_orders = db.querydatafromdatabase(sql,val,cols)
        
        # 2. create the table and add it to the db
        if publishers_orders.shape[0]:
            buttons = []
            for pub_order_id in publishers_orders['Order ID']:
                buttons += [
                    html.Div(
                        dbc.Button('View/Edit/Delete', href=f"/publishers/publishers_orders_profile?mode=edit&id={pub_order_id}",
                            size='sm', color='dark', ),
                            style={'text-align': 'center'}
                    )
                ]
            
            # we add the buttons to the table
            publishers_orders['Action'] = buttons

            # remove ID col
            # customers_individuals.drop('Customer ID', axis=1, inplace=True)

            publishers_orders_table = dbc.Table.from_dataframe(publishers_orders, striped=True, bordered=True, hover=True, size='sm', dark=False,)

            return [publishers_orders_table]
        
        else:
            return ["There are no records that match the search term."]

    else:
        raise PreventUpdate