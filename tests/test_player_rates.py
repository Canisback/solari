from solari import Leona
from solari.stats import PlayerPickrate, PlayerPickCount, PlayerWinrate, PlayerWins, PlayerLosses

def test_player_pickrate(match_set_2):
    l = Leona([
        PlayerPickrate()
    ])
    
    for m in match_set_2:
        l.push_match(m)
        
    stats = l.get_stats()
    
    # "w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0" played 6 times Jhin in 20 games
    assert stats["Pickrate"].loc[("w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0",202)] == 6/20
    # "CBPXs9Y9aqWlx60eg5XuDfCaX2Frfqz2rBHBPC9kGSN3QtA" played once Galio in 3 games
    assert stats["Pickrate"].loc[("CBPXs9Y9aqWlx60eg5XuDfCaX2Frfqz2rBHBPC9kGSN3QtA",3)] == 1/3
    
def test_player_pickcount(match_set_2):
    l = Leona([
        PlayerPickCount()
    ])
    
    for m in match_set_2:
        l.push_match(m)
        
    stats = l.get_stats()
    
    # "w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0" played 6 times Jhin in 20 games
    assert stats["Pick Count"].loc[("w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0",202)] == 6
    # "CBPXs9Y9aqWlx60eg5XuDfCaX2Frfqz2rBHBPC9kGSN3QtA" played once Galio in 3 games
    assert stats["Pick Count"].loc[("CBPXs9Y9aqWlx60eg5XuDfCaX2Frfqz2rBHBPC9kGSN3QtA",3)] == 1

def test_player_winrate(match_set_2):
    l = Leona([
        PlayerWinrate()
    ])
    
    for m in match_set_2:
        l.push_match(m)
        
    stats = l.get_stats()
    
    # "w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0" won 10 times in 20 games
    assert stats["Winrate"].loc["w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0"] == 10/20
    # "CBPXs9Y9aqWlx60eg5XuDfCaX2Frfqz2rBHBPC9kGSN3QtA" won once in 3 games
    assert stats["Winrate"].loc["CBPXs9Y9aqWlx60eg5XuDfCaX2Frfqz2rBHBPC9kGSN3QtA"] == 1/3
    
