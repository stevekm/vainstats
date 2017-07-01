import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go
import pandas as pd

import tools as vt
import parse as vp

data = vt.load_json(input_file = "data.txt")

available_keys = data.keys()
available_matches = [x['id'] for x in data['data']]

app = dash.Dash()

app.layout = html.Div([
    html.Div([

        html.Div([
        html.H1(children='Pick a Match'),
            dcc.Dropdown(
                id='dict-key',
                options=[{'label': i, 'value': i} for i in available_matches]
            )
            ],
        style={'width': '48%', 'display': 'inline-block'}),
    ]),

    html.Div(id='my-div')
])

@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='dict-key', component_property='value')]
)
def update_output_div(input_value):
    if input_value != None:
        match_id = input_value
        match = vp.get_match(data = data, match_id = match_id)
        rosters = vp.get_rosters(match = match)
        return('Match data: "{}"'.format(rosters))
    else:
        return('No match selected')


if __name__ == '__main__':
    app.run_server()
