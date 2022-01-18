from dash.dependencies import Input, Output, State
from dash import html
import dash_bootstrap_components as dbc

def callbacks(app):
    @app.callback(
        [   
            Output("page-content", "children"), 
        ],
        [
            Input("url", "pathname")
        ], 
        [
            State("reviewer_select","children"),
            State("reviewer_correct","children"),
            State("reviewer_download","children")
        ])
    def render_page_content(pathname, select, correct, download):
        if pathname == "/":
            return select
        elif pathname == "/correct":
            return correct
        elif pathname == "/dowload":
            return download

        return select