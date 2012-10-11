# -*- coding: utf-8 -*-
"""Sample model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
#from sqlalchemy.orm import relation, backref

from wangguo.model import DeclarativeBase, metadata, DBSession


class UserGift(object):
    def __init__(self, uid, fid, kind, tid, level, time, gid):
        self.uid = uid
        self.fid = fid
        self.kind = kind
        self.tid = tid
        self.level = level
        self.time = time
        self.gid = gid
