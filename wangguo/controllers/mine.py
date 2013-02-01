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
    #购买建筑 升级建筑 卖出建筑采用通用接口

    
    @expose('json')
    def upgradeMine(self, uid, bid, cost):
        uid = int(uid)
        bid = int(bid)
        cost = json.loads(cost)

        user = getUser(uid)
        ret = checkCost(uid, cost)
        if not ret:
            return dict(id=0)
        doCost(uid, cost)
        mine = DBSession.query(UserBuildings).filter_by(uid=uid, bid=bid).one()
        mine.level += 1
        return dict(id=1)

    @expose('json')
    def harvest(self, uid, bid, gain):
        uid = int(uid)
        bid = int(bid)
        gain = json.loads(gain)

        mine = DBSession.query(UserBuildings).filter_by(uid=uid, bid=bid).one()
        now = getTime()
        mine.objectTime = now
        doGain(uid, gain)
        return dict(id=1)
