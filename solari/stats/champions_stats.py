from .stats_types import ChampionStats, SpecialStats, DerivedStats
from .stats_managers import ChampionStatsManager

class ChampionGeneric(ChampionStats):
    """Stats for any single stats field under participants->stats
    
    Parameters
    ----------
    field : string
        The stats field that should be considered
        
    name : string, optional
        Rename the stats, default is the name of the field
        
    by_league : boolean
        Default at False, determine if the stats groups by league.
    
    """
    
    name = "Generic"
    
    def __init__(self, field, name=None, by_league = False):
        if name is None:
            self.name = field
        else:
            self.name = name
        
        self._field = field
        
        self._by_league = by_league
    
    def get_keys(self):
        return ("league","championId",) if self._by_league else ("championId",)
    
    def get_manager(self):
        return ChampionStatsManager
    
    def get_game_fields_required(self):
        return ["gameId"]
    
    def get_participant_fields_required(self):
        return ["championId"]
    
    def get_stats_fields_required(self):
        return [self._field]
    
    def get_id_fields_required(self):
        return ["summonerId"] if self._by_league else []
    
    def get_stats(self, df):
        groupby = list(self.get_keys())
        return df.groupby(groupby).mean()[self._field]

    
class ChampionGenericPerMin(ChampionStats):
    """Stats for any single stats field under participants->stats
    
    Parameters
    ----------
    field : string
        The stats field that should be considered
        
    name : string, optional
        Rename the stats, default is the name of the field
        
    by_league : boolean
        Default at False, determine if the stats groups by league.
    
    """
    
    name = "GenericPerMin"
    
    def __init__(self, field, name=None, by_league = False):
        if name is None:
            self.name = field + "PerMin"
        else:
            self.name = name
        
        self._field = field
        
        self._by_league = by_league
    
    def get_keys(self):
        return ("league","championId",) if self._by_league else ("championId",)
    
    def get_manager(self):
        return ChampionStatsManager
    
    def get_game_fields_required(self):
        return ["gameId", "gameDuration"]
    
    def get_participant_fields_required(self):
        return ["championId"]
    
    def get_stats_fields_required(self):
        return [self._field]
    
    def get_id_fields_required(self):
        return ["summonerId"] if self._by_league else []
    
    def get_stats(self, df):
        groupby = list(self.get_keys())
        df[self._field + "PerMin"] = df[self._field] / (df["gameDuration"] / 60)
        return df.groupby(groupby).mean()[self._field + "PerMin"]

class ChampionKDA(ChampionStats):
    """Stats for mean KDA per champion
    
    If the number of deaths is 0, to avoid division by 0, the number of deaths is set to 1.
    
    Parameters
    ----------
    by_league : boolean
        Default at False, determine if the stats groups by league.
    """
    
    name = "KDA"
    
    def __init__(self, by_league = False):
        self._by_league = by_league
    
    def get_keys(self):
        return ("league","championId",) if self._by_league else ("championId",)
    
    def get_manager(self):
        return ChampionStatsManager
    
    def get_game_fields_required(self):
        return ["gameId"]
    
    def get_participant_fields_required(self):
        return ["championId"]
    
    def get_stats_fields_required(self):
        return ["kills","deaths","assists"]
    
    def get_id_fields_required(self):
        return ["summonerId"] if self._by_league else []
    
    def get_stats(self, df):
        groupby = list(self.get_keys())
        
        df["KDA"] = (df["kills"] + df["assists"]) / (df["deaths"].replace(0,1))
        
        return df.groupby(groupby).mean()["KDA"]

    
class ChampionKillParticipation(ChampionStats):
    """Stats for mean Kill Participation per champion
    
    Parameters
    ----------
    by_league : boolean
        Default at False, determine if the stats groups by league.
    """
    
    name = "KP"
    
    def __init__(self, by_league = False):
        self._by_league = by_league
    
    def get_keys(self):
        return ("league","championId",) if self._by_league else ("championId",)
    
    def get_manager(self):
        return ChampionStatsManager
    
    def get_game_fields_required(self):
        return ["gameId"]
    
    def get_participant_fields_required(self):
        return ["championId", "teamId"]
    
    def get_stats_fields_required(self):
        return ["kills","assists"]
    
    def get_id_fields_required(self):
        return ["summonerId"] if self._by_league else []
    
    def get_stats(self, df):
        groupby = list(self.get_keys())
        
        kp = df.groupby(["gameId","teamId"]).sum()["kills"]
        
        df["kp"] = (df["kills"] + df["assists"]) / [kp.loc[(i["gameId"],i["teamId"])] for k,i in df.iterrows()]
        
        return df.groupby(groupby).mean()["kp"]