# Solari

[![PyPi](https://img.shields.io/pypi/v/solari)](https://pypi.org/project/solari/)

***

## Stats module for League of Legends

This library aims to manage stats from League of Legends match data in bulk in a very easy way from the user's point of view.

1. Call the stats needed
2. Give match data (straight from Riot API)
3. ...?
4. Profit


***

## How to use it

To install it : 

```
pip3 install solari
```

This library revolves around a Manager, here the Leona class, and a library of stats, that can sometime be configured.

First things first, you need to import the stats you need : 

```python
from solari.stats import ChampionPickrate, ChampionBanrate, ChampionWinrate, ChampionPresenceRate, ChampionPickCount
```

Then you need to instanciate Leona and pass the wanted stats : 

```python
from solari import Leona

l = Leona([
    ChampionPickrate(),
    ChampionBanrate(),
    ChampionWinrate(),
    ChampionPresenceRate(),
    ChampionPickCount()
])
```

Push a match data, this data being a parsed json from the match data straight from the Riot API : 

```python
l.push_match(match_data)
```

Note : this is for one match, push as many matches as you want by repeating the command.

Last step, getting the stats : 

```python
l.get_stats()
```

This will output a DataFrame of the stats grouped by championId. If the picked stats have multiple keys, understand if you have also stats regarding items, they will appear in another DataFrame.

Stats configuration happens during instantiation : 

```python
from solari.stats import ItemPickrate
l = Leona([
    ItemPickrate(by_champion=True)
])
```

### What this library does NOT do

 * Request match data : the role of this library only starts when you have the data
 * Change ID to name : this would require ddragon/cdragon and can easily be done afterward

More examples : https://github.com/Canisback/solari/blob/master/advanced_docs.md

## TODO

By order of priority :

1. ~~Implementing the "per_league" key, allowing stats to be grouped by players rank as well~~
2. Add more documentation on how to add Stats
3. ~~Add verification for DerivedStats required stats~~
4. Implementing more stats for champion and items
5. ~~Implementing stats by player~~