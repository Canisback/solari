from solari import Leona
from solari.stats import ChampionKDA, ChampionKillParticipation, ChampionGeneric, ChampionGenericPerMin


def test_champion_kda(match_set_2, leagues):
    l = Leona([
        ChampionKDA(by_league=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
    for m in leagues:
        l.push_league(m)
        
    stats = l.get_stats()
    
    # Miss Fortune picked in the only games with Platinum players and both Silver games
    assert stats["KDA"].loc[("SILVER",21)] == (
        (10+18) / 14 + 
        (8+13) / 9
    ) / 2
    assert stats["KDA"].loc[("PLATINUM",21)] == (
        (10+18) / 14
    )
    
def test_champion_kp(match_set_2, leagues):
    l = Leona([
        ChampionKillParticipation(by_league=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
    for m in leagues:
        l.push_league(m)
        
    stats = l.get_stats()
    
    # Miss Fortune picked in the only games with Platinum players and both Silver games
    assert stats["KP"].loc[("SILVER",21)] == (
        (10+18) / (10 + 15 + 3 + 15 + 6) + 
        (8+13) / (6 + 8 + 9 + 21 + 20)
    ) / 2
    assert stats["KP"].loc[("PLATINUM",21)] == (
        (10+18) / (10 + 15 + 3 + 15 + 6)
    )
    
    
def test_champion_generic(match_set_2, leagues):
    l = Leona([
        ChampionGeneric("goldEarned", by_league=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
    for m in leagues:
        l.push_league(m)
        
    stats = l.get_stats()
    
    # Miss Fortune picked in the only games with Platinum players and both Silver games
    assert stats["goldEarned"].loc[("SILVER",21)] == (
        14237  + 
        11588
        
    ) / 2
    assert stats["goldEarned"].loc[("PLATINUM",21)] == (
        14237
    )
    
    
def test_champion_generic_permin(match_set_2, leagues):
    l = Leona([
        ChampionGenericPerMin("goldEarned", by_league=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
    for m in leagues:
        l.push_league(m)
        
    stats = l.get_stats()
    
    # Miss Fortune picked in the only games with Platinum players and both Silver games
    assert stats["goldEarnedPerMin"].loc[("SILVER",21)] == (
        (14237 * 60 / 1218) + 
        (11588 * 60 / 1857)
        
    ) / 2
    assert stats["goldEarnedPerMin"].loc[("PLATINUM",21)] == (
        (14237 * 60 / 1218)
    )