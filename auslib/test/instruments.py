import inspect

import simplejson

import auslib.db

origDumps = simplejson.dumps
origLoads = simplejson.loads
origSelect = auslib.db.AUSTable.select
origUpdate = auslib.db.AUSTable.update
origInsert = auslib.db.AUSTable.insert
origDelete = auslib.db.AUSTable.delete

def getCaller():
    """Returns the name of the function that called the function that called us.
       We need to walk two frames up because the first frame is us, and the
       second is our caller."""
    frameInfo = inspect.getframeinfo(inspect.stack()[2][0])
    return (frameInfo[0], frameInfo[1], frameInfo[2])
    return inspect.getframeinfo(inspect.stack()[2][0])[2]

def instrumentJSON(counts):
    def dumps(*args, **kwargs):
        counts['dumps'].append(getCaller())
        return origDumps(*args, **kwargs)

    def loads(*args, **kwargs):
        counts['loads'].append(getCaller())
        return origLoads(*args, **kwargs)

    simplejson.dumps = dumps
    simplejson.loads = loads


def resetJSON():
    simplejson.dumps = origDumps
    simplejson.loads = origLoads


def instrumentAUSTable(counts):
    def select(self, *args, **kwargs):
        counts['select'].append(getCaller())
        return origSelect(self, *args, **kwargs)

    def update(self, *args, **kwargs):
        counts['update'].append(getCaller())
        return origUpdate(self, *args, **kwargs)

    def insert(self, *args, **kwargs):
        counts['insert'].append(getCaller())
        return origInsert(self, *args, **kwargs)

    def delete(self, *args, **kwargs):
        counts['delete'].append(getCaller())
        return origDelete(self, *args, **kwargs)

    auslib.db.AUSTable.select = select
    auslib.db.AUSTable.update = update
    auslib.db.AUSTable.insert = insert
    auslib.db.AUSTable.delete = delete

def resetAUSTable():
    auslib.db.AUSTable.select = origSelect
    auslib.db.AUSTable.update = origSelect
    auslib.db.AUSTable.insert = origSelect
    auslib.db.AUSTable.delete = origSelect