def test_player_winrate_by_champion(match_set_2):
    l = Leona([
        PlayerWinrate(by_champion=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
        
    stats = l.get_stats()
    
    # "w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0" won 5 times with Jhin in 6 games
    assert stats["Winrate"].loc[("w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0",202)] == 5/6
    # "CBPXs9Y9aqWlx60eg5XuDfCaX2Frfqz2rBHBPC9kGSN3QtA" won his 1 Galio game
    assert stats["Winrate"].loc[("CBPXs9Y9aqWlx60eg5XuDfCaX2Frfqz2rBHBPC9kGSN3QtA",3)] == 1
    
def test_player_wins(match_set_2):
    l = Leona([
        PlayerWins()
    ])
    
    for m in match_set_2:
        l.push_match(m)
        
    stats = l.get_stats()
    
    # "w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0" won 5 times with Jhin in 6 games
    assert stats["Wins"].loc["w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0"] == 10
    # "CBPXs9Y9aqWlx60eg5XuDfCaX2Frfqz2rBHBPC9kGSN3QtA" won his 1 Galio game
    assert stats["Wins"].loc["CBPXs9Y9aqWlx60eg5XuDfCaX2Frfqz2rBHBPC9kGSN3QtA"] == 1
    
def test_player_wins_by_champion(match_set_2):
    l = Leona([
        PlayerWins(by_champion=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
        
    stats = l.get_stats()
    
    # "w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0" won 5 times with Jhin in 6 games
    assert stats["Wins"].loc[("w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0",202)] == 5
    # "CBPXs9Y9aqWlx60eg5XuDfCaX2Frfqz2rBHBPC9kGSN3QtA" won his 1 Galio game
    assert stats["Wins"].loc[("CBPXs9Y9aqWlx60eg5XuDfCaX2Frfqz2rBHBPC9kGSN3QtA",3)] == 1
    
def test_player_losses(match_set_2):
    l = Leona([
        PlayerLosses()
    ])
    
    for m in match_set_2:
        l.push_match(m)
        
    stats = l.get_stats()
    
    # "w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0" won 5 times with Jhin in 6 games
    assert stats["Losses"].loc["w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0"] == 10
    # "CBPXs9Y9aqWlx60eg5XuDfCaX2Frfqz2rBHBPC9kGSN3QtA" won his 1 Galio game
    assert stats["Losses"].loc["CBPXs9Y9aqWlx60eg5XuDfCaX2Frfqz2rBHBPC9kGSN3QtA"] == 2
    
def test_player_losses_by_champion(match_set_2):
    l = Leona([
        PlayerLosses(by_champion=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
        
    stats = l.get_stats()
    
    # "w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0" won 5 times with Jhin in 6 games
    assert stats["Losses"].loc[("w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0",202)] == 1
    
    
def test_player_by_accountId(match_set_2):
    l = Leona([
        PlayerWinrate(by_accountId=True),
        PlayerWins(by_accountId=True),
        PlayerLosses(by_accountId=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
        
    stats = l.get_stats()
    
    # "w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0" won 10 times in 20 games
    assert stats["Winrate"].loc["yF56aAqvE4rpVSyqCUN-MFGzqEdrCi83PHN6XoeaVBhk6x4"] == 10/20
    # "CBPXs9Y9aqWlx60eg5XuDfCaX2Frfqz2rBHBPC9kGSN3QtA" won once in 3 games
    assert stats["Winrate"].loc["2voMrjFbfYuztOJhPlcpkv_hnTdnuSYmGNeMKt8dkH1Slw"] == 1/3
    
    # "w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0" won 5 times with Jhin in 6 games
    assert stats["Losses"].loc["yF56aAqvE4rpVSyqCUN-MFGzqEdrCi83PHN6XoeaVBhk6x4"] == 10
    # "CBPXs9Y9aqWlx60eg5XuDfCaX2Frfqz2rBHBPC9kGSN3QtA" won his 1 Galio game
    assert stats["Losses"].loc["2voMrjFbfYuztOJhPlcpkv_hnTdnuSYmGNeMKt8dkH1Slw"] == 2
    
    # "w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0" won 5 times with Jhin in 6 games
    assert stats["Losses"].loc["yF56aAqvE4rpVSyqCUN-MFGzqEdrCi83PHN6XoeaVBhk6x4"] == 10
    # "CBPXs9Y9aqWlx60eg5XuDfCaX2Frfqz2rBHBPC9kGSN3QtA" won his 1 Galio game
    assert stats["Losses"].loc["2voMrjFbfYuztOJhPlcpkv_hnTdnuSYmGNeMKt8dkH1Slw"] == 2
    
def test_player_by_champion_by_accountId(match_set_2):
    l = Leona([
        PlayerPickrate(by_accountId=True),
        PlayerPickCount(by_accountId=True),
        PlayerWinrate(by_champion=True, by_accountId=True),
        PlayerWins(by_champion=True, by_accountId=True),
        PlayerLosses(by_champion=True, by_accountId=True)
    ])
    
    for m in match_set_2:
        l.push_match(m)
        
    stats = l.get_stats()
    
    # "w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0" played 6 times Jhin in 20 games
    assert stats["Pickrate"].loc[("yF56aAqvE4rpVSyqCUN-MFGzqEdrCi83PHN6XoeaVBhk6x4",202)] == 6/20
    # "CBPXs9Y9aqWlx60eg5XuDfCaX2Frfqz2rBHBPC9kGSN3QtA" played once Galio in 3 games
    assert stats["Pickrate"].loc[("2voMrjFbfYuztOJhPlcpkv_hnTdnuSYmGNeMKt8dkH1Slw",3)] == 1/3
    
    # "w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0" played 6 times Jhin in 20 games
    assert stats["Pick Count"].loc[("yF56aAqvE4rpVSyqCUN-MFGzqEdrCi83PHN6XoeaVBhk6x4",202)] == 6
    # "CBPXs9Y9aqWlx60eg5XuDfCaX2Frfqz2rBHBPC9kGSN3QtA" played once Galio in 3 games
    assert stats["Pick Count"].loc[("2voMrjFbfYuztOJhPlcpkv_hnTdnuSYmGNeMKt8dkH1Slw",3)] == 1
    
    # "w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0" won 5 times with Jhin in 6 games
    assert stats["Winrate"].loc[("yF56aAqvE4rpVSyqCUN-MFGzqEdrCi83PHN6XoeaVBhk6x4",202)] == 5/6
    # "CBPXs9Y9aqWlx60eg5XuDfCaX2Frfqz2rBHBPC9kGSN3QtA" won his 1 Galio game
    assert stats["Winrate"].loc[("2voMrjFbfYuztOJhPlcpkv_hnTdnuSYmGNeMKt8dkH1Slw",3)] == 1
    
    # "w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0" won 5 times with Jhin in 6 games
    assert stats["Wins"].loc[("yF56aAqvE4rpVSyqCUN-MFGzqEdrCi83PHN6XoeaVBhk6x4",202)] == 5
    # "CBPXs9Y9aqWlx60eg5XuDfCaX2Frfqz2rBHBPC9kGSN3QtA" won his 1 Galio game
    assert stats["Wins"].loc[("2voMrjFbfYuztOJhPlcpkv_hnTdnuSYmGNeMKt8dkH1Slw",3)] == 1
    
    # "w1a12jIle4QklqchWLP_rYe9Q06iuVbkbgP-7tQbIO-jlz0" won 5 times with Jhin in 6 games
    assert stats["Losses"].loc[("yF56aAqvE4rpVSyqCUN-MFGzqEdrCi83PHN6XoeaVBhk6x4",202)] == 1