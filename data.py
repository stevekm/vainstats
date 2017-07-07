#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Set up data to use in the app
Functions for manipulating the app data
'''
import tools as vt
import parse as vp
import gamelocker

import logging
logger = logging.getLogger("data")

# ~~~~~ DATA SETUP ~~~~~ #
# initial datasets for the app
# demo data
logger.debug("Loading demo data")
demo_data = vt.load_json(input_file = "demo-data.txt")
demo_matches = [x['id'] for x in demo_data['data']]

# API data
logger.debug("Reading API key from file")
key = vt.get_api_key(keyfile = "key.txt")
logger.debug("Querying API for game data")
api = gamelocker.Gamelocker(key).Vainglory()
matches = api.matches({"page[limit]": 5}) #  "filter[playerNames]": "TheLegend27"

api_matches = [x.id for x in matches]

# ~~~~~ DATA FUNCTIONS ~~~~~ #
