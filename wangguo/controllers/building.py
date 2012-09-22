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
    """
    @expose('json')
    def upgradeBuild(self, uid, bid, silver, crystal, gold, people):
        uid = int(uid)
        bid = int(bid)
        silver = int(silver)
        crystal = int(crystal)
        gold = int(gold)
        people = int(people)

        cost = {'silver':silver, 'crystal':crystal, 'gold':gold}
        ret = checkCost(uid, cost)
        if ret:
            doCost(uid, cost)
            doGain(uid, {'people':people})
            building = DBSession.query(UserBuildings).filter_by(uid=uid, bid=bid).one()
            building.level += 1
            return dict(id=1)
        return dict(id=0)
    """
    @expose('json')
    def sellBuilding(self, uid, bid):
        uid = int(uid)
        bid = int(bid)
        build = DBSession.query(UserBuildings).filter_by(uid=uid).filter_by(bid=bid).one()
        cost = getCost('building', build.kind)
        cost = changeToSilver(cost)
        doGain(uid, cost)
        DBSession.delete(build)
        return dict(id=1)
    @expose('json')
    def finishBuild(self, uid, bid, kind, px, py, dir):
        uid = int(uid)
        bid = int(bid)
        kind = int(kind)
        px = int(px)
        py = int(py)
        dir = int(dir)
        cost = getCost('building', kind)
        ret = checkCost(uid, cost)
        if not ret:
            return dict(id=0)
        doCost(uid, cost)
        gain = getGain('building', kind)
        doGain(uid, gain)
        buildings = UserBuildings(uid=uid, bid=bid, kind=kind, px=px, py=py, state = 1)
        buildings.dir = dir
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
        if build.state == 2:
            return dict(id=0)
        cost = getCost('plant', objectId)
        ret = checkCost(uid, cost)
        if not ret:
            return dict(id=0)

        doCost(uid, cost)
        build.state = 2#working
        build.objectId = objectId
        build.objectTime = getTime()
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
            gain[k] *= rate;

        doGain(uid, gain)
        build.objectId = -1
        build.objectTime = 0
        build.state = 1
        return dict(id=1)



        


        

