from .stats_types import ChampionStats, SpecialStats, DerivedStats, ChampionBanStats
from .stats_managers import ChampionStatsManager, ChampionDuplicateStatsManager

import pandas as pd
from functools import lru_cache
    
class ChampionPickrate(ChampionStats):
    """Stats for pickrate per champion
    
    Count the number of times a champion is picked, divided by the number of games.
    
    When computed per league, the strategy is to count the number of time a champion is picked by a player with a league, divided by the total number of champions picked by players in the same league.
    
    Parameters
    ----------
    by_league : boolean
        Default at False, determine if the stats groups by league.
    """
    
    name = "Pickrate"
    
    def __init__(self, by_league = False):
        self._by_league = by_league
    
    def get_keys(self):
        return ("league","championId",) if self._by_league else ("championId",)
    
    def get_manager(self):
        if self._by_league:
            return ChampionDuplicateStatsManager
        return ChampionStatsManager
    
    def get_game_fields_required(self):
        return ["gameId"]
    
    def get_participant_fields_required(self):
        return ["championId"]
    
    def get_id_fields_required(self):
        return ["summonerId"] if self._by_league else []
    
    def get_stats(self, df):
        groupby = list(self.get_keys())
        
        picks = (
            df.groupby(groupby)
                .count()
                ["gameId"]
        )
        
        opportunities = (
            df.groupby(["league"])
                .count()
                ["gameId"]
        ) / 10 if self._by_league else len(df["gameId"].unique())

        
        return (picks/opportunities)
    
class ChampionPickCount(ChampionStats):
    """Stats for number of picks per champion
    
    Count the number of times a champion is picked.
    
    Parameters
    ----------
    by_league : boolean
        Default at False, determine if the stats groups by league.
    """
    name = "Pick Count"
    
    def __init__(self, by_league = False):
        self._by_league = by_league
    
    def get_keys(self):
        return ("league","championId",) if self._by_league else ("championId",)
    
    def get_manager(self):
        if self._by_league:
            return ChampionDuplicateStatsManager
        return ChampionStatsManager
    
    def get_game_fields_required(self):
        return ["gameId"]
    
    def get_participant_fields_required(self):
        return ["championId"]
    
    def get_id_fields_required(self):
        return ["summonerId"] if self._by_league else []
    
    def get_stats(self, df):
        groupby = list(self.get_keys())
        picks = (
            df.groupby(groupby)
                .count()
                ["gameId"]
        )
        
        return picks
    
    
class ChampionWinrate(ChampionStats):
    """Stats for winrate per champion
    
    Count the number of times a champion won, divided by the number of picks.
    
    Parameters
    ----------
    by_league : boolean
        Default at False, determine if the stats groups by league.
    """
    name = "Winrate"
    
    def __init__(self, by_league = False):
        self._by_league = by_league
    
    def get_keys(self):
        return ("league","championId",) if self._by_league else ("championId",)
    
    def get_manager(self):
        if self._by_league:
            return ChampionDuplicateStatsManager
        return ChampionStatsManager
    
    def get_game_fields_required(self):
        return ["gameId"]
    
    def get_participant_fields_required(self):
        return ["championId"]
    
    def get_stats_fields_required(self):
        return ["win"]
    
    def get_id_fields_required(self):
        return ["summonerId"] if self._by_league else []
    
    def get_stats(self, df):
        groupby = list(self.get_keys())
        
        picks = (
            df.groupby(groupby)
                .count()
                ["gameId"]
        )
        
        wins = (
            df[df["win"]]
                .groupby(groupby)
                .count()
                ["gameId"]
        )

        return (wins/picks).fillna(0)
    
    
    
