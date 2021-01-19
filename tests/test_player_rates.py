from solari import Leona
from solari.stats import PlayerPickrate, PlayerWinrate

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