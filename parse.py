'''
Functions for parsing payload data
'''

def get_match(data, match_id):
    '''
    Search a payload for a specific match
    '''
    for item in data['data']:
        if item['id'] == match_id:
            return(item)

def get_rosters(match):
    '''
    Get the roster IDs from a match list of dicts
    '''
    rosters = []
    for item in match['relationships']['rosters']['data']:
        if item['type'] == 'roster':
            rosters.append(item['id'])
    return(rosters)
