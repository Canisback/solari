from solari import Leona
from solari.stats import PlayerKDA, PlayerKillParticipation, PlayerGeneric, PlayerGenericPerMin


def test_player_kda(match_set_2):
    l = Leona([
        PlayerKDA()
    ])
    
    for m in match_set_2:
        l.push_match(m)
        
    stats = l.get_stats()
    
    # KDA for 20 games
    assert stats["KDA"].loc["w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0"] == (
        (5 + 12) / 10 + 
        (10 + 8) / 2 + 
        (1 + 1) / 3 + 
        (6 + 0) / 3 + 
        (5 + 9) / 5 + 
        (8 + 13) / 2 + 
        (9 + 8) / 4 + 
        (2 + 9) / 6 + 
        (4 + 6) / 5 + 
        (10 + 7) / 1 +  # Death at 0 put at 1
        (0 + 3) / 6 + 
        (21 + 7) / 10 + 
        (8 + 9) / 6 + 
        (8 + 11) / 4 + 
        (3 + 16) / 5 + 
        (8 + 8) / 5 + 
        (4 + 4) / 1 + 
        (2 + 2) / 3 + 
        (3 + 2) / 1 + 
        (5 + 33) / 7
    ) / 20

def test_player_kda_by_accountId(match_set_2):
    l = Leona([
        PlayerKDA(by_accountId=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
        
    stats = l.get_stats()
    
    # KDA for 20 games
    assert stats["KDA"].loc["yF56aAqvE4rpVSyqCUN-MFGzqEdrCi83PHN6XoeaVBhk6x4"] == (
        (5 + 12) / 10 + 
        (10 + 8) / 2 + 
        (1 + 1) / 3 + 
        (6 + 0) / 3 + 
        (5 + 9) / 5 + 
        (8 + 13) / 2 + 
        (9 + 8) / 4 + 
        (2 + 9) / 6 + 
        (4 + 6) / 5 + 
        (10 + 7) / 1 + # Death at 0 put at 1
        (0 + 3) / 6 + 
        (21 + 7) / 10 + 
        (8 + 9) / 6 + 
        (8 + 11) / 4 + 
        (3 + 16) / 5 + 
        (8 + 8) / 5 + 
        (4 + 4) / 1 + 
        (2 + 2) / 3 + 
        (3 + 2) / 1 + 
        (5 + 33) / 7
    ) / 20
    
    
def test_player_kda_by_champion(match_set_2):
    l = Leona([
        PlayerKDA(by_champion=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
        
    stats = l.get_stats()
    
    # KDA for 8 Vladimir games
    assert stats["KDA"].loc[("w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0",145)] == (
        (5 + 12) / 10 + 
        (10 + 8) / 2 + 
        (1 + 1) / 3 + 
        (6 + 0) / 3 + 
        (9 + 8) / 4 + 
        (10 + 7) / 1 +  # Death at 0 put at 1
        (8 + 9) / 6 + 
        (8 + 11) / 4
    ) / 8
    
    
def test_player_kp(match_set_2):
    l = Leona([
        PlayerKillParticipation()
    ])
    
    for m in match_set_2:
        l.push_match(m)
        
    stats = l.get_stats()
    
    # KDA for 20 games
    assert stats["KP"].loc["CBPXs9Y9aqWlx60eg5XuDfCaX2Frfqz2rBHBPC9kGSN3QtA"] == (
        (6 + 8) / (7+9+6+9+0) + 
        (3 + 9) / (1+3+10+4+3) + 
        (2 + 13) / (8+2+4+2+5)
    ) / 3
    
    
def test_player_kp_by_accountId(match_set_2):
    l = Leona([
        PlayerKillParticipation(by_accountId=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
        
    stats = l.get_stats()
    
    # KDA for 20 games
    assert stats["KP"].loc["2voMrjFbfYuztOJhPlcpkv_hnTdnuSYmGNeMKt8dkH1Slw"] == (
        (6 + 8) / (7+9+6+9+0) + 
        (3 + 9) / (1+3+10+4+3) + 
        (2 + 13) / (8+2+4+2+5)
    ) / 3

def test_player_kp_by_champion(match_set_2):
    l = Leona([
        PlayerKillParticipation(by_champion=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
        
    stats = l.get_stats()
    
    # KDA for 8 Vladimir games
    assert stats["KP"].loc[("w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0",22)] == (
        (2 + 9) / (2+2+8+2+3) + 
        (4 + 6) / (3+2+7+2+4)
    ) / 2
    
def test_player_generic(match_set_2):
    l = Leona([
        PlayerGeneric("goldEarned")
    ])
    
    for m in match_set_2:
        l.push_match(m)
        
    stats = l.get_stats()
    assert stats["goldEarned"].loc["CBPXs9Y9aqWlx60eg5XuDfCaX2Frfqz2rBHBPC9kGSN3QtA"] == (
        14925 + 4780 + 7789
    ) / 3
    
def test_player_generic_by_accountId(match_set_2):
    l = Leona([
        PlayerGeneric("goldEarned", by_accountId=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
        
    stats = l.get_stats()
    assert stats["goldEarned"].loc["2voMrjFbfYuztOJhPlcpkv_hnTdnuSYmGNeMKt8dkH1Slw"] == (
        14925 + 4780 + 7789
    ) / 3
    
def test_player_generic_perMin(match_set_2):
    l = Leona([
        PlayerGenericPerMin("goldEarned")
    ])
    
    for m in match_set_2:
        l.push_match(m)
        
    stats = l.get_stats()
    assert stats["goldEarnedPerMin"].loc["CBPXs9Y9aqWlx60eg5XuDfCaX2Frfqz2rBHBPC9kGSN3QtA"] == (
        (14925 * 60 /2163) + (4780 * 60 /912) + (7789 * 60 /1706)
    ) / 3
    
def test_player_generic_perMin_by_accountId(match_set_2):
    l = Leona([
        PlayerGenericPerMin("goldEarned", by_accountId=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
        
    stats = l.get_stats()
    assert stats["goldEarnedPerMin"].loc["2voMrjFbfYuztOJhPlcpkv_hnTdnuSYmGNeMKt8dkH1Slw"] == (
        (14925 * 60 /2163) + (4780 * 60 /912) + (7789 * 60 /1706)
    ) / 3
    
def test_player_generic_by_champion(match_set_2):
    l = Leona([
        PlayerGeneric("goldEarned", by_champion=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
        
    stats = l.get_stats()
    assert stats["goldEarned"].loc[("w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0",22)] == (
        9020 + 12083
    ) / 2
    
def test_player_generic_perMin_by_champion(match_set_2):
    l = Leona([
        PlayerGenericPerMin("goldEarned", by_champion=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
        
    stats = l.get_stats()
    assert stats["goldEarnedPerMin"].loc[("w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0",22)] == (
        (9020 * 60 / 1619) + (12083 * 60 / 1939)
    ) / 2
    
def test_player_generic_rename(match_set_2):
    l = Leona([
        PlayerGeneric("goldEarned", "Gold")
    ])
    
    for m in match_set_2:
        l.push_match(m)
        
    stats = l.get_stats()
    assert stats["Gold"].loc["CBPXs9Y9aqWlx60eg5XuDfCaX2Frfqz2rBHBPC9kGSN3QtA"] == (
        14925 + 4780 + 7789
    ) / 3
    
def test_player_generic_perMin_rename(match_set_2):
    l = Leona([
        PlayerGenericPerMin("goldEarned", "GoldPerMinute")
    ])
    
    for m in match_set_2:
        l.push_match(m)
        
    stats = l.get_stats()
    assert stats["GoldPerMinute"].loc["CBPXs9Y9aqWlx60eg5XuDfCaX2Frfqz2rBHBPC9kGSN3QtA"] == (
        (14925 * 60 /2163) + (4780 * 60 /912) + (7789 * 60 /1706)
    ) / 3