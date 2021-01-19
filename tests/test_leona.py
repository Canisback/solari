from solari import Leona
from solari.stats import ChampionPickrate, ChampionWinrate, ItemPickrate

def test_leona_no_of_stats_managers():
    l = Leona([
        ChampionPickrate()
    ])
    
    # One stats key results in one stats manager
    assert len(l._stats_manager) == 1

def test_leona_no_of_stats_managers_2():
    l = Leona([
        ChampionPickrate(),
        ItemPickrate()
    ])
    
    # Two stats key results in two stats managers
    assert len(l._stats_manager) == 2

def test_leona_no_of_stats_managers_2_2():
    l = Leona([
        ChampionPickrate(),
        ChampionWinrate(),
        ItemPickrate()
    ])
    
    # Two stats key results in two stats managers
    assert len(l._stats_manager) == 2

def test_leona_no_of_stats_managers_3():
    l = Leona([
        ChampionPickrate(),
        ChampionPickrate(by_league=True),
        ItemPickrate()
    ])
    
    # Three stats key results in three stats managers
    assert len(l._stats_manager) == 3
    
    
def test_leona_push_match(match_set_1):
    l = Leona([
        ChampionPickrate()
    ])
    
    for m in match_set_1:
        l.push_match(m)
        
    # Pushing 3 matches results in 30 rows for champions stats
    assert len(l._stats_manager[("championId",)]._stats_participants) == 30
    
    
def test_leona_count_match(match_set_1):
    l = Leona([
        ChampionPickrate()
    ])
    
    for m in match_set_1:
        l.push_match(m)
        
    # Pushing 3 matches results in the correct count
    assert l.get_match_count() == 3
    
    
def test_leona_push_league(league):
    l = Leona([
        ChampionPickrate()
    ])
    
    l.push_league(league)
    
    # The player inside is DIAMOND
    assert l._rank_manager.get_rank("R4XZL5kWvvbd6YfO-QipfZslCjl-4J-1K2fj8IxX0kh2CLk") == "DIAMOND"
    
    
def test_leona_set_players_rank(league):
    l = Leona([
        ChampionPickrate()
    ])
    
    l.set_players_rank({"R4XZL5kWvvbd6YfO-QipfZslCjl-4J-1K2fj8IxX0kh2CLk":"DIAMOND"})
    
    # The player inside is DIAMOND
    assert l._rank_manager.get_rank("R4XZL5kWvvbd6YfO-QipfZslCjl-4J-1K2fj8IxX0kh2CLk") == "DIAMOND"
    

def test_leona_get_keys():
    l = Leona([
        ChampionPickrate(),
        ChampionWinrate(),
        ItemPickrate()
    ])
    
    # Two stats key results in two stats managers
    assert l.get_keys() == [("championId",),("itemId",)]