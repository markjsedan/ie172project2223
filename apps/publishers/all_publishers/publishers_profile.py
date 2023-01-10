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
                dcc.Store(id='pub_allpub_toload', storage_type='memory', data=0),
            ]
        ),
        html.H2("Publisher Information"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Label("Publisher ID", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="pub_id", placeholder="Leave this blank",readonly=True
                    ),
                    width=7,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Publisher Name", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="pub_name", placeholder="Enter publisher name"
                    ),
                    width=7,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Landline Number", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="pub_ln", placeholder="Enter number"
                    ),
                    width=7,
                ),
            ],
            className="mb-3",
        ),
        html.Div(
            dbc.Row(
                [
                    dbc.Label("Delete Publisher", width=2),
                    dbc.Col(
                        dbc.Checklist(
                            id='pub_removerecord',
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
            id='pub_removerecord_div'
        ),
        html.Hr(),
        dbc.Button('Submit', color='dark', id='pub_submitbtn'),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress")),
                dbc.ModalBody("tempmessage", id='pub_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="pub_closebtn", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="pub_modal",
            is_open=False,
        ),
    ]
)


@app.callback(
    [
        Output('pub_allpub_toload', 'data'),
        Output('pub_removerecord_div', 'style')
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)
def pub_ln_loaddropdown(pathname, search):

    if pathname == '/publishers/publishers_profile':
        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]
        toload = 1 if mode == 'edit' else 0
        removerecord_div = None if toload else {'display': 'None'}
        
        return [toload, removerecord_div]

    else:
        raise PreventUpdate



@app.callback(
    [
        Output('pub_modal', 'is_open'),
        Output('pub_feedback_message', 'children'),
        Output('pub_closebtn', 'href')
    ],
    [
        Input('pub_submitbtn', 'n_clicks'),
        Input('pub_closebtn', 'n_clicks')
    ],
    [
        State('pub_id', 'value'),
        State('pub_name', 'value'),
        State('pub_ln', 'value'),
        State('url', 'search'),
        State('pub_removerecord', 'value'),
    ]
)
def pub_submitprocess(submitbtn, closebtn,

                            pub_id, name, landline_number,
                            search, removerecord):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False
        feedbackmessage = ''
        okay_href = None
    else:
        raise PreventUpdate

    if eventid == 'pub_submitbtn' and submitbtn:
        openmodal = True

        inputs = [
            name,
            landline_number
        ]

        if not all (inputs):
            feedbackmessage = "Please supply all inputs."
        else:
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]

            if mode == 'add':

                sqlcode = """INSERT INTO publishers(
                    pub_name,
                    pub_land_num,
                    pub_delete_ind
                )
                VALUES (%s, %s, %s)
                """
                values = [name, landline_number, False]
                db.modifydatabase(sqlcode, values)

                feedbackmessage = "Publisher information has been saved."
                okay_href = '/publishers/publishers_home'

            elif mode == 'edit':

                parsed = urlparse(search)
                cust_ind_id = parse_qs(parsed.query)['id'][0]

                sqlcode = """UPDATE publishers
                SET
                    pub_name = %s,
                    pub_land_num = %s,
                    pub_delete_ind = %s
                WHERE
                    pub_id = %s
                """

                todelete = bool(removerecord)

                values = [name, landline_number, todelete,pub_id]
                db.modifydatabase(sqlcode, values)

                feedbackmessage = "Publisher information has been updated."
                okay_href = '/publishers/publishers_home'

            else:
                raise PreventUpdate 

    elif eventid == 'pub_closebtn' and closebtn:
        pass

    else:
        raise PreventUpdate

    return [openmodal, feedbackmessage, okay_href]



@app.callback(
    [
        Output('pub_id', 'value'),
        Output('pub_name', 'value'),
        Output('pub_ln', 'value'),
    ],
    [
        Input('pub_allpub_toload', 'modified_timestamp'),
    ],
    [
        State('pub_allpub_toload', 'data'),
        State('url', 'search'),
    ]
)
def pub_loadprofile(timestamp,toload, search):
    if toload == 1:

        parsed = urlparse(search)
        cust_ind_id = parse_qs(parsed.query)['id'][0]
        # 1. query the details from the database
        sql = """ SELECT 
                    pub_id,
                    pub_name,
                    pub_land_num,
        FROM publishers
        WHERE pub_id = %s """     
        

        val = [pub_id]
        colnames = ["pub_id","name","landline number"]

        df = db.querydatafromdatabase(sql, val, colnames)

        # 2. load the value to the interface
        pub_id = df['pub_id'][0]
        name = df['name'][0]
        landline_number = df['landline number'][0]

        return [pub_id, name, landline_number]

    else:
        raise PreventUpdate