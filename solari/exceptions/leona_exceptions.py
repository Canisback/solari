class NoMatchPushed(Exception):
    def __init__(self):
        Exception.__init__(self, "No match have been pushed.")