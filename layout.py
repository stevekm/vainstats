#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Layouts for the main portion of the app using API data
'''
# dash modules
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import plotly.graph_objs as go
import plotly.plotly as py
import pandas as pd

# main heading
heading = [
html.H1(children = 'Welcome to vainstats - VainGlory game match stats & player ranking!'),
html.Div(id = 'null-div') # for empty returns in the app
]
