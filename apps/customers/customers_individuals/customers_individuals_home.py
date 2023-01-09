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
                dbc.DropdownMenuItem("A-Z", href="/customers/individuals/a-z"),
                dbc.DropdownMenuItem("Z-A", href="/customers/individuals/z-a"),
                dbc.DropdownMenuItem("Latest", href="/customers/individuals/latest"),
            ],
            nav=True,
            in_navbar=True,
            label="Sort by",
        ),
        dbc.Button("Add a customer", color="dark", className="me-2", href="/customers/individuals/profile"),
    ],
    brand="",
    # color="#ffffff",
    # dark=False,

)

nav_contents = [
    dbc.NavItem(dbc.NavLink("Individuals", href="/customers/individuals", active=True)),
    dbc.NavItem(dbc.NavLink("Institutions", href="/customers/institutions",)),
]
navs = html.Div(dbc.Nav(nav_contents,pills=True,fill=True))

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Label(html.H5("Search"), width=1),
                dbc.Col(
                    dbc.Input(
                        type="text", id="customers_individuals_filter", placeholder="Enter keyword/s"
                    ),
                    width=5,
                ),
            ],
            className="mb-3"
        ),
        dbc.Card(
            [
                dbc.CardHeader(html.H4("Customers > Individuals")),
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
                                    "This will contain the table for customers_individuals",
                                    id='customers_individuals_list',
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
        Output('customers_individuals_list', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('customers_individuals_filter', 'value'),
    ]
)
def updatecustomers_individuals_list(pathname, searchterm):
    if pathname == '/customers':
        # 1. query the relevant records, add filter first before query
        
        sql = """ SELECT cust_ind_id, cust_ind_name, cust_ind_prof, cust_ind_email
                FROM customers_individuals
                WHERE NOT cust_ind_delete_ind
        """
        val = []
        cols = ["Customer ID", "Customer Name", "Profession", "Email"]
        

        if searchterm:
            sql += """ AND cust_ind_id ILIKE %s"""
            val += [f"%{searchterm}%"]


        customers_individuals = db.querydatafromdatabase(sql,val,cols)
        
        # 2. create the table and add it to the db
        if customers_individuals.shape[0]:
            buttons = []
            for cust_ind_id in customers_individuals['Customer ID']:
                buttons += [
                    html.Div(
                        dbc.Button('View/Edit/Delete', href=f"/customers/individuals_profile?mode=edit&id={cust_ind_id}",
                            size='sm', color='dark', ),
                            style={'text-align': 'center'}
                    )
                ]
            
            # we add the buttons to the table
            customers_individuals['Action'] = buttons

            # remove ID col
            # customers_individuals.drop('Customer ID', axis=1, inplace=True)

            customers_individuals_table = dbc.Table.from_dataframe(customers_individuals, striped=True, bordered=True, hover=True, size='sm', dark=False,)

            return [customers_individuals_table]
        
        else:
            return ["There are no records that match the search term."]

    else:
        raise PreventUpdate