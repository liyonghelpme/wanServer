# -*- coding: utf-8 -*-
"""Sample model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
#from sqlalchemy.orm import relation, backref

from wangguo.model import DeclarativeBase, metadata, DBSession


class UserMessage(object):
    def __init__(self, uid, fid, kind, param, time):
        self.uid = uid
        self.fid = fid
        self.kind = kind
        self.param = param
        self.time = time
