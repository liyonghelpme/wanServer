# -*- coding: utf-8 -*-
"""Sample model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
#from sqlalchemy.orm import relation, backref

from wangguo.model import DeclarativeBase, metadata, DBSession


class UserBuildings(object):
    def __init__(self, uid, bid, kind, px, py, state, color=0):
        self.uid = uid
        self.bid = bid
        self.kind = kind
        self.px = px
        self.py = py
        self.state = state
        self.color = color
