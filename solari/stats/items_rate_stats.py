from .stats_types import ItemStats, SpecialStats, DerivedStats
from .stats_managers import ItemStatsManager

class ItemPickrate(ItemStats):
    """Stats for pickrate per item
    
    Count the number of times an item was picked, and divide by the number of games and players
    
    Allow for pickrate by item AND champion
    
    Parameters
    ----------
    by_champion : boolean
        Default at False, determine if the stats is made by itemId or by (itemId, championId)
    """
    
    name = "Pickrate"
    
    def __init__(self, by_champion=False, by_league = False):
        self._by_champion = by_champion
        self._by_league = by_league
    
    def get_keys(self):
        return ("itemId",) if not self._by_champion else ("championId","itemId")
    
    def get_manager(self):
        return ItemStatsManager
    
    def get_game_fields_required(self):
        return ["gameId"]
    
    def get_participant_fields_required(self):
        return ["participantId"] if not self._by_champion else ["championId"]
    
    def get_id_fields_required(self):
        return ["summonerId"] if self._by_league else []
    
    def get_stats(self, df):
        groupby = "itemId" if not self._by_champion else ["championId","itemId"]
        
        picks = (
            # We want items
            df.groupby(groupby)
                .count()
                ["gameId"]
        )
        
        return picks/(len(df["gameId"].unique()) *10)
    
    
class ItemWinrate(ItemStats, DerivedStats):
    """Stats for winrate per item
    
    Count the number of times an item was in a win, and divide by the number of picks
    
    Allow for winrate by item AND champion
    
    Parameters
    ----------
    by_champion : boolean
        Default at False, determine if the stats is made by itemId or by (itemId, championId)
    """
    
    name = "Winrate"
    priority = 1
    
    def __init__(self, by_champion=False, by_league = False):
        self._by_champion = by_champion
        self._by_league = by_league
    
    def get_keys(self):
        return ("itemId",) if not self._by_champion else ("championId","itemId")
    
    def get_manager(self):
        return ItemStatsManager
    
    def get_game_fields_required(self):
        return ["gameId"]
    
    def get_participant_fields_required(self):
        return [] if not self._by_champion else ["championId"]
    
    def get_stats_fields_required(self):
        return ["win"]
    
    def get_id_fields_required(self):
        return ["summonerId"] if self._by_league else []
    
    def get_stats_required(self):
        return [ItemPickrate]
    
    def get_stats(self, df, stats):
        picks = stats[ItemPickrate.name]
        
        groupby = "itemId" if not self._by_champion else ["championId","itemId"]
        
        wins = (
            # We want item wins
            df[df["win"]]
                .groupby(groupby)
                .count()
                ["gameId"]
        )

        return (wins/(picks*(len(df["gameId"].unique()) *10))).fillna(0).sort_values(ascending=False)
    