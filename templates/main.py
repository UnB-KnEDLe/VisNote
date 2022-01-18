from . import upload_page, review_page
import dash
from dash import html, dcc

def create_layout(app):
    return html.Div([
    
        # Homepage
        
        # Upload Page 

        upload_page.template(),
        
        # Rewiew annotations

        review_page.template(),
    ])