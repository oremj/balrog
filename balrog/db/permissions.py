import json

from sqlalchemy import Column, Integer, String, Table, Text
from sqlalchemy.orm import validates
from sqlalchemy.orm.query import Query

from . import Base
from .base import HistoryTable


class PermissionsBase(object):
    __tablename__ = "permissions"
    permission = Column(String(50), primary_key=True)
    username = Column(String(100), primary_key=True)
    options = Column(Text())
    data_version = Column(Integer(), default=1, nullable=False)


class Permissions(PermissionsBase, Base):
    class History(HistoryTable, PermissionsBase, Base):
        __tablename__ = "permissions_history"

    """allPermissions defines the structure and possible options for all
       available permissions. Most permissions are identified by an URL,
       potentially with variables in it. All URL based permissions can be
       augmented by using the "product" option. When specified, only requests
       involving the named product will be permitted. Additionally, any URL
       that supports more than one of: PUT, POST, or DELETE can by augmented
       by using the option "method". When specified, the permission with this
       option is only valid for requests through that HTTP method."""
    allPermissions = {
        'admin': [],
        '/releases/:name': ['method', 'product'],
        '/releases/:name/rollback': ['product'],
        '/releases/:name/builds/:platform/:locale': ['method', 'product'],
        '/rules': ['product'],
        '/rules/:id': ['method', 'product'],
        '/rules/:id/rollback': ['product'],
        '/users/:id/permissions/:permission': ['method'],
    }

    @validates("permission")
    def validatePermissionExists(self, key, permission):
        if permission not in Permissions.allPermissions:
            raise ValueError('Unknown permission "{}"'.format(permission))
        return permission

    @validates("options")
    def validateOptionsExist(self, key, options):
        print key
        raise ValueError()
        #for opt in options:
        #    if opt not in Permissions.allPermissions[permission]:
        #        raise ValueError('Unknown option "%s" for permission "%s"' % (opt, permission))

    # THIS ACTUALLY WORKS OMG OMG
    # Can we do it without passing session? Maybe a global objcet that we can get a new session from? Or can we return a query object and let the caller deal with the session?
    @classmethod
    def getAllUsers(cls):
        return Query(cls.username).distinct()

    @classmethod
    def grantPermission(cls, changed_by, username, permission, options=None):
        # TODO: can this assertion happen at the web layer instead?
        Permissions.assertPermissionExists(permission)
        if options:
            Permissions.assertOptionsExist(permission, options)
            options = json.dumps(options)
        # TODO: need something in a universal base to do history
        return cls(username=username, permission=permission, options=options)

    @classmethod
    def updatePermission(cls, changed_by, username, permission, old_data_version, options=None):
        Permissions.assertPermissionExists(permission)
        if options:
            Permissions.assertOptionsExist(permission, options)
            options = json.dumps(options)
        return cls(username=username, permission=permission, options=options)
