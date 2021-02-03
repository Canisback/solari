class NoMatchPushed(Exception):
    """
    No match pushed hence not able to compute stats
    """
    def __init__(self):
        Exception.__init__(self, "No match have been pushed.")
        
class MissingRequiredStats(Exception):
    """
    No match pushed hence not able to compute stats
    """
    def __init__(self):
        Exception.__init__(self, "A stats required to compute another is missing.")