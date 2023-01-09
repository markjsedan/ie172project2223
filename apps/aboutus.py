import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.exceptions import PreventUpdate
import pandas as pd

from app import app

layout = html.Div(
    [
        dbc.Row(
            [
                html.H2("OUR HISTORY"),
                dbc.Col("The Bookstore is a small-sized bookstore based in Quezon City, Philippines that sells a wide variety of books such as textbooks, novels, children’s books, and cookbooks. It was founded in 2017 by Mr. Bro Lee and is just recently turned over in the care of his daughter Ms. Juby Lee.",
                    width=7,
                ),
                # bro_lee_card = dbc.Card(
                #     [
                #         dbc.CardImg(src="/images/bro_lee_card.jpg", top=True),
                #         dbc.CardBody(
                #             html.P("Bro Lee", className="bro-lee-card")
                #         ),
                #     ],
                #     style={"width": "18rem"},
                # ),             
            ],
            style={'background-color': '#63AAC0'},
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.H2("OUR MISSION & VISION"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div("The store’s mission is to provide affordable and quality books to people of all ages for education, recreation, entertainment, and development. It aims at making people go back to reading physical books in this day of advanced technology, creating excitement about books, and making reading a part of people’s lifestyle."),
                    ],
                    width=7,
                    style={'backgrounfd-color': '#63AAC0'}
                ),            
            ],
        ),
    ],
)