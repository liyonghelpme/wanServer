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
    def getBasicAbility(self, id, level):
        pureData = calculateStage(id, level)
        cat = getData('soldier', id).get("category")
        pcoff = datas['soldierKind'][cat][4]
        mcoff = datas['soldierKind'][cat][5]
    	phyBasic = int(pureData['healthBoundary']*pureData['physicAttack']/pcoff)
    	magBasic = int(pureData['healthBoundary']*pureData['magicAttack']/mcoff)
    	ab = max(phyBasic, magBasic)/(33*13)
        return ab

    def getAddExp(self, id, level):
        basic = self.getBasicAbility(id, level)
        exp = (2*basic-1)*3
        return exp
    def getLevelUpExp(self, id, level):
        exp = self.getAddExp(id, level)
        return exp
            
    def getHealthBoundary(self, soldier):
        healthBoundary = calculateStage(soldier.kind, soldier.level)['healthBoundary']
        #药品增加的生命值上限
        if soldier.addHealthBoundaryTime > 0:
            healthBoundary += soldier.addHealthBoundary
        equips = DBSession.query(UserEquips).filter_by(uid=soldier.uid).all()
        #计算装备增加生命值上限
        for e in equips:
            if e.owner == soldier.sid:
                edata = getData('equip', e.equipKind)
                healthBoundary += edata['healthBoundary']
        return healthBoundary
        #data = getData('soldier', soldier.kind)
        #healthBoundary = data.get("health")+soldier.level*data.get("addHealth")
        #return healthBoundary
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
        soldier = UserSoldiers(uid=uid, sid=sid, kind=kind, name="", health = calculateStage(kind, 0)['healthBoundary'])
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

        
    @expose('json')
    def doRelive(self, uid, sid, crystal):
        uid = int(uid)
        sid = int(sid)
        crystal = int(crystal)

        cost = {'crystal':crystal} 
        ret = checkCost(uid, cost)
        if not ret:
            return dict(id=0)
        doCost(uid, cost)
        soldier = DBSession.query(UserSoldiers).filter_by(uid=uid).filter_by(sid=sid).one()
        soldier.dead = 0
        healthBoundary = self.getHealthBoundary(soldier)
        soldier.health = healthBoundary
        return dict(id=1)

    #检测药水数量是否足够
    @expose('json')
    def useDrug(self, uid, sid, tid):
        uid = int(uid)
        sid = int(sid)
        tid = int(tid)
        soldier = DBSession.query(UserSoldiers).filter_by(uid=uid).filter_by(sid=sid).one()
        drugs = DBSession.query(UserDrugs).filter_by(uid=uid).filter_by(drugKind = tid).one()
        if drugs.num <= 0:
            return dict(id=0)

        pureData = calculateStage(soldier.kind, soldier.level) 
        purePhyAttack = pureData['physicAttack'];
        pureMagAttack = pureData['magicAttack'];
        purePhyDef = pureData['physicDefense'];
        pureMagDef = pureData['magicDefense'];
        healthBoundary = self.getHealthBoundary(soldier)

        data = getData('drug', tid)
        soldier.health += data.get("health", 0)
        soldier.health = min(healthBoundary, soldier.health)
        
        #soldier.exp += data.get("exp", 0)
        #self.getLevelUp(soldier)

        if data.get("attack") != 0:
            soldier.addAttack = data.get("attack")
            soldier.addAttackTime = data.get("effectTime")
        elif data.get("defense") != 0:
            soldier.addDefense = data.get("defense")
            soldier.addDefenseTime = data.get("effectTime")
        elif data.get("healthBoundary") != 0:
            soldier.addHealthBoundary = data["healthBoundary"]
            soldier.addHealthBoundaryTime = data["effectTime"]
        elif data.get("relive") == 1:#复活药水 回复全部%的生命值
            soldier.dead = 0
            soldier.health = healthBoundary
        elif data.get("percentHealth") != 0:
            soldier.health += data.get("percentHealth")*healthBoundary/100
            soldier.health = min(soldier.health, healthBoundary)
        elif data.get("percentAttack") != 0:
            soldier.addAttack = data.get("percentAttack")*max(purePhyAttack, pureMagAttack)/100
            soldier.addAttackTime = data.get("")
        elif data.get("percentHealthBoundary") != 0:
            soldier.addHealthBoundary = data.get("percentHealthBoundary")*healthBoundary/100
            soldier.addHealthBoundaryTime = data.get("effectTime")
        elif data.get("percentDefense") != 0:
            soldier.addDefense = data.get("percentDefense")*max(purePhyDef, pureMagDef)/100
            soldier.addDefenseTime = data.get("effectTime")
            

        #drugs = DBSession.query(Drugs).filter_by(uid=uid).filter_by(drugKind = tid).one()
        drugs.num -= 1
        return dict(id=1)
    @expose('json')
    def useState(self, uid, sid):
        uid = int(uid)
        sid = int(sid)
        soldier = DBSession.query(UserSoldiers).filter_by(uid=uid).filter_by(sid=sid).one()
        soldier.addAttackTime -= 1
        soldier.addDefenseTime -= 1
        soldier.addHealthBoundaryTime -= 1

        soldier.addAttackTime = max(soldier.addAttackTime, 0)
        soldier.addDefenseTime = max(soldier.addDefenseTime, 0)
        soldier.addHealthBoundaryTime = max(soldier.addHealthBoundaryTime, 0)
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

    #奖励之后可能升级
    @expose('json')
    def inspireMe(self, uid, sid, exp):
        uid = int(uid)
        sid = int(sid)
        exp = int(exp)
        soldier = DBSession.query(UserSoldiers).filter_by(uid=uid).filter_by(sid=sid).one()
        soldier.exp += exp
        self.getLevelUp(soldier)
        return dict(id=1)

    #转职可能也需要消耗一些资源 类似于直接购买的价格
    @expose('json')
    def doTransfer(self, uid, sid, crystal):
        uid = int(uid)
        sid = int(sid)
        crystal = int(crystal)
        cost = {'crystal':crystal}
        ret = checkCost(uid, cost)
        if not ret:
            return dict(id=0)
        doCost(uid, cost)

        soldier = DBSession.query(UserSoldiers).filter_by(uid=uid).filter_by(sid=sid).one()
        curKind = soldier.kind%10
        print curKind, soldier.level
        soldier.kind += 1
        #if curKind < 3 and (curKind+1)*5 <= soldier.level and soldier.kind < 100:
        #    soldier.kind += 1
        #else:
        #    return dict(id=0)
        return dict(id=1)
    def getLevelNeedExp(self, expData, level):
        return expData[min(len(expData)-1, level)]
    #正常服务器刷新怪物 客户端 来处理
    #但是这里只是服务器记录数据
    #升级需要的经验
    def getLevelUp(self, soldier):
        #solData = getData('soldier', soldier.kind)
        #expData = getData('soldierLevelExp', solData.get("expId"))
        #expData = json.loads(expData.get("exp"))
        #expData = getLevelUpExp(soldier.kind, soldier.level)
        #print expData

        level = False
        while True:
            #ne = self.getLevelNeedExp(expData, soldier.level)
            ne = self.getLevelUpExp(soldier.kind, soldier.level)
            if soldier.exp >= ne:
                soldier.level += 1
                soldier.exp -= ne
                level = True
            else:
                break
        if level and soldier.dead == 0:
            healthBoundary = self.getHealthBoundary(soldier)
            soldier.health = healthBoundary
            
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
        #solEquip = DBSession.query(UserSolEquip).filter_by(uid=uid).filter_by(sid=sid).all()
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
    @expose('json')
    def challengeOver(self, uid, sols, reward, star, big, small):
        uid = int(uid)
        sols = json.loads(sols)
        try:
            reward = json.loads(reward)
        except:
            reward = []
        star = int(star)
        big = int(big)
        small = int(small)

        print sols
        for i in sols:
            #print i
            soldier = DBSession.query(UserSoldiers).filter_by(uid=uid).filter_by(sid=i[0]).one()
            soldier.health = i[1]
            soldier.exp = i[2]
            soldier.dead = i[3]
            soldier.level = i[4]
        print reward
        for i in reward:
            try:
                herb = DBSession.query(UserHerb).filter_by(uid=uid).filter_by(kind=i[0]).one()
            except:
                herb = UserHerb(uid=uid, kind=i[0], num=0)
                DBSession.add(herb)
            herb.num += i[1]
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
       
        num = getGoodsNum(uid, getKindsId('magicStone'), stoneId)
        if num < 1:
            return dict(id=0)
        updateGoodsNum(uid, getKindsId('magicStone'), stoneId, -1)
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









        

