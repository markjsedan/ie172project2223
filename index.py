from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import webbrowser

from app import app
from apps import commonmodules as cm
from apps.books import books_home
from apps import aboutus
from apps.customers.customers_individuals import customers_individuals_home


CONTENT_STYLE = {
    "margin-top": "4em",
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
        elif pathname == '/customers':
            returnlayout = customers_individuals_home.layout
        elif pathname == '/publishers':
            returnlayout = 'publishers'
        elif pathname == '/employees':
            returnlayout = 'employees'
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
