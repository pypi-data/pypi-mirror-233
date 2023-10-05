import plotly.graph_objects as go
from dash import Dash, html, dcc

rowEvenColor = 'lightgrey'
rowOddColor = 'white'

fig = go.Figure(data=[go.Table(
    header=dict(
        values=['<b>EXPENSES</b>', '<b>Q1</b>', '<b>Q2</b>'],
        align=['left'],
    ),
    cells=dict(
        values=[['Salaries', 'Office', '<b>TOTAL</b>'],
                [1200000, 2000, 12120000],
                [1300000, 2000, 130902000]],
        align=['left', 'center'],
    ),
)])

fig.show()


app = Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True)
