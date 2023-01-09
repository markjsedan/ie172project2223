from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table
import dash
from dash.exceptions import PreventUpdate
import pandas as pd

from app import app

bro_lee_card = dbc.Card(
    [
        dbc.CardImg(src="https://i.ibb.co/QM5x28Z/bro-lee-card.jpg", top=True),
        dbc.CardBody(
            html.P("Bro Lee", className="bro-lee-card")
        ),
    ],
    style={"width": "15rem",},
)
juby_lee_card = dbc.Card(
    [
        dbc.CardImg(src="https://i.ibb.co/WVH74H9/juby-lee-card.png", top=True),
        dbc.CardBody(
            html.P("Juby Lee", className="juby-lee-card")
        ),
    ],
    style={"width": "15rem",},
)

layout = html.Div(
    [
        dbc.Row(
            [
                html.H2("OUR HISTORY"),
                dbc.Col(html.Div("The Bookstore is a small-sized bookstore based in Quezon City, Philippines that sells a wide variety of books such as textbooks, novels, children’s books, and cookbooks."), width=7
                ),
                dbc.Col(html.Div("It was founded in 2017 by Mr. Bro Lee and is just recently turned over in the care of his daughter Ms. Juby Lee."), width=7
                ),
                dbc.Col(bro_lee_card, width="auto"),
                dbc.Col(juby_lee_card, width="auto"),
                html.Br(),
                html.H2("OUR MISSION & VISION"),
                dbc.Col(
                    [
                        html.Div("The store’s mission is to provide affordable and quality books to people of all ages for education, recreation, entertainment, and development. It aims at making people go back to reading physical books in this day of advanced technology, creating excitement about books, and making reading a part of people’s lifestyle."),
                    ],
                    width=7,
                    # style={'background-color': '#63AAC0'}
                ),            
            ],
            # style={"text-align":"center","background-color":"primary"},
        ),
    ],
)