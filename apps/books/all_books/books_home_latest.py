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
                dbc.DropdownMenuItem("A-Z", href="/books/books_home_atoz"),
                dbc.DropdownMenuItem("Z-A", href="/books/books_home_ztoa"),
                dbc.DropdownMenuItem("Latest", href="/books/books_home_latest"),
            ],
            nav=True,
            in_navbar=True,
            label="Sort by",
        ),
        dbc.Button("Add a book", color="dark", className="me-2", href="/books/books_profile?mode=add"),
    ],
    brand="",
    # color="#ffffff",
    # dark=False,

)

nav_contents = [
    dbc.NavItem(dbc.NavLink("All Books", href="/books", active=True)),
    dbc.NavItem(dbc.NavLink("Genres", href="/books/genres",)),
]
navs = html.Div(dbc.Nav(nav_contents,pills=True,fill=True))

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Label(html.H5("Search"), width=1, ),
                dbc.Col(
                    dbc.Input(
                        type="text", id="books_allbooks_filter_latest", placeholder="Enter keyword/s"
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
                                    id='books_allbooks_list_latest',
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
        Output('books_allbooks_list_latest', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('books_allbooks_filter_latest', 'value'),
    ]
)
def updatebooks_allbooks_list_latest(pathname, searchterm):
    if pathname == '/' or '/books':
        # 1. query the relevant records, add filter first before query
        
        sql = """ SELECT bk_title, bk_author, genre_name, bk_pub_yr, bk_inv_count, bk_id
                FROM books
                    INNER JOIN genres on books.genre_id = genres.genre_id
                ORDER BY bk_modified_date DESC
                WHERE NOT bk_delete_ind
        """
        val = []
        cols = ["Title", "Author", "Genre","Publication Year","Stock Quantity","Book ID"]
        

        if searchterm:
            sql += """ AND bk_title ILIKE %s"""
            val += [f"%{searchterm}%"]
            
        books_allbooks_latest = db.querydatafromdatabase(sql,val,cols)
        
        # 2. create the table and add it to the db
        if books_allbooks_latest.shape[0]:
            buttons = []
            for bk_id in books_allbooks_latest['Book ID']:
                buttons += [
                    html.Div(
                        dbc.Button('View/Edit/Delete', href=f"/books/books_profile?mode=edit&id={bk_id}",
                            size='sm', color='dark', ),
                            style={'text-align': 'center'}
                    )
                ]
            
            # we add the buttons to the table
            books_allbooks_latest['Action'] = buttons
            books_allbooks_latest.drop('Book ID', axis=1, inplace=True)
            books_allbooks_table_latest = dbc.Table.from_dataframe(books_allbooks_latest, striped=True, bordered=True, hover=True, size='sm', dark=False,)
            
            return [books_allbooks_table_latest]
        
        else:
            return ["There are no records that match the search term."]

    else:
        raise PreventUpdate



    
