# -*- coding: utf-8 -*-
"""Sample model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
#from sqlalchemy.orm import relation, backref

from wangguo.model import DeclarativeBase, metadata, DBSession


class UserEquips(object):
    def __init__(self, uid, eid, equipKind):
        self.uid = uid
        self.eid = eid
        self.equipKind = equipKind
        self.level = 0
        self.owner = -1
