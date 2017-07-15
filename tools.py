#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
General utility functions to use in the app
and functions for generating app components
'''
import logging
logger = logging.getLogger("tools")

# dash modules
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.plotly as py
import pandas as pd



# ~~~~~ MISC ~~~~~ #
def my_debugger(vars):
    '''
    Starts interactive Python terminal at location in script
    call with
    my_debugger(globals().copy())
    anywhere in your script
    or call
    my_debugger(locals().copy())
    from anywhere within this package
    '''
    import readline # optional, will allow Up/Down/History in the console
    import code
    # vars = globals().copy() # in python "global" variables are actually module-level
    vars.update(locals())
    shell = code.InteractiveConsole(vars)
    shell.interact()


def save_pydata(data, outfile):
    # save py data in pickle format
    # USAGE: save_pydata(python_object, "my_file.pickle")
    import pickle
    with open(outfile, 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        logger.debug("Saving data to pickle, file is: {0}".format(outfile))
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        logger.debug("Data saved to pickle successfully")

def load_pydata(infile):
    # open py pickle data
    import pickle
    with open(infile, 'rb') as f:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        data = pickle.load(f)
    return(data)

def load_json(input_file):
    '''
    Load JSON from a file
    '''
    import json
    logger.debug("Loading data from JSON")
    with open(input_file,"r") as f:
        my_item = json.load(f)
    return(my_item)

def get_api_key(keyfile = "api_keys/key.txt"):
    '''
    Extract the API key string from the first line of the give text file
    '''
    with open(keyfile, "r") as f:
        keys = []
        for line in f:
            keys.append(line.strip())
    return(keys[0])


# ~~~~~ DEMO JSON DATA ~~~~~ #
def get_match(data, match_id):
    '''
    Search a payload for a specific match
    '''
    logger.debug('Searching for match_id in data')
    for item in data['data']:
        if item['id'] == match_id:
            return(item)

def get_roster_ids(match):
    '''
    Get the roster IDs from a match list of dicts
    '''
    logger.debug('Searching for roster_ids in match')
    roster_ids = []
    for item in match['relationships']['rosters']['data']:
        if item['type'] == 'roster':
            roster_ids.append(item['id'])
    return(roster_ids)

def get_rosters(roster_ids, data):
    '''
    Get the team rosters for a match
    '''
    logger.debug('Searching for rosters in data')
    rosters = []
    # for item in match['relationships']['rosters']['data']:
    for item in data['included']:
        for id in roster_ids:
            if item['type'] == 'roster':
                if item['id'] == id:
                    rosters.append(item)
    return(rosters)


# ~~~~~ API PAYLOAD DATA ~~~~~ #
def get_glmatch(data, match_id):
    '''
    Find the matching gamelocker match
    '''
    logger.debug('Searching for match_id in data')
    for item in data:
        if item.id == match_id:
            return(item)

def glparticipant_dict(participant, roster_id):
    '''
    Make a big dict out of the participant entry from a match
    '''
    d = {**participant.stats,
    **{'id': participant.id},
    **{'hero': participant.actor},
    **participant.player.stats,
    **{'roster_id': roster_id}}
    return(d)

def make_glparticipant_stats_df(match):
    '''
    Make a df with the player and participant stats
    '''
    roster_df_list = [pd.DataFrame.from_dict({**roster.stats, **{'roster_id': roster.id}}, orient='index') for roster in match.rosters]
    roster_df = pd.concat(roster_df_list, axis=1).transpose()
    #
    participant_stats_df_list = [[pd.DataFrame.from_dict(glparticipant_dict(participant = participant, roster_id = roster.id), orient='index') for participant in roster.participants] for roster in match.rosters]
    participant_stats_df = pd.concat([pd.concat(df_list, axis=1).transpose() for df_list in participant_stats_df_list])
    #
    participant_stats_df_merge = pd.merge(participant_stats_df, roster_df[['roster_id', 'side']], on='roster_id')
    return(participant_stats_df_merge)



# ~~~~~ APP COMPONENTS ~~~~~ #
def html_df_table(df, max_rows = 10):
    '''
    Return HTML table to display on the app webpage
    '''
    return(
    html.Table(
    # Header
    [html.Tr([html.Th(col) for col in df.columns])] +

    # Body
    [html.Tr([
        html.Td(df.iloc[i][col]) for col in df.columns
    ]) for i in range(min(len(df), max_rows))]
    )
    )

def roster_df_plot(roster_df, plot_type):
    '''
    Returns a plot for a provided roster_df, where plot_type is a column names in the df that isn't 'side';
    example df:
    >>> roster_df
      acesEarned   gold heroKills krakenCaptures       side turretKills  \
    0          0  27699         2              0  right/red           0
    0          0  28608         8              0  left/blue           2

      turretsRemaining
    0                3
    0                5
    '''
    marker=dict(
        color=['rgba(204,204,204,1)', 'rgba(222,45,38,0.8)',
               'rgba(204,204,204,1)', 'rgba(204,204,204,1)',
               'rgba(204,204,204,1)'])
    color_key = {
    'right/red': 'red',
    'left/blue': 'blue'
    }
    colors = []
    for side in roster_df['side'].tolist():
        if side in color_key.keys():
            colors.append(color_key[side])
    if len(colors) == len(roster_df['side'].tolist()):
        return({
        'data': [go.Bar(x = roster_df['side'], y = roster_df[plot_type], marker = dict(color = colors))]
        })
    else:
        return({
        'data': [go.Bar(x = roster_df['side'], y = roster_df[plot_type])]
        })

def match_dropdown(matches, id, default_value = 'first'):
    '''
    Return a dropdown menu object based on the supplied matches
    '''
    if default_value == 'first':
        return(dcc.Dropdown(
            id = id,
            options = [{'label': '{0}: {1}'.format(i + 1, match), 'value': match} for i, match in enumerate(matches)],
            value = matches[0]))
    elif default_value == 'last':
        return(dcc.Dropdown(
            id = id,
            options = [{'label': '{0}: {1}'.format(i + 1, match), 'value': match} for i, match in enumerate(matches)],
            value = matches[-1]))
    elif default_value == None:
        return(dcc.Dropdown(
            id = id,
            options = [{'label': '{0}: {1}'.format(i + 1, match), 'value': match} for i, match in enumerate(matches)]))
    else:
        return(dcc.Dropdown(
            id = id,
            options = [{'label': '{0}: {1}'.format(i + 1, match), 'value': match} for i, match in enumerate(matches)]))

def create_radio_buttons(options, id, value = None):
    '''
    Return a radio button component
    options = [{'label': i, 'value': i} for i in plot_types]
    '''
    if value != None:
        return(dcc.RadioItems(options = options, id = id, value = value))
    else:
        return(dcc.RadioItems(options = options, id = id))
