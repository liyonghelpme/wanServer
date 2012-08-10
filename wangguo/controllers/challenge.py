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
        if challenge.challengeNum >= NEW_RANK:
            ranks = DBSession.query(UserGroupRank).filter("UserNewRank.rank>=%d and UserNewRank.rank<%d" % (offset, offset+limit)).limit(limit).all()
            res = [[i.uid, i.papayaId, i.score, i.rank, i.name] for i in ranks]
        #10次下新手 新手finish 表示不能挑战 在生成新的排名的时候才可以消除这些finish=1 首先删除
        else:
            ranks = DBSession.query(UserNewRank).filter("UserNewRank.rank>=%d and UserNewRank.rank<%d" % (offset, offset+limit)).limit(limit).all()
            res = [[i.uid, i.papayaId, i.score, i.rank, i.name, i.finish] for i in ranks]

        #返回的数据按照rank 排好序
        #数据中没有重复的rank  rank重复则保留uid 为自身的排名数据
        """
        res.sort(cmp=lambda x,y: x[3]-y[3])
        temp = []
        for i in range(0, len(res)):
            if len(temp) == 0:
                temp.append(res[i])
            else:
                if temp[-1][3] != res[i][3]:
                    temp.append(res[i])
                else:
                    if res[i][0] == uid:
                        temp[-1] = res[i]
        """
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
        soldiers = getChallengeSoldiers(oid)
        #equips = getEquips(oid)
        equips = getChallengeEquips(oid)

        #user = getUser(uid)
        #user.challengeNum += 1
        challenge = DBSession.query(UserChallengeFriend).filter_by(uid=uid).one()
        challenge.challengeNum += 1
        now = getTime()
        challenge.challengeTime = now
        challenge.lastMinusTime = now
        user = getUser(uid)
        other = getUser(oid)
        #第10次挑战迁移数据 新手阶段已经结束 
        if challenge.challengeNum == NEW_RANK:

            oldRank = DBSession.query(UserNewRank).filter_by(uid=uid).one()
            oldRank.finish = 1

            num = DBSession.query(UserGroupRank).filter("score >= %d" % (oldRank.score)).count()
            newRank = UserGroupRank(uid=uid, score=oldRank.score, rank=num, papayaId=user.papayaId, name=user.name)
            DBSession.add(newRank)
            
            #删除旧的新手rank 排名可能不连续 导致新手获取数据失败 标记新手阶段结束
            #DBSession.delete(oldRank)
            #newRank = DBSession.query(UserGroupRank).filter_by(uid=uid).one()
            #newRank.score = oldRank.score
        return dict(id=1, soldiers=soldiers, equips=equips, cityDefense = other.cityDefense)
    #胜利积分增级 登录返回用户排名的时候刷新排名
    #排名只在1个小时更新一次
    #士兵状态更新 需要一并发出
    @expose('json')
    def challengeResult(self, uid, crystal, score, sols): 
        uid = int(uid)
        crystal = int(crystal)
        score = int(score)
        sols = json.loads(sols)

        user = getUser(uid)
        rank = getRank(uid)
        rank.score += score
        rank.score = max(0, rank.score)
        user.crystal += crystal
        
        for i in sols:
            soldier = DBSession.query(UserSoldiers).filter_by(uid=uid).filter_by(sid=i[0]).one()
            soldier.health = i[1]
            soldier.exp = i[2]
            soldier.dead = i[3]
            soldier.level = i[4]

        return dict(id=1)
        

            

            
            

        

