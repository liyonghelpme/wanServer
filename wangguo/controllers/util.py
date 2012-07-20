# -*- coding: utf-8 -*-
"""Fallback controller."""
from tg import expose, flash, require, url,  request, redirect
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
import time

addKey = ["people", "cityDefense", "attack", "defense", "health", "gainsilver", "gaincrystal", "gaingold", "exp"]
costKey = ["silver", "gold", "crystal", "papaya", "free"]

beginTime=(2012,1,1,0,0,0,0,0,0)
def getTime():
    curTime = int(time.mktime(time.localtime())-time.mktime(beginTime))
    return curTime

def getData(key, id):
    return datas[key].get(id)

def getCost(key, id):
    data = getData(key, id)
    cost = dict()
    for i in costKey:
        val = data.get(i, 0)
        if val > 0:
            cost[i] = val
    return cost

def checkCost(uid, cost):
    print uid
    user = DBSession.query(UserInWan).filter_by(uid=uid).one()
    for k in cost:
        v = getattr(user, k)
        if v < cost[k]:
            return False
    return True
    
def doCost(uid, cost):
    user = DBSession.query(UserInWan).filter_by(uid=uid).one()
    for k in cost:
        v = getattr(user, k)
        setattr(user, k, v-cost[k])


def getGain(key, id):
    data = getData(key, id)
    gain = dict()
    for i in addKey:
        val = data.get(i, 0)
        if val > 0:
            i = i.replace('gain', '')
            gain[i] = val
    return gain

#增加经验重新计算等级
def doGain(uid, gain):        
    user = DBSession.query(UserInWan).filter_by(uid=uid).one()
    for k in gain:
        v = getattr(user, k)
        v += gain[k]
        if k == 'exp':
            levelExp = datas.get("levelExp")
            level = user.level
            oldLevel = level
            while True:
                needExp = levelExp[min(level, len(levelExp)-1)]
                if v >= needExp:
                    v -= needExp
                    level += 1
                else:
                    break
            if level != oldLevel:
                user.level = level

        setattr(user, k, v)

SELL_RATE = 10
Cry2Sil = 500
Gold2Sil = 1000
#将水晶 和 金币 转化成 银币
def changeToSilver(data):
    global SELL_RATE
    addSilver = 0
    for k in data:
        if k == 'crystal':
            addSilver += data[k]*Cry2Sil/SELL_RATE
        elif k == 'gold':
            addSilver += data[k]*Gold2Sil/SELL_RATE
        elif k == 'silver':
            addSilver += data[k]/SELL_RATE
    print "changeToSilver", data, addSilver
    data = {'silver':addSilver}
    return data
def getUser(uid):
    user = DBSession.query(UserInWan).filter_by(uid=uid).one()
    return user

def getSoldiers(uid):
    soldiers = DBSession.query(UserSoldiers).filter_by(uid=uid).all()
    res = dict()
    for i in soldiers:
        res[i.sid] = dict(id=i.kind, name=i.name, level=i.level, exp=i.exp, health=i.health, addAttack = i.addAttack, addDefense = i.addDefense, addAttackTime=i.addAttackTime, addDefenseTime=i.addDefenseTime, dead=i.dead)
    return res
