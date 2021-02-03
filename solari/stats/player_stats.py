from .stats_types import PlayerStats #, SpecialStats, DerivedStats
from .stats_managers import ChampionStatsManager
    
class PlayerGeneric(PlayerStats):
    """Stats for any single stats field under participants->stats by player
    
    Parameters
    ----------
    field : string
        The stats field that should be considered
        
    name : string, optional
        Rename the stats, default is the name of the field
        
    by_accountId : boolean
        Default at False, determine if the key should be accountId instead of summonerId
        
    by_champion : boolean
        Default at False, determine if the stats groups by champion.
    
    """
    
    name = "Generic"
    
    def __init__(self, field, name=None, by_accountId=False, by_champion = False):
        if name is None:
            self.name = field
        else:
            self.name = name
        
        self._field = field
        
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
    
    def get_game_fields_required(self):
        return ["gameId"]
    
    def get_participant_fields_required(self):
        return ["championId"]
    
    def get_stats_fields_required(self):
        return [self._field]
    
    def get_id_fields_required(self):
        return ["accountId"] if self._by_accountId else ["summonerId"]
    
    def get_stats(self, df):
        groupby = list(self.get_keys())
        return df.groupby(groupby).mean()[self._field]

    
class PlayerGenericPerMin(PlayerStats):
    """Stats for any single stats field under participants->stats by player
    
    Parameters
    ----------
    field : string
        The stats field that should be considered
        
    name : string, optional
        Rename the stats, default is the name of the field
        
    by_accountId : boolean
        Default at False, determine if the key should be accountId instead of summonerId
        
    by_champion : boolean
        Default at False, determine if the stats groups by champion.
    
    """
    
    name = "GenericPerMin"
    
    def __init__(self, field, name=None, by_accountId=False, by_champion = False):
        if name is None:
            self.name = field + "PerMin"
        else:
            self.name = name
        
        self._field = field
        
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
    
    def get_game_fields_required(self):
        return ["gameId", "gameDuration"]
    
    def get_participant_fields_required(self):
        return ["championId"]
    
    def get_stats_fields_required(self):
        return [self._field]
    
    def get_id_fields_required(self):
        return ["accountId"] if self._by_accountId else ["summonerId"]
    
    def get_stats(self, df):
        groupby = list(self.get_keys())
        df[self._field + "PerMin"] = df[self._field] * 60 / df["gameDuration"]
        return df.groupby(groupby).mean()[self._field + "PerMin"]
    

class PlayerKDA(PlayerStats):
    """Stats for KDA per player
    
    Count the KDA, and divide by the number of games per players.
    
    Allow for KDA by champion
    
    Parameters
    ----------
    by_accountId : boolean
        Default at False, determine if the key should be accountId instead of summonerId
        
    by_champion : boolean
        Default at False, determine if the stats is made by champion
    """
    
    name = "KDA"
    
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
    
    def get_game_fields_required(self):
        return ["gameId"]
    
    def get_stats_fields_required(self):
        return ["kills","deaths","assists"]
    
    def get_participant_fields_required(self):
        f = ["participantId"]
        if self._by_champion:
            f += ["championId"]
        return  f
    
    def get_id_fields_required(self):
        return ["accountId"] if self._by_accountId else ["summonerId"]
    
    def get_stats(self, df):
        groupby = list(self.get_keys())
        
        df["KDA"] = (df["kills"] + df["assists"]) / (df["deaths"].replace(0,1))
        
        return df.groupby(groupby).mean()["KDA"]
    
    
class PlayerKillParticipation(PlayerStats):
    """Stats for mean Kill Participation per player
    
    Allow for KP by champion
    
    Parameters
    ----------
    by_accountId : boolean
        Default at False, determine if the key should be accountId instead of summonerId
        
    by_champion : boolean
        Default at False, determine if the stats is made by champion
    """
    
    name = "KP"
    
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
    
    def get_game_fields_required(self):
        return ["gameId"]
    
    def get_participant_fields_required(self):
        return ["championId", "teamId"]
    
    def get_stats_fields_required(self):
        return ["kills","assists"]
    
    def get_id_fields_required(self):
        return ["accountId"] if self._by_accountId else ["summonerId"]
    
    def get_stats(self, df):
        groupby = list(self.get_keys())
        
        kp = df.groupby(["gameId","teamId"]).sum()["kills"]
        
        df["kp"] = (df["kills"] + df["assists"]) / [kp.loc[(i["gameId"],i["teamId"])] for k,i in df.iterrows()]
        
        return df.groupby(groupby).mean()["kp"]