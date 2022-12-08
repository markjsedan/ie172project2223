from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
import pandas as pd


from app import app

THEBOOKSTORE_LOGO = "https://i.ibb.co/YRzTCN6/THE-BOOKSTORE-LOGO.png"


# CSS Styling for the NavLink components
navlink_style = {
    'color': '#fff'
}

navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src=THEBOOKSTORE_LOGO, height="70px")),
                    dbc.Col(dbc.NavbarBrand("The Bookstore", className="ms-2")),
                ],
                align="center",
                className="g-0",
            ),
            href="/books",
            style={"textDecoration": "none", 'margin-left': '1.5em'}
        ),
        dbc.NavLink("Books", href="/books", style={'margin-left': '24em', 'margin-right': '2em', 'color': 'white'}),
        dbc.NavLink("Customers", href="/customers", style={'margin-right': '2em', 'color': 'white'}),
        dbc.NavLink("Publishers", href="/publishers", style={'margin-right': '2em', 'color': 'white'}),
        dbc.NavLink("Employees", href="/employees", style={'margin-right': '2em', 'color': 'white'}),
        dbc.NavLink("Reports", href="/reports", style={'margin-right': '2em', 'color': 'white'}),
        dbc.NavLink("About Us", href="/about_us", style={'margin-right': '2em', 'color': 'white'}),
    ],
    dark=True,
    color="dark",
)