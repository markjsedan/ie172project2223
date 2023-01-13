from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

from app import app
from apps import dbconnect as db


layout = html.Div(
    [
        dbc.Card(
            [
                dbc.CardHeader(html.H4("Reports")),
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                html.Div(
                                    "This will contain the table for employees",
                                    id='reports_list',
                                    style={'text-align': 'center'}
                                ),
                            ]
                        )
                    ]
                ),
            ]
        ),
    ],
)

@app.callback(
    [
        Output('reports_filter', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('reports_filter', 'value'),
    ]
)
def updatereports_filter(pathname, searchterm):
    if pathname == '/employees_home':
        # 1. query the relevant records, add filter first before query
        
        sql = """ SELECT emp_id, emp_name, emp_role, emp_email_address, emp_contact_number
                FROM employees
                WHERE NOT emp_delete_ind
        """
        val = []
        cols = ["Employee ID", "Employee Name", "Role", "Email", "Contact Number"]
        

        if searchterm:
            sql += """ AND emp_name ILIKE %s"""
            val += [f"%{searchterm}%"]


        employees = db.querydatafromdatabase(sql,val,cols)
        
        # 2. create the table and add it to the db
        if employees.shape[0]:
            buttons = []
            for emp_id in employees['Employee ID']:
                buttons += [
                    html.Div(
                        dbc.Button('View/Edit/Delete', href=f"/employees/employees_profile?mode=edit&id={emp_id}",
                            size='sm', color='dark', ),
                            style={'text-align': 'center'}
                    )
                ]
            
            # we add the buttons to the table
            employees['Action'] = buttons

            # remove ID col
            # customers_individuals.drop('Customer ID', axis=1, inplace=True)

            employees_table = dbc.Table.from_dataframe(employees, striped=True, bordered=True, hover=True, size='sm', dark=False,)

            return [employees_table]
        
        else:
            return ["There are no records that match the search term."]

    else:
        raise PreventUpdate
