class NoMatchPushed(Exception):
    """
    No match pushed hence not able to compute stats
    """
    def __init__(self):
        Exception.__init__(self, "No match have been pushed.")
        
class MissingRequiredStats(Exception):
    """
    The computed stats needs another stats
    """
    def __init__(self):
        Exception.__init__(self, "A stats required to compute another is missing.")
        
class MismatchingLeona(Exception):
    """
    The given Leona instance has another configuration
    """
    def __init__(self):
        Exception.__init__(self, " The given Leona instance has another configuration.")
    