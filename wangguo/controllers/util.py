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
import random

addKey = ["people", "cityDefense", "attack", "defense", "health", "gainsilver", "gaincrystal", "gaingold", "exp"]
costKey = ["silver", "gold", "crystal", "papaya", "free"]

#MSG_CHALLENGE = 0
#week == 0 
weekTime = (2012, 1, -5, 0, 0, 0, 0, 0, 0)
beginTime=(2012,1,1,0,0,0,0,0,0)
weekDiffTime = 5*24*3600
aWeek = 7*24*3600
#+ loginTime + weekDiffTime / 7*24*3600 = weekTimes 
#lastLoginTime nowLoginTime--->weekNum weekNum >= 1 firstLogin In this Week
def getWeekNum(t):
    t += weekDiffTime
    t /= aWeek
    return int(t)
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
        uk = k.encode('utf8')
        v = getattr(user, uk)
        v += gain[k]
        #提升经验 提升等级
        setattr(user, uk, v)

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
        #res[i.sid] = dict(id=i.kind, name=i.name, level=i.level, exp=i.exp, health=i.health, addAttack = i.addAttack, addDefense = i.addDefense, addAttackTime=i.addAttackTime, addDefenseTime=i.addDefenseTime, dead=i.dead, addHealthBoundary=i.addHealthBoundary, addHealthBoundaryTime=i.addHealthBoundaryTime)
        res[i.sid] = dict(id=i.kind, name=i.name, inTransfer=i.inTransfer, transferStartTime=i.transferStartTime)
    return res
def getChallengeSoldiers(uid):
    soldiers = DBSession.query(UserSoldiers).filter_by(uid=uid).all()
    res = []
    for i in soldiers:
        res.append(dict(sid=i.sid, id=i.kind))
    return res

def getEquips(uid):
    equips = DBSession.query(UserEquips).filter_by(uid=uid).all()
    res = {}
    for i in equips:
        res[i.eid] = {'kind':i.equipKind, 'owner':i.owner}
    return res
#如果对方没有使用某个装备就会导致对方的士兵实力下降
def getChallengeEquips(uid):
    equips = DBSession.query(UserEquips).filter_by(uid=uid).all()
    res = []
    for i in equips:
        if i.owner != -1:
            res.append({'kind':i.equipKind, 'owner':i.owner})
    return res
    
#NEW_RANK = 10
def getRankTable(uid):
    #user = getUser(uid)
    challenge = DBSession.query(UserChallengeFriend).filter_by(uid=uid).one()
    if challenge.challengeNum >= datas['PARAMS']['newRank']:
        rank = UserGroupRank
    else:
        rank = UserNewRank
    return rank
    
#在10次挑战结束的时候进行数据迁移 如果挑战数据为空 
def getRank(uid):
    #user = getUser(uid)
    challenge = DBSession.query(UserChallengeFriend).filter_by(uid=uid).one()
    if challenge.challengeNum >= datas['PARAMS']['newRank']:
        rank = DBSession.query(UserGroupRank).filter_by(uid=uid).one()
    else:
        rank = DBSession.query(UserNewRank).filter_by(uid=uid).one()
    #res = [rank.score, rank.rank]
    return rank

def calculateStage(id, level):
    return datas['soldier'][id]
    
def updateDrugNum(uid, tid, num):
    try:
        drug = DBSession.query(UserDrugs).filter_by(uid=uid, drugKind=tid).one()
    except:
        drug = UserDrugs(uid=uid, drugKind=tid, num=0)
        DBSession.add(drug)
    drug.num += num
def updateHerbNum(uid, tid, num):
    try:
        herb = DBSession.query(UserHerb).filter_by(uid=uid, kind=tid).one()
    except:
        herb = UserHerb(uid=uid, kind=tid, num=0)
        DBSession.add(herb)
    herb.num += num
def getKindId(s):
    return datas['Str2IntKind'][s]['id']
def getKindStr(k):
    return datas['TableMap'][k]['name']
def updateGoodsNum(uid, kind, tid, num):
    if kind == getKindId('magicStone') or kind == getKindId('goodsList'):
        try:
            stone = DBSession.query(UserGoods).filter_by(uid=uid, kind = kind, id=tid).one()
        except:
            stone = UserGoods(uid=uid, kind = kind, id=tid, num=0)
            DBSession.add(stone)
        stone.num += num
    elif kind == getKindId('drug'):
        updateDrugNum(uid, tid, num)
    elif kind == getKindId('herb'):
        updateHerbNum(uid, tid, num)
    elif getKindStr(kind) in ['silver', 'gold', 'crystal']:
        gain = {getKindStr(kind): num}
        doGain(uid, gain)
    else:
        print 'error not support update', kind, tid, num
def getGoodsNum(uid, kind, tid):
    try:
        stone = DBSession.query(UserGoods).filter_by(uid=uid, kind = kind, id=tid).one()
        return stone.num
    except:
        return 0

def getOtherData(oid):
    soldiers = getChallengeSoldiers(oid)
    equips = getChallengeEquips(oid)
    skills = DBSession.query(UserSkills).filter_by(uid=oid).all()
    skills = [[i.soldierId, i.skillId, i.level] for i in skills] 
    user = getUser(oid)
    return dict(soldiers=soldiers, equips=equips, skills=skills, cityDefense=user.cityDefense)


def getFarmNum(level):
    if level < 45:
        return level+5
    return 50
def getFarmCoff(level):
    if level < 20:
        return 100
    if level < 40:
        return 100+(level-19)*5
    return 2

def getFarmIncome(level):
    if level < 10:
        return 200
    if level < 20:
        return 216
    if level < 30:
        return 278
    return 323

def getTotalIncome(level):
    num = getFarmNum(level)
    per = getFarmIncome(level)
    coff = getFarmCoff(level)
    return num*per*coff/100

def getParams(k):
    return datas['PARAMS'][k]

def getFullGameParam(k):
    return FullGameParam[k]


def killSoldiers(uid, sols):
    for i in sols:
        #print i
        soldier = DBSession.query(UserSoldiers).filter_by(uid=uid).filter_by(sid=i).one()
        DBSession.delete(soldier)
        solEquips = DBSession.query(UserEquips).filter_by(uid=uid).filter_by(owner=i).all()
        #删除非套装装备
        for e in solEquips:
            if getData("equip", e.equipKind)["suit"] == 0:
                DBSession.delete(e)
            else:
                e.owner = -1
