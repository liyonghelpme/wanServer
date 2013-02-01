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

def getSellBuildData(id):
    gain = getGain('building', id)
    SELL_KEY = set(['people', 'cityDefense'])
    res = {}
    for k in gain:
        if k in SELL_KEY:
            res[k] = gain[k]
    return res
            

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
        res[i.sid] = dict(id=i.kind, name=i.name, inTransfer=i.inTransfer, transferStartTime=i.transferStartTime, inDead=i.inDead, deadStartTime=i.deadStartTime)
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
    return FullGameParams[k]


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
def killHero(uid, hero):
    curTime = getTime()
    for i in hero:
        soldier = DBSession.query(UserSoldiers).filter_by(uid=uid).filter_by(sid=i).one()
        soldier.inDead = 1
        soldier.deadStartTime = curTime
        


def hanData(name, data):
    names = []
    key = []
    res = []
    f = data.fetch_row(0, 1)
    for i in f:
        i = dict(i)
        if i.get('name') != None and i.get('id') != None:
            i['name'] = name+str(i['id'])
        if i.get('engName') != None:
            i.pop('engName')
        it = list(i.items())
        it = [list(k) for k in it]
        #it[4][1] = 'build'+str(i['id'])
        key = [k[0] for k in it]
        a = [k[1] for k in it]
        if i.get('id') != None:
            res.append([i['id'], a])

        if i.get('id') == None:
            return names
        if f[0].get('name', None) != None:
            if f[0].get('engName') != None:
                names = [ [name+str(i['id']), [i['name'], i.get('engName')]] for i in f]
            else:
                names = [ [name+str(i['id']), i['name']] for i in f]
                
        else:
            names = []


    if name == 'StoreAttWords':
        names = []
        res = []
        for i in f:
            k = i['key']
            n = 'StoreAttWords%s' % k
            res.append([k, n]);
            names.append([n, i['word']])
        #print 'var', name, '=', 'dict(', json.dumps(res), ');'
        return names

    if name == 'StoreWords':
        names = []
        res = []
        for i in f:
            k = i['kind']*10000+i['id']
            n = 'StoreWord%d' % k
            res.append([k,  n])
            names.append([n, i['words']])

        #print 'var', name, '=', 'dict(', json.dumps(res), ');'
        return names
    if name == 'newParam':
        res = {}
        for i in f:
            res[i['key']] = i['value']
        res = res.items()
        #print 'var', 'PARAMS', '=', 'dict(', json.dumps(res), ');'
        return []
    if name == 'PARAMS':
        res = {}
        for i in f:
            for k in i:
                res[k] = i[k]
        res = res.items()
        #print 'var', name, '=', 'dict(', json.dumps(res), ');'
        return []
    if name == 'heroSkill':
        res = []
        for i in f:
            res.append([i['hid'], i['skillId']])
        #print 'var', name, '=', 'dict(',json.dumps(res), ');'
        return []
    #if name == 'fightCost':
    #    res = []
    #    return []


    if name == 'loveTreeHeart':
        res = []
        for i in f:
            res = json.loads(i['num'])
        #print 'var', name, '=', json.dumps(res), ';'
        return []
    if name == 'statusPossible':
        res = []
        reward = []
        for i in f:
            res.append([i['id'], i['possible']])
            reward.append([i['id'], [i['gainsilver'], i['gaincrystal'], i['gaingold'], [i['sunflower'], i['sun'], i['flower'], i['star'], i['moon']]] ])
        #print 'var', name, '=', json.dumps(res), ';'
        key = ['gainsilver', 'gaincrystal', 'gaingold', 'nums']
        #print 'var', name+'Key', '=', json.dumps(key), ';'
        #print 'var', name+'Data', '=', 'dict(', json.dumps(reward), ');'
        return []


    #bigId--->monsterId
    if name == 'monsterAppear':
        res = dict()
        for i in f:
            r = res.get(i['firstNum']/10, [])
            r.append(i['id'])
            res[i['firstNum']/10] = r
        res = res.items()
        #print 'var', name, '=', 'dict(', json.dumps(res), ');'
        return []

    """
    if name == 'mineProduction':
        res = []
        keys = []
        for i in f:
            keys = i.keys()
            res.append(i.items())
        #print 'var', name+'Key', '=', json.dumps(keys), ';'
        #print 'var', name+'Data', '=', 'dict(', json.dumps(res), ');'
        return []
    """
    if name == 'equipLevel':
        for i in f:
            res = json.loads(i['levelCoff'])
        #print 'var', name, '=', json.dumps(res), ';'
        return []
    if name == 'levelDefense':
        res = []
        for i in f:
            res.append([i['level'], i['defense']])
        #print 'var', name, '=', json.dumps(res), ';'
        return []
    
    if name == 'mapReward':
        res = []
        for i in f:
            res.append([i['id'], json.loads(i['reward'])])
        #print 'var', name, '=', 'dict(', json.dumps(res), ');'
        return []

            
    if name == 'challengeReward':
        for i in f:
            res = json.loads(i['reward'])
        #print 'var', name, '=', json.dumps(res), ';'
        return []

    if name == 'soldierTransfer':
        res = []
        for i in f:
            res = json.loads(i['level'])
        #print 'var', name, '=', json.dumps(res), ';'
        return []
    if name == 'soldierAttBase':
        res = []
        for i in f:
            res = json.loads(i['base'])
        #print 'var', name, '=', json.dumps(res), ';'
        return []
    if name == 'soldierGrade':
        res = []
        for i in f:
            res.append([i['id'], int(i['level']*100)])
        #print 'var', name, '=', 'dict(', json.dumps(res), ');'
        return []
    if name == 'soldierKind':
        res = []
        for i in f:
            i['attribute'] = [int(at*100) for at in json.loads(i['attribute'])]
            res.append([i['id'], i['attribute']])

        #print 'var', name, '=', 'dict(', json.dumps(res), ');'
        return []
    if name == 'soldierLevel':
        res = []
        for i in f:
            res = json.loads(i['levelData'])
        #print 'var', name, '=', json.dumps(res), ';'
        return []
        

    if name == 'mapDefense':
        res = []
        for i in f:
            res.append([i['id'], i['defense']])
        #print 'var', name, '=', 'dict(', json.dumps(res), ');'
        return []
            

    if name == 'levelExp':
        res = []
        for i in f:
            res = json.loads(i['exp'])
        #print 'var', name, '=', json.dumps(res), ';'
        return [] 
     
    if name == 'RoundMonsterNum':
        res = {}
        key = ['id', 'mons']
        for i in f:
            k = i['id']
            v = [
                [i['kind0'], i['num0']],
                [i['kind1'], i['num1']],
                [i['kind2'], i['num2']],
                [i['kind3'], i['num3']],
                [i['kind4'], i['num4']],
            ]
            temp = []
            for p in v:
                if p[0] != -1:
                    temp.append(p)
            res[k] = [k, temp]
        res = res.items()
        #print 'var', name+'Key', '=', json.dumps(key), ';'
        #print 'var', name+'Data', '=', 'dict(', json.dumps(res), ');'
        return []

    
    if name == 'mapMonster':#大地图 小关的怪兽位置 类型 等级
        res = {}
        key = []
        for i in f:
            k = i['big']*10+i['small']
            mons = res.get(k, [])
            i.pop('big')
            i.pop('small')
            key = i.keys()
            it = i.values()
            mons.append(it)
            res[k] = mons
        res = res.items()
        #print 'var', name+'Key', '=', json.dumps(key), ';'
        #print 'var', name+'Data', '=', 'dict(', json.dumps(res), ');'
        return []
    if name == 'soldierLevelExp':
        res = []
        for i in f:
            i = dict(i)
            res.append([i['id'], json.loads(i['exp'])])
        #print 'var', name, '=', 'dict(', json.dumps(res), ');'
        return []

    #名字 描述desc 出现复活药水的数据
    if name == 'drug' or name == 'equip' or name == 'skills':
        res = []
        keys = []
        names = []
        #药品有商店名字和全名
        hasStoreName = False
        hasLevelName = False
        for i in f:
            i = dict(i)
            i['name'] = name+str(i['id'])
            i['des'] = name+'Des'+str(i['id'])
            i.pop('engName')
            if i.get('storeName') != None:
                hasStoreName = True
                i['storeName'] = name+'StoreName'+str(i['id'])
            if i.get('levelName') != None:
                hasLevelName = True
                i['levelName'] = name+'LevelName'+str(i['id'])
            if i.get('engDes') != None:
                i.pop('engDes')

            it = list(i.items())
            it = [list(k) for k in it]
            key = [k[0] for k in it]
            a = [k[1] for k in it]
            res.append([i['id'], a])

        
        names = [[name+str(i['id']), [i['name'], i['engName']]] for i in f]
        names += [[name+'Des'+str(i['id']), [i['des'], i.get('engDes', "")]] for i in f ]
        if hasStoreName:
            names += [[name+'StoreName'+str(i['id']), i['storeName']] for i in f]
        if hasLevelName:
            names += [[name+'LevelName'+str(i['id']), i['levelName']] for i in f]
        
        #print 'var', name+'Key', '=', json.dumps(key), ';'
        #print 'var', name+'Data', '=', 'dict(', json.dumps(res), ');'
        return names

    #if name == 'skills':
         
    if name == 'magicStone':
        res = []
        keys = []
        names = []
        for i in f:
            i = dict(i)
            i['name'] = name+str(i['id'])
            i['des'] = name+'Des'+str(i['id'])
            i.pop('engName')
            i.pop('pos0')
            i.pop('pos14')
            i.pop('pos29')
            i.pop('pos44')
            i.pop('pos59')
            i['possible'] = json.loads(i['possible'])
            it = list(i.items())
            it = [list(k) for k in it]
            key = [k[0] for k in it]
            a = [k[1] for k in it]
            res.append([i['id'], a])

        names = [[name+str(i['id']), [i['name'], i['engName']]] for i in f]
        names += [[name+'Des'+str(i['id']), i['des']] for i in f ]
        #print 'var', name+'Key', '=', json.dumps(key), ';'
        #print 'var', name+'Data', '=', 'dict(', json.dumps(res), ');'
        return names

    if name == 'goodsList':
        res = []
        keys = []
        names = []
        for i in f:
            i = dict(i)
            i['name'] = name+str(i['id'])
            i['des'] = name+'Des'+str(i['id'])
            i.pop('engName')
            i.pop('maxFail')
            i.pop('minFail')
            i.pop('maxBreak')
            i.pop('minBreak')
            i['possible'] = json.loads(i['possible'])

            it = list(i.items())
            it = [list(k) for k in it]
            key = [k[0] for k in it]
            a = [k[1] for k in it]
            res.append([i['id'], a])

        names = [[name+str(i['id']), [i['name'], i['engName']]] for i in f]
        names += [[name+'Des'+str(i['id']), i['des']] for i in f ]
        #print 'var', name+'Key', '=', json.dumps(key), ';'
        #print 'var', name+'Data', '=', 'dict(', json.dumps(res), ');'
        return names
        
        
    if name == 'herb':#药材中 描述
        res = []
        key = []
        for i in f:
            i = dict(i)
            i['name'] = 'herb'+str(i['id'])
            i['des'] = 'herbDes'+str(i['id'])
            i.pop('engName')
            it = list(i.items())
            it = [list(k) for k in it]
            #it[4][1] = 'build'+str(i['id'])
            key = [k[0] for k in it]
            a = [k[1] for k in it]
            res.append([i['id'], a])
        names = [['herb'+str(i['id']), [i['name'], i['engName']]] for i in f]
        names += [ ['herbDes'+str(i['id']), i['des']] for i in f]
        #print 'var', name+'Key', '=', json.dumps(key), ';'
        #print 'var', name+'Data', '=', 'dict(', json.dumps(res), ');'
        return names
            


    if name == 'smallMapInfo':
        res = []
        key = ['rewards']
        for i in f:
            i = dict(i)
            rewards = []
            if i['reward0Pos'] > 0:
                rewards.append([i['reward0'], i['reward0Pos']])
            if i['reward1Pos'] > 0:
                rewards.append([i['reward1'], i['reward1Pos']])
            res.append([i['id'], rewards])

    #Words 存放对话框字符串
    #strings 中存放物品名字 任务字符串 之类 来自其它数据表的字符串

    
    #name list [name, [chinese, english]]
    #res key key = [k[0] for k in it]
    #res data data = [ [id, [k[1] for k in it]] ]
    if name == 'soldier':
        res = []
        key = []
        for i in f:
            i = dict(i)
            #i['stage'] = json.loads(i['stage'])
            i['name'] = 'soldier' + str(i['id'])
            i.pop('engName')
            it = list(i.items())
            it = [list(k) for k in it]
            a = [k[1] for k in it]
            key = [k[0] for k in it]
            res.append([i['id'], a])

        names = [['soldier'+str(i['id']), [i['name'], i['engName']]] for i in f]
        #print 'var', name+'Key', '=', json.dumps(key), ';'
        #print 'var', name+'Data', '=', 'dict(', json.dumps(res).replace('0.0', '0'), ');'
        return names 
    if name == 'allTasks':
        res = []
        for i in f:
            i = dict(i)
            i['title'] = 'title'+str(i['id'])
            i['des'] = 'des'+str(i['id'])
            i['commandList'] = json.loads(i['commandList'])
            newCom = []
            for c in i['commandList']:
                if c.get('tip') != None:
                    old = c['tip']
                    c['tip'] = 'taskTip'+str(c['msgId'])
                newCom.append(c.items())
            i['commandList'] = newCom

            i['stageArray'] = json.loads(i['stageArray'])
            i['goldArray'] = json.loads(i['goldArray'])
            i['expArray'] = json.loads(i['expArray'])

            it = list(i.items())
            it = [list(k) for k in it]
            key = [k[0] for k in it]
            a = [k[1] for k in it]
            res.append([i['id'], a])

        names = [['title'+str(i['id']), [i['title'], i['engTitle']]] for i in f]
        names += [ ['des'+str(i['id']), [i['des'], i['engDes']]] for i in f]
        #print 'var', name+'Key', '=', json.dumps(key), ';'
        #print 'var', name+'Data', '=', 'dict(', json.dumps(res), ');'
        print 'task title'
        return names


    ##print json.dumps(names)
    #for n in names:
    #    #print '[','"'+n[0]+'"', ',','"'+ n[1]+'"','],'

    #print 'var', name+'Key', '=', json.dumps(key), ';'
    #print 'var', name+'Data', '=', 'dict(', json.dumps(res), ');'
    return names

def getAllNames():
    con = MySQLdb.connect(host = 'localhost', user='root', passwd=DB_PASSWORD, db='Wan2', charset='utf8')
    sqlName = ['building','crystal', 'challengeReward', 'drug', 'equip', 'fallThing', 'gold', 'herb', 'levelExp', 'plant', 'prescription', 'silver', 'soldier', 'soldierAttBase', 'soldierGrade', 'soldierKind', 'soldierLevel', 'soldierTransfer',  'allTasks', 'mapDefense',  'soldierName', 'mapReward', 'levelDefense', 'mineProduction', 'goodsList', 'equipLevel', 'magicStone', 'skills', 'monsterAppear', 'statusPossible', 'loveTreeHeart', 'heroSkill', 'mapBlood', 'fightingCost', 'newParam', 'StoreWords', 'StoreAttWords', 'MoneyGameGoods', 'ExpGameGoods', 'equipSkill', 'levelMaxFallGain', 'RoundMonsterNum', 'RoundMapReward', 'mapMonster']
    allNames = []
    for i in sqlName:
        sql = 'select * from '+i
        con.query(sql)
        res = con.store_result()
        allNames += hanData(i, res)
    con.close()
    return allNames

