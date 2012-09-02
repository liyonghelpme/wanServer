# -*- coding: utf-8 -*-
"""Sample model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
#from sqlalchemy.orm import relation, backref

from wangguo.model import DeclarativeBase, metadata, DBSession


#每周清理一次周数据
class UserHeart(object):
    def __init__(self, uid, weekNum, accNum, liveNum):
        self.uid = uid
        self.weekNum = weekNum
        self.accNum = accNum
        self.liveNum = liveNum
