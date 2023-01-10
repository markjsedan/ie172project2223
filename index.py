# from dash import dcc
# from dash import html
# import dash_bootstrap_components as dbc
# import dash
# from dash.dependencies import Input, Output, State
# from dash.exceptions import PreventUpdate

# import webbrowser

# from app import app
# from apps import commonmodules as cm
# from apps.books.all_books import books_home, books_profile
# from apps import aboutus
# from apps.customers.customers_individuals import customers_individuals_home, customers_individuals_profile
# from apps.customers.customers_institutions import customers_institutions_home, customers_institutions_profile
# from apps.employees import employees, employees_profile
# from apps import login, signup
# from apps.publishers import publishers, publishers_profile
# from apps.books.genres import genres, genres_profile
# # from apps.purchases.purchases_individuals import purchases_individuals_home, purchases_individuals_profile


# CONTENT_STYLE = {
#     "margin-top": "1em",
#     "margin-left": "1em",
#     "margin-right": "1em",
#     "padding": "1em 1em",
# }

# app.layout = html.Div(
#     [
#         dcc.Location(id='url', refresh=True),

#         # LOGIN DATA
#         # 1) logout indicator, storage_type='session' means that data will be retained
#         #  until browser/tab is closed (vs clearing data upon refresh)
#         dcc.Store(id='sessionlogout', data=False, storage_type='session'),
        
#         # 2) current_user_id -- stores user_id
#         dcc.Store(id='currentuserid', data=-1, storage_type='session'),
        
#         # 3) currentrole -- stores the role
#         # we will not use them but if you have roles, you can use it
#         dcc.Store(id='currentrole', data=-1, storage_type='session'),

#         html.Div(
#             cm.navbar,
#             id='navbar_div'
#         ),

#         # Page Content -- Div that contains page layout  
#         html.Div(id='page-content', style=CONTENT_STYLE),
#     ]
# )


# @app.callback(
#     [
#         Output('page-content', 'children'),
#         Output('navbar_div', 'style'),
#         Output('sessionlogout', 'data'),
#     ],
#     [
#         Input('url', 'pathname')
#     ],
#     [
#         State('sessionlogout', 'data'),
#         State('currentuserid', 'data'),
#     ]

# )

# def displaypage(pathname, sessionlogout, currentuserid):
    
#     ctx = dash.callback_context
#     if ctx.triggered:
#         eventid = ctx.triggered[0]['prop_id'].split('.')[0]    
#     else:
#         raise PreventUpdate

#     if eventid == 'url':
#         print(currentuserid, pathname)
#         if currentuserid < 0:
#             if pathname in ['/']:
#                 returnlayout = login.layout
#             elif pathname == '/signup':
#                 returnlayout = signup.layout
#             else:
#                 returnlayout = 'error404'
        
#         else:
#             if pathname in ['/logout']:
#                 returnlayout = login.layout
#                 sessionlogout = True

#             elif pathname == '/books':
#                 returnlayout = books_home.layout
#             elif pathname == '/books/books_profile':
#                 returnlayout = books_profile.layout
#             elif pathname == '/books/genres':
#                 returnlayout = genres.layout
#             elif pathname == '/books/genres_profile':
#                 returnlayout = genres_profile.layout
#             elif pathname == '/customers/individuals_home':
#                 returnlayout = customers_individuals_home.layout
#             elif pathname == '/customers/individuals_profile':
#                 returnlayout = customers_individuals_profile.layout
#             elif pathname == '/customers/institutions_home':
#                 returnlayout = customers_institutions_home.layout
#             elif pathname == '/customers/institutions_profile':
#                 returnlayout = customers_institutions_profile.layout
#             # elif pathname == '/purchases/individuals_home':
#             #     returnlayout = purchases_individuals_home.layout
#             # elif pathname == '/purchases/individuals_profile':
#             #     returnlayout = purchases_individuals_profile.layout
#             elif pathname == '/publishers':
#                 returnlayout = publishers.layout
#             elif pathname == '/publishers/publishers_profile':
#                 returnlayout = publishers_profile.layout
#             elif pathname == '/employees':
#                 returnlayout = employees.layout
#             elif pathname == '/employees/employees_profile':
#                 returnlayout = employees_profile.layout
#             elif pathname == '/reports':
#                 returnlayout = 'reports'
#             elif pathname == '/about_us':
#                 returnlayout = aboutus.layout
#             else:
#                 returnlayout = 'error404'
    
#     else:
#         raise PreventUpdate

#     navbar_div = {'display': 'none' if sessionlogout else 'unset'}
#     return [returnlayout, navbar_div, sessionlogout]


# if __name__ == '__main__':
#     webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
#     app.run_server(debug=False)


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
from apps.employees import employees_home, employees_profile
from apps import login, signup
from apps.publishers import publishers_home, publishers_profile, publishers_orders
from apps.books.genres import genres, genres_profile
from apps.purchases.purchases_individuals import purchases_individuals_home,purchases_individuals_profile


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
        Output('page-content', 'children'),
    ],
    [
        Input('url', 'pathname')
    ],

)

def displaypage(pathname):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]    
        if eventid == 'url': 
            if pathname == '/' or pathname =='/books':
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
            elif pathname == '/purchases/individuals_home':
                returnlayout = purchases_individuals_home.layout
            elif pathname == '/purchases/individuals_profile':
                returnlayout = purchases_individuals_profile.layout
            elif pathname == '/publishers/publishers_home':
                returnlayout = publishers_home.layout
            elif pathname == '/publishers/publishers_profile':
                returnlayout = publishers_profile.layout
            elif pathname == '/publishers/publishers_orders':
                returnlayout = publishers_orders.layout
            elif pathname == '/employees':
                returnlayout = employees_home.layout
            elif pathname == '/employees/employees_profile':
                returnlayout = employees_profile.layout
            elif pathname == '/about_us':
                returnlayout = aboutus.layout
            else:
                returnlayout = 'error404'
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

    return [returnlayout]


if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run_server(debug=True)
