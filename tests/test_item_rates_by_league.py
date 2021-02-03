from solari import Leona
from solari.stats import ItemPickrate, ItemWinrate

def test_item_pickrate(match_set_2, leagues):
    l = Leona([
        ItemPickrate(by_league=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
    for m in leagues:
        l.push_league(m)
        
    stats = l.get_stats()
    
    # BotRK picked once for two Platinum players
    assert stats["Pickrate"].loc[("PLATINUM",3153)] == 1/2
    # Collector picked 3 times for 5 Silver players
    assert stats["Pickrate"].loc[("SILVER",6676)] == 3/5
    # Ionian boots picked 5 times for 12 unranked players
    assert stats["Pickrate"].loc[("UNRANKED",3158)] == 5/12
    
def test_item_winrate(match_set_2, leagues):
    l = Leona([
        ItemWinrate(by_league=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
    for m in leagues:
        l.push_league(m)
        
    stats = l.get_stats()
    
    # BotRK picked once for two Platinum players and lost
    assert stats["Winrate"].loc[("PLATINUM",3153)] == 0
    # Collector picked 3 times for 5 Silver players and always lost
    assert stats["Winrate"].loc[("SILVER",6676)] == 0
    # Ionian boots picked 5 times for 12 unranked players and won 4 times
    assert stats["Winrate"].loc[("UNRANKED",3158)] == 4/5
    
    
def test_item_pickrate_by_champion(match_set_2, leagues):
    l = Leona([
        ItemPickrate(by_league=True, by_champion=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
    for m in leagues:
        l.push_league(m)
        
    stats = l.get_stats()
    
    # BotRK picked once for two Platinum players
    assert stats["Pickrate"].loc[("MASTER",360,6673)] == 2/3
    
def test_item_winrate_by_champion(match_set_2, leagues):
    l = Leona([
        ItemWinrate(by_league=True, by_champion=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
    for m in leagues:
        l.push_league(m)
        
    stats = l.get_stats()
    
    # BotRK picked once for two Platinum players
    assert stats["Winrate"].loc[("MASTER",360,6673)] == 1/2