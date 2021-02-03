from solari import Leona
from solari.stats import ChampionPickrate, ChampionWinrate, ChampionPickCount, ChampionBanrate, ChampionPresenceRate, ChampionBanCount
from solari.exceptions import MissingRequiredStats

def test_champion_pickrate(match_set_2, leagues):
    l = Leona([
        ChampionPickrate(by_league=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
    for i in leagues:
        l.push_league(i)
        
    stats = l.get_stats()
    
    # Samira got picked 5 times out of 20 games
    assert stats["Pickrate"].loc[("MASTER",777)] == 5/20
    
def test_champion_winrate(match_set_2, leagues):
    l = Leona([
        ChampionWinrate(by_league=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
    for i in leagues:
        l.push_league(i)
        
    stats = l.get_stats()
    
    # Samira won 4 times out of 5 games
    assert stats["Winrate"].loc[("MASTER",777)] == 4/5
    
    
def test_champion_banrate(match_set_2, leagues):
    l = Leona([
        ChampionBanrate(by_league=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
    for i in leagues:
        l.push_league(i)
        
    stats = l.get_stats()
    
    # Samira was banned in 9 out of 19 games
    assert stats["Banrate"].loc[("MASTER",777)] == 9/19
    
    
def test_champion_banrate_teamwise(match_set_2, leagues):
    l = Leona([
        ChampionBanrate(team_wise=True, by_league=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
    for i in leagues:
        l.push_league(i)
        
    stats = l.get_stats()
    
    # Samira was banned in 10 times in 19 games
    assert stats["Banrate"].loc[("MASTER",777)] == 10/19
    
def test_champion_pick_count(match_set_2, leagues):
    l = Leona([
        ChampionPickCount(by_league=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
    for i in leagues:
        l.push_league(i)
        
    stats = l.get_stats()
    
    # Samira was picked 5 times
    assert stats["Pick Count"].loc[("MASTER",777)] == 5
    
def test_champion_ban_count(match_set_2, leagues):
    l = Leona([
        ChampionBanCount(by_league=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
    for i in leagues:
        l.push_league(i)
        
    stats = l.get_stats()
    
    # Samira was banned in 9 games
    assert stats["Ban Count"].loc[("MASTER",777)] == 9
    
def test_champion_ban_count_teamwise(match_set_2, leagues):
    l = Leona([
        ChampionBanCount(team_wise=True, by_league=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
    for i in leagues:
        l.push_league(i)
        
    stats = l.get_stats()
    
    # Samira was banned 10 times
    assert stats["Ban Count"].loc[("MASTER",777)] == 10
    
    
def test_champion_presence(match_set_2, leagues):
    l = Leona([
        ChampionPickrate(by_league=True),
        ChampionBanrate(by_league=True),
        ChampionPresenceRate(by_league=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
    for i in leagues:
        l.push_league(i)
        
    stats = l.get_stats()
    
    # Samira was banned in 9 games and picked in 5 games out of 20
    assert stats["Presence"].loc[("MASTER",777)] == (5 + 9) / 20
    
def test_champion_presence(match_set_2, leagues):
    try:
        l = Leona([
            ChampionPresenceRate(by_league=True)
        ])
        assert False
    except MissingRequiredStats:
        assert True