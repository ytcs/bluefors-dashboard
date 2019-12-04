import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly
import model

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(
    html.Div([        
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=10*1000,  # in milliseconds
            n_intervals=0
        )
    ])
)

@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    temp6_data = list(zip(*model.read_channel('temp6', 8000)))
    temp8_data = list(zip(*model.read_channel('temp8', 8000)))

    fig = plotly.subplots.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
    fig.append_trace({
        'x': list(temp6_data[0]),
        'y': list(temp6_data[1]),
        'name': 'T6'
    }, 1, 1)
    fig.append_trace({
        'x': list(temp8_data[0]),
        'y': list(temp8_data[1]),
        'name': 'T8'
    }, 1, 1)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
