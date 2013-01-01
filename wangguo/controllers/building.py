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
import time

__all__ = ['BuildingController']


class BuildingController(BaseController):
    #主要是升级爱心树
    #卖出建筑物 只收回银币 由客户端决定
    @expose('json')
    def sellBuilding(self, uid, bid, silver):
        uid = int(uid)
        bid = int(bid)
        silver = int(silver)

        build = DBSession.query(UserBuildings).filter_by(uid=uid).filter_by(bid=bid).one()
        #cost = getCost('building', build.kind)
        #cost = changeToSilver(cost)
        gain = {'silver':silver}
        doGain(uid, gain)
        DBSession.delete(build)
        return dict(id=1)
    @expose('json')
    def finishBuild(self, uid, bid, kind, px, py, dir, color=0):
        uid = int(uid)
        bid = int(bid)
        kind = int(kind)
        px = int(px)
        py = int(py)
        dir = int(dir)
        color = int(color)

        cost = getCost('building', kind)
        ret = checkCost(uid, cost)
        if not ret:
            return dict(id=0)
        doCost(uid, cost)
        gain = getGain('building', kind)
        doGain(uid, gain)
        buildings = UserBuildings(uid=uid, bid=bid, kind=kind, px=px, py=py, state = getParams('buildFree'), color = color)
        buildings.dir = dir
        if kind == getParams('MineKind'):
            buildings.objectTime = getTime()
        DBSession.add(buildings)
        return dict(id=1)
    #bid px py dir
    @expose('json')
    def finishPlan(self, uid, builds):
        uid = int(uid)
        builds = json.loads(builds)
        for i in builds:
            try:
                build = DBSession.query(UserBuildings).filter_by(uid=uid).filter_by(bid=i[0]).one()
                build.px = i[1]
                build.py = i[2]
                build.dir = i[3]
            except:
                print "no such id building", uid, i
        return dict(id=1)
    #state 1 Free 2 work 
    @expose('json')
    def beginPlant(self, uid, bid, objectId):
        uid = int(uid)
        bid = int(bid)
        #time.sleep(3)
        objectId = int(objectId)
        build = DBSession.query(UserBuildings).filter_by(uid=uid).filter_by(bid=bid).one()
        if build.state != datas['PARAMS']['buildFree']:#可能处于 移动状态吗？
            return dict(id=0)
        cost = getCost('plant', objectId)
        ret = checkCost(uid, cost)
        if not ret:
            return dict(id=0)

        doCost(uid, cost)
        build.state = datas['PARAMS']['buildWork']
        build.objectId = objectId
        build.objectTime = getTime()
        return dict(id=1)

    #农田 兵营 等开始工作
    #objectKind == 数值
    #根据物体类型 物品id 得到cost
    @expose('json')
    def beginWork(self, uid, bid, objectKind, objectId):
        uid = int(uid)
        bid = int(bid)
        objectKind = int(objectKind)
        objectId = int(objectId)
        table = datas['TableMap'][objectKind]['name']
        cost = getCost(table, objectId)
        ret = checkCost(uid, cost)
        if not ret:
            return dict(id=0)

        build = DBSession.query(UserBuildings).filter_by(uid=uid).filter_by(bid=bid).one()
        if build.state != datas['PARAMS']['buildFree']:#正在工作
            return dict(id=0)

        doCost(uid, cost)
        build.state = datas['PARAMS']['buildWork']
        build.objectId = objectId
        build.objectTime = getTime()
        return dict(id=1)

    @expose('json')
    def accWork(self, uid, bid, objectKind, gold):
        uid = int(uid)
        bid = int(bid)
        objectKind = int(objectKind)
        gold = int(gold)

        build = DBSession.query(UserBuildings).filter_by(uid=uid).filter_by(bid=bid).one()
        if build.state != datas['PARAMS']['buildWork']:#没有工作
            return dict(id=0)
        cost = {'gold':gold}
        ret = checkCost(uid, cost)
        if not ret:
            return dict(id=0)
        doCost(uid, cost)

        table = datas['TableMap'][objectKind]['name']
        sol = getData(table, build.objectId)
        #startTime = build.objectTime
        needTime = sol['time']
        now = getTime()
        build.objectTime = now - needTime-1
        return dict(id=1)
    
    #收获士兵
    #招募英雄需要有初始技能
    #命名在 choosehero之后
    #change soldier Name
    @expose('json')
    def finishCall(self, uid, bid, sid):
        uid = int(uid)
        bid = int(bid)
        sid = int(sid)

        build = DBSession.query(UserBuildings).filter_by(uid=uid).filter_by(bid=bid).one()
        if build.state != datas['PARAMS']['buildWork']:
            return dict(id=0, status=0)

        now = getTime()
        passTime = now - build.objectTime
        needTime = getData('soldier', build.objectId)['time']
        if passTime < needTime:
            return dict(id=0, status=1)
        
        
        soldier = UserSoldiers(uid=uid, sid=sid, kind=build.objectId, name="")
        DBSession.add(soldier)

        sData = getData('soldier', build.objectId)
        #招募英雄学习技能
        if sData['isHero'] == 1:
            skillId = getData('heroSkill', build.objectId)['skillId']
            skill = UserSkills(uid=uid, soldierId=sid, skillId=skillId, level=0)
            DBSession.add(skill)

        build.state = datas['PARAMS']['buildFree']
        build.objectId = -1
        build.objectTime = 0
        return dict(id=1)


    @expose('json')
    def accPlant(self, uid, bid, gold):
        uid = int(uid)
        bid = int(bid)
        gold = int(gold)
        cost = {'gold':gold}
        buyable = checkCost(uid, cost)
        if not buyable:
            return dict(id=0)
        doCost(uid, cost)

        building = DBSession.query(UserBuildings).filter_by(uid=uid, bid=bid).one()
        plantData = getData("plant", building.objectId)
        needTime = plantData.get("time")
        now = getTime()
        building.objectTime = now-needTime-1
        return dict(id=1)
    @expose('json')
    def accWork(self, uid, bid, gold, leftTime):
        uid = int(uid)
        bid = int(bid)
        gold = int(gold)
        leftTime = int(leftTime)
        cost = {'gold':gold}
        buyable = checkCost(uid, cost)
        if not buyable:
            return dict(id=0)
        doCost(uid, cost)

        building = DBSession.query(UserBuildings).filter_by(uid=uid, bid=bid).one()
        building.objectTime -= leftTime
        return dict(id=1)

    @expose('json')
    def harvestPlant(self, uid, bid):
        print "harvestPlant"
        uid = int(uid)
        bid = int(bid)
        #time.sleep(3)
        build = DBSession.query(UserBuildings).filter_by(uid=uid).filter_by(bid=bid).one()
        data = getData('plant', build.objectId)
        need = data['time']
        cur = getTime()
        passTime = cur - build.objectTime
        gain = getGain('plant', build.objectId)
        if passTime < need:
            return dict(id=0, passTime=passTime, need=need)
        #rot 只收获经验
        if passTime > 3*need:
            gain = {'exp': gain['exp']}
            #for k in gain:
            #    gain[k] /= 2
        
        buildData = getData('building', build.kind)
        rate = buildData['rate']
        for k in gain:
            gain[k] *= rate/100;

        doGain(uid, gain)
        build.objectId = -1
        build.objectTime = 0
        build.state = datas['PARAMS']['buildFree']
        return dict(id=1)
    
    def addSol(self, build, objId):
        objectList = json.loads(build.objectList)
        index = None
        for i in objectList:
            if i[0] == objId:
                index = i
                break
        if index == None:
            objectList.append([objId, 1])
        else:
            index[1] += 1
        build.objectList = json.dumps(objectList)
    
    def realUpdateWorkTime(self, uid, bid):
        build = DBSession.query(UserBuildings).filter_by(uid=uid).filter_by(bid=bid).one()
        build.objectTime = getTime()
        build.objectId = 0
    #兵营开始工作
    @expose('json')
    def campUpdateWorkTime(self, uid, bid):
        uid = int(uid)
        bid = int(bid)
        self.realUpdateWorkTime(uid, bid)
        return dict(id=1)


    #兵营增加士兵类型
    @expose('json')
    def campAddSoldier(self, uid, bid, solId):
        uid = int(uid)
        bid = int(bid)
        solId = int(solId)
        solData = getData('soldier', solId)

        cost = getCost('soldier', solId)
        ret = checkCost(uid, cost)
        if not ret:
            return dict(id=0)
        doCost(uid, cost)
        build = DBSession.query(UserBuildings).filter_by(uid=uid).filter_by(bid=bid).one()
        self.addSol(build, solId)
        return dict(id=1)

    #兵营收获一个士兵 
    #更新兵营工作时间
    @expose('json')
    def campHarvestSoldier(self, uid, bid, solId, sid, name):
        print "campHarvestSoldier", name
        uid = int(uid)
        bid = int(bid)
        solId = int(solId)
        sid = int(sid)

        build = DBSession.query(UserBuildings).filter_by(uid=uid).filter_by(bid=bid).one()
        objectList = json.loads(build.objectList)
        index = None
        for i in objectList:
            if i[0] == solId:
                index = i
                i[1] -= 1
                if i[1] <= 0:
                    objectList.remove(i)
                break
        if index == None:
            return dict(id=0, reason="no such kind soldier")
        build.objectList = json.dumps(objectList)

        soldier = UserSoldiers(uid=uid, sid=sid, kind=solId, name=name)
        DBSession.add(soldier)
        
        build.objectTime += getData('soldier', solId)['time']#工作时间 向后推迟
        return dict(id=1)

    #加速兵营生产
    #重设生产时间 为当前预期时间 startTime - needTime
    #客户端传递需要时间
    @expose('json')
    def accCampWork(self, uid, bid, cost, needTime):
        uid = int(uid)
        bid = int(bid)
        cost = json.loads(cost)
        needTime = int(needTime)
        ret = checkCost(uid, cost)
        if not ret:
            return dict(id=0)
        doCost(uid, cost)

        build = DBSession.query(UserBuildings).filter_by(uid=uid).filter_by(bid=bid).one()
        build.objectTime -= needTime
        return dict(id=1)


        

