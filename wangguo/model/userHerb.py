# -*- coding: utf-8 -*-
"""Sample model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
#from sqlalchemy.orm import relation, backref

from wangguo.model import DeclarativeBase, metadata, DBSession


class UserHerb(object):
    def __init__(self, uid, kind, num):
        self.uid = uid
        self.kind = kind
        self.num = num
