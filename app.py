import os
import sys

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go
import pandas as pd

import tools as vt
import parse as vp

import yaml
import logging
import logging.config

# ~~~~~ LOGGING SETUP ~~~~~ #
scriptdir = os.path.dirname(os.path.realpath(__file__))

def logpath():
    '''
    Return the path to the main log file
    '''
    global scriptdir
    log_file = os.path.join(scriptdir, 'log.txt')
    return(logging.FileHandler(log_file))

config_yaml = os.path.join(scriptdir,'logging.yml')
logger = vt.log_setup(config_yaml = config_yaml, logger_name = "app")
logger.debug("App is starting...")

# ~~~~ SETUP ~~~~~~ #
data = vt.load_json(input_file = "data.txt")

available_keys = data.keys()
available_matches = [x['id'] for x in data['data']]

app = dash.Dash()

# ~~~~ UI ~~~~~~ #
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


# ~~~~ SERVER ~~~~~~ #
@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='dict-key', component_property='value')]
)
def update_output_div(input_value):
    logger.debug("Updating input value")
    if input_value != None:
        match_id = input_value
        logger.debug("Retreiving match from data set")
        match = vp.get_match(data = data, match_id = match_id)
        logger.debug("Getting roster ids for match")
        rosters = vp.get_roster_ids(match = match)
        return('Match rosters: "{}"'.format(rosters))
    else:
        return('No match selected')


if __name__ == '__main__':
    app.run_server()
