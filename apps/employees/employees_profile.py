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
                dcc.Store(id='emp_toload', storage_type='memory', data=0),
            ]
        ),
        html.H2("Employee Information"),
        html.Hr(),
        html.Div(
            dbc.Row(
                [
                    dbc.Label("Employee ID", width=2),
                    dbc.Col(
                        dbc.Input(
                            type="text", id="emp_id", placeholder="Leave this blank",readonly=True
                        ),
                        width=7,
                    ),
                ],
                className="mb-3",
            ),
            id="emp_id_div"
        ),
        dbc.Row(
            [
                dbc.Label("Employee Name", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="emp_name", placeholder="Enter employee name"
                    ),
                    width=7,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Role", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="emp_role", placeholder="Enter role"
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
                        type="text", id="emp_email", placeholder="Enter email address"
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
                        type="text", id="emp_contact_num", placeholder="Enter contact number"
                    ),
                    width=7,
                ),
            ],
            className="mb-3",
        ),
        html.Div(
            dbc.Row(
                [
                    dbc.Label("Delete Employee", width=2),
                    dbc.Col(
                        dbc.Checklist(
                            id='emp_removerecord',
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
            id='emp_removerecord_div'
        ),
        html.Hr(),
        dbc.Button('Submit', color='dark', id='emp_submitbtn'),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress")),
                dbc.ModalBody("tempmessage", id='emp_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="emp_closebtn", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="emp_modal",
            is_open=False,
        ),
    ]
)


@app.callback(
    [
        Output('emp_toload', 'data'),
        Output('emp_removerecord_div', 'style'),
        Output('emp_id_div', 'style')
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)

def emp_role_loaddropdown(pathname, search):

    if pathname == '/employees/employees_profile':
        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]
        toload = 1 if mode == 'edit' else 0
        removerecord_div = None if toload else {'display': 'None'}
        emp_id_div = None if toload else {'display': 'None'}
        
        return [toload, removerecord_div, emp_id_div]

    else:
        raise PreventUpdate



@app.callback(
    [
        Output('emp_modal', 'is_open'),
        Output('emp_feedback_message', 'children'),
        Output('emp_closebtn', 'href')
    ],
    [
        Input('emp_submitbtn', 'n_clicks'),
        Input('emp_closebtn', 'n_clicks')
    ],
    [
        State('emp_id', 'value'),
        State('emp_name', 'value'),
        State('emp_role', 'value'),
        State('emp_email', 'value'),
        State('emp_contact_num', 'value'),
        State('url', 'search'),
        State('emp_removerecord', 'value'),
    ]
)
def emp_submitprocess(submitbtn, closebtn,

                            id, name, role, email, contact_number,
                            search, removerecord):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False
        feedbackmessage = ''
        okay_href = None
    else:
        raise PreventUpdate

    if eventid == 'emp_submitbtn' and submitbtn:
        openmodal = True

        inputs = [
            name,
            role,
            email,
            contact_number
        ]

        if not all (inputs):
            feedbackmessage = "Please supply all inputs."
        else:
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]

            if mode == 'add':

                sqlcode = """INSERT INTO employees(
                    emp_name,
                    emp_role,
                    emp_email_address,
                    emp_contact_number,
                    emp_delete_ind
                )
                VALUES (%s, %s, %s, %s, %s)
                """
                values = [name, role, email, contact_number, False]
                db.modifydatabase(sqlcode, values)

                feedbackmessage = "Employee information has been saved."
                okay_href = '/employees_home'

            elif mode == 'edit':

                parsed = urlparse(search)
                empid = parse_qs(parsed.query)['id'][0]

                sqlcode = """UPDATE employees
                SET
                    emp_name = %s,
                    emp_role = %s,
                    emp_email_address = %s,
                    emp_contact_number = %s,
                    emp_delete_ind = %s
                WHERE
                    emp_id = %s
                """

                to_delete = bool(removerecord)

                values = [name, role, email, contact_number, to_delete, empid]
                db.modifydatabase(sqlcode, values)

                feedbackmessage = "Employee information has been updated."
                okay_href = '/employees_home'

            else:
                raise PreventUpdate 

    elif eventid == 'emp_closebtn' and closebtn:
        pass

    else:
        raise PreventUpdate

    return [openmodal, feedbackmessage, okay_href]


@app.callback(
    [
        Output('emp_id', 'value'),
        Output('emp_name', 'value'),
        Output('emp_role', 'value'),
        Output('emp_email', 'value'),
        Output('emp_contact_num', 'value'),
    ],
    [
        Input('emp_toload', 'modified_timestamp'),
    ],
    [
        State('emp_toload', 'data'),
        State('url', 'search'),
    ]
)
def emp_loadprofile(timestamp,to_load, search):
    if to_load == 1:

        parsed = urlparse(search)
        empid = parse_qs(parsed.query)['id'][0]
        # 1. query the details from the database
        sql = """ SELECT 
                    emp_id,
                    emp_name,
                    emp_role,
                    emp_email_address,
                    emp_contact_number
        FROM employees
        WHERE emp_id = %s"""     
        

        val = [empid]
        colnames = ["employee_id","employee_name","role","email","contact number"]

        df = db.querydatafromdatabase(sql, val, colnames)

        # 2. load the value to the interface
        employee_id = df['employee_id'][0]
        employee_name = df['employee_name'][0]
        role = df['role'][0]
        email = df['email'][0]
        contact_number = df['contact number'][0]

        return [employee_id, employee_name, role, email, contact_number]

    else:
        raise PreventUpdate