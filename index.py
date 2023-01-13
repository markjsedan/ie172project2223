from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import webbrowser

from app import app
from apps import commonmodules as cm
from apps.books.all_books import books_home, books_home_atoz, books_home_ztoa, books_home_latest, books_profile
from apps import aboutus
from apps.customers.customers_individuals import customers_individuals_home, customers_individuals_profile
from apps.customers.customers_institutions import customers_institutions_home, customers_institutions_profile
from apps.employees import employees_home, employees_profile
from apps.reports import reports_home
from apps import login, signup
from apps.publishers.all_publishers import publishers_home, publishers_profile
from apps.publishers.orders_to_publishers import publishers_orders, publishers_orders_profile
from apps.books.genres import genres, genres_profile, genres_atoz, genres_ztoa
from apps.purchases.purchases_individuals import purchases_individuals_home,  purchases_individuals_profile
from apps.purchases.purchases_institutions import purchases_institutions_home, purchases_institutions_profile


CONTENT_STYLE = {
    "margin-top": "1em",
    "margin-left": "1em",
    "margin-right": "1em",
    "padding": "1em 1em",
}

app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=True),

        # LOGIN DATA
        # 1) logout indicator, storage_type='session' means that data will be retained
        #  until browser/tab is closed (vs clearing data upon refresh)
        dcc.Store(id='sessionlogout', data=False, storage_type='session'),
        
        # 2) current_user_id -- stores user_id
        dcc.Store(id='currentuserid', data=-1, storage_type='session'),
        
        # 3) currentrole -- stores the role
        # we will not use them but if you have roles, you can use it
        dcc.Store(id='currentrole', data=-1, storage_type='session'),

        html.Div(
            cm.navbar,
            id='navbar_div'
        ),

        # Page Content -- Div that contains page layout  
        html.Div(id='page-content', style=CONTENT_STYLE),
    ]
)


@app.callback(
    [
        Output('page-content', 'children'),
        Output('navbar_div', 'style'),
        Output('sessionlogout', 'data'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'),
    ]

)

def displaypage(pathname, sessionlogout, currentuserid):
    
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]    
    else:
        raise PreventUpdate

    if eventid == 'url':
        print(currentuserid, pathname)
        if currentuserid < 0:
            if pathname in ['/']:
                returnlayout = login.layout
            elif pathname == '/signup':
                returnlayout = signup.layout
            else:
                returnlayout = 'error404'
        
        else:
            if pathname == '/logout':
                returnlayout = login.layout
                sessionlogout = True

            elif pathname in ['/', '/books']:
                returnlayout = books_home.layout
            elif pathname == '/books/books_home_atoz':
                returnlayout = books_home_atoz.layout
            elif pathname == '/books/books_home_ztoa':
                returnlayout = books_home_ztoa.layout
            elif pathname == '/books/books_home_latest':
                returnlayout = books_home_latest.layout
            elif pathname == '/books/books_profile':
                returnlayout = books_profile.layout
            elif pathname == '/books/genres':
                returnlayout = genres.layout
            elif pathname == '/books/genres_profile':
                returnlayout = genres_profile.layout
            elif pathname == '/books/genres_atoz':
                returnlayout = genres_atoz.layout
            elif pathname == '/books/genres_ztoa':
                returnlayout = genres_ztoa.layout
            elif pathname == '/customers/individuals_home':
                returnlayout = customers_individuals_home.layout
            elif pathname == '/customers/individuals_profile':
                returnlayout = customers_individuals_profile.layout
            elif pathname == '/customers/institutions_home':
                returnlayout = customers_institutions_home.layout
            elif pathname == '/customers/institutions_profile':
                returnlayout = customers_institutions_profile.layout
            elif pathname == '/purchases/individuals_home':
                returnlayout = purchases_individuals_home.layout
            elif pathname == '/purchases/individuals_profile':
                returnlayout = purchases_individuals_profile.layout
            elif pathname == '/purchases/institutions_home':
                returnlayout = purchases_institutions_home.layout
            elif pathname == '/purchases/institutions_profile':
                returnlayout = purchases_institutions_profile.layout
            elif pathname == '/publishers/publishers_home':
                returnlayout = publishers_home.layout
            elif pathname == '/publishers/publishers_profile':
                returnlayout = publishers_profile.layout
            elif pathname == '/publishers/publishers_orders':
                returnlayout = publishers_orders.layout
            elif pathname == '/publishers/publishers_orders_profile':
                returnlayout = publishers_orders_profile.layout
            elif pathname == '/employees_home':
                returnlayout = employees_home.layout
            elif pathname == '/employees/employees_profile':
                returnlayout = employees_profile.layout
            elif pathname == '/reports_home':
                returnlayout = reports_home.layout
            elif pathname == '/about_us':
                returnlayout = aboutus.layout
            else:
                returnlayout = 'error404'
    
    else:
        raise PreventUpdate

    navbar_div = {'display': 'none' if sessionlogout else 'unset'}
    return [returnlayout, navbar_div, sessionlogout]


if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run_server(debug=False)