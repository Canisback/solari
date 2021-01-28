from .stats_types import PlayerStats #, SpecialStats, DerivedStats
from .stats_managers import ChampionStatsManager

class PlayerPickrate(PlayerStats):
    """Stats for champion pickrate per player
    
    Count the number of times champion was picked, and divide by the number of games per players.
    
    Parameters
    ----------
    by_accountId : boolean
        Default at False, determine if the key should be accountId instead of summonerId
    """
    
    name = "Pickrate"
    
    def __init__(self, by_accountId=False):
        self._by_accountId = by_accountId
    
    def get_keys(self):
        key = ("championId",)
        
        if self._by_accountId:
            key = ("accountId",) + key
        else:
            key = ("summonerId",) + key
            
        return key
    
    def get_manager(self):
        return ChampionStatsManager
    
    def get_stats_fields_required(self):
        return []
    
    def get_game_fields_required(self):
        return ["gameId"]
    
    def get_participant_fields_required(self):
        f = ["participantId", "championId"]
        return  f
    
    def get_id_fields_required(self):
        return ["accountId"] if self._by_accountId else ["summonerId"]
    
    def get_stats(self, df):
        groupby = list(self.get_keys())
        
        picks = (
            df.groupby(groupby)
                .count()
                ["gameId"]
        )
        
        opportunities = (
            df.groupby(groupby[:-1])
                .count()
                ["gameId"]
        )
        
        return picks/opportunities

class PlayerPickCount(PlayerStats):
    """Stats for champion picks number per player
    
    Count the number of times champion was picked per players.
    
    Parameters
    ----------
    by_accountId : boolean
        Default at False, determine if the key should be accountId instead of summonerId
    """
    
    name = "Pick Count"
    
    def __init__(self, by_accountId=False):
        self._by_accountId = by_accountId
    
    def get_keys(self):
        key = ("championId",)
        
        if self._by_accountId:
            key = ("accountId",) + key
        else:
            key = ("summonerId",) + key
            
        return key
    
    def get_manager(self):
        return ChampionStatsManager
    
    def get_stats_fields_required(self):
        return []
    
    def get_game_fields_required(self):
        return ["gameId"]
    
    def get_participant_fields_required(self):
        f = ["participantId", "championId"]
        return  f
    
    def get_id_fields_required(self):
        return ["accountId"] if self._by_accountId else ["summonerId"]
    
    def get_stats(self, df):
        groupby = list(self.get_keys())
        
        picks = (
            df.groupby(groupby)
                .count()
                ["gameId"]
        )
        
        return picks

class PlayerWinrate(PlayerStats):
    """Stats for winrate per player
    
    Count the number of wins, and divide by the number of games per players.
    
    Allow for winrate by champion
    
    Parameters
    ----------
    by_accountId : boolean
        Default at False, determine if the key should be accountId instead of summonerId
        
    by_champion : boolean
        Default at False, determine if the stats is made by champion
    """
    
    name = "Winrate"
    
    def __init__(self, by_accountId=False, by_champion=False):
        self._by_accountId = by_accountId
        self._by_champion = by_champion
    
    def get_keys(self):
        if self._by_accountId:
            key = ("accountId",)
        else:
            key = ("summonerId",)
            
        if self._by_champion:
            key += ("championId",)
            
        return key
    
    def get_manager(self):
        return ChampionStatsManager
    
    def get_stats_fields_required(self):
        return ["win"]
    
    def get_game_fields_required(self):
        return ["gameId"]
    
    def get_participant_fields_required(self):
        f = ["participantId"]
        if self._by_champion:
            f += ["championId"]
        return  f
    
    def get_id_fields_required(self):
        return ["accountId"] if self._by_accountId else ["summonerId"]
    
    def get_stats(self, df):
        groupby = list(self.get_keys())
        
        picks = (
            df.groupby(groupby)
                .count()
                ["gameId"]
        )
        
        wins = (
            df[df["win"] == True].groupby(groupby)
                .count()
                ["gameId"]
        )

        return (wins/picks).fillna(0)


class PlayerWins(PlayerStats):
    """Stats for players number of wins
    
    Count the number of times a player won
    
    Allow for stats by champion
    
    Parameters
    ----------
    by_accountId : boolean
        Default at False, determine if the key should be accountId instead of summonerId
        
    by_champion : boolean
        Default at False, determine if the stats is made by champion
    """
    
    name = "Wins"
    
    def __init__(self, by_accountId=False, by_champion=False):
        self._by_accountId = by_accountId
        self._by_champion = by_champion
    
    def get_keys(self):        
        if self._by_accountId:
            key = ("accountId",)
        else:
            key = ("summonerId",)
            
        if self._by_champion:
            key += ("championId",)
        return key
    
    def get_manager(self):
        return ChampionStatsManager
    
    def get_stats_fields_required(self):
        return ["win"]
    
    def get_game_fields_required(self):
        return ["gameId"]
    
    def get_participant_fields_required(self):
        f = ["participantId"]
        if self._by_champion:
            f += ["championId"]
        return  f
    
    def get_id_fields_required(self):
        return ["accountId"] if self._by_accountId else ["summonerId"]
    
    def get_stats(self, df):
        groupby = list(self.get_keys())
        
        wins = (
            df[df["win"] == True].groupby(groupby)
                .count()
                ["gameId"]
        )
        
        return wins

class PlayerLosses(PlayerStats):
    """Stats for players number of losses
    
    Count the number of times a player lost
    
    Allow for stats by champion
    
    Parameters
    ----------
    by_accountId : boolean
        Default at False, determine if the key should be accountId instead of summonerId
        
    by_champion : boolean
        Default at False, determine if the stats is made by champion
    """
    
    name = "Losses"
    
    def __init__(self, by_accountId=False, by_champion=False):
        self._by_accountId = by_accountId
        self._by_champion = by_champion
    
    def get_keys(self):        
        if self._by_accountId:
            key = ("accountId",)
        else:
            key = ("summonerId",)
            
        if self._by_champion:
            key += ("championId",)
        return key
    
    def get_manager(self):
        return ChampionStatsManager
    
    def get_stats_fields_required(self):
        return ["win"]
    
    def get_game_fields_required(self):
        return ["gameId"]
    
    def get_participant_fields_required(self):
        f = ["participantId"]
        if self._by_champion:
            f += ["championId"]
        return  f
    
    def get_id_fields_required(self):
        return ["accountId"] if self._by_accountId else ["summonerId"]
    
    def get_stats(self, df):
        groupby = list(self.get_keys())
        
        losses = (
            df[df["win"] == False].groupby(groupby)
                .count()
                ["gameId"]
        )
        
        return losses