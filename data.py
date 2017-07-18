#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Set up data to use in the app
Functions for manipulating the app data
and functions that need direct access to the global data objects
'''
import logging
logger = logging.getLogger("data")

# dash modules
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.plotly as py
import pandas as pd

# app modules
import tools as vt
import gamelocker

# ~~~~~ DATA SETUP ~~~~~ #
# API data
logger.debug("Reading API key from file")
key = vt.get_api_key(keyfile = "key.txt")
logger.debug("Querying API for game data")
api = gamelocker.Gamelocker(key).Vainglory()
matches = api.matches({"page[limit]": 5}) #  "filter[playerNames]": "TheLegend27"

# placeholder for the roster df
roster_df = None

# vt.save_pydata(data = matches, outfile = "matches.pickle")

api_matches = [x.id for x in matches]

# ~~~~~ DATA FUNCTIONS ~~~~~ #
def make_api_roster_df(match_id):
    '''
    Return a df for the roster of an API quieried match
    '''
    global matches
    logger.debug("Match id: {0}".format(match_id))
    logger.debug("Retreiving specified match from data set")
    match = vt.get_glmatch(data = matches, match_id = match_id)
    logger.debug("Making roster df")
    roster_df_list = [pd.DataFrame.from_dict(item.stats, orient='index') for item in match.rosters]
    roster_df = pd.concat(roster_df_list, axis=1).transpose()
    logger.debug(roster_df)
    return(roster_df)
