class Stats:
    """Abstract class defining the basis of all Stats
    
    """
    
    def get_keys(self):
        """Return the keys of the Stats
            
        Returns
        -------
        keys : tuple of strings
            Key for the Stats
        """
        return ()
    
    def get_manager(self):
        """Return the StatsManager required
            
        Returns
        -------
        stats_manager : StatsManager
            StatsManager for the Stats
        """
        pass
    
    def get_game_fields_required(self):
        """Return the required fields at game level
            
        Returns
        -------
        game_fields_required : list of strings
            List of fields
        """
        return []
    
    def get_participant_fields_required(self):
        """Return the required fields at participant level
            
        Returns
        -------
        participant_fields_required : list of strings
            List of fields
        """
        return []
    
    def get_stats_fields_required(self):
        """Return the required fields at stats level
            
        Returns
        -------
        stats_fields_required : list of strings
            List of fields
        """
        return []
    
    def get_id_fields_required(self):
        """Return the required fields at ID level
            
        Returns
        -------
        id_fields_required : list of strings
            List of fields
        """
        return []
    
    def get_stats(self, df):
        """Return the computed stats
        
        Parameters
        ----------
        df : Pandas DataFrame
            DataFrame containing all fields required to compute the stats
            
        Returns
        -------
        stats : Pandas Series
            Value oif the computed stats grouped by the key
        """
        pass
    

class ChampionStats(Stats):
    """Abstract class defining a Stats for Champions
    
    """
    pass

class ItemStats(Stats):
    """Abstract class defining a Stats for Items
    
    """
    pass

class SpecialStats(Stats):
    """Abstract class defining a Stats that will handle itself the game data
    
    """
    
    def push_game(self, game):
        pass
    
    def get_stats(self):
        pass

class DerivedStats(Stats):
    """Abstract class defining a Stats that is derived from another and must be computed afterward
    
    """
    
    order = 0
    
    def get_stats(self, df, stats):
        pass
    
    def get_stats_required(self):
        return []