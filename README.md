# vainstats
Retrieve game data for Vainglory matches using the [Vainglory API](https://developer.vainglorygame.com/docs). 

__NOTE:__ Development of this app has shifted to focus on creating a [Python Dash](https://plot.ly/products/dash/) app. 

# Installation
## Anaconda
- __[Recomended]__ Install Python 3 with [Anaconda](https://www.continuum.io/downloads) and make it your default Python

## Setup
- Clone this repository:
```
git clone https://github.com/stevekm/vainstats.git
cd vainstats
```
- Get a Vainglory developer API key [here](https://developer.vainglorygame.com/), and save it in this repository directory under the file name `key.txt`. Example:
```
$ cat key.txt
AAAAAAA.BBBBBB.-CCCCC
```
## Dash
- If you are using Anaconda and `conda` (recomended), create an environment for Dash
```bash
./install_dash.sh
```
- Otherwise, install Dash with `pip`:
```bash
pip install -r requirements.txt
```

# Usage - Dash App
To start the Dash app:
```bash
 python app.py
```
Then navigate to the displayed IP address (e.g. `http://127.0.0.1:8050/`) in your web browser.

# Usage - Command Line App
To run the program and get a batch of random sample Vainglory game matches, simply run the following command:

```
./vainstats.py
```
## Lookup Player's Matches
To look up the latest matches for a specific player, use the `-n` argument and supply the desired player's in-game name:

```
./vainstats.pyy -n eLiza
```

## Number of Days to Search
By default, the program will search for player matches in the last day. To specify a different number of days to look back, add the `-d` argument:

```
./vainstats.py -n eLiza -p 3 -d 10
```
- NOTE: If no matches were found in the given time frame, a 404 error is returned. 

## Number of Results to Display

By default, up to 3 results will be returned. To specify a different maximum number, use the `-p` argument:

```
./vainstats.py -n eLiza -p 3 -d 10 -p 5
```

## Match Lookup

You can look up more information about a specific game match by using the `-m` argument and specifying the match ID:

```
./vainstats.py -m 7a6fd762-29d8-11e7-a2d2-0667892d829e
```

## Fail Finder
Player rankings (aka the 'Fail Finder') can be calculated by including the `--fail` argument along with a match ID:

```
./vainstats.py -m 59d62746-2905-11e7-a2d2-0667892d829e --fail
```

## Options
More specific match query criteria can be supplied with script arguments, such as:

```
./vainstats.py -r <region> -n <player in-game name> -k /path/to/api_key.txt -p <number of results to return> -d <number of days to search> -m <match ID>
```

## Example Output
- NOTE: Output format will change as development progresses

Searching for up to 3 matches played in the last day by player `eLiza`

```
$ ./vainstats.py -n eLiza -p 3 -d 1
Player name: eLiza
Region: North America
Retrieving player data...
Match ID is: None
search time is: 2017-04-25T21:56:02Z
------------------
Found match
id: a551798e-2a25-11e7-a2d2-0667892d829e
outcome: victory
type: blitz_pvp_ranked
date: 2017-04-26T02:11:29Z
duration: 224

------------------
Found match
id: 7c12bc86-2a89-11e7-a2d2-0667892d829e
outcome: victory
type: blitz_pvp_ranked
date: 2017-04-26T14:06:14Z
duration: 221

```

Searching for details on a specific match with 'Fail Finder' match rankings:

```
$ ./get_stats.py -m 59d62746-2905-11e7-a2d2-0667892d829e --fail
Player name: None
Region: North America
Retrieving player data...
Match ID is: 59d62746-2905-11e7-a2d2-0667892d829e
search time is: 2017-05-08T20:29:34Z
------------------
Found match
id: 59d62746-2905-11e7-a2d2-0667892d829e
outcome: victory
type: blitz_pvp_ranked
date: 2017-04-24T15:47:47Z
duration: 03:35

------------------

------------------
Player info
player name: Vitryus
player id: 069054d2-6eca-11e4-a9c4-06641bcbf424
player region: na
player level: 30
player wins: 1553
player win streak: 0
player loss streak: 1
played: 3132
played rank: 2058
match xp: 175450
match lifetimegold: 11735.6650391
------------------
Participant info
player skillTier: 8
player karmaLevel: 1
match hero: *Rona*
match skin: Rona_Skin_Fury_T3
match level: 30
match kills/deaths/assists: 3/3/0
match final gold: 102
match nonJungleMinionKills: 0
match turretCaptures: 0
match jungleKills: 13
match farm: 39.175
match wentAfk: False
match firstAfkTime: -1
match minionKills: 13
match krakenCaptures: 0
match goldMineCaptures: 1
match crystalMineCaptures: 0
match winner: False
------------------

------------------
Player info
player name: death0227
player id: 7fff2cc8-85d2-11e6-8f48-06fc87f1dd11
player region: na
player level: 11
player wins: 106
player win streak: 0
player loss streak: 2
played: 3
played rank: 0
match xp: 7553
match lifetimegold: 11606.6669922
------------------
Participant info
player skillTier: -1
player karmaLevel: 2
match hero: *Rona*
match skin: Rona_DefaultSkin
match level: 11
match kills/deaths/assists: 2/2/3
match final gold: 81
match nonJungleMinionKills: 3
match turretCaptures: 0
match jungleKills: 1
match farm: 5.25
match wentAfk: False
match firstAfkTime: -1
match minionKills: 4
match krakenCaptures: 0
match goldMineCaptures: 2
match crystalMineCaptures: 0
match winner: True
------------------

------------------
Player info
player name: carter1355
player id: 7edf667e-13cc-11e5-8431-06d90c28bf1a
player region: na
player level: 24
player wins: 655
player win streak: 0
player loss streak: 3
played: 1189
played rank: 736
match xp: 92008
match lifetimegold: 11735.6650391
------------------
Participant info
player skillTier: 4
player karmaLevel: 2
match hero: *Kestrel*
match skin: Kestrel_DefaultSkin
match level: 24
match kills/deaths/assists: 3/3/3
match final gold: 15
match nonJungleMinionKills: 1
match turretCaptures: 1
match jungleKills: 0
match farm: 3.5
match wentAfk: False
match firstAfkTime: -1
match minionKills: 1
match krakenCaptures: 0
match goldMineCaptures: 0
match crystalMineCaptures: 0
match winner: False
------------------

------------------
Player info
player name: frontierfighter
player id: 90b45d64-ecba-11e6-8caa-06d90c28bf1a
player region: na
player level: 15
player wins: 254
player win streak: 1
player loss streak: 0
played: 47
played rank: 0
match xp: 29430
match lifetimegold: 11631.6669922
------------------
Participant info
player skillTier: -1
player karmaLevel: 2
match hero: *Celeste*
match skin: Celeste_DefaultSkin
match level: 15
match kills/deaths/assists: 3/3/3
match final gold: 488
match nonJungleMinionKills: 2
match turretCaptures: 1
match jungleKills: 0
match farm: 5.25
match wentAfk: False
match firstAfkTime: -1
match minionKills: 2
match krakenCaptures: 0
match goldMineCaptures: 1
match crystalMineCaptures: 0
match winner: True
------------------

------------------
Player info
player name: REkT
player id: 87b65b32-ef36-11e4-b686-06eb725f8a76
player region: na
player level: 22
player wins: 115
player win streak: 0
player loss streak: 3
played: 217
played rank: 66
match xp: 79981
match lifetimegold: 11606.6669922
------------------
Participant info
player skillTier: -1
player karmaLevel: 1
match hero: *Taka*
match skin: Taka_DefaultSkin
match level: 22
match kills/deaths/assists: 3/2/2
match final gold: 338
match nonJungleMinionKills: 5
match turretCaptures: 0
match jungleKills: 1
match farm: 8.75
match wentAfk: False
match firstAfkTime: -1
match minionKills: 6
match krakenCaptures: 0
match goldMineCaptures: 1
match crystalMineCaptures: 0
match winner: True
------------------

------------------
Player info
player name: eLiza
player id: c8e90cbc-fc45-11e6-b893-06f4ee369f53
player region: na
player level: 12
player wins: 61
player win streak: 0
player loss streak: 2
played: 52
played rank: 0
match xp: 11891
match lifetimegold: 11735.6650391
------------------
Participant info
player skillTier: -1
player karmaLevel: 2
match hero: *Skaarf*
match skin: Skaarf_Skin_Infinity_T3
match level: 12
match kills/deaths/assists: 1/2/1
match final gold: 1083
match nonJungleMinionKills: 5
match turretCaptures: 1
match jungleKills: 0
match farm: 8.75
match wentAfk: False
match firstAfkTime: -1
match minionKills: 5
match krakenCaptures: 0
match goldMineCaptures: 1
match crystalMineCaptures: 0
match winner: False
------------------

------------------
Player Match Ranking
Name                      Hero           Team          Score                                           ID
----------          ----------     ----------       ----------             ------------------------------
Vitryus                 *Rona*           lost      244.055165039      069054d2-6eca-11e4-a9c4-06641bcbf424
carter1355           *Kestrel*           lost      101.509078372      7edf667e-13cc-11e5-8431-06d90c28bf1a
death0227               *Rona*            won      29.8221969922      7fff2cc8-85d2-11e6-8f48-06fc87f1dd11
frontierfighter      *Celeste*            won      24.0859669922      90b45d64-ecba-11e6-8caa-06d90c28bf1a
REkT                    *Taka*            won     0.156476992187      87b65b32-ef36-11e4-b686-06eb725f8a76
eLiza                 *Skaarf*           lost     -78.5654249609      c8e90cbc-fc45-11e6-b893-06f4ee369f53
```

# Extras
## Debug Mode
To also output the exact Python query commands for reproducibility, you can use `--debug`:

```
$ ./vainstats.py -n eLiza -m 7c12bc86-2a89-11e7-a2d2-0667892d829e --debug
Player name: eLiza
Region: North America
Retrieving player data...
Match ID is: 7c12bc86-2a89-11e7-a2d2-0667892d829e
search time is: 2017-04-25T21:58:16Z
------------------
Query Commands for Debugging:

header = {
"Accept": "application/vnd.api+json",
"Authorization": "AAAAAAA.BBBBBB.-CCCCC",
"X-TITLE-ID": "semc-vainglory"
}
query = {
"filter[createdAt-start]": "2017-04-25T21:58:16Z",
"filter[playerNames]": "eLiza",
"page[limit]": 3,
"sort": "-createdAt"
}
match_url = "https://api.dc01.gamelockerapp.com/shards/na/matches/7c12bc86-2a89-11e7-a2d2-0667892d829e"
import requests
import json
match = requests.get(match_url, headers=header, params=query)
dat = json.loads(match.content)
------------------

------------------
Found match
id: 7c12bc86-2a89-11e7-a2d2-0667892d829e
outcome: victory
type: blitz_pvp_ranked
date: 2017-04-26T14:06:14Z
duration: 221
```

This is useful if you need to copy/paste the Python commands elsewhere.

## Interactive Mode
For even more debugging, you can enter 'interactive' mode with `-i` in order to start an interactive Python session immediately after retrieving query results

```
$ ./vainstats.py -i
Player name: None
Region: North America
Retrieving player data...
Match ID is: None
search time is: 2017-05-02T11:22:25Z
------------------


# Starting interactive session, you might want to run some of these:

from get_stats import *

import json

print(match_ID)

print(json.dumps(dat, indent=4, sort_keys=True))

for item in dat['included']: print(item['type'])

------------------

Python 2.7.13 (default, Apr  4 2017, 08:47:57)
[GCC 4.2.1 Compatible Apple LLVM 8.1.0 (clang-802.0.38)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> 

```

# Software
- Dash app developed & tested with Python 3.6
- `vainstats.py` Developed under Python 2.7 and tested with 2.7 and 3.6
