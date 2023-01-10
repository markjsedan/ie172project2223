from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table
import dash
from dash.exceptions import PreventUpdate
import pandas as pd

from app import app

carousel = dbc.Carousel(
    items=[
        {"key": "1", "src": "https://i.ibb.co/SXy038J/hangzhou-g1d15fb310-1920.jpg"},
        {"key": "2", "src": "https://i.ibb.co/3R4MLjX/books-g5ee3029e7-1920.jpg"},
        {"key": "3", "src": "https://i.ibb.co/BysLb3P/library-g23b4210a5-1920.jpg"},
    ],
    # controls=False,
    # indicators=True,
    style={'height': "50px"},
    controls=False,
    indicators=False,
    interval=1000,
    ride="carousel"
)

card_history = dbc.Card(
    dbc.CardBody(
        [
            html.H2("OUR HISTORY", className="card-title"),
            html.Hr(),
            html.P(
                "The Bookstore is a small-sized bookstore based in Quezon City, Philippines that sells a wide variety of books such as textbooks, novels, children’s books, and cookbooks. It was founded in 2017 by Mr. Bro Lee and is just recently turned over in the care of his daughter Ms. Juby Lee."
            ),
            html.Br(),
            html.Br(),
            html.H2("OUR MISSION & VISION", className="card-title"),
            html.Hr(),
            html.P(
                "The store’s mission is to provide affordable and quality books to people of all ages for education, recreation, entertainment, and development. It aims at making people go back to reading physical books in this day of advanced technology, creating excitement about books, and making reading a part of people’s lifestyle."
            ),
        ]
    ),
    style={"width": "45rem","margin-left":"1.75em","opacity":".8"},
    color="light",
    outline=True,
)

card_one = dbc.Card(
    [
        dbc.CardImg(src="https://i.ibb.co/QM5x28Z/bro-lee-card.jpg", top=True),
        dbc.CardBody(html.H4("Bro Lee", className="card-title"))
    ],
    style={"width": "15rem"},
)

card_two = dbc.Card(
    [
        dbc.CardImg(src="https://i.ibb.co/WVH74H9/juby-lee-card.png", top=True),
        dbc.CardBody(html.H4("Juby Lee", className="card-title"))
    ],
    style={"width": "15rem"},
)

row_content = [
    dbc.Col(card_history),
    dbc.Col(card_one),
    dbc.Col(card_two),
]

layout = html.Div(
    [
        dbc.Row(carousel),
        dbc.Row(),
        dbc.Row(
            row_content,
            justify="evenly",
        ),
    ]
)


# layout = html.Div(
#     [
#         dbc.Row(
#             [
#                 html.H2("OUR HISTORY"),
#                 dbc.Col(html.Div("The Bookstore is a small-sized bookstore based in Quezon City, Philippines that sells a wide variety of books such as textbooks, novels, children’s books, and cookbooks. It was founded in 2017 by Mr. Bro Lee and is just recently turned over in the care of his daughter Ms. Juby Lee.")),
#             ]
#         ),
#         dbc.Br(),
#         dbc.Row(
#             [
#                 dbc.Col(card_one, width=5),
#                 dbc.Col(card_two, width=5),
#             ]
#         ),
#         dbc.Br(),
#         dbc.Row(
#             [
#                 html.H2("OUR MISSION & VISION"),
#                 dbc.Col(html.Div("The store’s mission is to provide affordable and quality books to people of all ages for education, recreation, entertainment, and development. It aims at making people go back to reading physical books in this day of advanced technology, creating excitement about books, and making reading a part of people’s lifestyle.")),
#             ],
#         ),    
#     ]
# )


# bro_lee_card = dbc.Card(
#     [
#         dbc.CardImg(src="https://i.ibb.co/QM5x28Z/bro-lee-card.jpg", top=True),
#         dbc.CardBody(
#             html.P("Bro Lee", className="bro-lee-card")
#         ),
#     ],
#     style={"width": "15rem",},
# )
# juby_lee_card = dbc.Card(
#     [
#         dbc.CardImg(src="https://i.ibb.co/WVH74H9/juby-lee-card.png", top=True),
#         dbc.CardBody(
#             html.P("Juby Lee", className="juby-lee-card")
#         ),
#     ],
#     style={"width": "15rem",},
# )

# layout = html.Div(
#     [
#         dbc.Row(
#             [
#                 html.H2("OUR HISTORY"),
#                 dbc.Col(html.Div("The Bookstore is a small-sized bookstore based in Quezon City, Philippines that sells a wide variety of books such as textbooks, novels, children’s books, and cookbooks."), width=7
#                 ),
#                 dbc.Col(html.Div("It was founded in 2017 by Mr. Bro Lee and is just recently turned over in the care of his daughter Ms. Juby Lee."), width=7
#                 ),
#                 dbc.Col(bro_lee_card, width="auto"),
#                 dbc.Col(juby_lee_card, width="auto"),
#                 html.Br(),
#                 html.H2("OUR MISSION & VISION"),
#                 dbc.Col(
#                     [
#                         html.Div("The store’s mission is to provide affordable and quality books to people of all ages for education, recreation, entertainment, and development. It aims at making people go back to reading physical books in this day of advanced technology, creating excitement about books, and making reading a part of people’s lifestyle."),
#                     ],
#                     width=7,
#                     # style={'background-color': '#63AAC0'}
#                 ),            
#             ],
#             # style={"text-align":"center","background-color":"primary"},
#         ),
#     ],
# )