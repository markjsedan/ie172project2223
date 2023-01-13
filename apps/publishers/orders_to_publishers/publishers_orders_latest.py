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
                # dbc.DropdownMenuItem("A-Z", href="/publishers/allpublishers/a-z"),
                # dbc.DropdownMenuItem("Z-A", href="/publishers/allpublishers/z-a"),
                dbc.DropdownMenuItem("Latest", href="/publishers/publishers_orders_latest"),
            ],
            nav=True,
            in_navbar=True,
            label="Latest",
        ),
        dbc.Button("Add an order", color="dark", className="me-2", href="/publishers/publishers_orders_profile?mode=add"),
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
                        type="text", id="publishers_orders_filter_latest", placeholder="Enter keyword/s"
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
                                    id='publishers_orders_list_latest',
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
        Output('publishers_orders_list_latest', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('publishers_orders_filter_latest', 'value'),
    ]
)
def updatepublishers_orders_list_latest(pathname, searchterm):
    if pathname == '/publishers/publishers_orders':
        # 1. query the relevant records, add filter first before query
        
        sql = """ SELECT pub_order_id, pub_name, pub_order_date, pub_order_amt
                FROM publishers_orders
                    INNER JOIN publishers on publishers_orders.pub_id = publishers.pub_id
                WHERE NOT pub_order_delete_ind
                ORDER BY pub_order_date DESC
        """
        val = []
        cols = ["Order ID", "Publisher Name", "Date Received", "Amount"]
        

        if searchterm:
            sql += """ AND pub_name ILIKE %s"""
            val += [f"%{searchterm}%"]


        publishers_orders_latest = db.querydatafromdatabase(sql,val,cols)
        
        # 2. create the table and add it to the db
        if publishers_orders_latest.shape[0]:
            buttons = []
            for pub_order_id in publishers_orders_latest['Order ID']:
                buttons += [
                    html.Div(
                        dbc.Button('View/Edit/Delete', href=f"/publishers/publishers_orders_profile?mode=edit&id={pub_order_id}",
                            size='sm', color='dark', ),
                            style={'text-align': 'center'}
                    )
                ]
            
            # we add the buttons to the table
            publishers_orders_latest['Action'] = buttons
            publishers_orders_table_latest = dbc.Table.from_dataframe(publishers_orders_latest, striped=True, bordered=True, hover=True, size='sm', dark=False,)

            return [publishers_orders_table_latest]
        
        else:
            return ["There are no records that match the search term."]

    else:
        raise PreventUpdate