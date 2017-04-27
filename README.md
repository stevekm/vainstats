# vainstats
Retrieve game data for Vainglory players using the [Vainglory API](https://developer.vainglorygame.com/docs). 

# Setup

First, clone this repository:
```
git clone https://github.com/stevekm/vainstats.git
cd vainstats
```

Get a Vainglory developer API key [here](https://developer.vainglorygame.com/). 

Save the API key in this repository directory under the file name `key.txt` in this format:

```
$ cat key.txt
AAAAAAA.BBBBBB.-CCCCC
```

# Usage
To run the program and get a batch of random sample Vainglory game matches, simply run the following command:

```
./get_stats.py
```

# Options
More specific match query criteria can be supplied with script arguments, such as:

```
./get_stats.py -r <region> -n <player in-game name> -k /path/to/api_key.txt -p <number of results to return> -d <number of days to search> -m <match ID>
```

For example:

```
$ ./get_stats.py -n eLiza -p 3 -d 1
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

## Debug Mode
To also output the exact Python query commands for reproducibility, you can use `--debug`:

```
$ ./get_stats.py -n eLiza -m 7c12bc86-2a89-11e7-a2d2-0667892d829e --debug
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
$ ./get_stats.py -m 7c12bc86-2a89-11e7-a2d2-0667892d829e -i
Player name: None
Region: North America
Retrieving player data...
Match ID is: 7c12bc86-2a89-11e7-a2d2-0667892d829e
search time is: 2017-04-25T22:00:16Z
Starting interactive session, you might want to run some of these:

from get_stats import *

import json

print(match_ID)

print(json.dumps(dat, indent=4, sort_keys=True))

Python 2.7.13 (default, Apr  4 2017, 08:47:57)
[GCC 4.2.1 Compatible Apple LLVM 8.1.0 (clang-802.0.38)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>>
```

