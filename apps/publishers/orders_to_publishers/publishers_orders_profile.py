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
                dcc.Store(id='prof_order_toload', storage_type='memory', data=0),
            ]
        ),
        html.H2("Order Information"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Label("Order ID", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="prof_order_id", placeholder="Leave this blank",readonly=True
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
                    html.Div(
                        dcc.Dropdown(
                            id="prof_order_pub_name",
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
                dbc.Label("Date Received", width=2),
                dbc.Col(
                    dcc.DatePickerSingle(
                        id='prof_order_date'
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
                        type="text", id="prof_order_amount", placeholder="Enter amount"
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
                            id='prof_order_removerecord',
                            options=[
                                {
                                    'label': "Mark for Deletion",
                                    'value': 1
                                }
                            ], 
                            style={'fontWeight':'bold'},
                        ),
                        width=7,
                    ),
                ],
                className="mb-3",
            ),
            id='prof_order_removerecord_div'
        ),
        html.Hr(),
        dbc.Button('Submit', color='dark', id='prof_order_submitbtn'),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress")),
                dbc.ModalBody("tempmessage", id='prof_order_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="prof_order_closebtn", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="prof_order_modal",
            is_open=False,
        ),
    ]
)


@app.callback(
    [
        Output('prof_order_pub_name', 'options'),
        Output('prof_order_toload', 'data'),
        Output('prof_order_removerecord_div', 'style')
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)
def order_profile_toload(pathname, search):

    if pathname == '/publishers/publishers_orders_profile':
        # publisher options
        sql = """
            SELECT pub_name as label, pub_id as value
            FROM publishers
            WHERE pub_delete_ind = False
        """
        values = []
        cols = ['label','value']
        pub_name_opts_df = db.querydatafromdatabase(sql, values, cols)
        pub_name_opts = pub_name_opts_df.to_dict('records')

        # to_load
        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if mode == 'edit' else 0
        removerecord_div = None if to_load else {'display': 'None'}

    else:
        raise PreventUpdate

    return [pub_name_opts, to_load, removerecord_div]




@app.callback(
    [
        Output('prof_order_modal', 'is_open'),
        Output('prof_order_feedback_message', 'children'),
        Output('prof_order_closebtn', 'href')
    ],
    [
        Input('prof_order_submitbtn', 'n_clicks'),
        Input('prof_order_closebtn', 'n_clicks')
    ],
    [
        State('prof_order_id', 'value'),
        State('prof_order_pub_name', 'value'),
        State('prof_order_date', 'date'),
        State('prof_order_amount', 'value'),
        State('url', 'search'),
        State('prof_order_removerecord', 'value'),
    ]
)
def order_submitprocess(submitbtn, closebtn,

                            order_id, publisher, date, amount,
                            search, removerecord):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False
        feedbackmessage = ''
        okay_href = None
    else:
        raise PreventUpdate

    if eventid == 'prof_order_submitbtn' and submitbtn:
        openmodal = True

        inputs = [
            publisher,
            date,
            amount
        ]

        if not all (inputs):
            feedbackmessage = "Please supply all inputs."
        else:
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]

            if mode == 'add':

                sqlcode = """INSERT INTO publishers_orders(
                    pub_id,
                    pub_order_date,
                    pub_order_amt,
                    pub_order_delete_ind
                )
                VALUES (%s, %s, %s, %s)
                """
                values = [publisher, date, amount, False]
                db.modifydatabase(sqlcode, values)

                feedbackmessage = "Order information has been saved."
                okay_href = '/publishers/publishers_orders'

            elif mode == 'edit':

                parsed = urlparse(search)
                pub_order_id = parse_qs(parsed.query)['id'][0]

                sqlcode = """UPDATE publishers_orders
                SET
                    pub_id = %s,
                    pub_order_date = %s,
                    pub_order_amt = %s,
                    pub_order_delete_ind = %s
                WHERE
                    pub_order_id = %s
                """

                to_delete = bool(removerecord)

                values = [publisher, date, amount, to_delete, order_id]
                db.modifydatabase(sqlcode, values)

                feedbackmessage = "Order information has been updated."
                okay_href = '/publishers/publishers_orders'

            else:
                raise PreventUpdate 

    elif eventid == 'prof_order_closebtn' and closebtn:
        pass

    else:
        raise PreventUpdate

    return [openmodal, feedbackmessage, okay_href]



@app.callback(
    [
        Output('prof_order_id', 'value'),
        Output('prof_order_pub_name', 'value'),
        Output('prof_order_date', 'date'),
        Output('prof_order_amount', 'value'),
    ],
    [
        Input('prof_order_toload', 'modified_timestamp'),
    ],
    [
        State('prof_order_toload', 'data'),
        State('url', 'search'),
    ]
)
def order_loadprofile(timestamp,to_load, search):
    if to_load == 1:

        parsed = urlparse(search)
        pub_order_id = parse_qs(parsed.query)['id'][0]
        # 1. query the details from the database
        sql = """ SELECT 
                    pub_order_id,
                    pub_id,
                    pub_order_date,
                    pub_order_amt
        FROM publishers_orders
        WHERE pub_order_id = %s """     
        
        val = [pub_order_id]
        colnames = ["order_id","publisher","date","amount"]

        df = db.querydatafromdatabase(sql, val, colnames)

        # 2. load the value to the interface
        order_id = df['order_id'][0]
        publisher = df['publisher'][0]
        date = df['date'][0]
        amount = df['amount'][0]

        return [order_id, publisher, date, amount]

    else:
        raise PreventUpdate