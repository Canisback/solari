from solari import Leona
from solari.stats import ItemPickrate, ItemWinrate


def test_item_pickrate(match_set_1):
    l = Leona([
        ItemPickrate()
    ])
    
    for m in match_set_1:
        l.push_match(m)
        
    stats = l.get_stats()
    
    # Nightbringer picked 7 times in 3 games
    assert stats["Pickrate"].loc[4636] == 7/30
    
def test_item_pickrate_with_duplicate(match_set_1):
    l = Leona([
        ItemPickrate()
    ])
    
    for m in match_set_1:
        l.push_match(m)
        
    stats = l.get_stats()
    
    # Needlessly large rod picked 8 times, but twice in duplicate
    assert stats["Pickrate"].loc[1058] == 6/30
    

def test_item_winrate(match_set_1):
    l = Leona([
        ItemWinrate()
    ])
    
    for m in match_set_1:
        l.push_match(m)
        
    stats = l.get_stats()
    
    # Nightbringer won 3 times in 7 picks
    assert stats["Winrate"].loc[4636] == 3/7
    
    
def test_item_winrate_with_duplicate(match_set_1):
    l = Leona([
        ItemWinrate()
    ])
    
    for m in match_set_1:
        l.push_match(m)
        
    stats = l.get_stats()
    
    # Needlessly large rod won 4 times out of the 8 picks, but twice in duplicate
    assert stats["Winrate"].loc[1058] == 4/6
    

def test_item_pickrate_by_champion(match_set_1):
    l = Leona([
        ItemPickrate(by_champion=True)
    ])
    
    for m in match_set_1:
        l.push_match(m)
        
    stats = l.get_stats()
    
    # Nightbringer picked 2 times in 3 Zoe
    assert stats["Pickrate"].loc[(142,4636)] == 2/3
    

def test_item_winrate_by_champion(match_set_1):
    l = Leona([
        ItemWinrate(by_champion=True)
    ])
    
    for m in match_set_1:
        l.push_match(m)
        
    stats = l.get_stats()
    
    # Nightbringer won 1 time in 2 picks by Zoe
    assert stats["Winrate"].loc[(142,4636)] == 1/2
    
def test_item_multiple_keys(match_set_1):
    l = Leona([
        ItemPickrate(),
        ItemPickrate(by_champion=True)
    ])
    
    for m in match_set_1:
        l.push_match(m)
        
    stats = l.get_stats()
    
    # There should by two DataFrames
    assert len(stats) == 2
    # One index by itemId only
    assert stats[("itemId",)]["Pickrate"].loc[4636] == 7/30
    # One index by itemId and championId
    assert stats[("championId","itemId")]["Pickrate"].loc[(142,4636)] == 2/3
    
def test_item_by_key(match_set_1):
    l = Leona([
        ItemPickrate(),
        ItemPickrate(by_champion=True)
    ])
    
    for m in match_set_1:
        l.push_match(m)
        
    stats = l.get_stats()
    
    # There should by two DataFrames
    assert len(stats) == 2
    # Directly check for the itemId index
    l.get_stats(("itemId",))["Pickrate"].loc[4636] == 7/30