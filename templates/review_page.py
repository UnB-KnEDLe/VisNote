import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import dash_daq as daq

def template():
    sidebar = html.Div(className = 'reviewer_sidebar', children=
            [
                html.Button(children=[" <- Return"], className="base_button_reverse", id="button_return_upload_page", n_clicks=0),
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



    visualization_panel = html.Div(id="reviewer_layout_panel", children=[
        html.Div(id='reviewer_topmenu', children=[
            html.H6('points'),
            daq.ToggleSwitch(id='view_switch',value=False),                        
            html.H6('list'),
            html.H6('|'),
            html.H6('relation'),
            daq.ToggleSwitch(id='level_switch',value=False),                        
            html.H6('entity'),
            html.H6('|'),
            html.H6('tags'),
            daq.ToggleSwitch(id='color_code_switch',value=False),                        
            html.H6('state'),
        ]),

        html.Div(id='reviewer_annotations_view', children=[
            html.Div(id='reviewer_point_visualization', children=[
                dcc.Graph(id="point_visualization")
            ]),

            html.Div(id='reviewer_list_visualization', style={'display':'none'}, children=[
                html.H6('Lista de annotations - a implementar'),
            ])
        ])
    ])
    


    content = html.Div(id="page-content", className = "reviewer_content")

    select_content = [visualization_panel]

    correct_content = [html.P("Correct annotations!")]

    download_content = [html.P("Download annotations!")]

    return html.Div(id = 'reviewer_page', children =[dcc.Location(id="url"), sidebar, content,
                    html.Div(style = {"display":"none"}, children=[
                        html.Div(id="reviewer_select", children=select_content),
                        html.Div(id="reviewer_correct", children=correct_content),
                        html.Div(id="reviewer_download", children=download_content)
                    ])])
