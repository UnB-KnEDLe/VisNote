# -*- coding: utf-8 -*-
import os
import dash

from backend import create_layout, demo_callbacks

external_scripts = [
    "https://kit.fontawesome.com/6bf2d0c0a8.js"
]

external_stylesheets = [
{
    'href': 'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
    'rel': 'stylesheet',
    'integrity': 'sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf',
    'crossorigin': 'anonymous'
}
]

# for the Local version, import local_layout and local_callbacks
# from local import local_layout, local_callbacks

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}], external_scripts=external_scripts, external_stylesheets=external_stylesheets)
server = app.server
app.title = 'VisNote'
app.layout = create_layout(app)
demo_callbacks(app)

# Running server
if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
