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
        dbc.Button("Add a publisher", color="dark", className="me-2", href="/publishers/publishers_profile?mode=add"),
    ],
    brand="",
    # color="#ffffff",
    # dark=False,

)

nav_contents = [
<<<<<<< HEAD:apps/publishers/publishers_home.py
    dbc.NavItem(dbc.NavLink("All Publishers", href="/publishers/publishers_home", active=True)),
    dbc.NavItem(dbc.NavLink("Orders to Publishers", href="/publishers/publishers_orders",)),
=======
    dbc.NavItem(dbc.NavLink("All Publishers", href="/publishers", active=True)),
    dbc.NavItem(dbc.NavLink("Orders to Publishers", href="/publishers/orders",)),
>>>>>>> f80d5a539ea3c4aa3af75cd2e59906ee8fb7892c:apps/publishers/publishers.py
]
navs = html.Div(dbc.Nav(nav_contents,pills=True,fill=True))

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Label(html.H5("Search"), width=1),
                dbc.Col(
                    dbc.Input(
                        type="text", id="publishers_filter", placeholder="Enter keyword/s"
                    ),
                    width=5,
                ),
            ],
            className="mb-3"
        ),
        dbc.Card(
            [
                dbc.CardHeader(html.H4("Publishers > All Publishers")),
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
                                    "This will contain the table for publishers",
                                    id='publishers_list',
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
        Output('publishers_list', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('publishers_filter', 'value'),
    ]
)
def updatepublishers_list(pathname, searchterm):
<<<<<<< HEAD:apps/publishers/publishers_home.py
    if pathname == '/publishers/publishers_home':
=======
    if pathname == '/publishers':
>>>>>>> f80d5a539ea3c4aa3af75cd2e59906ee8fb7892c:apps/publishers/publishers.py
        # 1. query the relevant records, add filter first before query
        
        sql = """ SELECT pub_id, pub_name, pub_ln
                FROM publishers
                WHERE NOT publishers_delete_ind
        """
        val = []
        cols = ["Publisher ID", "Publisher Name", "Landline Number"]
        

        if searchterm:
            sql += """ AND pub_name ILIKE %s"""
            val += [f"%{searchterm}%"]


        publishers = db.querydatafromdatabase(sql,val,cols)
        
        # 2. create the table and add it to the db
        if publishers.shape[0]:
            buttons = []
            for pub_id in publishers['Customer ID']:
                buttons += [
                    html.Div(
                        dbc.Button('View/Edit/Delete', href=f"/publishers/publishers_profile?mode=edit&id={pub_id}",
                            size='sm', color='dark', ),
                            style={'text-align': 'center'}
                    )
                ]
            
            # we add the buttons to the table
            publishers['Action'] = buttons

            # remove ID col
            # customers_individuals.drop('Customer ID', axis=1, inplace=True)

            publishers_table = dbc.Table.from_dataframe(publishers, striped=True, bordered=True, hover=True, size='sm', dark=False,)

            return [publishers_table]
        
        else:
            return ["There are no records that match the search term."]

    else:
        raise PreventUpdate