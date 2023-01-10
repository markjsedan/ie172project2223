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
                dcc.Store(id='order_profile_toload', storage_type='memory', data=0),
            ]
        ),
        html.H2("Order Information"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Label("Order ID", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="order_id", placeholder="Leave this blank",readonly=True
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
                dbc.Label("Date Received", width=2),
                dbc.Col(
                    dcc.DatePickerSingle(
                        id='order_date'
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
                        type="text", id="order_amount", placeholder="Enter amount"
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
                            id='order_removerecord',
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
            id='order_removerecord_div'
        ),
        html.Hr(),
        dbc.Button('Submit', color='dark', id='order_submitbtn'),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress")),
                dbc.ModalBody("tempmessage", id='order_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="order_closebtn", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="order_modal",
            is_open=False,
        ),
    ]
)


@app.callback(
    [
        Output('order_toload', 'data'),
        Output('order_removerecord_div', 'style')
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)
def order_profile_toload(pathname, search):

    if pathname == '/publishers/orders_profile':
        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]
        toload = 1 if mode == 'edit' else 0
        removerecord_div = None if toload else {'display': 'None'}
        
        return [toload, removerecord_div]

    else:
        raise PreventUpdate




@app.callback(
    [
        Output('order_modal', 'is_open'),
        Output('order_feedback_message', 'children'),
        Output('order_closebtn', 'href')
    ],
    [
        Input('order_submitbtn', 'n_clicks'),
        Input('order_closebtn', 'n_clicks')
    ],
    [
        State('order_id', 'value'),
        State('pub_name', 'value'),
        State('order_date', 'value'),
        State('order_amount', 'value'),
        State('url', 'search'),
        State('order_removerecord', 'value'),
    ]
)
def order_submitprocess(submitbtn, closebtn,

                            order_id, pub_name, order_date, order_amount,
                            search, removerecord):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False
        feedbackmessage = ''
        okay_href = None
    else:
        raise PreventUpdate

    if eventid == 'order_submitbtn' and submitbtn:
        openmodal = True

        inputs = [
            order_id,
            pub_name,
            order_date,
            order_amount,
        ]

        if not all (inputs):
            feedbackmessage = "Please supply all inputs."
        else:
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]

            if mode == 'add':

                sqlcode = """INSERT INTO orders(
                    pub_name,
                    order_date,
                    order_amount
                    order_delete_ind
                )
                VALUES (%s, %s, %s, %s)
                """
                values = [pub_name, order_date, order_amount, False]
                db.modifydatabase(sqlcode, values)

                feedbackmessage = "Order information has been saved."
                okay_href = '/publishers/orders'

            elif mode == 'edit':

                parsed = urlparse(search)
                order_id = parse_qs(parsed.query)['id'][0]

                sqlcode = """UPDATE orders
                SET
                    pub_name = %s,
                    order_date = %s,
                    order_amount = %s,
                    order_delete_ind = %s
                WHERE
                    order_id = %s
                """

                todelete = bool(removerecord)

                values = [pub_name, order_date, order_amount, todelete, order_id]
                db.modifydatabase(sqlcode, values)

                feedbackmessage = "Customer information has been updated."
                okay_href = '/publishers/orders'

            else:
                raise PreventUpdate 

    elif eventid == 'order_closebtn' and closebtn:
        pass

    else:
        raise PreventUpdate

    return [openmodal, feedbackmessage, okay_href]



@app.callback(
    [
        Output('order_id', 'value'),
        Output('pub_name', 'value'),
        Output('order_date', 'value'),
        Output('order_amount', 'value'),
    ],
    [
        Input('order_toload', 'modified_timestamp'),
    ],
    [
        State('order_toload', 'data'),
        State('url', 'search'),
    ]
)
def order_loadprofile(timestamp,toload, search):
    if toload == 1:

        parsed = urlparse(search)
        pur_ind_id = parse_qs(parsed.query)['id'][0]
        # 1. query the details from the database
        sql = """ SELECT 
                    order_id,
                    pub_name,
                    order_date,
                    order_amount,
        FROM orders
        WHERE order_id = %s """     
        

        val = [order_id]
        colnames = ["order_id","pub_name","order_date","order_amount"]

        df = db.querydatafromdatabase(sql, val, colnames)

        # 2. load the value to the interface
        order_id = df['order_id'][0]
        pub_name = df['pub_name'][0]
        order_date = df['order_date'][0]
        order_amount = df['order_amount'][0]

        return [order_id, pub_name, order_date, order_amount]

    else:
        raise PreventUpdate