#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Functions for parsing payload data
'''
import logging
logger = logging.getLogger("parse")

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


def get_glmatch(data, match_id):
    '''
    Find the matching gamelocker match
    '''
    logger.debug('Searching for match_id in data')
    for item in data:
        if item.id == match_id:
            return(item)
