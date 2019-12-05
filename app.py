import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly
import model
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(
    html.Div([
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=80*1000,  # in milliseconds
            n_intervals=0
        )
    ])
)

@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    fig = plotly.subplots.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
    fig.layout['uirevision']=True
    channels = model.get_channels()
    for c in sorted(channels):
        data = model.read_channel(c,8000)
        fig.append_trace({
            'x': list(data[0]),
            'y': list(data[1]),
            'name': c
        }, 1 if 'temp' in c else 2, 1)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
