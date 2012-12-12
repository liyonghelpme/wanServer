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

__all__ = ['ChallengeController']

#位置上升之后调整所有在我位置之后的用户rank+1
class ChallengeController(BaseController):
    #得到排行榜数据
    #uid papayaId score rank name
    @expose('json')
    def getRank(self, uid, offset, limit):  
        uid = int(uid)
        offset = int(offset)
        limit = int(limit)
        #user = getUser(uid)
        challenge = DBSession.query(UserChallengeFriend).filter_by(uid=uid).one()
        #10次以上为普通挑战
        if challenge.challengeNum >= datas['PARAMS']['newRank']:
            ranks = groupRankCollect.find_one()["res"]
            ret = ranks[offset:offset+limit]
            res = [[i['uid'], i['papayaId'], i['score'], i['rank'], i['name'], i['level']] for i in ret]
        #10次下新手 新手finish 表示不能挑战 在生成新的排名的时候才可以消除这些finish=1 首先删除
        else:
            ranks = newRankCollect.find_one()["res"]
            ret = ranks[offset:offset+limit]
            res = [[i['uid'], i['papayaId'], i['score'], i['rank'], i['name'], i['level']] for i in ret]
        return dict(id=1, res=res)
    #big = 0 small = 0
    @expose('json')
    def challengeSelf(self, uid, oid):
        con = MySQLdb.connect(host = 'localhost', user='root', passwd='badperson3', db='Wan2', charset='utf8')
        sql = 'select * from mapMonster'
        con.query(sql)
        res = con.store_result()
        allData = res.fetch_row(0, 1)


        allMapData = {}
        for a in allData:
            k = a['big']*10+a['small']
            mons = allMapData.get(k, [])
            mons.append(a)
            allMapData[k] = mons

        mons = allMapData[0]

        print mons
        #for i in mons:
        #    i['sid'] = -1

        sql = 'select * from mapEquip'
        con.query(sql)
        res = con.store_result()
        allData = res.fetch_row(0, 1)
        allEquip = {}
        for a in allData:
            k = a['big']*10+a['small']
            equip = allEquip.get(k, [])
            equip.append({'kind':a['id'], 'level':a['level'], 'owner':a['owner']})
            allEquip[k] = equip
        equip = allEquip.get(0, [])
        

        con.close()
        return dict(id=1, soldiers=mons, equips=equip, cityDefense=100)
    #敌人满血满魔 
    @expose('json')
    def challengeOther(self, uid, oid):
        uid = int(uid)
        oid = int(oid)
        curTime = getTime()
        try:
            exist = DBSession.query(UserChallengeRecord).filter_by(uid=uid, oid=oid).one()
            #今天已经挑战过了
            return dict(id=0)
        except:
            pass
        record = UserChallengeRecord(uid=uid, oid=oid, time=curTime)
        DBSession.add(record)

        #soldiers = getSoldiers(oid)
        #soldiers = getChallengeSoldiers(oid)
        #equips = getEquips(oid)
        #equips = getChallengeEquips(oid)
        #skills = DBSession.query(UserSkills).filter_by(uid=oid).all()
        #skills = [[i.soldierId, i.skillId, i.level] for i in skills] 

        oData = getOtherData(oid)

        #user = getUser(uid)
        #user.challengeNum += 1
        challenge = DBSession.query(UserChallengeFriend).filter_by(uid=uid).one()
        challenge.challengeNum += 1
        now = getTime()
        challenge.challengeTime = now
        challenge.lastMinusTime = now
        user = getUser(uid)
        #other = getUser(oid)
        #第10次挑战迁移数据 新手阶段已经结束 
        if challenge.challengeNum == datas['PARAMS']['newRank']:

            oldRank = DBSession.query(UserNewRank).filter_by(uid=uid).one()
            oldRank.finish = 1

            num = DBSession.query(UserGroupRank).filter("score >= %d" % (oldRank.score)).count()
            newRank = UserGroupRank(uid=uid, score=oldRank.score, rank=num, papayaId=user.papayaId, name=user.name)
            DBSession.add(newRank)
            
            #删除旧的新手rank 排名可能不连续 导致新手获取数据失败 标记新手阶段结束
            #DBSession.delete(oldRank)
            #newRank = DBSession.query(UserGroupRank).filter_by(uid=uid).one()
            #newRank.score = oldRank.score
        
        oData.update({'id':1})
        #return dict(id=1, soldiers=soldiers, equips=equips, cityDefense = other.cityDefense, skills=skills)
        return oData
    #胜利积分增级 登录返回用户排名的时候刷新排名
    #排名只在1个小时更新一次
    #士兵状态更新 需要一并发出
    #挑战普通人 抢走水晶数量

    @expose('json')
    def challengeResult(self, uid, fid, crystal, score, sols, mid): 
        uid = int(uid)
        fid = int(fid)
        crystal = int(crystal)
        score = int(score)
        sols = json.loads(sols)
        mid = int(mid)

        user = getUser(uid)
        rank = getRank(uid)
        rank.score += score
        rank.score = max(0, rank.score)
        user.crystal += crystal
        
        killSoldiers(uid, sols)

        msg = UserMessage(uid=uid, fid=fid, kind=datas['PARAMS']['MSG_CHALLENGE'], param=crystal, time=getTime(), mid=mid)
        DBSession.add(msg)

        return dict(id=1)
        

    @expose('json')
    def enableDif(self, uid, big, gold):
        uid = int(uid)
        big = int(big)
        gold = int(gold)
        #small = int(small)
        cost = {'gold':gold}
        ret = checkCost(uid, cost)
        if not ret:
            return dict(id=1, status=0)
        doCost(uid, cost)

        chaLevel = UserUnlockLevel(uid=uid, levelId=big)
        DBSession.add(chaLevel)
        return dict(id=1)


            
            

        

