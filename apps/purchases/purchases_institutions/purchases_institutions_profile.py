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
                dcc.Store(id='pur_ins_toload', storage_type='memory', data=0),
            ]
        ),
        html.H2("Purchase Information"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Label("Purchase ID", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="pur_ins_id", placeholder="Leave this blank",readonly=True
                    ),
                    width=7,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Purchaser", width=2),
                dbc.Col(
                    html.Div(
                        dcc.Dropdown(
                        id='pur_ins_name',
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
                dbc.Label("Date", width=2),
                dbc.Col(
                    dcc.DatePickerSingle(
                        id="pur_ins_date"
                    ),
                    width=7,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Amount", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="pur_ins_amt", placeholder="Enter amount of purchase"
                    ),
                    width=7,
                ),
            ],
            className="mb-3",
        ),
        html.Div(
            dbc.Row(
                [
                    dbc.Label("Delete Transaction", width=2),
                    dbc.Col(
                        dbc.Checklist(
                            id='pur_ins_removerecord',
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
            id='pur_ins_removerecord_div'
        ),
        html.Hr(),
        dbc.Button('Submit', color='dark', id='pur_ins_submitbtn'),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress")),
                dbc.ModalBody("tempmessage", id='pur_ins_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="pur_ins_closebtn", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="pur_ins_modal",
            is_open=False,
        ),
    ]
)


@app.callback(
    [
        Output('pur_ins_name','options'),
        Output('pur_ins_toload', 'data'),
        Output('pur_ins_removerecord_div', 'style')
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)
def pur_ins_prof_toload(pathname, search):

    if pathname == '/purchasers/institutions_profile':
        sql = """
            SELECT cust_ins_name as label, cust_ins_id as value
            FROM customers_institutions
            WHERE NOT cust_ins_delete_ins
        """ 
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)

        cust_name_options = df.to_dict('records')

        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]
        toload = 1 if mode == 'edit' else 0
        removerecord_div = None if toload else {'display': 'None'}
        
        return [cust_name_options, toload, removerecord_div]

    else:
        raise PreventUpdate




@app.callback(
    [
        Output('pur_ins_modal', 'is_open'),
        Output('pur_ins_feedback_message', 'children'),
        Output('pur_ins_closebtn', 'href')
    ],
    [
        Input('pur_ins_submitbtn', 'n_clicks'),
        Input('pur_ins_closebtn', 'n_clicks')
    ],
    [
        State('pur_ins_id', 'value'),
        State('pur_ins_name', 'value'),
        State('pur_ins_date', 'value'),
        State('pur_ins_amt', 'value'),
        State('url', 'search'),
        State('pur_ins_removerecord', 'value'),
    ]
)
def pur_ins_submitprocess(submitbtn, closebtn,

                            purchaser_id, name, date, amount,
                            search, removerecord):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False
        feedbackmessage = ''
        okay_href = None
    else:
        raise PreventUpdate

    if eventid == 'pur_ins_submitbtn' and submitbtn:
        openmodal = True

        inputs = [
            name,
            date,
            amount
        ]

        if not all (inputs):
            feedbackmessage = "Please supply all inputs."
        else:
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]

            if mode == 'add':

                sqlcode = """INSERT INTO purchasers_institutions(
                    pur_ins_name,
                    pur_ins_date,
                    pur_ins_amt,
                    pur_ins_delete_ins
                )
                VALUES (%s, %s, %s)
                """
                values = [name, date, amount, False]
                db.modifydatabase(sqlcode, values)

                feedbackmessage = "Purchase information has been saved."
                okay_href = '/purchasers/institutions_home'

            elif mode == 'edit':

                parsed = urlparse(search)
                pur_ins_id = parse_qs(parsed.query)['id'][0]

                sqlcode = """UPDATE purchasers_institutions
                SET
                    pur_ins_name = %s,
                    pur_ins_date = %s,
                    pur_ins_amt = %s,
                    pur_ins_delete_ins = %s
                WHERE
                    pur_ins_id = %s
                """

                todelete = bool(removerecord)

                values = [name, date, amount, todelete, purchaser_id]
                db.modifydatabase(sqlcode, values)

                feedbackmessage = "Purchase information has been updated."
                okay_href = '/purchasers/institutions_home'

            else:
                raise PreventUpdate 

    elif eventid == 'pur_ins_closebtn' and closebtn:
        pass

    else:
        raise PreventUpdate

    return [openmodal, feedbackmessage, okay_href]



@app.callback(
    [
        Output('pur_ins_id', 'value'),
        Output('pur_ins_name', 'value'),
        Output('pur_ins_date', 'value'),
        Output('pur_ins_amt', 'value'),
    ],
    [
        Input('pur_ins_toload', 'modified_timestamp'),
    ],
    [
        State('pur_ins_toload', 'data'),
        State('url', 'search'),
    ]
)
def pur_ins_loadprofile(timestamp,toload, search):
    if toload == 1:

        parsed = urlparse(search)
        pur_ins_id = parse_qs(parsed.query)['id'][0]
        # 1. query the details from the database
        sql = """ SELECT 
                    pur_ins_id,
                    pur_ins_name,
                    pur_ins_date,
                    pur_ins_amt
        FROM purchasers_institutions
        WHERE pur_ins_id = %s """     
        

        val = [pur_ins_id]
        colnames = ["purchaser_id","name","date","amount"]

        df = db.querydatafromdatabase(sql, val, colnames)

        # 2. load the value to the interface
        purchaser_id = df['purchaser_id'][0]
        name = df['name'][0]
        date = df['date'][0]
        amount = df['amount'][0]

        return [purchaser_id, name, date, amount]

    else:
        raise PreventUpdate