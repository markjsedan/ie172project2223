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
                dcc.Store(id='genre_toload', storage_type='memory', data=0),
            ]
        ),
        html.H2("Genre"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Label("Genre ID", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="genre_id", placeholder="Leave this blank",readonly=True
                    ),
                    width=7,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Genre Name", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="genre_name", placeholder="Enter genre name"
                    ),
                    width=7,
                ),
            ],
            className="mb-3",
        ),
        html.Div(
            dbc.Row(
                [
                    dbc.Label("Delete Genre", width=2),
                    dbc.Col(
                        dbc.Checklist(
                            id='genre_removerecord',
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
            id='genre_removerecord_div'
        ),
        html.Hr(),
        dbc.Button('Submit', color='dark', id='genre_submitbtn'),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress")),
                dbc.ModalBody("tempmessage", id='genre_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="genre_closebtn", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="genre_modal",
            is_open=False,
        ),
    ]
)


@app.callback(
    [
        Output('genre_toload', 'data'),
        Output('genre_removerecord_div', 'style')
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)
def genre_name_loaddropdown(pathname, search):

    if pathname == '/books/genres_profile':
        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]
        toload = 1 if mode == 'edit' else 0
        removerecord_div = None if toload else {'display': 'None'}
        
        return [toload, removerecord_div]

    else:
        raise PreventUpdate




@app.callback(
    [
        Output('genre_modal', 'is_open'),
        Output('genre_feedback_message', 'children'),
        Output('genre_closebtn', 'href')
    ],
    [
        Input('genre_submitbtn', 'n_clicks'),
        Input('genre_closebtn', 'n_clicks')
    ],
    [
        State('genre_id', 'value'),
        State('genre_name', 'value'),
        State('url', 'search'),
        State('genre_removerecord', 'value')
    ]
)
def genre_submitprocess(submitbtn, closebtn,
                            
                        genre_id, name, 
                        search, removerecord):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False
        feedbackmessage = ''
        okay_href = None
    else:
        raise PreventUpdate

    if eventid == 'genre_submitbtn' and submitbtn:
        openmodal = True

        inputs = [name]

        if not all (inputs):
            feedbackmessage = "Please supply all inputs."
        else:
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]

            if mode == 'add':

                sqlcode = """INSERT INTO genres(
                    genre_name,
                    genre_delete_ind
                )
                VALUES (%s, %s)
                """
                values = [name, False]
                db.modifydatabase(sqlcode, values)

                feedbackmessage = "Genre has been saved."
                okay_href = '/books/genres'

            elif mode == 'edit':

                parsed = urlparse(search)
                genre_id = parse_qs(parsed.query)['id'][0]

                sqlcode = """UPDATE genres
                SET
                    genre_name = %s,
                    genre_delete_ind = %s
                WHERE
                    genre_id = %s
                """

                todelete = bool(removerecord)

                values = [name, todelete, genre_id]
                db.modifydatabase(sqlcode, values)

                feedbackmessage = "Genre has been updated."
                okay_href = '/books/genres'

            else:
                raise PreventUpdate 

    elif eventid == 'genre_closebtn' and closebtn:
        pass

    else:
        raise PreventUpdate

    return [openmodal, feedbackmessage, okay_href]



@app.callback(
    [
        Output('genre_id', 'value'),
        Output('genre_name', 'value'),
    ],
    [
        Input('genre_toload', 'modified_timestamp'),
    ],
    [
        State('genre_toload', 'data'),
        State('url', 'search'),
    ]
)
def genre_loadprofile(timestamp, toload, search):
    if toload == 1:

        parsed = urlparse(search)
        genre_id = parse_qs(parsed.query)['id'][0]
        # 1. query the details from the database
        sql = """ SELECT 
                    genre_id,
                    genre_name
        FROM genres
        WHERE genre_id = %s """     
        

        val = [genre_id]
        colnames = ["genre_id","name"]

        df = db.querydatafromdatabase(sql, val, colnames)

        # 2. load the value to the interface
        genre_id = df['genre_id'][0]
        name = df['name'][0]

        return [genre_id, name]

    else:
        raise PreventUpdate