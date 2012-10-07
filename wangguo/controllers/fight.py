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
from wangguo.controllers.util import *

#from wangguo.model import DBSession, metadata
from wangguo.model import *

__all__ = ['FightController']


class FightController(BaseController):
    #增加任务完成数目 num = 0 表示出现新的用户任务num += num
    @expose('json')
    def makeFighting(self, uid, kind, crystal, gold):
        uid = int(uid)
        kind = int(kind)
        crystal = int(crystal)
        gold = int(gold)

        cost = {'crystal':crystal, 'gold':gold}
        ret = checkCost(uid, cost)
        if ret:
            doCost(uid, cost)
            fighting = UserFighting(uid=uid, failNum = 0, kind=kind)
            DBSession.add(fighting)
            return dict(id=1)
        return dict(id=0)

    @expose('json')
    def attackArena(self, uid, oid, crystal, gold):
        uid = int(uid)
        oid = int(oid)
        crystal = int(crystal)
        gold = int(gold)
        #擂台不存在了
        try:
            arena = DBSession.query(UserFighting).filter_by(uid=oid).one()
        except:
            return dict(id=0, status=0)

        cost = {'crystal':crystal, 'gold':gold}
        ret = checkCost(uid, cost)
        if ret:
            doCost(uid, cost)
            record = UserFightRecord(uid=uid, oid=oid, time=getTime())
            DBSession.add(record)
            oData = getOtherData(oid) 
            
            oData.update({'id':1})
            return oData
        return dict(id=0, status=1)
    #胜利才需要同步数据
    @expose('json')
    def attackOver(self, uid, oid, sols, crystal, gold, win):
        uid = int(uid)
        oid = int(oid)
        sols = json.loads(sols)
        crystal = int(crystal)
        gold = int(gold)
        win = int(win)
        gain = {'crystal':crystal, 'gold':gold}
        doGain(uid, gain)

        attackRank = DBSession.query(UserAttack).filter_by(uid=uid).one()
        attackRank.total += 1
        if win == 1:
            attackRank.suc += 1

        for i in sols:
            soldier = DBSession.query(UserSoldiers).filter_by(uid=uid).filter_by(sid=i[0]).one()
            soldier.health = i[1]
            soldier.exp = i[2]
            soldier.dead = i[3]
            soldier.level = i[4]
        return dict(id=1)

    #tingFailMaxNum应对结束 就可以重新挑战
    @expose('json')
    def defenseOther(self, uid, oid):
        uid = int(uid)
        oid = int(oid)
        oData = getOtherData(oid)
        oData.update({'id':1})
        return oData
    @expose('json')
    def defenseOver(self, uid, oid, sols, crystal, gold, win):
        uid = int(uid)
        oid = int(oid)
        sols = json.loads(sols)
        crystal = int(crystal)
        gold = int(gold)
        win = int(win)


        defenseRank = DBSession.query(UserDefense).filter_by(uid=uid).one()
        defenseRank.total += 1
        if win == 1:
            defenseRank.suc += 1

        for i in sols:
            soldier = DBSession.query(UserSoldiers).filter_by(uid=uid).filter_by(sid=i[0]).one()
            soldier.health = i[1]
            soldier.exp = i[2]
            soldier.dead = i[3]
            soldier.level = i[4]

        arena = DBSession.query(UserFighting).filter_by(uid=uid).one()
        if win == 0:
            arena.failNum += 1

        params = datas['PARAMS']

        record = DBSession.query(UserFightRecord).filter_by(uid=oid, oid=uid).one()
        DBSession.delete(record)

        #最大失败次数 则删除擂台
        if arena.failNum >= params['maxFailNum']:#擂台超期 清理 挑战数据
            records = DBSession.query(UserFightRecord).filter_by(oid=uid).all()
            for i in records:
                DBSession.delete(i)
            DBSession.delete(arena)
            
        gain = {'crystal':crystal, 'gold':gold}
        doGain(uid, gain)
        return dict(id=1)

    @expose('json')
    def defenseTimeOut(self, uid):
        uid = int(uid)
        try:
            arena = DBSession.query(UserFighting).filter_by(uid=uid).one()
            DBSession.delete(arena)
        except:
            pass

        records = DBSession.query(UserFightRecord).filter_by(oid=uid).all()
        for i in records:
            DBSession.delete(i)
        return dict(id=1)

    #获取所有挑战者信息 如果挑战这太多 则 获取部分limit100
    @expose('json')
    def getMyArena(self, uid):
        uid = int(uid)
        try:
            arena = DBSession.query(UserFighting).filter_by(uid=uid).one()
            arena = [[arena.failNum, arena.kind]]
        except:
            arena = []
            #return dict(id=1, arena = [], challengers = [])

        challengers = DBSession.query(UserFightRecord).filter_by(oid=uid).limit(100).all()
        temp = []
        for i in challengers:
            try:
                userData = DBSession.query(UserInWan).filter_by(uid=i.uid).one()
                attackRank = DBSession.query(UserAttack).filter_by(uid=i.uid).one()
            except:
                continue
            temp.append([i.uid, i.time, userData.name, userData.level, attackRank.total, attackRank.suc])    
        return dict(id=1, arena = arena, challengers = temp)


    @expose('json')
    def getArenaRecord(self, uid):
        uid = int(uid)
        record = DBSession.query(UserFightRecord).filter_by(uid=uid).all()
        record = [[i.oid, i.time] for i in record]
        return dict(id=1, record=record)

        

    @expose('json')
    def getArenaNum(self, uid):
        uid = int(uid)
        arenaNum = DBSession.query(UserFighting).count()
        return dict(id=1, arenaNum=arenaNum)
    #拒绝使用缓存 重度依赖MYSQL 数据库 直到 增加机器
    @expose('json')
    def getRandArena(self, uid, offset, limit):#随机偏移 数量
        uid = int(uid)
        offset = int(offset)
        limit = int(limit)

        arena = DBSession.query(UserFighting).all()
        res = range(offset, min(offset+limit, len(arena)))
        res += range(0, min(limit-len(res), offset))
        ret = []
        for i in res:
            try:
                userData = DBSession.query(UserInWan).filter_by(uid=arena[i].uid).one()
                defenseRank = DBSession.query(UserDefense).filter_by(uid=arena[i].uid).one()
            except:
                continue
            ret.append([arena[i].uid, arena[i].failNum, arena[i].kind, userData.name, userData.level, defenseRank.total, defenseRank.suc])
        return dict(id=1, arena=ret)

    @expose('json')
    def getAttackRank(self, uid, offset, limit):
        uid = int(uid)
        offset = int(offset)
        limit = int(limit)

        try:
            result = attackCollect.find_one()['res']
            ret = result[offset:offset+limit]
            ret = [[i['uid'], i['papayaId'], i['suc'], i['rank'], i['name'], i['total'], i['level']] for i in ret]
        except:
            ret = []

        return dict(id=1, res=ret)

    @expose('json')
    def getDefenseRank(self, uid, offset, limit):
        uid = int(uid)
        offset = int(offset)
        limit = int(limit)

        try:
            result = defenseCollect.find_one()['res']
            ret = result[offset:offset+limit]
            ret = [[i['uid'], i['papayaId'], i['suc'], i['rank'], i['name'], i['total'], i['level']] for i in ret]
        except:
            ret = []

        return dict(id=1, res=ret)

