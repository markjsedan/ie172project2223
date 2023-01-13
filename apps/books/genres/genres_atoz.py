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


sort_add = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("A-Z", href="/books/genres_atoz"),
                dbc.DropdownMenuItem("Z-A", href="/books/genres_ztoa"),
            ],
            nav=True,
            in_navbar=True,
            label="Sort from A to Z",
        ),
        dbc.Button("Add a genre", color="dark", className="me-2", href="/books/genres_profile?mode=add"),
    ],
    brand="",
    # color="#ffffff",
    # dark=False,

)

nav_contents = [
    dbc.NavItem(dbc.NavLink("All Books", href="/books")),
    dbc.NavItem(dbc.NavLink("Genres", href="/books/genres", active=True)),
]
navs = html.Div(dbc.Nav(nav_contents,pills=True,fill=True))

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Label(html.H5("Search"), width=1, ),
                dbc.Col(
                    dbc.Input(
                        type="text", id="genres_filter_atoz", placeholder="Enter keyword/s"
                    ),
                    width=5,
                ),
            ],
            className="mb-3"
        ),
        dbc.Card(
            [
                dbc.CardHeader(html.H4("Books > Genres")),
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
                                    "This will contain the table for genres",
                                    id='genres_list_atoz',
                                    style={'text-align': 'center'}
                                ),
                            ]
                        )
                    ]
                ),
            ]
        ),
    ],
)
@app.callback(
    [
        Output('genres_list_atoz', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('genres_filter_atoz', 'value'),
    ]
)
def updategenres_list_atoz(pathname, searchterm):
    if pathname == '/books/genres':
        # 1. query the relevant records, add filter first before query
        
        sql = """ SELECT genre_id, genre_name
                FROM genres
                WHERE NOT genre_delete_ind
                ORDER BY genre_name
        """
        val = []
        cols = ["Genre ID", "Genre"]
        

        if searchterm:
            sql += """ AND genre_name ILIKE %s"""
            val += [f"%{searchterm}%"]


        genres_atoz = db.querydatafromdatabase(sql,val,cols)
        
        # 2. create the table and add it to the db
        if genres_atoz.shape[0]:
            buttons = []
            for genre_id in genres_atoz['Genre ID']:
                buttons += [
                    html.Div(
                        dbc.Button('View/Edit/Delete', href=f"/books/genres_profile?mode=edit&id={genre_id}",
                            size='sm', color='dark', ),
                            style={'text-align': 'center'}
                    )
                ]
            
            # we add the buttons to the table
            genres_atoz['Action'] = buttons

            # remove ID col
            # customers_individuals.drop('Customer ID', axis=1, inplace=True)

            genres_table_atoz = dbc.Table.from_dataframe(genres_atoz, striped=True, bordered=True, hover=True, size='sm', dark=False,)

            return [genres_table_atoz]
        
        else:
            return ["There are no records that match the search term."]

    else:
        raise PreventUpdate