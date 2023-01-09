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
                dcc.Store(id='cust_ins_toload', storage_type='memory', data=0),
            ]
        ),
        html.H2("Customer Information"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Label("Customer ID", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="cust_ins_id", placeholder="Leave this blank",readonly=True
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
                    dbc.Input(
                        type="text", id="cust_ins_name", placeholder="Enter customer name"
                    ),
                    width=7,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Profession", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="cust_ins_prof", placeholder="Enter profession"
                    ),
                    width=7,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Email", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="cust_ins_email", placeholder="Enter email address"
                    ),
                    width=7,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Contact Number", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="cust_ins_contact_num", placeholder="Enter contact number"
                    ),
                    width=7,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Address", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="cust_ins_address", placeholder="Enter address"
                    ),
                    width=7,
                ),
            ],
            className="mb-3",
        ),
        html.Div(
            dbc.Row(
                [
                    dbc.Label("Delete Customer", width=2),
                    dbc.Col(
                        dbc.Checklist(
                            id='cust_ins_removerecord',
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
            id='cust_ins_removerecord_div'
        ),
        html.Hr(),
        dbc.Button('Submit', color='dark', id='cust_ins_submitbtn'),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress")),
                dbc.ModalBody("tempmessage", id='cust_ins_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="cust_ins_closebtn", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="cust_ins_modal",
            is_open=False,
        ),
    ]
)


@app.callback(
    [
        Output('cust_ins_toload', 'data'),
        Output('cust_ins_removerecord_div', 'style')
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)
def cust_ins_prof_loaddropdown(pathname, search):

    if pathname == '/customers/institutions_profile':
        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]
        toload = 1 if mode == 'edit' else 0
        removerecord_div = None if toload else {'display': 'None'}
        
        return [toload, removerecord_div]

    else:
        raise PreventUpdate




@app.callback(
    [
        Output('cust_ins_modal', 'is_open'),
        Output('cust_ins_feedback_message', 'children'),
        Output('cust_ins_closebtn', 'href')
    ],
    [
        Input('cust_ins_submitbtn', 'n_clicks'),
        Input('cust_ins_closebtn', 'n_clicks')
    ],
    [
        State('cust_ins_id', 'value'),
        State('cust_ins_name', 'value'),
        State('cust_ins_prof', 'value'),
        State('cust_ins_email', 'value'),
        State('cust_ins_contact_num', 'value'),
        State('cust_ins_address', 'value'),
        State('url', 'search'),
        State('cust_ins_removerecord', 'value'),
    ]
)
def cust_ins_submitprocess(submitbtn, closebtn,

                            customer_id, name, profession, email, contact_number, address,
                            search, removerecord):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False
        feedbackmessage = ''
        okay_href = None
    else:
        raise PreventUpdate

    if eventid == 'cust_ins_submitbtn' and submitbtn:
        openmodal = True

        inputs = [
            name,
            profession,
            email,
            contact_number,
            address
        ]

        if not all (inputs):
            feedbackmessage = "Please supply all inputs."
        else:
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]

            if mode == 'add':

                sqlcode = """INSERT INTO customers_institutions(
                    cust_ins_name,
                    cust_ins_prof,
                    cust_ins_email,
                    cust_ins_contact_num,
                    cust_ins_address,
                    cust_ins_delete_ind
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                values = [name, profession, email, contact_number, address, False]
                db.modifydatabase(sqlcode, values)

                feedbackmessage = "Customer information has been saved."
                okay_href = '/customers/institutions_home'

            elif mode == 'edit':

                parsed = urlparse(search)
                cust_ins_id = parse_qs(parsed.query)['id'][0]

                sqlcode = """UPDATE customers_institutions
                SET
                    cust_ins_name = %s,
                    cust_ins_prof = %s,
                    cust_ins_email = %s,
                    cust_ins_contact_num = %s,
                    cust_ins_address = %s,
                    cust_ins_delete_ind = %s
                WHERE
                    cust_ins_id = %s
                """

                todelete = bool(removerecord)

                values = [name, profession, email, contact_number, address, todelete,cust_ins_id]
                db.modifydatabase(sqlcode, values)

                feedbackmessage = "Customer information has been updated."
                okay_href = '/customers/institutions_home'

            else:
                raise PreventUpdate 

    elif eventid == 'cust_ins_closebtn' and closebtn:
        pass

    else:
        raise PreventUpdate

    return [openmodal, feedbackmessage, okay_href]



@app.callback(
    [
        Output('cust_ins_id', 'value'),
        Output('cust_ins_name', 'value'),
        Output('cust_ins_prof', 'value'),
        Output('cust_ins_email', 'value'),
        Output('cust_ins_contact_num', 'value'),
        Output('cust_ins_address', 'value'),
    ],
    [
        Input('cust_ins_toload', 'modified_timestamp'),
    ],
    [
        State('cust_ins_toload', 'data'),
        State('url', 'search'),
    ]
)
def cust_ins_loadprofile(timestamp,toload, search):
    if toload == 1:

        parsed = urlparse(search)
        cust_ins_id = parse_qs(parsed.query)['id'][0]
        # 1. query the details from the database
        sql = """ SELECT 
                    cust_ins_id,
                    cust_ins_name,
                    cust_ins_prof,
                    cust_ins_email,
                    cust_ins_contact_num,
                    cust_ins_address,
        FROM customers_institutions
        WHERE cust_ins_id = %s """     
        

        val = [cust_ins_id]
        colnames = ["customer_id","name","profession","email","contact number","address"]

        df = db.querydatafromdatabase(sql, val, colnames)

        # 2. load the value to the interface
        customer_id = df['customer_id'][0]
        name = df['name'][0]
        profession = df['profession'][0]
        email = df['email'][0]
        contact_number = df['contact number'][0]
        address = df['address'][0]

        return [customer_id, name, profession, email, contact_number, address]

    else:
        raise PreventUpdate