#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Set up data to use in the app
'''
import tools as vt
import parse as vp
import gamelocker

import logging
logger = logging.getLogger(__name__)

logger.debug("Loading demo data")
demo_data = vt.load_json(input_file = "demo-data.txt")


logger.debug("Reading API key from file")
key = vt.get_api_key(keyfile = "key.txt")
logger.debug("Querying API for game data")
api = gamelocker.Gamelocker(key).Vainglory()
matches = api.matches({"page[limit]": 5}) #  "filter[playerNames]": "TheLegend27"

api_matches = [x.id for x in matches]
