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

#from wangguo.model import DBSession, metadata
from wangguo.model import *
from wangguo.controllers.util import *

__all__ = ['SoldierController']


class SoldierController(BaseController):
    #增加生命值 和 经验的药水
    #增加攻击力 和 防御力 的药水 如何使用 用户闯关一次 之后 作用消失 使用之后 作用若干回合 只能使用一次
    #在所有士兵页面 点击 某个士兵 选择复活药水 复活士兵 购买药水

    @expose('json')
    def useDrugInRound(self, uid, tid):
        uid = int(uid)
        tid = int(tid)
        drugs = DBSession.query(UserDrugs).filter_by(uid=uid).filter_by(drugKind = tid).one()
        if drugs.num <= 0:
            return dict(id=0)
        drugs.num -= 1
        return dict(id=1)

        


    #ToDo 检测 装备数量是否足够
    #士兵卖出之后 士兵使用的装备 全被归还
    
    @expose('json')
    def useEquip(self, uid, sid, eid):
        uid = int(uid)
        sid = int(sid)
        eid = int(eid)
        equip = DBSession.query(UserEquips).filter_by(uid=uid, eid=eid).one()
        equip.owner = sid
        return dict(id=1)
    
    @expose('json')
    def reliveHero(self, uid, sid):
        uid = int(uid)
        sid = int(sid)
        soldier = DBSession.query(UserSoldiers).filter_by(uid=uid).filter_by(sid=sid).one()
        soldier.inDead = 0
        soldier.deadStartTime = 0
        return dict(id=1)
    @expose('json')
    def accReliveHero(self, uid, sid, leftTime, cost):
        uid = int(uid)
        sid = int(sid)
        leftTime = int(leftTime)
        cost = json.loads(cost)
        ret = checkCost(uid, cost)
        if not ret:
            return dict(id=0)
        doCost(uid, cost)

        soldier = DBSession.query(UserSoldiers).filter_by(uid=uid).filter_by(sid=sid).one()
        soldier.deadStartTime -= leftTime
        return dict(id=1)


    #转职可能也需要消耗一些资源 类似于直接购买的价格
    @expose('json')
    def doTransfer(self, uid, sid, cost):
        uid = int(uid)
        sid = int(sid)
        cost = json.loads(cost)
        ret = checkCost(uid, cost)
        if not ret:
            return dict(id=0)
        doCost(uid, cost)

        soldier = DBSession.query(UserSoldiers).filter_by(uid=uid).filter_by(sid=sid).one()
        soldier.inTransfer = 1
        soldier.transferStartTime = getTime()
        return dict(id=1)
    @expose('json')
    def doAcc(self, uid, sid, leftTime, gold):
        uid = int(uid)
        sid = int(sid)
        leftTime = int(leftTime)
        gold = int(gold)

        cost = {'gold':gold}
        ret = checkCost(uid, cost)
        if not ret:
            return dict(id=0)

        doCost(uid, cost)
        soldier = DBSession.query(UserSoldiers).filter_by(uid=uid, sid=sid).one()
        soldier.transferStartTime -= leftTime
        return dict(id=1)

    @expose('json')
    def finishTransfer(self, uid, sid):
        uid = int(uid)
        sid = int(sid)
        soldier = DBSession.query(UserSoldiers).filter_by(uid=uid).filter_by(sid=sid).one()
        soldier.kind += 1
        soldier.inTransfer = 0
        soldier.transferStartTime = 0
        return dict(id=1)

            


    @expose('json')
    def unloadThing(self, uid, eid):
        uid = int(uid)
        eid = int(eid)
        equip = DBSession.query(UserEquips).filter_by(uid=uid, eid=eid).one()
        equip.owner = -1
        return dict(id=1)

    @expose('json')
    def game1Over(self, uid, sid, health, exp, level):
        uid = int(uid)
        sid = int(sid)
        exp = int(exp)
        health = int(health)
        level = int(level)

        sol = DBSession.query(UserSoldiers).filter_by(uid=uid, sid=sid).one()
        sol.health = health
        sol.exp = exp
        sol.level = level
        return dict(id=1)
    @expose('json')
    def game2Over(self, uid, silver, crystal, gold):
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
    def game4Over(self, uid, soldiers):#增加经验士兵列表sid health exp level
        uid = int(uid)
        soldiers = json.loads(soldiers)
        for i in soldiers:
            sol = DBSession.query(UserSoldiers).filter_by(uid=uid, sid=i[0])
            sol.health = i[1]
            sol.exp = i[2]
            sol.level = i[3]
        return dict(id=1)
    @expose('json')
    def playGame4(self, uid, cost):
        uid = int(uid)
        cost = json.loads(cost)
        ret = checkCost(uid, cost)
        if not ret:
            return dict(id=0)
        doCost(uid, cost)
        return dict(id=1)

    







        

