from .stats_types import ChampionStats, SpecialStats, DerivedStats
from .stats_managers import ChampionStatsManager

import pandas as pd
    
class ChampionPickrate(ChampionStats):
    """Stats for pickrate per champion
    
    Count the number of times a champion is picked, divided by the number of games, then multiplied by 10 (number of players per game).
    
    When computed per league, the strategy is to count the number of time a champion is picked by a player with a league, divided by the total number of champions picked by players in the same league, then multipled by 10.
    
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
        ) if self._by_league else len(df["gameId"].unique())

        
        return (picks/opportunities) * 10
    
class ChampionPickCount(ChampionStats):
    """Stats for number of picks per champion
    
    Count the number of times a champion is picked.
    
    Parameters
    ----------
    by_league : boolean
        Default at False, determine if the stats groups by league.
    """
    name = "Count"
    
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

        return (wins/picks).fillna(0).sort_values(ascending=False)
    
    
    
class ChampionBanrate(ChampionStats, SpecialStats):
    """Stats for banrate per champion
    
    Count the number of times a champion is banned, divided by the number of games, then multiplied by 10 (number of players per game).
    
    When computed per league, the strategy is to count the number of time a champion is banned by a player with a league, divided by the total number of champions banned by players in the same league, then multipled by 10.
    
    Parameters
    ----------
    by_league : boolean
        Default at False, determine if the stats groups by league.
    """
    name = "Banrate"
    
    def __init__(self, team_wise = False, by_league = False):
        self._champion_bans = []
        self._team_wise = team_wise
        self._by_league = by_league
    
    def get_keys(self):
        return ("league","championId",) if self._by_league else ("championId",)
    
    def get_id_fields_required(self):
        return ["summonerId"] if self._by_league else []
    
    def get_manager(self):
        return ChampionStatsManager
    
    def push_game(self, match_data):
        if self._by_league:
            summonerIds = {}
            for p in match_data["participantIdentities"]:
                summonerIds[p["participantId"]] = p["player"]["summonerId"]
                    
        for t in match_data["teams"]:
            for b in t["bans"]:
                if self._by_league:
                    self._champion_bans.append({"gameId":match_data["gameId"], "championId":b["championId"], "summonerId": summonerIds[b["pickTurn"]]})
                else:
                    self._champion_bans.append({"gameId":match_data["gameId"], "championId":b["championId"]})
                
    def get_stats(self):
        groupby = list(self.get_keys())
        
        df = pd.DataFrame(self._champion_bans)
        
        if self._by_league:
            df["league"] = df["summonerId"].map(lambda x: self._rank_manager.get_rank(x))
        
        
        
        game_number = (
            df.groupby(["league"])
                .count()
                ["gameId"]
        ) if self._by_league else len(df["gameId"].unique())
        
        # game_number = len(df["gameId"].unique())
        
        if not self._team_wise:
            df.drop_duplicates(inplace=True)
        
        bans = (
            df.groupby(groupby)
                .count()
                ["gameId"]
        )
        
        return (bans/game_number) * 10
    
class ChampionPresenceRate(ChampionStats, DerivedStats):
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