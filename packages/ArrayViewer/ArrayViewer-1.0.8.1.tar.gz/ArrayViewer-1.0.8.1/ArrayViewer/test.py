# import dash
# import dash_html_components as html
# import json

# from dash.dependencies import Output, Input
# from dash_extensions import Keyboard

# app = dash.Dash()
# app.layout = html.Div([Keyboard(id="keyboard"), html.Div(id="output")])


# @app.callback(Output("output", "children"), [Input("keyboard", "keydown")])
# def keydown(event):
    # return json.dumps(event)


# if __name__ == '__main__':
import dash
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

dct = {"Outer": {"Inner": None, 'Inner2': None}}


def traverse(D, key):
    print(key, D.keys())
    if D == None:
        return None
    return [traverse(D[k], f"{key}-{i}") for i, k in enumerate(D)]


print(traverse(dct, "0"))


class DS(html.Summary):
    def __init__(self, Det, Sum):

        super().__init__(id=Det, children=[DS(s) for s in Sum])


app.layout = html.Div(
    [
        html.Details(
            [
                html.Summary(
                    html.A(id='outer-link', children=['Outer Link']),
                ),
                html.Div(
                    [
                        html.Details(
                            html.Summary(
                                html.A(id='inner-link', children=['Inner Link'])
                            )
                        )
                    ],
                    style={'text-indent': '2em'}
                )
            ]
        ),
        html.Div(id='outer-count'),
        html.Div(id='inner-count'),
        html.Div(id='last-clicked')
    ]
)


@app.callback(
    [
        Output('outer-count', 'children'),
        Output('inner-count', 'children'),
        Output('last-clicked', 'children')
    ],
    [
        Input('outer-link', 'n_clicks'),
        Input('outer-link', 'n_clicks_timestamp'),
        Input('inner-link', 'n_clicks'),
        Input('inner-link', 'n_clicks_timestamp')
    ],
)
def divclick(outer_link_clicks, outer_link_time, inner_link_clicks, inner_link_time):
    if outer_link_time is None:
        outer_link_time = 0
    if inner_link_time is None:
        inner_link_time = 0

    timestamps = {
        'None': 1,
        'Outer Link': outer_link_time,
        'Inner Link': inner_link_time
    }

    last_clicked = max(timestamps, key=timestamps.get)

    return(
        'Outer link clicks: ' + str(outer_link_clicks),
        'Inner link clicks: ' + str(inner_link_clicks),
        'Last clicked: ' + last_clicked
    )

if __name__ == '__main__':
    app.run_server()   # app.run_server()
