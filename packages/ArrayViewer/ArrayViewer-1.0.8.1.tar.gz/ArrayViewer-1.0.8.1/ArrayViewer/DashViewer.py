"""
Created on Mon Mar 13 12:04:31 2023
ArrayViewer.DashViewer

@author: alexschw

Creates a Viewer in the Dash style.
"""

from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from dash_treeview_antd import TreeView
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


class DTree(html.Div):
    def __init__(self):
        self.Tree = TreeView(id='fileTree', multiple=False, checkable=False,
                             expanded=['0'], data={'title': 'Files', 'key': '0'},
                             children=dcc.Upload("Add new file"))
        # self.secTree = TreeView(id='dataTree', multiple=False, checkable=False,
                                # expanded=['0'], data={'title': 'Data', 'key': '0'})
        self.secTree = self.testTree2()
        super().__init__(self.Tree, id="datatree", className="data_box")

    def testTree(self):
        return TreeView(id='input', multiple=False, checkable=False,
                        expanded=['0'], data={
                            'title': 'Parent', 'key': '0', 'children': [{
                                'title': 'Child', 'key': '0-0', 'children': [
                                    {'title': 'Subchild1', 'key': '0-0-1'},
                                    {'title': 'Subchild2', 'key': '0-0-2'},
                                    {'title': 'Subchild3', 'key': '0-0-3'},
                                ]}]})
    def testTree2(self):
        return html.Details([
            html.Summary([html.Summary([html.Tr("A"), html.Tr("B"),
                                        html.Tr("C")]), html.Summary("A")])
        ])


def generate_fast_access():
    return html.Div(id="fastaccess", className="data_box", children=
                    html.Table([html.Tr([html.Td("min: 0.0", id="min_text"),
                                         html.Td("max: 1.0", id="max_text")]),
                                html.Br(),
                                html.Tr(dcc.Checklist(["Transpose"],[])),
                                html.Br(),
                                html.Tr([html.Td(dcc.Input(id="permute_txt")),
                                         html.Td(html.Button("Permute", id="permute_btn"))])]))


class Slice():
    def __init__(self, n):
        self._n = n
        rowOddColor = 'white'
        rowEvenColor = 'lightgrey'
        self.Fig = go.Figure(data=[go.Table(
            header=dict(values=['<b>EXPENSES</b>', '<b>Q1</b>', '<b>Q2</b>', '<b>Q3</b>', '<b>Q4</b>'],
                        line_color='darkslategray', fill_color='grey',
                        align=['left', 'center'], font=dict(color='white', size=12)),
            cells=dict(values=[['Salaries', 'Office', 'Merchandise', 'Legal', '<b>TOTAL</b>'],
                               [1200000, 20000, 80000, 2000, 12120000],
                               [1300000, 20000, 70000, 2000, 130902000],
                               [1300000, 20000, 120000, 2000, 131222000],
                               [1400000, 20000, 90000, 2000, 14102000]],
                       line_color='darkslategray',
                       # 2-D list of colors for alternating rows
                       fill_color=[[rowOddColor, rowEvenColor, rowOddColor, rowEvenColor, rowOddColor]*5],
                       align=['left', 'center'], font=dict(color='darkslategray', size=11)))])

    def get_table(self):
        return self.Fig

    def change_slices(self, n=2):
        self.n_slices = n
        self.children = None


def generate_slices(n=2):
    return html.Table([html.Tr()])

def generate_table(dataframe, max_rows=1000):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ], style={'margin-right': 'auto', 'margin-left': 'auto'}, draggable="true")


def create_layout(current_tree):
    """ Create the layout structure for the dash app. """
    tabs = dcc.Tabs(id="tabs", value="f", children=[
        dcc.Tab(label="Files", value="f"), dcc.Tab(label="Data", value="d")])
    fast_acc = generate_fast_access()
    fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])
    chart = html.Div(dcc.Graph(figure=fig, responsive=True), id="chartview",
                     className="data_box")
    range_slider = html.Div(dcc.RangeSlider(0, 20, vertical=True, id="rangeslider"),
                            id="rangeview",  className="data_box")
    modal = dbc.Modal([dbc.ModalHeader("Header"), "Up"], id="modal", is_open=False)
    slv = Slice(2)
    return html.Div(id="wrapper", children=[
        html.Div(id="left-panel", children=[tabs, current_tree, fast_acc]),
        html.Div(id="right-panel", children=[chart, range_slider]),
        html.Div(dcc.Graph(slv.get_table()), id="slice", className="data_box"),
        modal, dcc.ConfirmDialog(id="message")
    ])


@app.callback(Output("datatree", "children"),
              Input("tabs", "value"))
def put_dtree(tab):
    """ Create the datatree Tabs """
    if tab == "f":
        return CurrentTree.Tree
    return CurrentTree.secTree


@app.callback(Output("modal", "is_open"),
              Input("permute_btn", "n_clicks"),
              State("modal", "is_open"))
def toggle(n1, is_open):
    if n1:
        return not is_open
    return is_open


@app.callback([Output("message", "message"), Output("message", "displayed")],
              Input("fileTree", "selected"))
def clicked(item):
    if item:
        return str(item[0]), True
    return "", False


if __name__ == '__main__':
    CurrentTree = DTree()
    app.layout = create_layout(CurrentTree)

    app.run_server(debug=True)
