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
        res[i.sid] = dict(id=i.kind, name=i.name, level=i.level, exp=i.exp, health=i.health, addAttack = i.addAttack, addDefense = i.addDefense, addAttackTime=i.addAttackTime, addDefenseTime=i.addDefenseTime, dead=i.dead, addHealthBoundary=i.addHealthBoundary, addHealthBoundaryTime=i.addHealthBoundaryTime)
    return res
def getChallengeSoldiers(uid):
    soldiers = DBSession.query(UserSoldiers).filter_by(uid=uid).all()
    res = []
    for i in soldiers:
        res.append(dict(sid=i.sid, id=i.kind, level=i.level, addAttack = i.addAttack, addDefense = i.addDefense, addAttackTime=i.addAttackTime, addDefenseTime=i.addDefenseTime, addHealthBoundary=i.addHealthBoundary, addHealthBoundaryTime=i.addHealthBoundaryTime))
    return res

def getEquips(uid):
    equips = DBSession.query(UserEquips).filter_by(uid=uid).all()
    res = {}
    for i in equips:
        res[i.eid] = {'kind':i.equipKind, 'level':i.level, 'owner':i.owner}
    return res
#如果对方没有使用某个装备就会导致对方的士兵实力下降
def getChallengeEquips(uid):
    equips = DBSession.query(UserEquips).filter_by(uid=uid).all()
    res = []
    for i in equips:
        if i.owner != -1:
            res.append({'kind':i.equipKind, 'level':i.level, 'owner':i.owner})
    return res
    
NEW_RANK = 10
def getRankTable(uid):
    #user = getUser(uid)
    challenge = DBSession.query(UserChallengeFriend).filter_by(uid=uid).one()
    if challenge.challengeNum >= NEW_RANK:
        rank = UserGroupRank
    else:
        rank = UserNewRank
    return rank
    
#在10次挑战结束的时候进行数据迁移
def getRank(uid):
    #user = getUser(uid)
    challenge = DBSession.query(UserChallengeFriend).filter_by(uid=uid).one()
    if challenge.challengeNum >= NEW_RANK:
        rank = DBSession.query(UserGroupRank).filter_by(uid=uid).one()
    else:
        rank = DBSession.query(UserNewRank).filter_by(uid=uid).one()
    #res = [rank.score, rank.rank]
    return rank

def calculateStage(id, level):
    stage = stagePool.get(id)
    for i in range(1, len(stage)):
        if level < stage[i][0]:
            break
    begin = stage[i-1]
    end = stage[i]
    levelDiff = end[0]-begin[0]

    addHealth = end[1][0]-begin[1][0];
    addMagicDefense = end[1][1]-begin[1][1];
    addPhysicDefense = end[1][2]-begin[1][2];
    addPhysicAttack = end[1][3]-begin[1][3];
    addMagicAttack = end[1][4]-begin[1][4];


    physicAttack = begin[1][3]+(level-begin[0])*addPhysicAttack/levelDiff; 
    physicDefense = begin[1][2]+(level-begin[0])*addPhysicDefense/levelDiff; 

    magicAttack = begin[1][4]+(level-begin[0])*addMagicAttack/levelDiff; 
    magicDefense = begin[1][1]+(level-begin[0])*addMagicDefense/levelDiff; 
    healthBoundary = begin[1][0]+(level-begin[0])*int(addHealth)/levelDiff;
    return [physicAttack, magicAttack, physicDefense, magicDefense, healthBoundary]
