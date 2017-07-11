#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Dash app for the vainstats API querying and player ranking
'''

# ~~~~~ LOGGING SETUP ~~~~~ #
# set up the first logger for the app
import os
import log as vlog
# path to the current script's dir
scriptdir = os.path.dirname(os.path.realpath(__file__))

def logpath():
    '''
    Return the path to the main log file; needed by the logging.yml
    use this for dynamic output log file paths & names
    '''
    global scriptdir
    return(vlog.logpath(scriptdir = scriptdir, logfile = 'log.txt'))

config_yaml = os.path.join(scriptdir,'logging.yml')
logger = vlog.log_setup(config_yaml = config_yaml, logger_name = "app")
logger.debug("App is starting...")


# ~~~~~ LIBRARIES ~~~~~ #
# system modules
import sys
import gamelocker

# dash modules
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.plotly as py
# import plotly.offline
import pandas as pd

# app modules
import tools as vt
import parse as vp
import data as vd


# ~~~~ SETUP ~~~~~~ #
app = dash.Dash()


# ~~~~ APP UI ~~~~~~ #
# main div
app.layout = html.Div([
    # main heading
    html.H1(children = 'Welcome to vainstats - VainGlory game match stats & player ranking!'),
    # first sub-div
    html.Div([
        # first sub-sub-div
        html.Div([
            html.H2(children = 'Pick a Match from the demo list:'),
            dcc.Dropdown(
                id = 'dict-key',
                options = [{'label': '{0}: {1}'.format(i + 1, match), 'value': match} for i, match in enumerate(vd.demo_matches)],
                value = vd.demo_matches[0]
            ),
            # dcc.RadioItems(
            #     id='plot-type',
            #     options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
            #     value='Linear',
            #     labelStyle={'display': 'inline-block'}
            # )
            dcc.RadioItems(id='plot-type'),
            ],
        style = {'width': '48%', 'display': 'inline-block'}
        ),
    ]),

    # second sub-div
    html.H4(children='Match Stats'),
    html.Div(id = 'roster-table'),
    html.Div([
        dcc.Graph(id='demo-roster-gold-plot'),
    ]),

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
def make_demo_roster_df(match_id):
    '''
    Return a df for the roster of a given match
    '''
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
    return(roster_df)

def make_api_roster_df(match_id):
    '''
    Return a df for the roster of an API quieried match
    '''
    logger.debug("Match id: {0}".format(match_id))
    logger.debug("Retreiving specified match from data set")
    match = vp.get_glmatch(data = vd.matches, match_id = match_id)
    logger.debug("Making roster df")
    roster_df_list = [pd.DataFrame.from_dict(item.stats, orient='index') for item in match.rosters]
    roster_df = pd.concat(roster_df_list, axis=1).transpose()
    logger.debug(roster_df)
    return(roster_df)

@app.callback(
    Output(component_id = 'roster-table', component_property = 'children'),
    [Input(component_id = 'dict-key', component_property = 'value')]
)
def update_roster_table(input_value):
    logger.debug("Updating input value: {0}".format(input_value))
    if input_value != None:
        match_id = input_value
        roster_df = make_demo_roster_df(match_id = match_id)
        return(vt.html_df_table(df = roster_df))
    else:
        return('No match selected')

@app.callback(
    dash.dependencies.Output('plot-type', 'options'),
    [dash.dependencies.Input('dict-key', 'value')])
def set_demo_plot_options(input_value):
    match_id = input_value
    roster_df = make_demo_roster_df(match_id = match_id)
    plot_types = [c for c in roster_df.columns if c != 'side']
    return [{'label': i, 'value': i} for i in plot_types]

@app.callback(
    dash.dependencies.Output('plot-type', 'value'),
    [dash.dependencies.Input('dict-key', 'value')])
def set_demo_plot_value(input_value):
    match_id = input_value
    roster_df = make_demo_roster_df(match_id = match_id)
    plot_types = [c for c in roster_df.columns if c != 'side']
    return(plot_types[0])

@app.callback(
    Output(component_id = 'demo-roster-gold-plot', component_property = 'figure'),
    [Input(component_id = 'dict-key', component_property = 'value'),
    Input(component_id = 'plot-type', component_property = 'value')]
)
def update_demo_roster_gold_plot(input_value, plot_type):
    logger.debug("Updating input value: {0}".format(input_value))
    if input_value != None:
        match_id = input_value
        roster_df = make_demo_roster_df(match_id = match_id)
        return({
        'data': [go.Bar(x = roster_df['side'], y = roster_df[plot_type])]
        })
    else:
        return('No match selected')



@app.callback(
    Output(component_id = 'api-roster-table', component_property = 'children'),
    [Input(component_id = 'selected-api-match-id', component_property = 'value')]
)
def update_api_roster_table(input_value):
    if input_value != None:
        logger.debug("Updating selected-api-match-id value: {0}".format(input_value))
        match_id = input_value
        roster_df = make_api_roster_df(match_id = match_id)
        return(vt.html_df_table(df = roster_df))
    else:
        return('No match selected')


if __name__ == '__main__':
    app.run_server()
