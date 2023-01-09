import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
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
                dbc.DropdownMenuItem("A-Z", href="/books/allbooks/a-z"),
                dbc.DropdownMenuItem("Z-A", href="/books/allbooks/z-a"),
                dbc.DropdownMenuItem("Latest", href="/books/allbooks/latest"),
            ],
                nav=True,
                in_navbar=True,
                label="Sort by",
        ),
        dbc.Button("Add a book", color="#63AAC0", className="me-1"),
    ],
    brand="Books",
    color="dark",
)


layout = html.Div(
    [
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                        "Search", className="ms-2", n_clicks=0
                    ),
                    width="auto",
                ),
                dbc.Col(dbc.Input(type="search", placeholder="Enter keyword/s")),
            ],
            className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
            align="center",
            style={'background-color': '#63AAC0'},
        ),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.NavItem(dbc.NavLink("All Books", href="/books/allbooks")),
                dbc.NavItem(dbc.NavLink("Authors", href="/books/authors")),
            ],
            style={'background-color': '#63AAC0'},
        ),
        html.Br(),
        html.Br(),
        dbc.Row(sort_add, width="auto"),
    ],
)



    
