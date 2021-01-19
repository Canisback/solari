from solari import Leona
from solari.solari import RankManager

def test_set_rank():
    rm = RankManager()
    
    rm.set_rank("player","rank")
    
    assert rm._players_rank["player"] == "rank"
    
def test_get_rank():
    rm = RankManager()
    
    rm.set_rank("player","rank")
    
    assert rm.get_rank("player") == "rank"
    
def test_get_rank_unranked():
    rm = RankManager()
    
    rm.set_rank("player","rank")
    
    assert rm.get_rank("player_2") == "UNRANKED"
    
def test_set_players_rank():
    rm = RankManager()
    
    rm.set_players_rank({"player":"rank"})
    
    assert rm.get_rank("player") == "rank"