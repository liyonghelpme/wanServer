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
    @expose('json')
    def recoverHealth(self, uid, sid, addHealth):
        uid = int(uid)
        sid = int(sid)
        addHealth = int(addHealth)
        soldier = DBSession.query(UserSoldiers).filter_by(uid=uid, sid=sid).one()
        soldier.health += addHealth
        return dict(id=1)

            
    #接口不再使用 由兵营的beginWork 取代
    @expose('json')
    def buySoldier(self, uid, sid, kind):
        uid = int(uid)
        sid = int(sid)
        kind = int(kind)
        cost = getCost("soldier", kind)
        ret = checkCost(uid, cost)
        if not ret:
            return dict(id=0)
        doCost(uid, cost)
        soldier = UserSoldiers(uid=uid, sid=sid, kind=kind, name="")
        DBSession.add(soldier)
        return dict(id=1)
    @expose('json')
    def setName(self, uid, sid, name):
        uid = int(uid)
        sid = int(sid)
        print "setName", uid, sid, name
        soldier = DBSession.query(UserSoldiers).filter_by(uid=uid).filter_by(sid=sid).one()
        soldier.name = name
        return dict(id=1)
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
    def sellSoldier(self, uid, sid):
        uid = int(uid)
        sid = int(sid)
        soldier = DBSession.query(UserSoldiers).filter_by(uid=uid).filter_by(sid=sid).one()
        DBSession.delete(soldier)
        cost = getCost('soldier', soldier.kind)
        cost = changeToSilver(cost)
        doGain(uid, cost)
        equips = DBSession.query(UserEquips).filter_by(uid=uid, owner=sid).all()
        for i in equips:
            equips.owner = -1
        return dict(id=1)
    @expose('json')
    def trainOver(self, uid, sols):
        uid = int(uid)
        sols = json.loads(sols)

        for i in sols:#经验 等级 生命值 死亡
            soldier = DBSession.query(UserSoldiers).filter_by(uid=uid).filter_by(sid=i[0]).one()
            soldier.health = i[1]
            soldier.exp = i[2]
            soldier.dead = i[3]
            soldier.level = i[4]
        return dict(id=1)
            
    #sid health exp dead level
    #士兵闯关成功升级
    #士兵闯关失败 更新士兵 数据 dead = 1 的 将被删除
    #测试： 士兵使用装备 士兵 阵亡 装备消除
    @expose('json')
    def challengeOver(self, uid, sols, reward, star, big, small):
        uid = int(uid)
        sols = json.loads(sols)
        try:
            reward = json.loads(reward)
        except:
            reward = {}
        star = int(star)
        big = int(big)
        small = int(small)

        print sols
        killSoldiers(uid, sols)
        #死亡士兵 杀死
        print reward
        doGain(uid, reward)
        curStar = DBSession.query(UserChallenge).filter_by(uid=uid).filter_by(big=big).filter_by(small=small).one()

        if curStar.star < 2:
            addCry = 0
            if star == 2:
                addCry = 1
            if star == 3:
                addCry = 3
            user = DBSession.query(UserInWan).filter_by(uid=uid).one()
            user.crystal += addCry
        curStar.star = star
        return dict(id=1)
    @expose('json')
    def unloadThing(self, uid, eid):
        uid = int(uid)
        eid = int(eid)
        equip = DBSession.query(UserEquips).filter_by(uid=uid, eid=eid).one()
        equip.owner = -1
        return dict(id=1)

    @expose('json')
    def buySkill(self, uid, soldierId, skillId):
        uid = int(uid)
        soldierId = int(soldierId)
        skillId = int(skillId)

        cost = getCost('skills', skillId)
        if not checkCost(uid, cost):
            return dict(id=0)
        doCost(uid, cost)
        
        skill = UserSkills(uid=uid, soldierId=soldierId, skillId=skillId, level=0)
        DBSession.add(skill)
        return dict(id=1)

    @expose('json')
    def upgradeSkill(self, uid, soldierId, skillId, stoneId):
        uid = int(uid)
        soldierId = int(soldierId)
        skillId = int(skillId)
        stoneId = int(stoneId)
       
        num = getGoodsNum(uid, getKindId('magicStone'), stoneId)
        if num < 1:
            return dict(id=0)
        updateGoodsNum(uid, getKindId('magicStone'), stoneId, -1)
        gData = getData('magicStone', stoneId)
        possible = gData.get('possible')
        
        skill = DBSession.query(UserSkills).filter_by(uid=uid, soldierId=soldierId, skillId=skillId).one()
        suc = possible[min(skill.level, len(possible)-1)]
        rv = random.randint(0, 100)
        print rv, suc
        if rv < suc:
            skill.level += 1
            return dict(id=1, suc=1)
        return dict(id=1, suc=0)

    @expose('json')
    def giveupSkill(self, uid, soldierId, skillId):
        uid = int(uid)
        soldierId = int(soldierId)
        skillId = int(skillId)

        skill = DBSession.query(UserSkills).filter_by(uid=uid, soldierId=soldierId, skillId=skillId).one()
        DBSession.delete(skill)
        return dict(id=1)
    @expose('json')
    def trainDouble(self, uid, gold):
        uid = int(uid)
        gold = int(gold)
        cost = {'gold': gold}
        ret = checkCost(uid, cost)
        if ret:
            doCost(uid, cost)
            return dict(id=1)
        return dict(id=0)
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









        

