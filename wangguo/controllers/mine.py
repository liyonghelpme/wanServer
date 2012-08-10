# -*- coding: utf-8 -*-
"""Fallback controller."""
from tg import expose, flash, require, url, request, redirect
from tg.i18n import ugettext as _, lazy_ugettext as l_
from wangguo import model
from repoze.what import predicates
from wangguo.controllers.secure import SecureController

from tgext.admin.tgadminconfig import TGAdminConfig
from tgext.admin.controller import AdminController

from wangguo.lib.base import BaseController
from wangguo.controllers.error import ErrorController
from wangguo.controllers.util import *

#from wangguo.model import DBSession, metadata
from wangguo.model import *

__all__ = ['GoodsController']


class MineController(BaseController):
    @expose('json')
    def upgradeMine(self, uid):
        uid = int(uid)

        user = getUser(uid)
        if user.colorCrystal >= 1:
            user.colorCrystal -= 1
            mine = DBSession.query(UserCrystalMine).filter_by(uid=uid).one()
            mine.level += 1
            return dict(id=1)
        return dict(id=0)
    @expose('json')
    def harvest(self, uid, crystal):
        uid = int(uid)
        crystal = int(crystal)

        mine = DBSession.query(UserCrystalMine).filter_by(uid=uid).one()
        now = getTime()
        mine.objectTime = now
        user = getUser(uid)
        user.crystal += crystal
        return dict(id=1)