class ChampionBanrate(ChampionStats, ChampionBanStats):
    """Stats for banrate per champion
    
    Count the number of times a champion is banned, divided by the number of games, then multiplied by 10 (number of players per game).
    
    When computed per league, the count is duplicated for each different player league in the game.
    
    Parameters
    ----------
    team_wise : boolean
        Default at False, determine if a duplciate ban should be counted.
    by_league : boolean
        Default at False, determine if the stats groups by league.
    """
    name = "Banrate"
    
    def __init__(self, team_wise = False, by_league = False):
        self._team_wise = team_wise
        self._by_league = by_league
    
    def get_keys(self):
        return ("league","championId",) if self._by_league else ("championId",)
    
    def get_id_fields_required(self):
        return ["summonerId"] if self._by_league else []
    
    def get_game_fields_required(self):
        return ["gameId"]
    
    def get_manager(self):
        if self._by_league:
            return ChampionDuplicateStatsManager
        return ChampionStatsManager
                
    def get_stats(self, dfs):
        df = dfs[0]
        df_bans = dfs[1]
        
        groupby = list(self.get_keys())
        
        game_number = (
            df_bans.groupby(["league"])
                .count()
                ["gameId"]
        ) / 10 if self._by_league else len(df_bans["gameId"].unique())
        
        # game_number = len(df["gameId"].unique())
        
        if not self._team_wise:
            if self._by_league:
                df_bans.drop_duplicates(subset=["gameId","championId","league"], inplace=True)
            else:
                df_bans.drop_duplicates(subset=["gameId","championId"], inplace=True)
        
        bans = (
            df_bans.groupby(groupby)
                .count()
                ["gameId"]
        )
        
        return (bans/game_number)
    
class ChampionBanCount(ChampionStats, ChampionBanStats):
    """Stats for number of bans per champion
    
    Count the number of times a champion is banned, at max 1 per game.
    
    When computed per league, the count is duplicated for each different player league in the game.
    
    Parameters
    ----------
    team_wise : boolean
        Default at False, determine if a duplciate ban should be counted.
    by_league : boolean
        Default at False, determine if the stats groups by league.
    """
    name = "Ban Count"
    
    def __init__(self, team_wise = False, by_league = False):
        self._champion_bans = []
        self._team_wise = team_wise
        self._by_league = by_league
    
    def get_keys(self):
        return ("league","championId",) if self._by_league else ("championId",)
    
    def get_id_fields_required(self):
        return ["summonerId"] if self._by_league else []
    
    def get_game_fields_required(self):
        return ["gameId"]
    
    def get_manager(self):
        if self._by_league:
            return ChampionDuplicateStatsManager
        return ChampionStatsManager
                
    def get_stats(self, dfs):
        df, df_bans = dfs
        
        groupby = list(self.get_keys())
        
        if not self._team_wise:
            if self._by_league:
                df_bans.drop_duplicates(subset=["gameId","championId","league"], inplace=True)
            else:
                df_bans.drop_duplicates(subset=["gameId","championId"], inplace=True)
        
        bans = (
            df_bans.groupby(groupby)
                .count()
                ["gameId"]
        )
        
        return bans
    
class ChampionPresenceRate(ChampionStats, DerivedStats, ChampionBanStats):
    """Stats for presence per champion
    
    Add banrates and pickrates. Only works if the banrate strategy is set to the default one, instead of team wise.
    
    Parameters
    ----------
    by_league : boolean
        Default at False, determine if the stats groups by league.
    """
    name = "Presence"
    priority = 1
    
    def __init__(self, by_league = False):
        self._by_league = by_league
    
    def get_keys(self):
        return ("league","championId",) if self._by_league else ("championId",)
    
    def get_manager(self):
        if self._by_league:
            return ChampionDuplicateStatsManager
        return ChampionStatsManager
    
    def get_game_fields_required(self):
        return ["gameId"]
    
    def get_participant_fields_required(self):
        return ["championId"]
    
    def get_stats_fields_required(self):
        return ["win"]
    
    def get_id_fields_required(self):
        return ["summonerId"] if self._by_league else []
    
    def get_stats_required(self):
        return [ChampionPickrate, ChampionBanrate]
    
    def get_stats(self, dfs, stats):
        df, df_bans = dfs
        
        df_temp = pd.DataFrame()
        df_temp["pickrate"] = stats[ChampionPickrate.name]
        df_temp["banrate"] = stats[ChampionBanrate.name]
        
        df_temp = df_temp.fillna(0)
        
        ban_games = (
            df_bans.drop_duplicates(subset=["gameId","league"]).groupby(["league"])
                .count()
                ["gameId"]
        ) / 10 if self._by_league else len(df_bans["gameId"].unique())
        
        pick_games = (
            df.drop_duplicates(subset=["gameId","league"]).groupby(["league"])
                .count()
                ["gameId"]
        ) / 10 if self._by_league else len(df["gameId"].unique())
        
        return (df_temp["pickrate"] +( df_temp["banrate"] * (ban_games / pick_games )))