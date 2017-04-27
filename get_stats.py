#!/usr/bin/env python
'''
This script will retrieve player data from the Vainglory game API
'''
# ~~~~~~ LOAD PACKAGES ~~~~~ #
import requests
import json
import argparse
import sys
from datetime import datetime, timedelta

# ~~~~ CUSTOM FUNCTIONS ~~~~~~ #
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

def json_dump(data, output_file):
    '''
    Write JSON data to a file
    '''
    with open(output_file, 'w') as o:
        json.dump(data, o, indent=4, sort_keys=True)

def print_div(message = ''):
    '''
    Print a message with a divider
    '''
    divider = '------------------'
    print('{0}\n{1}'.format(divider, message))


def get_api_key(keyfile = "api_keys/key.txt"):
    '''
    Extract the API key string from the first line of the give text file
    '''
    with open(keyfile, "r") as f:
        keys = []
        for line in f:
            keys.append(line.strip())
    return(keys[0])

def get_region_name(region):
    '''
    Return the full region name from the given abbreviation
    '''
    region_dict = {
    'na': 'North America',
    'eu': 'Europe',
    'sa': 'South America',
    'ea': 'East Asia',
    'sg': 'Southeast Asia (SEA)'
    }
    if region in region_dict.keys():
        return(region_dict[region])
    else:
        print("ERROR: Region '{}' is not recognized. Available regions are:".format(region))
        for key, value in region_dict.iteritems():
            print('{}: {}'.format(key, value))
        print("Exiting...")
        sys.exit()

def print_match(match):
    '''
    Print out information from a match item
    '''
    # my_debugger(locals().copy())
    # if match['type'] != 'match':
        # sys.exit()
    match_gameMode = match['attributes']['gameMode']
    match_id = match['id']
    match_createdAt = match['attributes']['createdAt']
    match_endGameReason = match['attributes']['stats']['endGameReason']
    match_duration = match['attributes']['duration']
    print_div(message = "Found match")
    print('id: {0}'.format(match_id))
    print('outcome: {0}'.format(match_endGameReason))
    print('type: {0}'.format(match_gameMode))
    print('date: {0}'.format(match_createdAt))
    print('duration: {0}'.format(match_duration))
    print("")

def print_dict_source(dict_name, dict_obj):
    '''
    Print a dictionary to the console in copy/pasteable code format
    '''
    print('{0} = {1}'.format(dict_name, json.dumps(dict_obj, sort_keys=True, indent=0)))

def print_str_source(str_name, str_obj, quote = True):
    '''
    Print a dictionary to the console in copy/pasteable code format
    '''
    if quote == False:
        print('{0} = {1}'.format(str_name, str_obj))
    elif quote == True:
        print('{0} = "{1}"'.format(str_name, str_obj))

def print_debug_query(header, query, match_url):
    '''
    Print the query commands to console in an easy copy/paste format for debugging
    '''
    print_div(message = "Query Commands:\n")
    print_dict_source("header", header)
    print_dict_source("query", query)
    print_str_source("match_url", match_url)
    print('import requests')
    print_str_source("match", 'requests.get(match_url, headers=header, params=query)', quote = False)
    print_div()

def get_match_data(username, key, match_url, match_ID, days_to_subtract, debug_mode):
    '''
    Get data from a game match
    '''
    search_time = (datetime.today() - timedelta(days=days_to_subtract)).replace(microsecond=0).isoformat()
    search_time = str(search_time + "Z")
    print("Match ID is: {0}".format(match_ID))
    print("search time is: {0}".format(search_time))
    header = {
        "Authorization": key,
        "X-TITLE-ID": "semc-vainglory",
        "Accept": "application/vnd.api+json"
    }
    query = {
        "sort": "-createdAt", # sort most -> lease recent
        "filter[createdAt-start]": search_time, # "2017-02-28T13:25:30Z",
        "page[limit]": "5"
    }
    if username != None:
        query["filter[playerNames]"] = username
    if debug_mode == True:
        print_debug_query(header, query, match_url)
    # sys.exit()
    match = requests.get(match_url, headers=header, params=query)
    dat = json.loads(match.content)
    # my_debugger(locals().copy())
    if match_ID == None:
        # my_debugger(locals().copy())
        for item in dat['data']:
            print_match(item)
    elif match_ID != None:
        print_match(dat['data'])

def build_match_url(region, match_ID):
    '''
    Build the URL to submit to the API match query
    '''
    url_base = "https://api.dc01.gamelockerapp.com/shards"
    region_url = '/'.join([url_base, region])
    match_url = '/'.join([region_url, "matches"])
    if match_ID != None:
        match_url = '/'.join([match_url, match_ID])
    return(match_url)

# ~~~~ GET SCRIPT ARGS ~~~~~~ #
parser = argparse.ArgumentParser(description='Vainglory Player Match Stats')
# required flags

# optional flags
parser.add_argument("-n", default = None, type = str,  dest = 'name', metavar = 'name', help="Player's in-game username")
parser.add_argument("-d", default = 0, type = int,  dest = 'days', metavar = 'days', help="Number of past days in which to search for matches")
parser.add_argument("-m", default = None, type = str, dest = 'match', metavar = 'match', help="Match ID to look up")
parser.add_argument("-k", default = 'key.txt', type = str, dest = 'api_key_file', metavar = 'api_key_file', help="Path to text file containing the player's API key. (get one here: https://developer.vainglorygame.com/)")
parser.add_argument("-r", default = 'na', type = str, dest = 'region', metavar = 'region', help="Player's region. Possibilties: na, eu, sa, ea, or sg. Details here: https://developer.vainglorygame.com/docs?python#regions")
parser.add_argument("--debug", default = False, action='store_true', dest = 'debug_mode', help="Print the query command")

args = parser.parse_args()

username = args.name
api_key_file = args.api_key_file
region = args.region
match_ID = args.match
days = args.days
debug_mode = args.debug_mode

if __name__ == "__main__":
    print('Player name: {}'.format(username))
    print('Region: {}'.format(get_region_name(region = region)))
    key = get_api_key(api_key_file)
    print("Retrieving player data...")
    match_url = build_match_url(region, match_ID)
    get_match_data(username = username, key = key, match_url = match_url, match_ID = match_ID, days_to_subtract = days, debug_mode = debug_mode)
    # my_debugger(globals().copy())
