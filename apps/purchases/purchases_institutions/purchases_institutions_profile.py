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
                        type="text", id="prof_pur_ins_id", placeholder="Leave this blank",readonly=True
                    ),
                    width=7,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Customer Name", width=2),
                dbc.Col(
                    html.Div(
                        dcc.Dropdown(
                            id='prof_cust_ins_name',
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
                        id="prof_pur_ins_date"
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
                        type="text", id="prof_pur_ins_amt", placeholder="Enter amount of purchase"
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
        Output('prof_cust_ins_name','options'),
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

    if pathname == '/purchases/institutions_profile':
        # customer options
        sql = """
            SELECT cust_ins_name as label, cust_ins_id as value
            FROM customers_institutions
            WHERE cust_ins_delete_ind = False
        """ 
        values = []
        cols = ['label','value']
        cust_name_opts_df = db.querydatafromdatabase(sql, values, cols)
        cust_name_opts = cust_name_opts_df.to_dict('records')

        #  to_load
        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if mode == 'edit' else 0
        removerecord_div = None if to_load else {'display': 'None'}

    else:
        raise PreventUpdate

    return [cust_name_opts, to_load, removerecord_div]



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
        State('prof_pur_ins_id', 'value'),
        State('prof_cust_ins_name', 'value'),
        State('prof_pur_ins_date', 'date'),
        State('prof_pur_ins_amt', 'value'),
        State('url', 'search'),
        State('pur_ins_removerecord', 'value'),
    ]
)
def pur_ins_submitprocess(submitbtn, closebtn,

                            pur_id, customer, date, amount,
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
            customer,
            date,
            amount
        ]

        if not all (inputs):
            feedbackmessage = "Please supply all inputs."
        else:
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]

            if mode == 'add':

                sqlcode = """INSERT INTO purchases_institutions(
                    cust_ins_id,
                    pur_ins_date,
                    pur_ins_amt,
                    pur_ins_delete_ind
                )
                VALUES (%s, %s, %s, %s)
                """
                values = [customer, date, amount, False]
                db.modifydatabase(sqlcode, values)

                feedbackmessage = "Purchase information has been saved."
                okay_href = '/purchases/institutions_home'

            elif mode == 'edit':

                parsed = urlparse(search)
                pur_id = parse_qs(parsed.query)['id'][0]

                sqlcode = """UPDATE purchases_institutions
                SET
                    cust_ins_id = %s,
                    pur_ins_date = %s,
                    pur_ins_amt = %s,
                    pur_ins_delete_ind = %s
                WHERE
                    pur_ins_id = %s
                """

                to_delete = bool(removerecord)

                values = [customer, date, amount, to_delete, pur_id]
                db.modifydatabase(sqlcode, values)

                feedbackmessage = "Purchase information has been updated."
                okay_href = '/purchases/institutions_home'

            else:
                raise PreventUpdate 

    elif eventid == 'pur_ins_closebtn' and closebtn:
        pass

    else:
        raise PreventUpdate

    return [openmodal, feedbackmessage, okay_href]



@app.callback(
    [
        Output('prof_pur_ins_id', 'value'),
        Output('prof_cust_ins_name', 'value'),
        Output('prof_pur_ins_date', 'date'),
        Output('prof_pur_ins_amt', 'value'),
    ],
    [
        Input('pur_ins_toload', 'modified_timestamp'),
    ],
    [
        State('pur_ins_toload', 'data'),
        State('url', 'search'),
    ]
)
def pur_ins_loadprofile(timestamp,to_load, search):
    if to_load == 1:

        parsed = urlparse(search)
        pur_id = parse_qs(parsed.query)['id'][0]
        # 1. query the details from the database
        sql = """ SELECT 
                    pur_ins_id,
                    cust_ins_id,
                    pur_ins_date,
                    pur_ins_amt
        FROM purchases_institutions
        WHERE pur_ins_id = %s """     
        
        val = [pur_id]
        colnames = ["pur_id","customer","date","amount"]

        df = db.querydatafromdatabase(sql, val, colnames)

        # 2. load the value to the interface
        pur_id = df['pur_id'][0]
        customer = df['customer'][0]
        date = df['date'][0]
        amount = df['amount'][0]

        return [pur_id, customer, date, amount]

    else:
        raise PreventUpdate