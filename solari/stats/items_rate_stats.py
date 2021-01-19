from .stats_types import ItemStats, SpecialStats, DerivedStats
from .stats_managers import ItemStatsManager

class ItemPickrate(ItemStats):
    """Stats for pickrate per item
    
    Count the number of times an item was picked, and divide by the number of games and players.
    
    Allow for pickrate by item AND champion, and also per league.
    Multiple picks by the same player in the same game only counts as 1.
    
    Parameters
    ----------
    by_champion : boolean
        Default at False, determine if the stats is made by itemId or by (itemId, championId)
        
    by_league : boolean
        Default at False, determine if the stats groups by league.
    """
    
    name = "Pickrate"
    
    def __init__(self, by_champion=False, by_league = False):
        self._by_champion = by_champion
        self._by_league = by_league
    
    def get_keys(self):
        key = ("itemId",)
        
        if self._by_champion:
            key = ("championId",) + key
        
        if self._by_league:
            key = ("league",) + key
            
        return key
    
    def get_manager(self):
        return ItemStatsManager
    
    def get_stats_fields_required(self):
        return []
    
    def get_game_fields_required(self):
        return ["gameId"]
    
    def get_participant_fields_required(self):
        f = ["participantId"]
        if self._by_champion:
            f += ["championId"]
        return  f
    
    def get_id_fields_required(self):
        return ["summonerId"] if self._by_league else []
    
    def get_stats(self, df):
        groupby = list(self.get_keys())
        
        picks = (
            df.drop_duplicates(subset=["participantId","gameId","itemId"]).groupby(groupby)
                .count()
                ["gameId"]
        )
        
        opportunities = (
            df.drop_duplicates(subset=["participantId","gameId"]).groupby(groupby[:-1])
                .count()
                ["gameId"]
        ) if self._by_league or self._by_champion else len(df["gameId"].unique()) * 10
        
        return picks/opportunities
    
    
class ItemWinrate(ItemStats):
    """Stats for winrate per item
    
    Count the number of times an item was in a win, and divide by the number of picks
    
    Allow for winrate by item AND champion
    
    Parameters
    ----------
    by_champion : boolean
        Default at False, determine if the stats is made by itemId or by (itemId, championId)
        
    by_league : boolean
        Default at False, determine if the stats groups by league.
    """
    
    name = "Winrate"
    priority = 1
    
    def __init__(self, by_champion=False, by_league = False):
        self._by_champion = by_champion
        self._by_league = by_league
    
    def get_keys(self):
        key = ("itemId",)
        
        if self._by_champion:
            key = ("championId",) + key
        
        if self._by_league:
            key = ("league",) + key
            
        return key
    
    def get_manager(self):
        return ItemStatsManager
    
    def get_game_fields_required(self):
        return ["gameId"]
    
    def get_participant_fields_required(self):
        f = ["participantId"]
        if self._by_champion:
            f += ["championId"]
        return  f
    
    def get_stats_fields_required(self):
        return ["win"]
    
    def get_id_fields_required(self):
        return ["summonerId"] if self._by_league else []
    
    def get_stats(self, df):
        groupby = list(self.get_keys())
        
        picks = (
            df.drop_duplicates(subset=["participantId","gameId","itemId"]).groupby(groupby)
                .count()
                ["gameId"]
        )
        
        wins = (
            df.drop_duplicates(subset=["participantId","gameId","itemId"]).query('win == True')
                .groupby(groupby)
                .count()
                ["gameId"]
        )

        return (wins/picks).fillna(0)
    