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
    def buyEquip(self, uid, eid, equipKind):
        uid = int(uid)
        eid = int(eid)
        equipKind = int(equipKind)

        cost = getCost('equip', equipKind)
        ret = checkCost(uid, cost)
        if not ret:
            return dict(id=0)

        #try:
        #    equip = DBSession.query(UserEquips).filter_by(uid=uid).filter_by(equipKind=equipKind).one()
        #except:
        equip = UserEquips(uid=uid, eid=eid, equipKind=equipKind)
        DBSession.add(equip)

        doCost(uid, cost)
        return dict(id=1)

    @expose('json')
    def upgradeEquip(self, uid, eid):
        uid = int(uid)
        eid = int(eid)
        equip = DBSession.query(UserEquips).filter_by(uid=uid, eid=eid).one()
        try:
            goods = DBSession.query(UserGoods).filter_by(uid=uid, kind=TREASURE_STONE).one()
        except:
            return dict(id=0)
        if goods.num > 0:
            goods.num -= 1
            equip.level += 1
        else:
            return dict(id=0)
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

    @expose('json')
    def makeDrug(self, uid, pid):
        uid = int(uid)
        pid = int(pid)
        prescription = getData('prescription', pid)
        needs = prescription['needs']
        kind = prescription['kind']
        tid = prescription['tid']
        #print needs
        print needs

        allHerb = []
        for i in needs:
            try:
                herb = DBSession.query(UserHerb).filter_by(uid=uid, kind=i[0]).one()
                allHerb.append(herb)
                if herb.num < i[1]:
                    return dict(id=0, reason='herb not')
            except:
                return dict(id=0, reason='herb not')

        for i in range(0, len(allHerb)):
            allHerb[i].num -= needs[i][1]

        try:
            drug = DBSession.query(UserDrugs).filter_by(uid=uid, drugKind=kind).one()
        except:
            drug = UserDrugs(uid=uid, drugKind=kind, num=0)
            DBSession.add(drug)
        drug.num += 1
        return dict(id=1)

    @expose('json')
    def makeEquip(self, uid, eid, pid):
        uid = int(uid)
        pid = int(pid)
        prescription = getData('prescription', pid)
        needs = prescription['needs']
        kind = prescription['kind']
        tid = prescription['tid']
        
        print needs

        allHerb = []
        for i in needs:
            try:
                herb = DBSession.query(UserHerb).filter_by(uid=uid, kind=i[0]).one()
                allHerb.append(herb)
                if herb.num < i[1]:
                    return dict(id=0, reason='herb not')
            except:
                return dict(id=0, reason='herb not')
        for i in range(0, len(allHerb)):
            allHerb[i].num -= needs[i][1]
            #print allHerb[i].num

        equip = UserEquips(uid=uid, eid=eid, equipKind=pid)
        DBSession.add(equip)
        return dict(id=1)
    @expose('json')
    def sellDrug(self, uid, kind, silver):
        uid = int(uid)
        kind = int(kind)
        silver = int(silver)

        user = getUser(uid)
        user.silver += silver

        drug = DBSession.query(UserDrugs).filter_by(uid=uid, drugKind=kind).one()
        drug.num = 0
        return dict(id=1)

    @expose('json')
    def sellEquip(self, uid, eid, silver):
        uid = int(uid)
        eid = int(eid)
        silver = int(silver)

        user = getUser(uid)
        user.silver += silver

        equip = DBSession.query(UserEquips).filter_by(uid=uid, eid=eid).one()
        DBSession.delete(equip)

        return dict(id=1)

