import dash
from dash import html, dcc
import dash_daq as daq
import dash_bootstrap_components as dbc

def template():
    return html.Div(id = "uploader_page", className='uploader_page', children =[

            # 1. Add annotations
            html.Div([
                html.H1('Add your  annotations', className='uploader_title'),
                html.Div(className='uploader_file_type',children=[
                    html.H6('XML'),
                    daq.ToggleSwitch(id='file-type-switch',value=False),                        
                    html.H6('CSV'),                    
                ]),
                dcc.Upload(
                    id='upload_annotations',
                    children=html.Div([
                        html.Img(src='assets/img/file.svg', className='uploader_img'),
                        html.H3('Drop files here.', className='uploader_text'),
                        html.Button('Select a File', className='base_button')
                    ], className='upload_box'),
                    multiple=True # permite fazer o upload de mais de um documento
                ),
            ], className='uploader_card'),
            
            # Button to "review annotations" page
            html.Button(children=["Review Annotations ->"], className="base_button", id="button_review_annotations", n_clicks=0, style={"display":"none"}),
            html.Button(id="value-button_review_annotations", className="Button",n_clicks=0, style={"display":"none"}),

            # Annotations Output
            html.Div(id='uploader_output'),

            # Loading to show its still running
            dcc.Loading(
                    id="uploader_loading",
                    children=[html.Div(id="uploader_loading_output")],
                    type="circle",
                ),
            
        ])