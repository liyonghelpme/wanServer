# -*- coding: utf-8 -*-
"""Sample model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
#from sqlalchemy.orm import relation, backref

from wangguo.model import DeclarativeBase, metadata, DBSession


class UserCrystalMine(object):
    def __init__(self, uid, px, py, state, objectTime, level, bid):
        self.uid = uid
        self.px = px
        self.py = py
        self.state = state
        self.objectTime = objectTime
        self.state = state
        self.bid = bid

