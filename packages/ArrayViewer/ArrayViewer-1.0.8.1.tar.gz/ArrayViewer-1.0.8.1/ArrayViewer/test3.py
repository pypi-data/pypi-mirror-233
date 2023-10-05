## From: https://community.plotly.com/t/drag-and-drop-cards/42480/4
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, ClientsideFunction, State

class Slice(dbc.Card):
    """ A single Slice. """
    def __init__(self, n):
        super().__init__(id=f"child{n}", children=[])


app = dash.Dash(
    __name__,
    external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/dragula/3.7.2/dragula.min.js"],
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

app.layout = html.Div(id="main", children=[

    html.Div(id="drag_container0", className="container", children=[
        dbc.Row(id="drag_container", className="container", children=[
            dbc.Col(dbc.Card([
                dbc.CardHeader("Card 1"),
                dbc.CardBody(
                    "Some content"
                ),
            ])),
            dbc.Col(dbc.Card([
                dbc.CardHeader("Card 2"),
                dbc.CardBody(
                    "Some other content"
                ),
            ])),
            dbc.Col(dbc.Card([
                dbc.CardHeader("Card 3"),
                dbc.CardBody(
                    "Some more content"
                ),
            ])),
        ], style={'padding': 10}),
    ])
])

app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="make_draggable"),
    Output("drag_container0", "data-drag"),
    Input("drag_container", "id")
)

if __name__ == "__main__":
    app.run_server(debug=True)
