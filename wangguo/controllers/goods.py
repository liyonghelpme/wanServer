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


class GoodsController(BaseController):
    #购买物品 消耗资源
    @expose('json')
    def buyDrug(self, uid, drugKind):
        uid = int(uid)
        drugKind = int(drugKind)

        cost = getCost('drug', drugKind)
        ret = checkCost(uid, cost)
        if not ret:
            return dict(id=0)

        try:
            drug = DBSession.query(UserDrugs).filter_by(uid=uid).filter_by(drugKind=drugKind).one()
        except:
            drug = UserDrugs(uid=uid, drugKind=drugKind, num = 0)
            DBSession.add(drug)
        drug.num += 1


        doCost(uid, cost)
        return dict(id=1)
        
    @expose('json')
    def buyEquip(self, uid, equipKind):
        uid = int(uid)
        equipKind = int(equipKind)

        cost = getCost('equip', equipKind)
        ret = checkCost(uid, cost)
        if not ret:
            return dict(id=0)

        try:
            equip = DBSession.query(UserEquips).filter_by(uid=uid).filter_by(equipKind=equipKind).one()
        except:
            equip = UserEquips(uid=uid, equipKind=equipKind, num=0)
            DBSession.add(equip)
        equip.num += 1

        doCost(uid, cost)
        return dict(id=1)
    @expose('json')
    def pickObj(self, uid, silver, crystal, gold):
        uid = int(uid)
        silver = int(silver)
        crystal = int(crystal)
        gold = int(gold)
        user = getUser(uid)
        user.silver += silver
        user.crystal += crystal
        user.gold += gold
        return dict(id=1)



