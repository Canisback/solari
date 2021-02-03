import pandas as pd
from functools import lru_cache
from .stats_types import SpecialStats, DerivedStats, ChampionBanStats
from ..exceptions import MissingRequiredStats

class StatsManager: # pragma: no cover
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
        
    Raises
    ------
    MissingRequiredStats
        If a required stats from Derived Stats are missing
    """
    
    def __init__(self, stats, rank_manager):
        self._stats_participants = []
        self._champion_bans = []
        
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
        
        self._ban_stats = any([issubclass(s.__class__, ChampionBanStats) for s in stats])
        
        for s in self._special_stats:
            s.set_rank_manager(self._rank_manager)
        
        # Listing all required stats for derived stats
        derived_required = list(set([i for j in self._derived_stats for i in j.get_stats_required()]))
        if not all([any([isinstance(s, d) for s in stats]) for d in derived_required]):
            raise MissingRequiredStats
        
    def push_game(self, match_data):
        
        for s in self._special_stats:
            s.push_game(match_data)
        
        
        if len(self._id_fields) > 0:
            ids = {}
            for p in match_data["participantIdentities"]:
                ids[p["participantId"]] = {}
                for i in self._id_fields:
                    ids[p["participantId"]][i] = p["player"][i]
        
        for p in match_data["participants"]:
            row = {f:p[f] for f in self._participant_fields}
            row.update({f:p["stats"][f] for f in self._stats_fields})
            row.update({f:match_data[f] for f in self._game_fields})
            if len(self._id_fields) > 0:
                row.update({f:ids[p["participantId"]][f] for f in self._id_fields})
            
            self._stats_participants.append(row)
            
        if self._ban_stats:
            for t in match_data["teams"]:
                for b in t["bans"]:
                    self._champion_bans.append({"gameId":match_data["gameId"], "championId":b["championId"]})
        
    def get_stats(self):
        df = pd.DataFrame(self._stats_participants)
        
        if "summonerId" in df.columns.values:
            df["league"] = df["summonerId"].map(lambda x: self._rank_manager.get_rank(x))
            
        
        if self._ban_stats:
            df_bans = pd.DataFrame(self._champion_bans)
            if "summonerId" in df_bans.columns.values:
                df_bans["league"] = df_bans["summonerId"].map(lambda x: self._rank_manager.get_rank(x))
        
        stats = {s.name:s.get_stats(df if not issubclass(s.__class__, ChampionBanStats) else (df,df_bans)) for s in self._stats}
        
        stats.update({s.name:s.get_stats() for s in self._special_stats})
        
        for s in self._derived_stats:
            stats.update({s.name:s.get_stats(df if not issubclass(s.__class__, ChampionBanStats) else (df,df_bans), stats)})
        
        return pd.DataFrame(stats).fillna(0, downcast="infer")
    
    
class ChampionDuplicateStatsManager(StatsManager):
    """Manager for Stats at Champion level, duplicated by league
    
    This manager is aimed for Stats requiring a row per participant and per league, for champion rate stats per league
        
    Parameters
    ----------
    stats : list of Stats
        List of all instantiated Stats to be computed
    
    rank_manager : RankManager
        Manager for players rank
        
    Raises
    ------
    MissingRequiredStats
        If a required stats from Derived Stats are missing
    """
    
    def __init__(self, stats, rank_manager):
        self._stats_participants = []
        self._champion_bans = []
        
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
        
        self._ban_stats = any([issubclass(s.__class__, ChampionBanStats) for s in stats])
        
        # Listing all required stats for derived stats
        derived_required = list(set([i for j in self._derived_stats for i in j.get_stats_required()]))
        if not all([any([isinstance(s, d) for s in stats]) for d in derived_required]):
            raise MissingRequiredStats
            
            
    def push_game(self, match_data):
        
        for s in self._special_stats:
            s.push_game(match_data)
        
        
        if len(self._id_fields) > 0:
            ids = {}
            for p in match_data["participantIdentities"]:
                ids[p["participantId"]] = {}
                for i in self._id_fields:
                    ids[p["participantId"]][i] = p["player"][i]
        
        for p in match_data["participants"]:
            row = {f:p[f] for f in self._participant_fields}
            row.update({f:p["stats"][f] for f in self._stats_fields})
            row.update({f:match_data[f] for f in self._game_fields})
            if len(self._id_fields) > 0:
                row.update({f:ids[p["participantId"]][f] for f in self._id_fields})
            
            self._stats_participants.append(row)
            
        if self._ban_stats:
            for t in match_data["teams"]:
                for b in t["bans"]:
                    self._champion_bans.append({"gameId":match_data["gameId"], "championId":b["championId"], "summonerId": ids[b["pickTurn"]]["summonerId"]})
        
    def get_stats(self):
        df = pd.DataFrame(self._stats_participants)
        
        df["league"] = df["summonerId"].map(lambda x: self._rank_manager.get_rank(x))
            
        # Creating the list of different leagues present in each game
        league_per_gameId = df.groupby(["gameId"])["league"].unique()
        @lru_cache(maxsize=1)
        def get_league_per_gameId(gameId):
            return league_per_gameId.loc[gameId]
        
        # One entry for each different league in the game
        entries = []
        for i, row in df.iterrows():
            for lbg in get_league_per_gameId(row["gameId"]):
                row["league"] = lbg
                entries.append(row.to_dict())
                
        # Dataframe with the duplicates
        df_entries = pd.DataFrame(entries)
        
        
        if self._ban_stats:
            df_bans = pd.DataFrame(self._champion_bans)
            df_bans["league"] = df_bans["summonerId"].map(lambda x: self._rank_manager.get_rank(x))
                
            entries = []
            for i, row in df_bans.iterrows():
                for lbg in get_league_per_gameId(row["gameId"]):
                    row["league"] = lbg
                    entries.append(row.to_dict())
            df_bans_entries = pd.DataFrame(entries)
        
        stats = {s.name:s.get_stats(df_entries if not issubclass(s.__class__, ChampionBanStats) else (df_entries,df_bans_entries)) for s in self._stats}
        
        stats.update({s.name:s.get_stats() for s in self._special_stats})
        
        for s in self._derived_stats:
            stats.update({s.name:s.get_stats(df_entries if not issubclass(s.__class__, ChampionBanStats) else (df_entries,df_bans_entries), stats)})
        
        return pd.DataFrame(stats).fillna(0, downcast="infer")
    
    
class ItemStatsManager(StatsManager):
    """Manager for Stats at Item level
    
    This manager is aimed for Stats requiring a row per item
        
    Parameters
    ----------
    stats : list of Stats
        List of all instantiated Stats to be computed
    
    rank_manager : RankManager
        Manager for players rank
        
    Raises
    ------
    MissingRequiredStats
        If a required stats from Derived Stats are missing
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
        
        # Listing all required stats for derived stats
        derived_required = list(set([i for j in self._derived_stats for i in j.get_stats_required()]))
        if not all([any([isinstance(s, d) for s in stats]) for d in derived_required]):
            raise MissingRequiredStats
        
        
    def push_game(self, match_data):
        
        for s in self._special_stats:
            s.push_game(match_data)
        
        
        if len(self._id_fields) > 0:
            ids = {}
            for p in match_data["participantIdentities"]:
                ids[p["participantId"]] = {}
                for i in self._id_fields:
                    ids[p["participantId"]][i] = p["player"][i]
        
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
        
        return pd.DataFrame(stats).fillna(0, downcast="infer")
    