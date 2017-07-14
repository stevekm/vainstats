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

            html.Div(children = [
            # dropdown menu for the demo matches
            vt.match_dropdown(matches = vd.demo_matches, id = 'demo-match-selection', default_value = 'first')
            ], id = 'demo-match-selection-div'),

            html.H2(children = 'Roster Plot'),
            html.H3(children = 'Pick a Plot type:'),
            # dcc.RadioItems(id = 'demo-plot-type'),
            html.Div(children = [
            dcc.RadioItems(id='demo-plot-type')
            ],
            id = 'demo-plot-type-div'),

            html.H4(children = 'Match Roster Stats'),
            html.Div(id = 'demo-roster-table'),
            html.Div(children = [
                dcc.Graph(id = 'demo-roster-gold-plot'),
            ])
            ], style = {'width': '48%', 'display': 'inline-block'}),
    ]),


    # API data section
    html.Div(children = [
        # first sub-sub-div
        html.Div(children = [
            html.H2(children = 'API Queried Matches:'),

            html.Div(children = [
            # dropdown menu for the API matches
            vt.match_dropdown(matches = vd.api_matches, id = 'api-match-selection')
            ],
            id = 'api-match-selection-div'),


            html.Button('Get New Matches', id='api-match-update-matches-button'),
            html.H2(children = 'Roster Plot'),
            html.H3(children = 'Pick a Plot type:'),

            # buttons to choose plot data
            html.Div(children = [
            dcc.RadioItems(id='api-roster-plot-data-type-selection')
            ],
            id = 'api-roster-plot-data-div'),

            html.H4(children = 'Match Roster Stats'),
            html.Div(id = 'api-roster-table'),
            html.Div([
                dcc.Graph(id = 'api-roster-plot'),
            ])
            ], style = {'width': '48%', 'display': 'inline-block'})
    ])
])



# ~~~~ APP SERVER ~~~~~~ #


def create_radio_buttons(options, id, value = None):
    '''
    Return a radio button component
    options = [{'label': i, 'value': i} for i in plot_types]
    '''
    if value != None:
        return(dcc.RadioItems(options = options, id = id, value = value))
    else:
        return(dcc.RadioItems(options = options, id = id))


# demo data
@app.callback(
    Output(component_id = 'demo-roster-table', component_property = 'children'),
    [Input(component_id = 'demo-match-selection', component_property = 'value')]
)
def update_roster_table(input_value):
    logger.debug("Updating input value: {0}".format(input_value))
    # if vd.demo_roster_df == None:
    #     return('No match selected')
    # else:
    if input_value != None:
        match_id = input_value
        vd.demo_roster_df = vd.make_demo_roster_df(match_id = match_id)
        return(vt.html_df_table(df = vd.demo_roster_df))
    else:
        return('No match selected')

@app.callback(
    Output(component_id = 'demo-plot-type-div', component_property = 'children'),
    [Input(component_id = 'demo-match-selection', component_property = 'value')])
def update_demo_roster_plot_options(match_id):
    '''
    Rebuild the radio button component for the roster plot based on selected match
    '''
    logger.debug("Rebuilding radio buttons for plot selection for match: {0}".format(match_id))
    # if vd.demo_roster_df == None:
    #     return('No match selected')
    # else:
    vd.demo_roster_df = vd.make_demo_roster_df(match_id = match_id)
    plot_types = [c for c in vd.demo_roster_df.columns if c != 'side']
    logger.debug("plot_types are: {0}".format(plot_types))

    plot_type_options = [{'label': i, 'value': i} for i in plot_types]
    selected_plot_type = plot_types[-1] # last item, usually has values

    logger.debug("selected_plot_type is: {0}".format(selected_plot_type))
    return(create_radio_buttons(options = plot_type_options, id = 'demo-plot-type', value = selected_plot_type))

@app.callback(
    Output(component_id = 'demo-roster-gold-plot', component_property = 'figure'),
    [Input(component_id = 'demo-match-selection', component_property = 'value'),
    Input(component_id = 'demo-plot-type', component_property = 'value')]
)
def update_demo_roster_gold_plot(input_value, plot_type):
    logger.debug("Updating input value: {0}".format(input_value))
    # if vd.demo_roster_df == None:
    #     return('No match selected')
    # else:
    if input_value != None:
        match_id = input_value
        vd.demo_roster_df = vd.make_demo_roster_df(match_id = match_id)
        return(vt.roster_df_plot(roster_df = vd.demo_roster_df, plot_type = plot_type))
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
    Output(component_id = 'api-roster-plot-data-div', component_property = 'children'),
    [Input(component_id = 'api-match-selection', component_property = 'value')])
def update_api_roster_plot_options(match_id):
    '''
    Rebuild the radio button component for the roster plot based on selected match
    '''
    logger.debug("Rebuilding radio buttons for plot selection for match: {0}".format(match_id))
    roster_df = vd.make_api_roster_df(match_id = match_id)

    plot_types = [c for c in roster_df.columns if c != 'side']
    logger.debug("plot_types are: {0}".format(plot_types))

    plot_type_options = [{'label': i, 'value': i} for i in plot_types]
    selected_plot_type = plot_types[-1] # last item, usually has values

    logger.debug("selected_plot_type is: {0}".format(selected_plot_type))
    return(create_radio_buttons(options = plot_type_options, id = 'api-roster-plot-data-type-selection', value = selected_plot_type))

@app.callback(
    Output(component_id = 'api-roster-plot', component_property = 'figure'),
    [Input(component_id = 'api-match-selection', component_property = 'value'),
    Input(component_id = 'api-roster-plot-data-type-selection', component_property = 'value')]
)
def update_api_roster_plot(match_id, plot_type):
    logger.debug("Updating input value for plot: {0}".format(match_id))
    if match_id != None:
        roster_df = vd.make_api_roster_df(match_id = match_id)
        return(vt.roster_df_plot(roster_df = roster_df, plot_type = plot_type))
    else:
        return('No match selected')


@app.callback(
    Output(component_id = 'api-match-selection-div', component_property = 'children'),
    events = [Event('api-match-update-matches-button', 'click')])
def update_api_data():
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
