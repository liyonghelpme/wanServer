# -*- coding: utf-8 -*-
"""Sample model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
#from sqlalchemy.orm import relation, backref

from wangguo.model import DeclarativeBase, metadata, DBSession


class UserInviteRank(object):
    def __init__(self, uid, inviteCode, inviteNum, rank, inputYet):
        self.uid = uid
        self.inviteCode = inviteCode
        self.inviteNum = inviteNum
        self.rank = rank
        self.inputYet = inputYet
