#!/usr/bin/env python
'''
This script will retrieve player data from the Vainglory game API
'''
# ~~~~~~ LOAD PACKAGES ~~~~~ #
import requests
import json
import argparse
import sys

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

def get_match_data(username, key, match_url):
    '''
    Get data from a game match
    '''
    header = {
        "Authorization": key,
        "X-TITLE-ID": "semc-vainglory",
        # "Accept": "application/vnd.api+json"
        "Accept": "application/json"
    }
    query = {
        "filter[playerNames]": username
        # "page[limit]": "3"
    }
    match = requests.get(match_url, headers=header) #, params=query)
    dat = json.loads(match.content)
    with open('data.txt', 'w') as outfile:
        json.dump(dat['data'], outfile, indent=4, sort_keys=True)
    with open('included.txt', 'w') as outfile:
        json.dump(dat['included'], outfile, indent=4, sort_keys=True)
    my_debugger(locals().copy())
    for item in dat['included']: print(item); print("")
    dat['data'][0]['attributes']

def get_query(username, key, region, query_type = "match", *args, **kwargs):
    '''
    Get a query from the Vainglory game API
    '''
    url_base = "https://api.dc01.gamelockerapp.com/shards"
    region_url = '/'.join([url_base, region])
    if query_type == "match":
        match_url = '/'.join([region_url, "matches"])
        get_match_data(username = username, key = key, match_url = match_url)
    elif query_type == "player":
        player_url = '/'.join([region_url, "players"])

# ~~~~ GET SCRIPT ARGS ~~~~~~ #
parser = argparse.ArgumentParser(description='Vainglory Player Match Stats')
# required flags
parser.add_argument("-u",  type = str, dest = 'username', metavar = 'username', help="Player's in-game username")

# optional flags
parser.add_argument("-k", default = 'key.txt', type = str, dest = 'api_key_file', metavar = 'api_key_file', help="Path to text file containing the player's API key. (get one here: https://developer.vainglorygame.com/)")
parser.add_argument("-r", default = 'na', type = str, dest = 'region', metavar = 'region', help="Player's region. Possibilties: na, eu, sa, ea, or sg. Details here: https://developer.vainglorygame.com/docs?python#regions")

args = parser.parse_args()

username = args.username
api_key_file = args.api_key_file
region = args.region

if __name__ == "__main__":
    print('Player name: {}'.format(username))
    print('Region: {}'.format(get_region_name(region = region)))
    key = get_api_key(api_key_file)
    print("Retrieving player data...")
    get_query(region = region, key = key, username = username)
    #
