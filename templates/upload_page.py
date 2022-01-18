import dash
from dash import html, dcc

def template():
    return html.Div(id = "uploader_page", className='uploader_page', children =[

            # 1. Add annotations
            html.Div([
                html.H1('1. Add annotations', className='uploader_title'),
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

            # Annotations Output
            html.Div(id='uploader_output')
            
        ])