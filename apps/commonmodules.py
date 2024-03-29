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
                # className="g-0",
            ),
            href="/books",
            style={"textDecoration": "none", 'margin-left': '1.5em'}
        ),
        dbc.NavLink("Books", href="/books", style={'margin-left': '5em', 'margin-right': '3em', 'color': 'white'}),
        dbc.NavLink("Customers", href="/customers/individuals_home", style={'margin-right': '3em', 'color': 'white'}),
        dbc.NavLink("Purchases", href="/purchases/individuals_home", style={'margin-right': '3em', 'color': 'white'}),
        dbc.NavLink("Publishers", href="/publishers/publishers_home", style={'margin-right': '3em', 'color': 'white'}),
        dbc.NavLink("Employees", href="/employees_home", style={'margin-right': '3em', 'color': 'white'}),
        dbc.NavLink("Reports", href="/reports_home", style={'margin-right': '3em', 'color': 'white'}),
        dbc.NavLink("About Us", href="/about_us", style={'margin-right': '3em', 'color': 'white'}),
        dbc.NavLink("Logout", href="/logout", style={'margin-right': '3em', 'color': 'yellow'}),
    ],
    dark=True,
    color="dark",
)