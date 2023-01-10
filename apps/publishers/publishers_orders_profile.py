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
                dcc.Store(id='orderprof_toload', storage_type='memory', data=0),
            ]
        ),
        html.H2("Order Information"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Label("Order ID", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="orderprof_id", placeholder="Leave this blank",readonly=True
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
                        type="text", id="orderprof_pub_name", placeholder="Enter publisher name"
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
                        id='orderprof_date'
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
                        type="text", id="orderprof_amount", placeholder="Enter amount"
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
                            id='orderprof_removerecord',
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
            id='orderprof_removerecord_div'
        ),
        html.Hr(),
        dbc.Button('Submit', color='dark', id='orderprof_submitbtn'),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress")),
                dbc.ModalBody("tempmessage", id='orderprof_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="orderprof_closebtn", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="orderprof_modal",
            is_open=False,
        ),
    ]
)


@app.callback(
    [
        Output('orderprof_toload', 'data'),
        Output('orderprof_removerecord_div', 'style')
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
        Output('orderprof_modal', 'is_open'),
        Output('orderprof_feedback_message', 'children'),
        Output('orderprof_closebtn', 'href')
    ],
    [
        Input('orderprof_submitbtn', 'n_clicks'),
        Input('orderprof_closebtn', 'n_clicks')
    ],
    [
        State('orderprof_id', 'value'),
        State('orderprof_pub_name', 'value'),
        State('orderprof_date', 'value'),
        State('orderprof_amount', 'value'),
        State('url', 'search'),
        State('orderprof_removerecord', 'value'),
    ]
)
def order_submitprocess(submitbtn, closebtn,

                            orderid, pubname, orderdate, orderamount,
                            search, removerecord):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False
        feedbackmessage = ''
        okay_href = None
    else:
        raise PreventUpdate

    if eventid == 'orderprof_submitbtn' and submitbtn:
        openmodal = True

        inputs = [
            orderid,
            pubname,
            orderdate,
            orderamount,
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
                values = [pubname, orderdate, orderamount, False]
                db.modifydatabase(sqlcode, values)

                feedbackmessage = "Order information has been saved."
                okay_href = '/publishers/orders'

            elif mode == 'edit':

                parsed = urlparse(search)
                orderid = parse_qs(parsed.query)['id'][0]

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

                values = [pubname, orderdate, orderamount, todelete, orderid]
                db.modifydatabase(sqlcode, values)

                feedbackmessage = "Order information has been updated."
                okay_href = '/publishers/orders'

            else:
                raise PreventUpdate 

    elif eventid == 'orderprof_closebtn' and closebtn:
        pass

    else:
        raise PreventUpdate

    return [openmodal, feedbackmessage, okay_href]



@app.callback(
    [
        Output('orderprof_id', 'value'),
        Output('orderprof_pub_name', 'value'),
        Output('orderprof_date', 'value'),
        Output('orderprof_amount', 'value'),
    ],
    [
        Input('orderprof_toload', 'modified_timestamp'),
    ],
    [
        State('orderprof_toload', 'data'),
        State('url', 'search'),
    ]
)
def order_loadprofile(timestamp,toload, search):
    if toload == 1:

        parsed = urlparse(search)
        orderid = parse_qs(parsed.query)['id'][0]
        # 1. query the details from the database
        sql = """ SELECT 
                    order_id,
                    pub_name,
                    order_date,
                    order_amount,
        FROM orders
        WHERE order_id = %s """     
        

        val = [orderid]
        colnames = ["Order ID","Publisher Name","Date Received","Amount"]

        df = db.querydatafromdatabase(sql, val, colnames)

        # 2. load the value to the interface
        orderid = df['orderid'][0]
        pubname = df['pubname'][0]
        orderdate = df['orderdate'][0]
        orderamount = df['orderamount'][0]

        return [orderid, pubname, orderdate, orderamount]

    else:
        raise PreventUpdate