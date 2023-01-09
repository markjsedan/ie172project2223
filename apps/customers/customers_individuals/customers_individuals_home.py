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


layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Label(html.H5("Search"), width=1),
                dbc.Col(
                    dbc.Input(
                        type="text", id="customers_individuals_filter", placeholder="Enter keywords"
                    ),
                    width="7",
                ),
            ],
            className="mb-3"
        ),
        # dbc.Row(
        #     [
        #         dbc.Col(
        #             dbc.Button(
        #                 "Search Customers", color="dark", className="ms-2", n_clicks=0
        #             ),
        #             width="auto",
        #         ),
        #         dbc.Col(dbc.Input(type="search", placeholder="Enter keyword/s")),
        #     ],
        #     className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
        #     align="center",
        # ),
        
        # html.H2("Individuals"),
        html.Hr(),
        dbc.Card(
            [
                dbc.CardHeader(html.H4("Customers - Individuals")),
                dbc.CardBody(
                    [
                        dbc.Button("Add Customer", color="dark", href='/customers/individuals_profile?mode=add'),
                        html.Hr(),
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
                        dbc.Button('Edit/Delete', href=f"/customers/individuals_profile?mode=edit&id={cust_ind_id}",
                            size='sm', color='primary', ),
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