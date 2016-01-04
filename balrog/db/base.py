from sqlalchemy import Column, Integer, String, event
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm.session import Session as SASession
from sqlalchemy.types import BigInteger


# TODO: need to define for mysql too?
TimestampInteger = BigInteger().with_variant(sqlite.INTEGER(), 'sqlite')


def onUpdate(mapper, connection, target):
    print target
    raise Exception()


class BalrogTable(object):
    data_version = Column(Integer(), default=1, nullable=False)
    
    def __init__(self, *args, **kwargs):
        event.listen(self, "before_update", onUpdate)
        super(BalrogTable, self).__init__(*args, **kwargs)


class HistoryTable(object):
    """Represents a history table that may be attached to another AUSTable.
       History tables mirror the structure of their `baseTable', with the exception
       that nullable and primary_key attributes are always overwritten to be
       True and False respectively. Additionally, History tables have a unique
       change_id for each row, and record the username making a change, and the
       timestamp of each change. The methods forInsert, forDelete, and forUpdate
       will generate appropriate INSERTs to the History table given appropriate
       inputs, and are documented below. History tables are never versioned,
       and cannot have history of their own."""

    change_id = Column(Integer(), primary_key=True, autoincrement=True)
    changed_by = Column(String(100), nullable=False)
    timestamp = Column(TimestampInteger, nullable=False)

    def getTimestamp(self):
        t = int(time.time() * 1000)
        return t
