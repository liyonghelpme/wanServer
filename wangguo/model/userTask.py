# -*- coding: utf-8 -*-
"""Sample model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
#from sqlalchemy.orm import relation, backref

from wangguo.model import DeclarativeBase, metadata, DBSession


class UserTask(object):
    def __init__(self, uid, tid, number, finish, stage):
        self.uid = uid
        self.tid = tid
        self.number = number
        self.finish = finish
        self.stage = stage
