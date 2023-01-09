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


sort_add = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("A-Z", href="/books/allbooks/a-z"),
                dbc.DropdownMenuItem("Z-A", href="/books/allbooks/z-a"),
                dbc.DropdownMenuItem("Latest", href="/books/allbooks/latest"),
            ],
            nav=True,
            in_navbar=True,
            label="Sort by",
        ),
        dbc.Button("Add a book", color="dark", className="me-2", href="/books/books_profile"),
    ],
    brand="",
    # color="#ffffff",
    # dark=False,

)

nav_contents = [
    dbc.NavItem(dbc.NavLink("All Books", href="/books/allbooks", active=True)),
    dbc.NavItem(dbc.NavLink("Authors", href="/books/authors",)),
]
navs = html.Div(dbc.Nav(nav_contents,pills=True,fill=True))

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Label(html.H5("Search"), width=1, ),
                dbc.Col(
                    dbc.Input(
                        type="text",
                        id="books_filter",
                        placeholder="Enter keyword/s"
                    ),
                    width=5,
                ),
            ],
            className="mb-3"
        ),
        dbc.Card(
            [
                dbc.CardHeader(html.H4("Books > All Books")),
                dbc.CardBody(
                    [
                        dbc.Row(navs, style={'fontWeight':'bold',"color":"dark"}
                        ),
                        html.Hr(),
                        dbc.Row(
                            dbc.Col(sort_add),
                        ),
                        html.Div(
                            [
                                html.Div(
                                    "This will contain the table for books",
                                    id='books_allbooks_list',
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
        Output('books_allbooks_list', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('books_allbooks_filter', 'value'),
    ]
)
def updatebooks_allbooks_list(pathname, searchterm):
    if pathname == '/books':
        # 1. query the relevant records, add filter first before query
        
        sql = """ SELECT bk_title, au_id, genre_id, bk_inv_count
                FROM books
                WHERE NOT bk_delete_ind
        """
        val = []
        cols = ["Title", "Author", "Genre", "Stock Quantity"]
        

        if searchterm:
            sql += """ AND bk_title ILIKE %s"""
            val += [f"%{searchterm}%"]


        books_allbooks = db.querydatafromdatabase(sql,val,cols)
        
        # 2. create the table and add it to the db
        if books_allbooks.shape[0]:
            buttons = []
            for bk_title in books_allbooks['Title']:
                buttons += [
                    html.Div(
                        dbc.Button('Edit/Delete', href=f"/books/books_profile?mode=edit&id={bk_title}",
                            size='sm', color='dark', ),
                            style={'text-align': 'center'}
                    )
                ]
            
            # we add the buttons to the table
            books_allbooks['Action'] = buttons

            # remove ID col
            # customers_individuals.drop('Customer ID', axis=1, inplace=True)

            books_allbooks_table = dbc.Table.from_dataframe(books_allbooks, striped=True, bordered=True, hover=True, size='sm', dark=False,)

            return [books_allbooks_table]
        
        else:
            return ["There are no records that match the search term."]

    else:
        raise PreventUpdate



    
