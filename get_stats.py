#!/usr/bin/env python
'''
This script will retrieve player data from the Vainglory game API
'''
# ~~~~~~ LOAD PACKAGES ~~~~~ #
from __future__ import division
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

def mkdirs(path, return_path=False):
    '''
    Make a directory, and all parent dir's in the path
    '''
    import sys
    import os
    import errno
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
    if return_path:
        return path


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
        print("ERROR: Region '{0}' is not recognized. Available regions are:".format(region))
        for key, value in region_dict.iteritems():
            print('{0}: {1}'.format(key, value))
        print("Exiting...")
        sys.exit()

def print_match(match):
    '''
    Print out information from a match item
    '''
    import time
    # my_debugger(locals().copy())
    # if match['type'] != 'match':
        # sys.exit()
    match_gameMode = match['attributes']['gameMode']
    match_id = match['id']
    match_createdAt = match['attributes']['createdAt']
    match_endGameReason = match['attributes']['stats']['endGameReason']
    match_duration = match['attributes']['duration']
    match_duration = time.strftime("%M:%S", time.gmtime(match_duration))
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
    Print a string to the console in copy/pasteable code format
    '''
    if quote == False:
        print('{0} = {1}'.format(str_name, str_obj))
    elif quote == True:
        print('{0} = "{1}"'.format(str_name, str_obj))

def print_debug_query(header, query, match_url):
    '''
    Print the query commands to console in an easy copy/paste format for debugging
    '''
    print_div(message = "Query Commands for Debugging:\n")
    print_dict_source("header", header)
    print_dict_source("query", query)
    print_str_source("match_url", match_url)
    print('import requests')
    print('import json')
    print_str_source("match", 'requests.get(match_url, headers=header, params=query)', quote = False)
    print_str_source("dat", "json.loads(match.content)", quote = False)
    print_div()

def get_match_data(username, key, match_url, match_ID, days_to_subtract, page_limit, debug_mode, i_mode, harvest_mode, fail_mode):
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
        "page[limit]": page_limit
    }
    if username != None:
        query["filter[playerNames]"] = username
    if debug_mode == True:
        print_debug_query(header, query, match_url)
    match = requests.get(match_url, headers=header, params=query)
    # check for error code in API payload return
    match.raise_for_status()
    dat = json.loads(match.content)
    if i_mode == True:
        print_div()
        print('\n# Starting interactive session, you might want to run some of these:')
        print('\nfrom get_stats import *\n')
        print('import json\n')
        print('print(match_ID)\n')
        print("print(json.dumps(dat, indent=4, sort_keys=True))\n")
        print("for item in dat['included']: print(item['type'])\n")
        print("for item in dat['data']: print('{} {}'.format(item['type'], item['id']))\n")
        print_div()
        # scratchpad goes here....
        # for item in dat['included']: print(item.keys())
        # for item in dat['included']: print(item['type'])
        # for item in dat['included']: print('{}\t{}'.format(item['type'], item['id'])); print item.keys()
        # for item in dat['included']:
        #     if item['type'] == 'participant': print item
        # for n, item in enumerate(dat['included']):
        #     if item['type'] == 'participant': print(n); print(item.keys())
        # dat['included'][10]['attributes']['name']
        # dat['included'][9]['type']
        my_debugger(locals().copy())
    if match_ID == None:
        # my_debugger(locals().copy())
        for item in dat['data']:
            print_match(item)
            save_match_data(item, harvest_mode = harvest_mode)
        for item in dat['included']:
            save_match_included(item, harvest_mode = harvest_mode)
    elif match_ID != None:
        print_match(dat['data'])
        save_match_data(dat['data'], harvest_mode = harvest_mode)
        save_match_included(dat['included'], harvest_mode = harvest_mode)
        user_data = refactor_included_assets(dat['included'])
        if fail_mode == True: fail_finder(user_data)


def save_match_included(included, harvest_mode, output_dir = "saved_matches"):
    '''
    Save the 'included' assets to a JSON
    '''
    import os
    if harvest_mode == True:
        mkdirs(output_dir)
        included_id = included['id']
        included_type = included['type']
        output_filename = os.path.join(output_dir, '{0}_{1}.json'.format(included_id, included_type))
        json_dump(included, output_filename)
        print('Saved included assets data to file:\n{0}\n'.format(output_filename))


def save_match_data(match, harvest_mode, output_dir = "saved_matches"):
    '''
    Saves a JSON file for the match data
    '''
    import os
    if harvest_mode == True:
        mkdirs(output_dir)
        match_id = match['id']
        output_filename = os.path.join(output_dir, match_id + '_data.json')
        json_dump(match, output_filename)
        print('Saved match data to file:\n{0}\n'.format(output_filename))

def print_player(player_obj):
    '''
    Print out formatted information about the player object
    '''
    player_region = player_obj['attributes']['shardId']
    player_name = player_obj['attributes']['name']
    player_wins = player_obj['attributes']['stats']['wins']
    player_played_rank = player_obj['attributes']['stats']['played_ranked']
    player_winstreak = player_obj['attributes']['stats']['winStreak']
    player_lossstreak = player_obj['attributes']['stats']['lossStreak']
    player_played = player_obj['attributes']['stats']['played']
    player_level = player_obj['attributes']['stats']['level']
    player_lifetimegold = player_obj['attributes']['stats']['lifetimeGold']
    player_xp = player_obj['attributes']['stats']['xp']
    player_id = player_obj['id']
    # print_div()
    # print(player_obj)
    print('player name: {0}'.format(player_name))
    print('player id: {0}'.format(player_id))
    print('player region: {0}'.format(player_region))
    print('player level: {0}'.format(player_level))
    print('player wins: {0}'.format(player_wins))
    print('player win streak: {0}'.format(player_winstreak))
    print('player loss streak: {0}'.format(player_lossstreak))
    print('played: {0}'.format(player_played))
    print('played rank: {0}'.format(player_played_rank))
    print('match xp: {0}'.format(player_xp))
    print('match lifetimegold: {0}'.format(player_lifetimegold))

def print_participant(participant_obj):
    '''
    Print out formatted information about a participant
    '''
    participant_id = participant_obj['relationships']['player']['data']['id']
    participant_gold = participant_obj['attributes']['stats']['gold']
    participant_deaths = participant_obj['attributes']['stats']['deaths']
    participant_nonJungleMinionKills = participant_obj['attributes']['stats']['nonJungleMinionKills']
    participant_skillTier = participant_obj['attributes']['stats']['skillTier']
    participant_turretCaptures = participant_obj['attributes']['stats']['turretCaptures']
    participant_winner = participant_obj['attributes']['stats']['winner']
    participant_karmaLevel = participant_obj['attributes']['stats']['karmaLevel']
    participant_jungleKills = participant_obj['attributes']['stats']['jungleKills']
    participant_kills = participant_obj['attributes']['stats']['kills']
    participant_farm = participant_obj['attributes']['stats']['farm']
    participant_firstAfkTime = participant_obj['attributes']['stats']['firstAfkTime']
    participant_assists = participant_obj['attributes']['stats']['assists']
    participant_minionKills = participant_obj['attributes']['stats']['minionKills']
    participant_level = participant_obj['attributes']['stats']['level']
    participant_items_list = participant_obj['attributes']['stats']['items']
    participant_skin = participant_obj['attributes']['stats']['skinKey']
    participant_krakenCaptures = participant_obj['attributes']['stats']['krakenCaptures']
    participant_goldMineCaptures = participant_obj['attributes']['stats']['goldMineCaptures']
    participant_crystalMineCaptures = participant_obj['attributes']['stats']['crystalMineCaptures']
    participant_wentAfk = participant_obj['attributes']['stats']['wentAfk']
    participant_hero = participant_obj['attributes']['actor']
    # print_div()
    # print('participant id: {0}'.format(participant_id)) # same as player ID
    print('player skillTier: {0}'.format(participant_skillTier))
    print('player karmaLevel: {0}'.format(participant_karmaLevel))
    print('match hero: {0}'.format(participant_hero))
    print('match skin: {0}'.format(participant_skin))
    print('match level: {0}'.format(participant_level))
    print('match kills/deaths/assists: {0}/{1}/{2}'.format(participant_kills, participant_deaths, participant_assists))
    print('match final gold: {0}'.format(participant_gold))
    print('match nonJungleMinionKills: {0}'.format(participant_nonJungleMinionKills))
    print('match turretCaptures: {0}'.format(participant_turretCaptures))
    print('match jungleKills: {0}'.format(participant_jungleKills))
    print('match farm: {0}'.format(participant_farm))
    print('match wentAfk: {0}'.format(participant_wentAfk))
    print('match firstAfkTime: {0}'.format(participant_firstAfkTime))
    print('match minionKills: {0}'.format(participant_minionKills))
    print('match krakenCaptures: {0}'.format(participant_krakenCaptures))
    print('match goldMineCaptures: {0}'.format(participant_goldMineCaptures))
    print('match crystalMineCaptures: {0}'.format(participant_crystalMineCaptures))
    print('match winner: {0}'.format(participant_winner))

    # print(participant_obj.keys())
    # print(participant_obj['attributes'])

def parse_players_participants(players_list, participants_list):
    '''
    '''
    from collections import defaultdict
    users = defaultdict(dict)

    for player in players_list:
        # print_player(player)
        player_id = player['id']
        users[player_id]['player'] = player
    for participant in participants_list:
        # print_participant(participant)
        participant_id = participant['relationships']['player']['data']['id']
        users[participant_id]['participant'] = participant
    for user_id in users.keys():
        print_div()
        print_div(message = "Player info")
        print_player(users[user_id]['player'])
        print_div(message = "Participant info")
        print_participant(users[user_id]['participant'])
    return(users)


def refactor_included_assets(match_included):
    '''
    Build a new dict from the API 'included' object, one entry per item ID
    '''
    players = []
    participants = []
    for item in match_included:
        item_type = item['type']
        item_id = item['id']
        if item_type == "player":
            players.append(item)
        if item_type == "participant":
            participants.append(item)
    user_data = parse_players_participants(players_list = players, participants_list = participants)
    return(user_data)


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


def fail_finder(user_data):
    '''
    Ranks players in a match based on included assets user data
    '''
    from collections import defaultdict
    rankings = defaultdict(lambda: defaultdict(float))
    print_div()
    print_div(message = "Player Match Ranking")
    for key, value in user_data.iteritems():
        # value['participant']['attributes']['stats']['itemUses']
        # value['participant']['attributes']['stats']['itemGrants']
        rankings[key]['hero'] = value['participant']['attributes']['actor']
        rankings[key]['name'] = value['player']['attributes']['name']
        rankings[key]['user-stats'] += value['player']['attributes']['stats']['level']
        rankings[key]['user-stats'] += value['player']['attributes']['stats']['wins'] / 100
        rankings[key]['user-stats'] += value['player']['attributes']['stats']['played_ranked'] / 75
        rankings[key]['user-stats'] += value['player']['attributes']['stats']['played'] / 100
        rankings[key]['user-stats'] += value['player']['attributes']['stats']['winStreak'] * 10
        rankings[key]['user-stats'] -= value['player']['attributes']['stats']['lossStreak'] * 10
        rankings[key]['match-stats'] += value['participant']['attributes']['stats']['karmaLevel'] * 10
        rankings[key]['match-stats'] += value['participant']['attributes']['stats']['skillTier'] * 10
        rankings[key]['match-stats'] += value['player']['attributes']['stats']['lifetimeGold'] / 1000
        rankings[key]['match-stats'] += value['player']['attributes']['stats']['xp'] / 100000
        # rankings[key]['match-stats'] -= value['participant']['attributes']['stats']['gold']
        rankings[key]['match-stats'] -= value['participant']['attributes']['stats']['gold'] / 10
        rankings[key]['match-stats'] -= value['participant']['attributes']['stats']['deaths']
        rankings[key]['match-stats'] += value['participant']['attributes']['stats']['kills']
        rankings[key]['match-stats'] += value['participant']['attributes']['stats']['turretCaptures'] * 3
        rankings[key]['match-stats'] += value['participant']['attributes']['stats']['jungleKills']
        rankings[key]['match-stats'] += value['participant']['attributes']['stats']['farm']
        rankings[key]['match-stats'] += value['participant']['attributes']['stats']['assists'] * 0.5
        rankings[key]['match-stats'] += value['participant']['attributes']['stats']['minionKills'] / 10
        rankings[key]['match-stats'] += value['participant']['attributes']['stats']['krakenCaptures'] * 5
        rankings[key]['match-stats'] += value['participant']['attributes']['stats']['goldMineCaptures'] * 3
        rankings[key]['match-stats'] += value['participant']['attributes']['stats']['crystalMineCaptures'] * 2
        if value['participant']['attributes']['stats']['winner'] == True:
            rankings[key]['match-stats'] += 10
        if value['participant']['attributes']['stats']['firstAfkTime'] > 0:
            rankings[key]['match-stats'] -= 50
        if value['participant']['attributes']['stats']['wentAfk'] != False:
            rankings[key]['match-stats'] -= 50
        rankings[key]['total'] = rankings[key]['match-stats'] + rankings[key]['user-stats']
    # my_debugger(locals().copy())
    for key, data in rankings.items():
        print('\t'.join([data['name'], data['hero'], str(data['total']), key]))


# ~~~~ GET SCRIPT ARGS ~~~~~~ #
parser = argparse.ArgumentParser(description='Vainglory Player Match Stats')
# required flags

# optional flags
parser.add_argument("-n", default = None, type = str,  dest = 'name', metavar = 'name', help="Player's in-game username")
parser.add_argument("-d", default = 1, type = int,  dest = 'days', metavar = 'days', help="Number of past days in which to search for matches")
parser.add_argument("-p", default = 3, type = int,  dest = 'pages', metavar = 'page limit', help="'Page Limit'; number of matches to return")
parser.add_argument("-m", default = None, type = str, dest = 'match', metavar = 'match', help="Match ID to look up")
parser.add_argument("-k", default = 'key.txt', type = str, dest = 'api_key_file', metavar = 'api_key_file', help="Path to text file containing the player's API key. (get one here: https://developer.vainglorygame.com/)")
parser.add_argument("-r", default = 'na', type = str, dest = 'region', metavar = 'region', help="Player's region. Possibilties: na, eu, sa, ea, or sg. Details here: https://developer.vainglorygame.com/docs?python#regions")
parser.add_argument("--debug", default = False, action='store_true', dest = 'debug_mode', help="Print the query command to console, so you can copy/paste the code elsewhere")
parser.add_argument("-i", "--interactive", default = False, action='store_true', dest = 'i_mode', help="Start an interactive Python session after querying match data")
parser.add_argument("--harvest", default = False, action='store_true', dest = 'harvest_mode', help="'Harvest' mode, saves each match to a JSON file")
parser.add_argument("--fail", default = False, action='store_true', dest = 'fail_mode', help="'Fail Finder' mode, ranks players in a match (match ID required)")



args = parser.parse_args()

username = args.name
api_key_file = args.api_key_file
region = args.region
match_ID = args.match
days = args.days
debug_mode = args.debug_mode
page_limit = args.pages
i_mode = args.i_mode
harvest_mode = args.harvest_mode
fail_mode = args.fail_mode

if __name__ == "__main__":
    print('Player name: {0}'.format(username))
    print('Region: {0}'.format(get_region_name(region = region)))
    key = get_api_key(api_key_file)
    print("Retrieving player data...")
    match_url = build_match_url(region, match_ID)
    get_match_data(username = username, key = key, match_url = match_url, match_ID = match_ID, days_to_subtract = days, page_limit = page_limit, debug_mode = debug_mode, i_mode = i_mode, harvest_mode = harvest_mode, fail_mode = fail_mode)
    # my_debugger(globals().copy())
