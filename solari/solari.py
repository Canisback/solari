from .stats.stats_managers import ChampionStatsManager, ItemStatsManager

class Leona:
    """
    Entrypoint for the match data and the stats that will be computed.

    Parameters
    ----------
    stats : list of Stats
        List of all instantiated Stats to be computed
    ...
    Methods
    -------
    push_match(match_data)
        Forward the raw match data from Riot API to the stats manager which will handle the stats
        
    get_stats(key=None)
        Return a list of key:DataFrame giving the computed stats
        
    get_keys()
        Get the list of keys that are used for the stats
    """
    
    def __init__(self, stats):
        
        keys_managers = []
        
        for s in stats:
            keys_managers.append({"keys":s.get_keys(),"manager":s.get_manager()})
            
        self._keys_managers = [i for n, i in enumerate(keys_managers) if i not in keys_managers[n + 1:]]
        
        self._stats_manager = {}
        
        for k in self._keys_managers:
            self._stats_manager[k["keys"]] = k["manager"]([s for s in stats if s.get_keys() == k["keys"]])
            
    def get_keys(self):
        """Get the list of keys that are used for the stats
        
        Returns
        -------
        keys : list of tuples
            The list of keys considered by the computed stats
        """
        return self._stats_manager.keys()
        
    def push_match(self, match_data):
        """Forward the raw match data from Riot API to the stats manager which will handle the stats

        Parameters
        ----------
        match_data : dict
            Raw data from Riot API match-v4 endpoint
        """
        
        for s in self._stats_manager:
            self._stats_manager[s].push_game(match_data)
        
    def get_stats(self, key=None):
        """Return a list of key:DataFrame giving the computed stats
        
        If a key is given, return only the corresponding DataFrame.
        If there is only one key available, return only the corresponding DataFrame.

        Parameters
        ----------
        key : tuple
            Specific key to consider when computing and returning stats.
            
        Returns
        -------
        stats : DataFrame or dict<key,DataFrame>
            The computed stats
        """
        
        if key is None:
            if len(self._stats_manager) > 1:
                return {k:v.get_stats() for k,v in self._stats_manager.items()}
            
            return next(iter(self._stats_manager.values())).get_stats()
        
        return self._stats_manager[key].get_stats()
