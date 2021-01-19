from solari import Leona
from solari.stats import ChampionKDA, ChampionKillParticipation, ChampionGeneric, ChampionGenericPerMin


def test_champion_kda(match_set_1):
    l = Leona([
        ChampionKDA()
    ])
    
    for m in match_set_1:
        l.push_match(m)
        
    stats = l.get_stats()
    
    assert stats["KDA"].loc[142] == (
        (15+8) / 14 + 
        (19+8) / 11 + 
        (12+9) / 8 
    ) / 3
    
def test_champion_kp(match_set_1):
    l = Leona([
        ChampionKillParticipation()
    ])
    
    for m in match_set_1:
        l.push_match(m)
        
    stats = l.get_stats()
    
    assert stats["KP"].loc[142] == (
        (15+8) / 39 + 
        (19+8) / 59 + 
        (12+9) / 40 
    ) / 3
    
def test_champion_generic_gold(match_set_1):
    l = Leona([
        ChampionGeneric("goldEarned")
    ])
    
    for m in match_set_1:
        l.push_match(m)
        
    stats = l.get_stats()
    
    assert stats["goldEarned"].loc[142] == (
        11401 + 
        16146 + 
        12102
    ) / 3
    
def test_champion_generic_gold_with_rename(match_set_1):
    l = Leona([
        ChampionGeneric("goldEarned", "Gold")
    ])
    
    for m in match_set_1:
        l.push_match(m)
        
    stats = l.get_stats()
    
    assert stats["Gold"].loc[142] == (
        11401 + 
        16146 + 
        12102
    ) / 3
    
def test_champion_generic_permin_gold(match_set_1):
    l = Leona([
        ChampionGenericPerMin("goldEarned")
    ])
    
    for m in match_set_1:
        l.push_match(m)
        
    stats = l.get_stats()
    
    assert stats["goldEarnedPerMin"].loc[142] == (
        11401 / (991/60) + 
        16146 / (1647/60) + 
        12102 / (1153/60)
    ) / 3