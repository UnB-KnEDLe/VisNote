import dash

from templates.main import create_layout
from src.main import  main_callbacks

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}], external_stylesheets=external_stylesheets)
server = app.server
app.title = 'VisNote'
app.layout = create_layout(app)
main_callbacks(app)

# Running server 
if __name__ == "__main__":
    app.run_server(debug=True)