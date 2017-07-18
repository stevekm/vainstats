#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Layout for the offline demo data for the app
'''
# dash modules
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import plotly.graph_objs as go
import plotly.plotly as py
import pandas as pd

import tools as vt
import offline_data as vod

# Demo data section
offline_div = html.Div([
    # first sub-sub-div
    html.Div([
        html.H2(children = 'Pick a Match from the demo list:'),

        html.Div(children = [
        # dropdown menu for the demo matches
        vt.match_dropdown(matches = vod.demo_matches, id = 'demo-match-selection', default_value = 'first')
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
        ]),
], id = 'demo-div',
style = {'width': '48%', 'display': 'inline-block'})
