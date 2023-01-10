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

add = dbc.NavbarSimple(
    children=[
        # dbc.DropdownMenu(
        #     children=[
        #         dbc.DropdownMenuItem("A-Z", href="/publishers/allpublishers/a-z"),
        #         dbc.DropdownMenuItem("Z-A", href="/publishers/allpublishers/z-a"),
        #         dbc.DropdownMenuItem("Latest", href="/publishers/allpublishers/latest"),
        #     ],
        #     nav=True,
        #     in_navbar=True,
        #     label="Sort by",
        # ),
        dbc.Button("Add an order", color="dark", className="me-2", href="/publishers/orders_profile?mode=add"),
    ],
    brand="",
    # color="#ffffff",
    # dark=False,

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
                        type="text", id="orders_filter", placeholder="Enter keyword/s"
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
                            dbc.Col(add),
                        ),
                        html.Div(
                            [
                                html.Div(
                                    "This will contain the table for orders to publishers",
                                    id='orders_list',
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
        Output('orders_list', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('orders_filter', 'value'),
    ]
)
def updatepublishers_orders_list(pathname, searchterm):
    if pathname == '/publishers/publishers_orders':
        # 1. query the relevant records, add filter first before query
        
        sql = """ SELECT order_id, pub_name, order_date, order_amount
                FROM orders
                WHERE NOT orders_delete_ind
        """
        val = []
        cols = ["Order ID", "Publisher Name", "Date Received", "Amount"]
        

        if searchterm:
            sql += """ AND order_id ILIKE %s"""
            val += [f"%{searchterm}%"]


        orders = db.querydatafromdatabase(sql,val,cols)
        
        # 2. create the table and add it to the db
        if orders.shape[0]:
            buttons = []
            for order_id in orders['Customer ID']:
                buttons += [
                    html.Div(
                        dbc.Button('View/Edit/Delete', href=f"/publishers/publishers_orders_profile?mode=edit&id={pub_id}",
                            size='sm', color='dark', ),
                            style={'text-align': 'center'}
                    )
                ]
            
            # we add the buttons to the table
            orders['Action'] = buttons

            # remove ID col
            # customers_individuals.drop('Customer ID', axis=1, inplace=True)

            orders_table = dbc.Table.from_dataframe(orders, striped=True, bordered=True, hover=True, size='sm', dark=False,)

            return [orders_table]
        
        else:
            return ["There are no records that match the search term."]

    else:
        raise PreventUpdate