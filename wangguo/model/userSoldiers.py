# -*- coding: utf-8 -*-
"""Sample model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
#from sqlalchemy.orm import relation, backref

from wangguo.model import DeclarativeBase, metadata, DBSession


class UserSoldiers(object):
    def __init__(self, uid, sid, kind, name):
        self.uid = uid
        self.sid = sid
        self.kind = kind
        self.name = name
