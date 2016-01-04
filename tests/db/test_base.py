import unittest

from sqlalchemy import Column, Integer, String, create_engine

from balrog.db import Base, BalrogTable, Session, HistoryTable


class Foo(Base, BalrogTable):
    __tablename__ = "foo"
    id = Column(Integer(), primary_key=True)
    desc = Column(String(50))

    class History(HistoryTable):
        __tablename__ = "foo_history"

    def __init__(self, *args, **kwargs):
        Base.__init__(self, *args, **kwargs)
        BalrogTable.__init__(self, *args, **kwargs)

class TestCustomQuerying(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        Session.configure(bind=engine)
        session = Session()
        session.add(Foo(id=1, desc="first"))
        session.add(Foo(id=2, desc="second"))
        session.commit()

    def testDataVersionIncrease(self):
        session = Session()
        foo = session.query(Foo).filter(Foo.id==1).one()
        foo.desc = "firsted"
        session.add(foo)
        session.commit()
        self.assertEquals(session.query(Foo.data_version).filter(Foo.id==1).one()[0], 2)

    def testDataVersionRequired(self):
        session = Session()
        foo = session.query(Foo).filter(Foo.id==1).one()
        foo.desc = "firsted"
        session.add(foo)
        self.assertRaises(ValueError, session.commit)

    def testHistoryRowRecorded(self):
        pass

    def testRollback(self):
        pass
