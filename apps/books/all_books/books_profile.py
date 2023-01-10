from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
from urllib.parse import urlparse, parse_qs

from app import app
from apps import dbconnect as db    


layout = html.Div(
    [
        html.Div(
            [
                dcc.Store(id='bookinfo_toload', storage_type='memory', data=0),
            ]
        ),
        html.H2("Book Information"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Label("Book Title", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="bookinfo_title", placeholder="Enter title"
                    ),
                    width=7,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Author", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="bookinfo_author", placeholder="Enter author"
                    ),
                    width=7,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Genre", width=2),
                dbc.Col(
                    html.Div(
                        dcc.Dropdown(
                            id='bookinfo_genre',
                            clearable=True,
                            searchable=True
                        ), 
                        className="dash-bootstrap"
                    ),
                    width=7,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Publisher", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="bookinfo_publisher", placeholder="Enter publisher"
                    ),
                    width=7,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Release Date", width=2),
                dbc.Col(
                    dcc.DatePickerSingle(
                        id='bookinfo_releasedate'
                    ),
                    width=7,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Price", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="bookinfo_price", placeholder="Enter price"
                    ),
                    width=7,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Inventory Count", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="bookinfo_count", placeholder="Enter title"
                    ),
                    width=7,
                ),
            ],
            className="mb-3",
        ),
        html.Div(
            dbc.Row(
                [
                    dbc.Label("Delete Book", width=2),
                    dbc.Col(
                        dbc.Checklist(
                            id='bookinfo_removerecord',
                            options=[
                                {
                                    'label': "Mark for Deletion",
                                    'value': 1
                                }
                            ], # I want the label to be bold
                            style={'fontWeight':'bold'},
                        ),
                        width=7,
                    ),
                ],
                className="mb-3",
            ),
            id='bookinfo_removerecord_div'
        ),
        html.Hr(),
        dbc.Button('Submit', color='dark', id='bookinfo_submitbtn'),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress")),
                dbc.ModalBody("tempmessage", id='bookinfo_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="bookinfo_closebtn", className="ms-auto", n_clicks=0,
                    )
                ),
            ],
            id="bookinfo_modal",
            is_open=False,
        ),
    ]
)


@app.callback(
    [
        Output('bookinfo_genre', 'options'),
        Output('bookinfo_toload', 'data'),
        Output('bookinfo_removerecord_div', 'style')
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)

def bookinfo_loaddropdown(pathname, search):
    
    if pathname == '/books/books_profile':
        sql = """
            SELECT genre_name as label, genre_id as value
            FROM genres
            WHERE genre_delete_ind = False
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)

        genre_opts = df.to_dict('records')

        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]

        to_load = 1 if mode == 'edit' else 0
        removerecord_div = None if to_load else {'display': 'none'}
    
    else:
        raise PreventUpdate

    return [genre_opts, to_load, removerecord_div]




@app.callback(
    [
        Output('bookinfo_modal', 'is_open'),
        Output('bookinfo_feedback_message', 'children'),
        Output('bookinfo_closebtn', 'href')
    ],
    [
        Input('bookinfo_submitbtn', 'n_clicks'),
        Input('bookinfo_closebtn', 'n_clicks')
    ],
    [
        State('bookinfo_title', 'value'),
        State('bookinfo_author', 'value'),
        State('bookinfo_genre', 'value'),
        State('bookinfo_publisher', 'value'),
        State('bookinfo_releasedate', 'date'),
        State('bookinfo_price', 'value'),
        State('bookinfo_count', 'value'),
        State('url', 'search'),
        State('bookinfo_removerecord', 'value'),
    ]
)
def bookinfo_submitprocess(submitbtn, closebtn,

                            title, author, genre, publisher, releasedate, price, count,
                            search, removerecord):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False
        feedbackmessage = ''
        okay_href = None
    else:
        raise PreventUpdate

    if eventid == 'bookinfo_submitbtn' and submitbtn:
        openmodal = True

        inputs = [
            title,
            author,
            genre,
            publisher,
            releasedate,
            price,
            count
        ]

        if not all (inputs):
            feedbackmessage = "Please supply all inputs."
        elif len(title)>256:
            feedbackmessage = "Title is too long (length>256)."
        
        else:
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]

            if mode == 'add':

                sqlcode = """INSERT INTO books(
                    bk_title,
                    au_id,
                    genre_id,
                    pub_id,
                    bk_pub_yr,
                    bk_price,
	                bk_inv_count,
                    bk_delete_ind
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = [title, author, genre, publisher, releasedate, price, count, False]
                db.modifydatabase(sqlcode, values)

                feedbackmessage = "Book information has been saved."
                okay_href = '/books'

            elif mode == 'edit':

                parsed = urlparse(search)
                bookid = parse_qs(parsed.query)['id'][0]

                sqlcode = """UPDATE books
                SET

                    bk_title = %s,
                    au_id = %s,
                    genre_id = %s,
                    pub_id = %s,
                    bk_pub_yr = %s,
                    bk_price = %s,
	                bk_inv_count = %s,
                    bk_delete_ind = %s
                WHERE
                    bk_id = %s
                """

                to_delete = bool(removerecord)

                values = [title, author, genre, publisher, releasedate, price, count, to_delete, bookid]
                db.modifydatabase(sqlcode, values)

                feedbackmessage = "Book information has been updated."
                okay_href = '/books'

            else:
                raise PreventUpdate 

    elif eventid == 'bookinfo_closebtn' and closebtn:
        pass

    else:
        raise PreventUpdate

    return [openmodal, feedbackmessage, okay_href]


@app.callback(
    [
        Output('bookinfo_title', 'value'),
        Output('bookinfo_author', 'value'),
        Output('bookinfo_genre', 'value'),
        Output('bookinfo_publisher', 'value'),
        Output('bookinfo_releasedate', 'date'),
        Output('bookinfo_price', 'value'),
        Output('bookinfo_count', 'value'),
    ],
    [
        Input('bookinfo_toload', 'modified_timestamp'),
    ],
    [
        State('bookinfo_toload', 'data'),
        State('url', 'search'),
    ]
)
def bookinfo_loadprofile(timestamp, to_load, search):
    if to_load == 1:

        # 1. query the book details from the database
        sql = """ SELECT bk_title, bk_title, au_id, genre_id, pub_id, bk_pub_yr, bk_price, bk_inv_count
        FROM books
        WHERE book_id = %s"""     
        
        parsed = urlparse(search)
        bookid = parse_qs(parsed.query)['id'][0]

        val = [bookid]
        colnames = ['title', 'author', 'genre', 'publisher', 'reldate', 'price', 'count']

        df = db.querydatafromdatabase(sql, val, colnames)

        # 2. load the value to the interface
        title = df['title'][0]
        author = df['author'][0]
        genre = df['genre'][0]
        publisher = df['publisher'][0]
        reldate = df['reldate'][0]
        price = df['price'][0]
        count = df['count'][0]

        return [title, author, genre, publisher, reldate, price, count]

    else:
        raise PreventUpdate