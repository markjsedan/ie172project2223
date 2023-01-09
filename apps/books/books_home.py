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
        dbc.Button("Add a book", color="primary", className="me-2", href="/books/books_profile"),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("A-Z", href="/books/allbooks/a-z"),
                dbc.DropdownMenuItem("Z-A", href="/books/allbooks/z-a"),
                dbc.DropdownMenuItem("Latest", href="/books/allbooks/latest"),
            ],
            nav=True,
            in_navbar=True,
            label="Sort by",
        ),
    ],
    brand="",
    color="#ffffff",
    dark=False,

)

nav_contents = [
    dbc.NavItem(dbc.NavLink("All Books", href="/books/allbooks", active=True)),
    dbc.NavItem(dbc.NavLink("Authors", href="/books/authors",)),
]
navs = html.Div(dbc.Nav(nav_contents,pills=True,fill=True))

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Label(html.H5("Search"), width=1, ),
                dbc.Col(
                    dbc.Input(
                        type="text",
                        id="books_filter",
                        placeholder="Enter keyword/s"
                    ),
                    width=5,
                ),
            ],
        ),
        html.Hr(),
        dbc.Card(
            [
                dbc.CardHeader(html.H4("Books > All Books")),
                dbc.CardBody(
                    [
                        dbc.Row(navs, style={'fontWeight':'bold',"color":"dark"}
                        ),
                        html.Hr(),
                        dbc.Row(
                            dbc.Col(sort_add),
                        ),
                    ]
                ),
            ]
        ),
        # dbc.Row(
        #     [
        #         dbc.Label(html.H5("Search"), width=1, style={'margin-left': '2em'}),
        #         dbc.Col(
        #             dbc.Input(
        #                 type="text",
        #                 id="books_filter",
        #                 placeholder="Enter keyword/s"
        #             ),
        #             width=5,
        #         ),
        #     ],
        # ),
        # html.Hr(),
        # # dbc.Row(
        # #     [
        # #         dbc. Col(dbc.NavItem(dbc.NavLink("All Books", href="/books/allbooks", style={'margin-left': '2em', 'margin-right': '3em'}))),
        # #         dbc. Col(dbc.NavItem(dbc.NavLink("Authors", href="/books/authors", style={'margin-right': '2em'}))),
        # #     ],
        # dbc.Row(navs
        # ),
        # html.Hr(),
        # dbc.Row(
        #     dbc.Col(sort_add),
        # ),
    ],
    # style={'background-color': '#63AAC0'},
)

html.Div("Table with books will go here.",
    id='books_bookslist')



    
