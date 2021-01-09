# Advanced docs

To keep the home readme clean, more examples here.

## List of all Stats available

 * **ChampionPickrate** : Pickrate for each champion. Can be processed by league.
 * **ChampionPickCount** : Number of picks for each champion. Can be processed by league.
 * **ChampionWinrate** : Winrate for each champion. Can be processed by league.
 * **ChampionBanrate** : Banrate for each champion. Can be processed by league.
 * **ChampionPresenceRate** : Presence rate for each champion. Can be processed by league.
***
 * **ChampionGeneric** : Generic stats class. Must be passed a field from the  participant "stats" from the Riot API data. Can be processed by league.
 * **ChampionGenericPerMin** : Generic stats per minute class. Must be passed a field from the  participant "stats" from the Riot API data. Can be processed by league.
 * **ChampionKDA** : Mean KDA for each champion. Can be processed by league.
 * **ChampionKillParticipation** : Mean Kill Participation per champion. Can be processed by league.
***
 * **ItemPickrate** : Pickrate for each item. Can be processed by champion and/or by league.
 * **ItemWinrate** : Winrate for each item. Can be processed by champion and/or by league.
 
 
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