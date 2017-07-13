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
from dash.dependencies import Input, Output, State, Event
import plotly.graph_objs as go
import plotly.plotly as py
import pandas as pd

# app modules
import tools as vt
import parse as vp
import data as vd


# ~~~~ APP SETUP ~~~~~~ #
app = dash.Dash()


# ~~~~ APP UI ~~~~~~ #
# main div
app.layout = html.Div([
    # main heading
    html.H1(children = 'Welcome to vainstats - VainGlory game match stats & player ranking!'),
    html.Div(id = 'null-div'), # for empty returns in the app
    # Demo data section
    html.Div([
        # first sub-sub-div
        html.Div([
            html.H2(children = 'Pick a Match from the demo list:'),

            # dropdown menu for the demo matches
            html.Div(children = [
            vt.match_dropdown(matches = vd.demo_matches, id = 'demo-match-selection')
            ], id = 'demo-match-selection-div'),

            html.H2(children = 'Roster Plot'),
            html.H3(children = 'Pick a Plot type:'),
            dcc.RadioItems(id='demo-plot-type'),
            ],
        style = {'width': '48%', 'display': 'inline-block'}
        ),

        # second sub-div
        html.H4(children='Match Roster Stats'),
        html.Div(id = 'demo-roster-table'),
        html.Div([
            dcc.Graph(id='demo-roster-gold-plot'),
        ]),
    ]),

    # API data section
    html.Div([
        # first sub-sub-div
        html.Div([
            html.H2(children = 'API Queried Matches:'),

            # dropdown menu for the API matches
            html.Div(children = [
            vt.match_dropdown(matches = vd.api_matches, id = 'api-match-selection')
            ],
            id = 'api-match-selection-div'),


            html.Button('Get New Matches', id='api-match-update-matches-button'),
            html.H2(children = 'Roster Plot'),
            html.H3(children = 'Pick a Plot type:'),
            dcc.RadioItems(id='api-plot-type'),
            ],
        style = {'width': '48%', 'display': 'inline-block'}
        ),

        html.H4(children='Match Roster Stats'),
        html.Div(id = 'api-roster-table'),
        html.Div([
            dcc.Graph(id='api-roster-plot'),
        ]),
    ])
])



# ~~~~ APP SERVER ~~~~~~ #

# demo data
@app.callback(
    Output(component_id = 'demo-roster-table', component_property = 'children'),
    [Input(component_id = 'demo-match-selection', component_property = 'value')]
)
def update_roster_table(input_value):
    logger.debug("Updating input value: {0}".format(input_value))
    if input_value != None:
        match_id = input_value
        roster_df = vd.make_demo_roster_df(match_id = match_id)
        return(vt.html_df_table(df = roster_df))
    else:
        return('No match selected')

@app.callback(
    dash.dependencies.Output('demo-plot-type', 'options'),
    [dash.dependencies.Input('demo-match-selection', 'value')])
def set_demo_plot_options(input_value):
    match_id = input_value
    roster_df = vd.make_demo_roster_df(match_id = match_id)
    plot_types = [c for c in roster_df.columns if c != 'side']
    return [{'label': i, 'value': i} for i in plot_types]

@app.callback(
    dash.dependencies.Output('demo-plot-type', 'value'),
    [dash.dependencies.Input('demo-match-selection', 'value')])
def set_demo_plot_value(input_value):
    match_id = input_value
    roster_df = vd.make_demo_roster_df(match_id = match_id)
    plot_types = [c for c in roster_df.columns if c != 'side']
    return(plot_types[0])

@app.callback(
    Output(component_id = 'demo-roster-gold-plot', component_property = 'figure'),
    [Input(component_id = 'demo-match-selection', component_property = 'value'),
    Input(component_id = 'demo-plot-type', component_property = 'value')]
)
def update_demo_roster_gold_plot(input_value, plot_type):
    logger.debug("Updating input value: {0}".format(input_value))
    if input_value != None:
        match_id = input_value
        roster_df = vd.make_demo_roster_df(match_id = match_id)
        return(vt.roster_df_plot(roster_df = roster_df, plot_type = plot_type))
    else:
        return('No match selected')


# api data
@app.callback(
    Output(component_id = 'api-roster-table', component_property = 'children'),
    [Input(component_id = 'api-match-selection', component_property = 'value')]
)
def update_api_roster_table(match_id):
    if match_id != None:
        logger.debug("Updating selected-api-match-id value: {0}".format(match_id))
        roster_df = vd.make_api_roster_df(match_id = match_id)
        return(vt.html_df_table(df = roster_df))
    else:
        return('No match selected')

@app.callback(
    Output(component_id = 'api-plot-type', component_property = 'options'),
    [Input(component_id = 'api-match-selection', component_property = 'value')])
def set_demo_plot_options(match_id):
    roster_df = vd.make_api_roster_df(match_id = match_id)
    plot_types = [c for c in roster_df.columns if c != 'side']
    return [{'label': i, 'value': i} for i in plot_types]

@app.callback(
    Output(component_id = 'api-plot-type', component_property = 'value'),
    [Input(component_id = 'api-match-selection', component_property = 'value')])
def set_demo_plot_value(match_id):
    roster_df = vd.make_api_roster_df(match_id = match_id)
    plot_types = [c for c in roster_df.columns if c != 'side']
    return(plot_types[0])

@app.callback(
    Output(component_id = 'api-roster-plot', component_property = 'figure'),
    [Input(component_id = 'api-match-selection', component_property = 'value'),
    Input(component_id = 'api-plot-type', component_property = 'value')]
)
def update_demo_roster_gold_plot(match_id, plot_type):
    logger.debug("Updating input value: {0}".format(match_id))
    if match_id != None:
        roster_df = vd.make_api_roster_df(match_id = match_id)
        return(vt.roster_df_plot(roster_df = roster_df, plot_type = plot_type))
    else:
        return('No match selected')


@app.callback(
    Output(component_id = 'api-match-selection-div', component_property = 'children'),
    events = [Event('api-match-update-matches-button', 'click')])
def update_data():
    '''
    Update the matches that have been queried from the API
    Rebuild the dropdown selection menu div
    NOTE: click events might break with future Dash updates
    '''
    logger.debug("Querying the API for new matches;")
    logger.debug("old matches:\n{0}".format(vd.api_matches))
    vd.matches = vd.api.matches({"page[limit]": 5}) #  "filter[playerNames]": "TheLegend27"
    vd.api_matches = [x.id for x in vd.matches]
    logger.debug("new matches:\n{0}".format(vd.api_matches))
    return(vt.match_dropdown(matches = vd.api_matches, id = 'api-match-selection'))


if __name__ == '__main__':
    app.run_server()
