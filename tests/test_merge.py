from solari import Leona
from solari.stats import ChampionKDA, ChampionKillParticipation, ChampionGeneric, ChampionGenericPerMin
from solari.stats import ChampionPickrate, ChampionWinrate, ChampionPickCount, ChampionBanrate, ChampionPresenceRate, ChampionBanCount
from solari.stats import ItemPickrate, ItemWinrate

def test_merge_champion_pickrate(match_set_2, leagues):
    l = Leona([
        ChampionPickrate(by_league=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
    for i in leagues:
        l.push_league(i)
        
    stats = l.get_stats()
    
    l2 = Leona([
        ChampionPickrate(by_league=True)
    ])
    l3 = Leona([
        ChampionPickrate(by_league=True)
    ])
    
    for m in match_set_2[:10]:
        l2.push_match(m)
    for m in match_set_2[10:]:
        l3.push_match(m)
    for i in leagues:
        l2.push_league(i)
        
    l2.merge(l3)
    
    assert stats.equals(l2.get_stats())
    
    

def test_merge_item_pickrate(match_set_1):
    l = Leona([
        ItemPickrate()
    ])
    
    for m in match_set_1:
        l.push_match(m)
        
    stats = l.get_stats()
    
    l2 = Leona([
        ItemPickrate()
    ])
    l3 = Leona([
        ItemPickrate()
    ])
    
    
    for m in match_set_1[:2]:
        l2.push_match(m)
    for m in match_set_1[2:]:
        l3.push_match(m)
        
    l2.merge(l3)
    
    assert stats.equals(l2.get_stats())
    
def test_merge_redundant_games(match_set_2,leagues):
    l = Leona([
        ChampionPickrate(by_league=True),
        ChampionWinrate(by_league=True),
        ChampionPickCount(by_league=True),
        ChampionBanrate(by_league=True),
        ChampionBanCount(by_league=True),
        ChampionPresenceRate(by_league=True),
        ChampionKDA(by_league=True),
        ItemPickrate(),
        ItemWinrate()
    ])
    
    for m in match_set_2:
        l.push_match(m)
    for i in leagues:
        l.push_league(i)
        
    stats = l.get_stats()
    
    
    l2 = Leona([
        ChampionPickrate(by_league=True),
        ChampionWinrate(by_league=True),
        ChampionPickCount(by_league=True),
        ChampionBanrate(by_league=True),
        ChampionBanCount(by_league=True),
        ChampionPresenceRate(by_league=True),
        ChampionKDA(by_league=True),
        ItemPickrate(),
        ItemWinrate()
    ])
    l3 = Leona([
        ChampionPickrate(by_league=True),
        ChampionWinrate(by_league=True),
        ChampionPickCount(by_league=True),
        ChampionBanrate(by_league=True),
        ChampionBanCount(by_league=True),
        ChampionPresenceRate(by_league=True),
        ChampionKDA(by_league=True),
        ItemPickrate(),
        ItemWinrate()
    ])
    
    for m in match_set_2[:15]:
        l2.push_match(m)
    for m in match_set_2[10:]:
        l3.push_match(m)
    for i in leagues:
        l2.push_league(i)
        
    l2.merge(l3)
    assert stats[("itemId",)].equals(l2.get_stats()[("itemId",)])
    assert stats[("league","championId")].equals(l2.get_stats()[("league","championId")])