from .stats_types import ChampionStats, SpecialStats, DerivedStats
from .stats_managers import ChampionStatsManager

import pandas as pd
    
class ChampionPickrate(ChampionStats):
    
    name = "Pickrate"
    
    def __init__(self, by_league = False):
        self._by_league = by_league
    
    def get_keys(self):
        return ("championId",)
    
    def get_manager(self):
        return ChampionStatsManager
    
    def get_game_fields_required(self):
        return ["gameId"]
    
    def get_participant_fields_required(self):
        return ["championId"]
    
    def get_id_fields_required(self):
        return ["summonerId"] if self._by_league else []
    
    def get_stats(self, df):
        picks = (
            # We want champions
            df.groupby("championId")
                .count()
                ["gameId"]
        )
        
        return picks/len(df["gameId"].unique())
    
class ChampionPickCount(ChampionStats):
    
    name = "Count"
    
    def __init__(self, by_league = False):
        self._by_league = by_league
    
    def get_keys(self):
        return ("championId",)
    
    def get_manager(self):
        return ChampionStatsManager
    
    def get_game_fields_required(self):
        return ["gameId"]
    
    def get_participant_fields_required(self):
        return ["championId"]
    
    def get_id_fields_required(self):
        return ["summonerId"] if self._by_league else []
    
    def get_stats(self, df):
        picks = (
            # We want champions
            df.groupby("championId")
                .count()
                ["gameId"]
        )
        
        return picks
    
    
class ChampionWinrate(ChampionStats, DerivedStats):
    
    name = "Winrate"
    priority = 1
    
    def __init__(self, by_league = False):
        self._by_league = by_league
    
    def get_keys(self):
        return ("championId",)
    
    def get_manager(self):
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
        return [ChampionPickrate]
    
    def get_stats(self, df, stats):
        picks = stats[ChampionPickrate.name]
        
        wins = (
            # We want champions wins
            df[df["win"]]
                .groupby("championId")
                .count()
                ["gameId"]
        )

        return (wins/(picks*(len(df["gameId"].unique())))).fillna(0).sort_values(ascending=False)
    
    
    
class ChampionBanrate(ChampionStats, SpecialStats):
    
    name = "Banrate"
    
    def __init__(self, team_wise = False):
        self._champion_bans = []
        self._team_wise = team_wise
    
    def get_keys(self):
        return ("championId",)
    
    def get_manager(self):
        return ChampionStatsManager
    
    def push_game(self, game):
        for t in game["teams"]:
            for b in t["bans"]:
                self._champion_bans.append({"gameId":game["gameId"], "championId":b["championId"]})
                
    def get_stats(self):
        
        df = pd.DataFrame(self._champion_bans)
        
        game_number = len(df["gameId"].unique())
        
        if not self._team_wise:
            df.drop_duplicates(inplace=True)
        
        banrate = (
            # We want champions
            df.groupby("championId")
                .count()
                # Sorted by most banned champions
                .sort_values("championId", ascending=False)
                ["gameId"]
                # Divided by number of games to get a percentage
                /game_number
        )
        
        return banrate
    
class ChampionPresenceRate(ChampionStats, DerivedStats):
    
    name = "Presence"
    priority = 1
    
    def __init__(self, by_league = False):
        self._by_league = by_league
    
    def get_keys(self):
        return ("championId",)
    
    def get_manager(self):
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
    
    def get_stats(self, df, stats):
        picks = stats[ChampionPickrate.name]
        bans = stats[ChampionBanrate.name]
        
        return (picks + bans).fillna(0).sort_values(ascending=False)