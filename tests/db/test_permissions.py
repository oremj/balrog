import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from balrog.db import Base, Session, Permissions


class TestPermissions(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        Session.configure(bind=engine)
        session = Session()
        session.add(Permissions(permission="/rules", username="cathy"))

    def testGrantPermission(self):
        session = Session()
        self.assertEquals(session.query(Permissions).filter_by(username="jess").count(), 0)
        session.add(Permissions(permission="/rules/:id", username="jess"))
        ret = session.query(Permissions).filter_by(username="jess").all()
        self.assertEquals(len(ret), 1)
        ret = ret[0]
        self.assertEquals(ret.permission, "/rules/:id")
        self.assertEquals(ret.username, "jess")
        self.assertEquals(ret.options, None)
        self.assertEquals(ret.data_version, 1)

#    def testUpdatePermission(self):
#        session = Session()
#        session.add(Permissions(username="cathy", permission="/rules/:id", 1, {"method": "POST"}))
#        ret = session.query(Permissions).filter_by(username="cathy").all()
#        self.assertEquals(len(ret), 1)
#        ret = ret[0]
#        self.assertEquals(ret.permission, "/rules/:id")
#        self.assertEquals(ret.username, "cathy")
#        self.assertEquals(ret.options, '{"method": "POST"}')
#        self.assertEquals(ret.data_version, 2)
