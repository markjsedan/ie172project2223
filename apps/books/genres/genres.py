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
                dbc.DropdownMenuItem("A-Z", href="/books/genres/a-z"),
                dbc.DropdownMenuItem("Z-A", href="/books/genres/z-a"),
                dbc.DropdownMenuItem("Latest", href="/books/genres/latest"),
            ],
            nav=True,
            in_navbar=True,
            label="Sort by",
        ),
        dbc.Button("Add a genre", color="dark", className="me-2", href="/books/genres_profile"),
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
                        type="text", id="genres_filter", placeholder="Enter keyword/s"
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
                                    id='genres_list',
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
        Output('genres_list', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('genres_filter', 'value'),
    ]
)
def updategenres_list(pathname, searchterm):
    if pathname == '/books':
        # 1. query the relevant records, add filter first before query
        
        sql = """ SELECT genre_id, genre_name
                FROM books
                WHERE NOT genre_delete_ind
        """
        val = []
        cols = ["Genre ID", "Genre"]
        

        if searchterm:
            sql += """ AND genre_id ILIKE %s"""
            val += [f"%{searchterm}%"]


        genres = db.querydatafromdatabase(sql,val,cols)
        
        # 2. create the table and add it to the db
        if genres.shape[0]:
            buttons = []
            for genre_id in genres['Genre ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Edit/Delete', href=f"/books/genres_profile?mode=edit&id={genre_id}",
                            size='sm', color='dark', ),
                            style={'text-align': 'center'}
                    )
                ]
            
            # we add the buttons to the table
            genres['Action'] = buttons

            # remove ID col
            # customers_individuals.drop('Customer ID', axis=1, inplace=True)

            genres_table = dbc.Table.from_dataframe(genres, striped=True, bordered=True, hover=True, size='sm', dark=False,)

            return [genres_table]
        
        else:
            return ["There are no records that match the search term."]

    else:
        raise PreventUpdate