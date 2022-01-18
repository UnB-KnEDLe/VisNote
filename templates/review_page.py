import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

def template():
    sidebar = html.Div(className = 'reviewer_sidebar', children=
            [
                html.H2("VisNote"),
                
                dbc.Nav(className='reviewer_sidebar_menu', children=
                    [
                        dbc.NavLink("Select", href="/", active="exact", className="nav_link"),
                        dbc.NavLink("Correct", href="/correct", active="exact", className="nav_link"),
                        dbc.NavLink("Download", href="/dowload", active="exact", className="nav_link"),
                    ],
                    vertical=True,
                ),
            ]
        )

    control_panel = html.Div(id="reviewer_control_panel", children=[])
    

    content = html.Div(id="page-content", className = "reviewer_content")

    select_content = [html.P("Select annotations!")]

    correct_content = [html.P("Correct annotations!")]

    download_content = [html.P("Download annotations!")]

    return html.Div(id = 'reviewer_page', children =[dcc.Location(id="url"), sidebar, content,
                    html.Div(style = {"display":"none"}, children=[
                        html.Div(id="reviewer_select", children=select_content),
                        html.Div(id="reviewer_correct", children=correct_content),
                        html.Div(id="reviewer_download", children=download_content)
                    ])])
