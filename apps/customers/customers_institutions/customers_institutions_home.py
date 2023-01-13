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
                dbc.DropdownMenuItem("A-Z", href="/customers/institutions/a-z"),
                dbc.DropdownMenuItem("Z-A", href="/customers/institutions/z-a"),
                dbc.DropdownMenuItem("Latest", href="/customers/institutions/latest"),
            ],
            nav=True,
            in_navbar=True,
            label="Sort by",
        ),
        dbc.Button("Add a customer", color="dark", className="me-2", href="/customers/institutions_profile?mode=add"),
    ],
    brand="",
    # color="#ffffff",
    # dark=False,

)

nav_contents = [
    dbc.NavItem(dbc.NavLink("Individuals", href="/customers/individuals_home")),
    dbc.NavItem(dbc.NavLink("Institutions", href="/customers/institutions_home", active=True)),
]
navs = html.Div(dbc.Nav(nav_contents,pills=True,fill=True))

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Label(html.H5("Search"), width=1),
                dbc.Col(
                    dbc.Input(
                        type="text", id="customers_institutions_filter", placeholder="Enter keyword/s"
                    ),
                    width=5,
                ),
            ],
            className="mb-3"
        ),
        dbc.Card(
            [
                dbc.CardHeader(html.H4("Customers > Institutions")),
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
                                    "This will contain the table for customers (institutions)",
                                    id='customers_institutions_list',
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
        Output('customers_institutions_list', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('customers_institutions_filter', 'value'),
    ]
)
def updatecustomers_institutions_list(pathname, searchterm):
    if pathname == '/customers/institutions_home':
        # 1. query the relevant records, add filter first before query
        
        sql = """ SELECT cust_ins_id, cust_ins_name, cust_ins_cp, cust_ins_cp_role, cust_ins_cp_email
                FROM customers_institutions
                WHERE NOT cust_ins_delete_ind
        """
        val = []
        cols = ["Customer ID", "Customer Name", "Contact Person", "Role", "Email"]
        

        if searchterm:
            sql += """ AND cust_ins_name ILIKE %s"""
            val += [f"%{searchterm}%"]


        customers_institutions = db.querydatafromdatabase(sql,val,cols)
        
        # 2. create the table and add it to the db
        if customers_institutions.shape[0]:
            buttons = []
            for cust_ins_id in customers_institutions['Customer ID']:
                buttons += [
                    html.Div(
                        dbc.Button('View/Edit/Delete', href=f"/customers/institutions_profile?mode=edit&id={cust_ins_id}",
                            size='sm', color='dark', ),
                            style={'text-align': 'center'}
                    )
                ]
            

            customers_institutions['Action'] = buttons
            customers_institutions_table = dbc.Table.from_dataframe(customers_institutions, striped=True, bordered=True, hover=True, size='sm', dark=False,)

            return [customers_institutions_table]
        
        else:
            return ["There are no records that match the search term."]

    else:
        raise PreventUpdate