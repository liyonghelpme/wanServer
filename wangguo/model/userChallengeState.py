# -*- coding: utf-8 -*-
"""Sample model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
#from sqlalchemy.orm import relation, backref

from wangguo.model import DeclarativeBase, metadata, DBSession


class UserChallengeState(object):
    def __init__(self, uid, level, activeScore, protectTime):
        self.uid = uid
        self.level = level
        self.activeScore = activeScore
        self.protectTime = protectTime
