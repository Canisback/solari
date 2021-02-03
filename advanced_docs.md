# Advanced docs

To keep the home readme clean, more examples here.

## List of all Stats available

 * **ChampionPickrate** : Pickrate for each champion. Can be processed by league.
 * **ChampionPickCount** : Number of picks for each champion. Can be processed by league.
 * **ChampionWinrate** : Winrate for each champion. Can be processed by league.
 * **ChampionBanrate** : Banrate for each champion. Can be processed by league.
 * **ChampionBanCount** : Number of bans for each champion. Can be processed by league.
 * **ChampionPresenceRate** : Presence rate for each champion. Can be processed by league.
***
 * **ChampionGeneric** : Generic stats class for champions. Must be passed a field from the participant "stats" from the Riot API data. Can be processed by league.
 * **ChampionGenericPerMin** : Generic stats per minute class for champions. Must be passed a field from the  participant "stats" from the Riot API data. Can be processed by league.
 * **ChampionKDA** : Mean KDA for each champion. Can be processed by league.
 * **ChampionKillParticipation** : Mean Kill Participation per champion. Can be processed by league.
***
 * **ItemPickrate** : Pickrate for each item. Can be processed by champion and/or by league.
 * **ItemWinrate** : Winrate for each item. Can be processed by champion and/or by league.
***
 * **PlayerPickrate** : Pickrate for each champion and player.
 * **PlayerWinrate** : Winrate for each player. Can be processed by champion.
 * **PlayerPickCount** : Number of picks per player and champion.
 * **PlayerWins** : Number of wins per player. Can be processed by champion.
 * **PlayerLosses** : Number of losses per player. Can be processed by champion.
***
 * **PlayerGeneric** : Generic stats class for players. Must be passed a field from the participant "stats" from the Riot API data. Can be processed by champion.
 * **PlayerGenericPerMin** : Generic stats per minute class for players. Must be passed a field from the  participant "stats" from the Riot API data. Can be processed by champion.
 * **PlayerKDA** : Mean KDA for each player. Can be processed by champion.
 * **PlayerKillParticipation** : Mean Kill Participation per player. Can be processed by champion.
 
# Examples

Most basic example : 

```python
from solari.stats import ChampionPickrate, ChampionBanrate, ChampionWinrate, ChampionPresenceRate, ChampionPickCount
from solari import Leona

l = Leona([
    ChampionPickrate(),
    ChampionBanrate(),
    ChampionWinrate(),
    ChampionPresenceRate(),
    ChampionPickCount()
])


# Consider matches a list containing results from the Riot API match endpoint
for match_data in matches:
    l.push_match(match_data)
    
l.get_stats()
```


Item stats can be processed by champion. Note that as both have different keys (one is only by itemId, the second by championId and itemId), they can be processed by the same Leona instance. This will output two different DataFrames, referenced by key : 

```python
from solari.stats import ItemPickrate, ItemWinrate
from solari import Leona

l = Leona([
    ItemPickrate(),
    ItemWinrate(),
    ItemPickrate(by_champion=True),
    ItemWinrate(by_champion=True)
])


# Consider matches a list containing results from the Riot API match endpoint
for match_data in matches:
    l.push_match(match_data)
    
l.get_stats()
```


Stats can also be processed by league, but will require information about players rank. One solution is to give Leona a dict {summonerId:rank}, or give raw league by leagueId data.

```python
from solari.stats import ChampionPickrate, ChampionBanrate, ChampionWinrate, ChampionPresenceRate, ChampionPickCount
from solari import Leona

l = Leona([
    ChampionPickrate(by_league=True),
    ChampionBanrate(by_league=True),
    ChampionWinrate(by_league=True)
])


# Consider matches a list containing results from the Riot API match endpoint
for match_data in matches:
    l.push_match(match_data)
    
# Two solutions : 
# 1) Give a dict : 
l.set_players_rank(players_rank)

# 2) Push league data
# Consider leagues a list containing results from the Riot API league by leagueId endpoint
for league_data in leagues:
    l.push_league(push_league)
    
l.get_stats()
```

Stats by player are also possible. Only for pickrate, winrate and winrate per champion (for now) : 

```python
from solari.stats import PlayerPickrate, PlayerWinrate
from solari import Leona

l = Leona([
    PlayerPickrate(),
    PlayerWinrate(by_champion=True)
])


# Consider matches a list containing results from the Riot API match endpoint
for match_data in matches:
    l.push_match(match_data)

l.get_stats()
```


Asking for stats without pushing matches gives a specific error : 

```python
from solari import Leona
from solari.stats import ChampionPickrate, ChampionWinrate
from solari.exceptions import NoMatchPushed

l = Leona([
    ChampionPickrate(),
    ChampionWinrate()
])

try:
    l.get_stats()
except NoMatchPushed:
    print("Please push some matches")
```