from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import webbrowser

from app import app
from apps import commonmodules as cm
from apps.books.all_books import books_home, books_profile
from apps import aboutus
from apps.customers.customers_individuals import customers_individuals_home, customers_individuals_profile
from apps.customers.customers_institutions import customers_institutions_home, customers_institutions_profile
from apps.employees import employees, employees_profile
from apps.publishers import publishers, publishers_profile
from apps.books.genres import genres, genres_profile


CONTENT_STYLE = {
    "margin-top": "1em",
    "margin-left": "1em",
    "margin-right": "1em",
    "padding": "1em 1em",
}

app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=True),
        cm.navbar,
        html.Div(id='page-content', style=CONTENT_STYLE),
    ]
)


@app.callback(
    [
        Output('page-content', 'children')
    ],
    [
        Input('url', 'pathname')
    ]
)

def displaypage(pathname):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]   
        
    else:
        raise PreventUpdate

    if eventid == 'url':
        if pathname in ['/', '/books']:
            returnlayout = books_home.layout
        elif pathname == '/books/books_profile':
            returnlayout = books_profile.layout
        elif pathname == '/books/genres':
            returnlayout = genres.layout
        elif pathname == '/books/genres_profile':
            returnlayout = genres_profile.layout
        elif pathname == '/customers/individuals_home':
            returnlayout = customers_individuals_home.layout
        elif pathname == '/customers/individuals_profile':
            returnlayout = customers_individuals_profile.layout
        elif pathname == '/customers/institutions_home':
            returnlayout = customers_institutions_home.layout
        elif pathname == '/customers/institutions_profile':
            returnlayout = customers_institutions_profile.layout
        elif pathname == '/publishers':
            returnlayout = publishers.layout
        elif pathname == '/publishers/publishers_profile':
            returnlayout = publishers_profile.layout
        elif pathname == '/employees':
            returnlayout = employees.layout
        elif pathname == '/employees/employees_profile':
            returnlayout = employees_profile.layout
        elif pathname == '/reports':
            returnlayout = 'reports'
        elif pathname == '/about_us':
            returnlayout = aboutus.layout
        else:
            returnlayout = 'error404'
    
    else:
        raise PreventUpdate

    return[returnlayout]

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run_server(debug=False)
