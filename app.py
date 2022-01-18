# -*- coding: utf-8 -*-
import dash

from main_layout import create_layout
from main import  main_callbacks

# for the Local version, import local_layout and local_callbacks
# from local import local_layout, local_callbacks

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],external_stylesheets=external_stylesheets)
server = app.server
app.title = 'VisNote 2.0'
app.layout = create_layout(app)
main_callbacks(app)

# Running server 
if __name__ == "__main__":
    app.run_server(debug=True)