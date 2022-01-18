from . import uploader, reviewer

import dash
from dash.dependencies import Input, Output

def main_callbacks(app):

    @app.callback(
        [ 
            Output("button_review_annotations", "style"),   

            Output("uploader_page", "style"),
            Output("reviewer_page", "style"),          
        ],
        [
            Input('upload_annotations', 'contents'),
            Input("button_review_annotations", "n_clicks")
        ]
    )
    def control_displays(upload_annotations,review_annotations):       
        # vê qual foi o input que ativou o callback
        context = dash.callback_context
        trigger = context.triggered[0]['prop_id']

        displays = [
            {"display":"none"}, #button review_annotations
            {"display":"none"}, #uploader page
            {}, #reviewer page
        ]

        if str(trigger) == 'upload_annotations.contents':
            displays = [
                {}, #button review_annotations
                {},  #uploader page
                {"display":"none"}, #reviewer page
            ]

        elif str(trigger) == 'button_review_annotations.n_clicks':
            displays = [
                {"display":"none"}, #button review_annotations
                {"display":"none"},  #uploader page
                {}, #reviewer page
            ]

        else: 
            displays = [
            {"display":"none"}, #button review_annotations
            {"display":"none"}, #uploader page
            {}, #reviewer page
        ]

        return displays

    # Part 1 - upload annotations
    uploader.callbacks(app)

    # Part 2 - review annotations
    reviewer.callbacks(app)