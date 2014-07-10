version = "0.5"

# TODO: comment about why this is needed
class DbWrapper(object):
    def __init__(self):
        self.db = None

    def setDb(self, db):
        self.db = db

    def __getattr__(self, name):
        if not self.db:
            raise RuntimeError("No database configured")
        return getattr(self.db, name)

dbo = DbWrapper()
