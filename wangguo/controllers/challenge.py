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
import random
from sqlalchemy.sql import select

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
    
    @expose('json')
    def clearProtectTime(self, uid):
        uid = int(uid)
        challengeState = DBSession.query(UserChallengeState).filter_by(uid=uid).one()
        challengeState.protectTime = 0
        return dict(id=1)
    
    def getUserInfo(self, userRank, otherUser):
        return {'uid':otherUser.uid, 
                'id':otherUser.papayaId, 
                'score':userRank.score, 
                'rank':userRank.rank, 
                'name':otherUser.name, 
                'level':otherUser.level, 
                'cityDefense':otherUser.cityDefense, 
                "silver":otherUser.silver, 
                "crystal":otherUser.crystal,
                "heroId":otherUser.heroId}
    @expose('json')
    def getRevenge(self, uid, oid):
        uid = int(uid)
        oid = int(oid)

        userRank = getRank(oid)
        otherUser = getUser(oid)
        user = self.getUserInfo(userRank, otherUser)

        return dict(id=1, user= user)

    #足够活跃的用户随机生成1个
    #等级区间内 活跃用户随机生成1个 作为挑战对象
    @expose('json')
    def getRandChallenge(self, uid):
        uid = int(uid)
        user = getUser(uid)
        #获取某个等级范围的用户
        userLevel = user.level
        levOff = 2#+-2 +-4 +-8
        #寻找活跃用户
        now = getTime()
        lastProtectTime = now - getFullGameParam("ProtectTime")
        find = False
        while levOff < getFullGameParam("maxLevelOff"):
            #print 'levOff', levOff, lastProtectTime
            #首先获取用户范围
            #接着获取随机的用户 开始位置
            twoUid = DBSession.execute("select max(uid), min(uid) from UserChallengeState where uid != %d and protectTime <= %d and level >= %d and level <= %d and activeScore > %d " % (uid, lastProtectTime, (userLevel-levOff), userLevel+levOff, getFullGameParam("activeThresh"))).fetchall()
            
            twoFind = False
            if len(twoUid) > 0:
                maxUid = twoUid[0][0]
                minUid = twoUid[0][1]
                #集合为空
                if maxUid != None and minUid != None:
                    print "maxUid", maxUid, minUid
                    twoFind = True
                    #>= UID
                    cut = random.randint(minUid, maxUid)
                    print "cut is", cut
                    
                    #limit产生1个即可
                    possibles = DBSession.query(UserChallengeState).filter("uid >= %d and uid != %d and protectTime <= %d and level >= %d and level <= %d and activeScore > %d " % (cut, uid, lastProtectTime, (userLevel-levOff), userLevel+levOff, getFullGameParam("activeThresh"))).limit(1).all()
                    #print 'possibles', possibles, lastProtectTime, userLevel-levOff, userLevel+levOff, getFullGameParam("activeThresh")
                    if len(possibles) > 0:
                        other = possibles[0]
                        try:
                            exist = DBSession.query(UserChallengeRecord).filter_by(uid=uid, oid=other.uid).one()
                        except:
                            userRank = getRank(other.uid)
                            #避免只有UserChallengeState 但是没有该用户的数据
                            otherUser = getUser(other.uid)
                            #参考客户端的 data/constant 中定义的ChallengeRankKey
                            find = True
                            break
            levOff *= 2
        if not find:
            #没有活跃用户可打 攻击非活跃用户
            possibles = DBSession.query(UserChallengeState).filter("activeScore <= %d and protectTime <= %d and uid != %d" % (getFullGameParam("activeThresh"), lastProtectTime, uid)).limit(20).all()
            if len(possibles) > 0:
                rd = random.randint(0, len(possibles)-1)
                other = possibles[rd]
                try:
                    exist = DBSession.query(UserChallengeRecord).filter_by(uid=uid, oid=other.uid).one()
                except:
                    #var cs = new ChallengeScene(uid, papayaId, score, rank, CHALLENGE_FRI, data[diff]);

                    userRank = getRank(other.uid)
                    otherUser = getUser(other.uid)
                    #参考客户端的 data/constant 中定义的ChallengeRankKey
                    find = True
                    
                #return dict(id=1, uid=other.uid)
        if find:
            user = self.getUserInfo(userRank, otherUser)
            return dict(id=1, user=user)

        #没有用户可用
        return dict(id=0)
                

    #敌人满血满魔 
    #只是获取敌人的士兵数据
    @expose('json')
    def challengeOther(self, uid, oid):
        uid = int(uid)
        oid = int(oid)

        oData = getOtherData(oid)
        oData.update({'id':1})
        return oData
    #胜利积分增级 登录返回用户排名的时候刷新排名
    #排名只在1个小时更新一次
    #士兵状态更新 需要一并发出
    #挑战普通人 抢走水晶数量
    @expose('json')
    def realChallenge(self, uid, fid):
        uid = int(uid)
        fid = int(fid)
        now = getTime()
        #增加挑战记录
        try:
            exist = DBSession.query(UserChallengeRecord).filter_by(uid=uid, oid=fid).one()
            #今天已经挑战过了
        #没有挑战记录则增加
        except:
            record = UserChallengeRecord(uid=uid, oid=fid, time=now)
            DBSession.add(record)
            pass
        #增加挑战活跃度
        challengeState = DBSession.query(UserChallengeState).filter_by(uid=uid).one()
        challengeState.activeScore += getFullGameParam("challengeScore")
        #增加挑战次数
        challenge = DBSession.query(UserChallengeFriend).filter_by(uid=uid).one()
        challenge.challengeNum += 1

        challenge.challengeTime = now
        challenge.lastMinusTime = now

        user = getUser(uid)
        #第10次挑战迁移数据 新手阶段已经结束 
        if challenge.challengeNum == datas['PARAMS']['newRank']:
            oldRank = DBSession.query(UserNewRank).filter_by(uid=uid).one()
            oldRank.finish = 1

            num = DBSession.query(UserGroupRank).filter("score >= %d" % (oldRank.score)).count()
            newRank = UserGroupRank(uid=uid, score=oldRank.score, rank=num, papayaId=user.papayaId, name=user.name)
            DBSession.add(newRank)
        return dict(id=1)

    @expose('json')
    def challengeResult(self, uid, fid, reward, score, sols, mid, win, revenge, deadHero): 
        #print "challengeResult",uid, fid, reward, score, sols, mid, win, revenge, hero
        uid = int(uid)
        fid = int(fid)
        reward = json.loads(reward)
        score = int(score)
        sols = json.loads(sols)
        mid = int(mid)
        win = int(win)
        revenge = int(revenge)
        deadHero = json.loads(deadHero)

        user = getUser(uid)
        rank = getRank(uid)
        rank.score += score
        rank.score = max(0, rank.score)
        doGain(uid, reward)

        challengeState = DBSession.query(UserChallengeState).filter_by(uid=fid).one()
        if win:
            challengeState.activeScore -= getFullGameParam("winScore")
        else:
            challengeState.activeScore -= getFullGameParam("lostScore")
        
        #小于保护阈值 且 没有开启保护状态
        now = getTime()
        passTime = now - challengeState.protectTime
        if passTime >= getFullGameParam("ProtectTime")  and challengeState.activeScore <= getFullGameParam("activeThresh"):
            challengeState.protectTime = now
        killSoldiers(uid, sols)

        #挑战成功才记录消息 并 等待对方登录
        if win == 1 and revenge == 0:#不是复仇 则 记录 消息 用于扣除资源
            msg = UserMessage(uid=uid, fid=fid, kind=datas['PARAMS']['MSG_CHALLENGE'], param=json.dumps(reward), time=getTime(), mid=mid)
            DBSession.add(msg)
        killHero(uid, deadHero)
        return dict(id=1)

    #客户端读取 抢劫消息
    @expose('json')
    def readChallengeMsg(self, uid, msgs, totalCost):
        uid = int(uid)
        msgs = json.loads(msgs)
        totalCost = json.loads(totalCost)

        for m in msgs:
            msg = DBSession.query(UserMessage).filter_by(uid=m[0], fid=uid, mid=m[1]).one()
            DBSession.delete(msg)
        doCost(uid, totalCost)
        return dict(id=1)
    

    #sid health exp dead level
    #士兵闯关成功升级
    #士兵闯关失败 更新士兵 数据 dead = 1 的 将被删除
    #测试： 士兵使用装备 士兵 阵亡 装备消除
    @expose('json')
    def challengeOver(self, uid, sols, reward, star, big, small, rewardEquip, deadHero):
        uid = int(uid)
        sols = json.loads(sols)
        try:
            reward = json.loads(reward)
        except:
            reward = {}
        star = int(star)
        big = int(big)
        small = int(small)
        rewardEquip = json.loads(rewardEquip)
        deadHero = json.loads(deadHero)

        print sols
        killSoldiers(uid, sols)
        #死亡士兵 杀死
        print reward
        doGain(uid, reward)
        curStar = DBSession.query(UserChallenge).filter_by(uid=uid).filter_by(big=big).filter_by(small=small).one()
        #只有获取更多星才更新数据
        if curStar.star < star:
            curStar.star = star

        for i in rewardEquip:
            equip = UserEquips(uid=uid, eid=i['eid'], equipKind=i['kind'])
            DBSession.add(equip)
        killHero(uid, deadHero)

        return dict(id=1)
            
            

        

