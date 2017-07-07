#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Dash app for the vainstats API querying and player ranking
'''

# ~~~~~ LIBRARIES ~~~~~ #
# system modules
import os
import sys
import gamelocker

# dash modules
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

# this app modules
import tools as vt
import parse as vp
import data as vd

# logging modules
import yaml
import logging
import logging.config


# ~~~~~ LOGGING SETUP ~~~~~ #
# path to the current script's dir
scriptdir = os.path.dirname(os.path.realpath(__file__))

def logpath():
    '''
    Return the path to the main log file; needed by the logging.yml
    use this for dynamic output log file paths & names
    '''
    global scriptdir
    log_file = os.path.join(scriptdir, 'log.txt')
    return(logging.FileHandler(log_file))

config_yaml = os.path.join(scriptdir,'logging.yml')
logger = vt.log_setup(config_yaml = config_yaml, logger_name = "app")
logger.debug("App is starting...")


# ~~~~ SETUP ~~~~~~ #
available_matches = [x['id'] for x in vd.demo_data['data']]

app = dash.Dash()



# ~~~~ APP UI ~~~~~~ #
# main div
app.layout = html.Div([
    # invisible div placeholder
    html.Div(id = 'global-data'),
    # main heading
    html.H1(children = 'Welcome to vainstats - VainGlory game match stats & player ranking!'),
    # first sub-div
    html.Div([
        # first sub-sub-div
        html.Div([
            html.H2(children = 'Pick a Match from the demo list:'),
            dcc.Dropdown(
                id = 'dict-key',
                options = [{'label': '{0}: {1}'.format(i + 1, match), 'value': match} for i, match in enumerate(available_matches)]
            )
            ],
        style = {'width': '48%', 'display': 'inline-block'}
        ),
    ]),

    # second sub-div
    html.H4(children='Match Stats'),
    html.Div(id = 'roster-table'),

    # third sub div
    html.Div([
        # first sub-sub-div
        html.Div([
            html.H2(children = 'API Queried Matches:'),
            dcc.Dropdown(
                id = 'selected-api-match-id',
                options = [{'label': '{0}: {1}'.format(i + 1, match), 'value': match} for i, match in enumerate(vd.api_matches)]
                ,
                value = vd.api_matches[0]
            )
            ],
        style = {'width': '48%', 'display': 'inline-block'}
        ),
        html.H4(children='Match Stats'),
        html.Div(id = 'api-roster-table')
    ])
])


# ~~~~ APP SERVER ~~~~~~ #
@app.callback(
    Output(component_id = 'roster-table', component_property = 'children'),
    [Input(component_id = 'dict-key', component_property = 'value')]
)
def update_roster_table(input_value, max_rows=10):
    logger.debug("Updating input value: {0}".format(input_value))
    if input_value != None:
        match_id = input_value
        logger.debug("Match id: {0}".format(match_id))

        logger.debug("Retreiving specified match from data set")
        match = vp.get_match(data = vd.demo_data, match_id = match_id)

        logger.debug("Getting roster ids for the match")
        rosters_ids = vp.get_roster_ids(match = match)
        logger.debug("Roster ids: {0}".format(rosters_ids))

        logger.debug("Getting rosters for the match")
        rosters = vp.get_rosters(roster_ids = rosters_ids, data = vd.demo_data)
        for item in rosters:
            logger.debug(item)

        logger.debug("Making roster df")
        roster_df_list = [pd.DataFrame.from_dict(item['attributes']['stats'], orient='index') for item in rosters]
        roster_df = pd.concat(roster_df_list, axis=1).transpose()

        logger.debug(roster_df)

        return(
        vt.html_df_table(df = roster_df, max_rows = 10)
        # html.Table(
        # # Header
        # [html.Tr([html.Th(col) for col in roster_df.columns])] +
        #
        # # Body
        # [html.Tr([
        #     html.Td(roster_df.iloc[i][col]) for col in roster_df.columns
        # ]) for i in range(min(len(roster_df), max_rows))]
        # )
    )
    else:
        return('No match selected')

@app.callback(
    Output(component_id = 'global-data', component_property = 'children'),
    [Input(component_id = 'selected-api-match-id', component_property = 'value')]
)
def set_api_match(input_value):
    '''
    Set the API match object based on the selected match
    '''
    logger.debug("Setting global match from selected-api-match-id value: {0}".format(input_value))
    if input_value != None:
        match_id = input_value
        logger.debug("Match id: {0}".format(match_id))

        logger.debug("Retreiving specified match from data set")
        vd.match = vp.get_glmatch(data = vd.matches, match_id = match_id)
    return()

@app.callback(
    Output(component_id = 'api-roster-table', component_property = 'children'),
    [Input(component_id = 'selected-api-match-id', component_property = 'value')]
)
def update_api_roster_table(input_value, max_rows=10):
    logger.debug("Updating selected-api-match-id value: {0}".format(input_value))
    if hasattr(vd, 'match'):
        logger.debug("Making roster df")
        roster_df_list = [pd.DataFrame.from_dict(item.stats, orient='index') for item in vd.match.rosters]
        roster_df = pd.concat(roster_df_list, axis=1).transpose()

        logger.debug(roster_df)

        return(vt.html_df_table(df = roster_df, max_rows = 10))
    else:
        return('No match selected')


if __name__ == '__main__':
    app.run_server()
