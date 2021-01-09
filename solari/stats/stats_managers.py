import pandas as pd
from .stats_types import SpecialStats, DerivedStats

class StatsManager:
    """Abstract class defining the basis of Stats Managers
        
    Parameters
    ----------
    stats : list of Stats
        List of all instantiated Stats to be computed

    rank_manager : RankManager
        Manager for players rank
    """
    
    def __init__(self, stats, rank_manager):
        pass
    
    def push_game(self, match_data):
        """Process the match_data according to the needs of the Stats
        
        Parameters
        ----------
        match_data : dict
            Raw data from Riot API match-v4 endpoint

        """
        pass
    
    def get_stats(self):
        """Return the computed stats
            
        Returns
        -------
        stats : Pandas DataFrame
            Value of the computed stats grouped by the key
        """
        pass
    
class ChampionStatsManager(StatsManager):
    """Manager for Stats at Champion level
    
    This manager is aimed for Stats requiring a row per participant
        
    Parameters
    ----------
    stats : list of Stats
        List of all instantiated Stats to be computed
    
    rank_manager : RankManager
        Manager for players rank
    """
    
    def __init__(self, stats, rank_manager):
        self._stats_participants = []
        
        self._rank_manager = rank_manager
        
        game_fields = []
        participant_fields = []
        stats_fields = []
        id_fields = []
        
        for s in stats:
            game_fields += s.get_game_fields_required()
            participant_fields += s.get_participant_fields_required()
            stats_fields += s.get_stats_fields_required()
            id_fields += s.get_id_fields_required()
            
        self._game_fields = list(set(game_fields))
        self._participant_fields = list(set(participant_fields))
        self._stats_fields = list(set(stats_fields))
        self._id_fields = list(set(id_fields))
        
        self._stats = [s for s in stats if not issubclass(s.__class__, SpecialStats) and not issubclass(s.__class__, DerivedStats)]
        self._derived_stats = sorted([s for s in stats if not issubclass(s.__class__, SpecialStats) and issubclass(s.__class__, DerivedStats)], key=lambda s: s.priority)
        self._special_stats = [s for s in stats if issubclass(s.__class__, SpecialStats)]
        
        for s in self._special_stats:
            s.set_rank_manager(self._rank_manager)
        
        
    def push_game(self, match_data):
        
        for s in self._special_stats:
            s.push_game(match_data)
        
        
        if len(self._id_fields) > 0:
            ids = {}
            for p in match_data["participantIdentities"]:
                ids[p["participantId"]] = {}
                for i in self._id_fields:
                    ids[p["participantId"]][i] = p["player"][i]
        
        rows = []
        
        for p in match_data["participants"]:
            row = {f:p[f] for f in self._participant_fields}
            row.update({f:p["stats"][f] for f in self._stats_fields})
            row.update({f:match_data[f] for f in self._game_fields})
            if len(self._id_fields) > 0:
                row.update({f:ids[p["participantId"]][f] for f in self._id_fields})
            
            self._stats_participants.append(row)
        
    def get_stats(self):
        df = pd.DataFrame(self._stats_participants)
        
        if "summonerId" in df.columns.values:
            df["league"] = df["summonerId"].map(lambda x: self._rank_manager.get_rank(x))
        
        stats = {s.name:s.get_stats(df) for s in self._stats}
        
        stats.update({s.name:s.get_stats() for s in self._special_stats})
        
        for s in self._derived_stats:
            stats.update({s.name:s.get_stats(df, stats)})
        
        return pd.DataFrame(stats).fillna(0)
    
    
class ItemStatsManager(StatsManager):
    """Manager for Stats at Item level
    
    This manager is aimed for Stats requiring a row per item
        
    Parameters
    ----------
    stats : list of Stats
        List of all instantiated Stats to be computed
    
    rank_manager : RankManager
        Manager for players rank
    """
    
    def __init__(self, stats, rank_manager):
        self._stats_items = []
        
        self._rank_manager = rank_manager
        
        game_fields = []
        participant_fields = []
        stats_fields = []
        id_fields = []
        
        for s in stats:
            game_fields += s.get_game_fields_required()
            participant_fields += s.get_participant_fields_required()
            stats_fields += s.get_stats_fields_required()
            id_fields += s.get_id_fields_required()
            
        self._game_fields = list(set(game_fields))
        self._participant_fields = list(set(participant_fields))
        self._stats_fields = list(set(stats_fields))
        self._id_fields = list(set(id_fields))
        
        self._stats = [s for s in stats if not issubclass(s.__class__, SpecialStats) and not issubclass(s.__class__, DerivedStats)]
        self._derived_stats = sorted([s for s in stats if not issubclass(s.__class__, SpecialStats) and issubclass(s.__class__, DerivedStats)], key=lambda s: s.priority)
        self._special_stats = [s for s in stats if issubclass(s.__class__, SpecialStats)]
        
    def push_game(self, match_data):
        
        for s in self._special_stats:
            s.push_game(match_data)
        
        
        if len(self._id_fields) > 0:
            ids = {}
            for p in match_data["participantIdentities"]:
                ids[p["participantId"]] = {}
                for i in self._id_fields:
                    ids[p["participantId"]][i] = p["player"][i]
        
        rows = []
        
        for p in match_data["participants"]:
            for i in ["item0","item1","item2","item3","item4","item5","item6"]:
                if (item:= p["stats"][i]) > 0:
                    row = {f:p[f] for f in self._participant_fields}
                    row.update({f:p["stats"][f] for f in self._stats_fields})
                    row.update({f:match_data[f] for f in self._game_fields})
                    if len(self._id_fields) > 0:
                        row.update({f:ids[p["participantId"]][f] for f in self._id_fields})
                    row["itemId"] = item

                    self._stats_items.append(row)
        
    def get_stats(self):
        df = pd.DataFrame(self._stats_items)
        
        if "summonerId" in df.columns.values:
            df["league"] = df["summonerId"].map(lambda x: self._rank_manager.get_rank(x))
        
        stats = {s.name:s.get_stats(df) for s in self._stats}
        
        stats.update({s.name:s.get_stats() for s in self._special_stats})
        
        for s in self._derived_stats:
            stats.update({s.name:s.get_stats(df, stats)})
        
        return pd.DataFrame(stats).fillna(0)