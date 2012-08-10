# -*- coding: utf-8 -*-
"""Sample model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
#from sqlalchemy.orm import relation, backref

from wangguo.model import DeclarativeBase, metadata, DBSession


class UserGroupRank(object):
    def __init__(self, uid, score, rank, papayaId, name):
        self.uid = uid
        self.score = score
        self.rank = rank
        self.papayaId = papayaId
        self.name = name
