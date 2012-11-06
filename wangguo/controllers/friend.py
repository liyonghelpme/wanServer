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
from random import randint
import math

__all__ = ['FriendController']


class FriendController(BaseController):
    @expose('json')
    def finishInvite(self, uid, inviteCode):
        uid = int(uid)
        inviteCode = int(inviteCode)
        user = getUser(uid)
        if user.level >= getParams('inviteLevel'):
            return dict(id=0, status=0)
        inviteRank = DBSession.query(UserInviteRank).filter_by(uid=uid).one()
        if inviteRank.inputYet:
            return dict(id=0, status=1)
        try:
            inv = DBSession.query(UserInviteRank).filter_by(inviteCode=inviteCode).one()
        except:
            return dict(id=0, status=2)
        if inv.uid == uid:
            return dict(id=0, status=3)

        inviteRank.inputYet = True
        #发送邀请成功消息
        inv.inviteNum += 1
        gain = {'gold': getParams('inviteGold')}
        doGain(inv.uid, gain)

        return dict(id=1)
        
    #每天第一次登录 生成新的box
    @expose('json')
    def genNewBox(self, uid):
        uid = int(uid)
        box = DBSession.query(UserTreasureBox).filter_by(uid=uid).one()
        box.has = 1
        box.helperList = '[]'
        return dict(id=1)
    @expose('json')
    def getFriend(self, uid, papayaId):
        uid = int(uid)
        papayaId = int(papayaId)
        try:
            friend = DBSession.query(UserInWan).filter_by(papayaId=papayaId).one()
        except:
            return dict(id=0, status=0)
        
        soldiers = getSoldiers(friend.uid)
        box = DBSession.query(UserTreasureBox).filter_by(uid=friend.uid).one()
        try:
            helperList = json.loads(box.helperList)
        except:
            helperList = []
        papayaIdName = []
        hasBox = box.has
        for i in helperList:
            if i != -1:
                helper = getUser(i)
                papayaIdName.append([helper.papayaId, helper.name])
            else:
                papayaIdName.append([friend.papayaId, friend.name])
            
        mine = DBSession.query(UserCrystalMine).filter_by(uid=friend.uid).one()
        loveTree = DBSession.query(UserBuildings).filter_by(uid=friend.uid, kind=datas['PARAMS']['loveTreeId']).one()
        return dict(id=1, level=friend.level, soldiers=soldiers, fid = friend.uid, name=friend.name, helperList = helperList, hasBox = hasBox, papayaIdName=papayaIdName, mineLevel=mine.level, heartLevel=loveTree.level)

        #该用户没有在服务器注册，fid 返回-1 更新
        #return dict(id=1, level=0, soldiers={}, fid = -1)
    @expose('json')
    def helpOpen(self, uid, fid):
        uid = int(uid)
        fid = int(fid)
        box = DBSession.query(UserTreasureBox).filter_by(uid=fid).one()
        try:
            helperList = json.loads(box.helperList)
        except:
            helperList = []
        if box.has:
            if len(helperList) < datas['PARAMS']['maxBoxFriNum'] and uid not in helperList:

                helperList.append(uid)
                box.helperList = json.dumps(helperList)
                return dict(id=1)
        return dict(id=0, status=0)
    @expose('json')
    def selfOpen(self, uid):
        uid = int(uid)
        box = DBSession.query(UserTreasureBox).filter_by(uid=uid).one()
        user = getUser(uid)
        try:
            helperList = json.loads(box.helperList)
        except:
            helperList = []
        if box.has:
            if len(helperList) < datas['PARAMS']['maxBoxFriNum']:
                cost = {'gold':datas['PARAMS']['selfOpenGold']}
                ret = checkCost(uid, cost)
                if ret:
                    doCost(uid, cost)
                    helperList.append(-1)
                    box.helperList = json.dumps(helperList)
                    return dict(id=1)
        return dict(id=0)
    #分阶段1 ----》 2 ----》 3
    #KIND ID NUM
    def genBoxReward(self, uid):
        user = getUser(uid)

        rewards = []#kind ID ----> silver crystal number 对应的是 数量 而不是 ID
        allKinds = ["drug", 'magicStone', "goodsList", "crystal", "gold", "silver"]
        possible = [datas['BoxReward'][a]['possible'] for a in allKinds]
        #ids = [datas['BoxReward'][a]['id'] for a in allKinds]
        totalPossible = sum(possible)
        eachPossible = [sum(possible[:i]) for i in xrange(1, len(possible)+1)]
        allDrugs = [i+j for i in xrange(0, 40, 10) for j in [0, 1, 3, 4]]
        gain = {}

        for i in xrange(0, 3):
            p = randint(0, totalPossible-1)
            kind = len(allKinds)-1
            #kind = allKinds[-1]
            for e in xrange(0, len(eachPossible)):
                if p <= eachPossible[e]:
                    #kind = allKinds[e]
                    kind = e
                    break
            realKind = allKinds[kind]

            allKinds.pop(kind)
            eachPossible.pop(kind)
            possible.pop(kind)
            totalPossible = sum(possible)
            #allKinds.remove(kind)

            kind = realKind
            param = 0
            num = 1
            if kind == 'magicStone':
                param = randint(0, 3)
            elif kind == 'drug':
                param = allDrugs[randint(0, len(allDrugs)-1)]
            elif kind == 'goodsList':
                param = randint(0, 3)
            elif kind == 'crystal':
                num = max(int(math.sqrt(user.level)), 5)
            elif kind == 'gold':
                num = max(int(math.sqrt(user.level)), 1)
            elif kind == 'silver':
                num = getTotalIncome(user.level)/10
            else:
                param = 0
                num = 0
            rewards.append([getKindId(kind), param, num])
            updateGoodsNum(uid, getKindId(kind), param, num)
        return rewards
            
    @expose('json')
    def openBox(self, uid):
        uid = int(uid)
        box = DBSession.query(UserTreasureBox).filter_by(uid=uid).one()
        try:
            helperList = json.loads(box.helperList)
        except:
            helperList = []
        if box.has:
            if len(helperList) >= datas['PARAMS']['maxBoxFriNum']:
                rewards = self.genBoxReward(uid)
                box.has = 0
                box.helperList = '[]'
                return dict(id=1, rewards=rewards)
        return dict(id=0)


    #fid -1 表示这个好友没有在游戏中
    @expose('json')
    def getMyFriend(self, uid):
        uid = int(uid)
        friend = DBSession.query(UserFriend).filter_by(uid=uid).all()
        res = []
        for i in friend:
            res.append([i.papayaId, i.fid, i.lev, i.name])
        return dict(id=1, res=res) 
    @expose('json')
    def addFriend(self, uid, flist):
        uid = int(uid)
        flist = json.loads(flist)#[papayaId,]
        res = []
        for f in flist:
            try:
                friend = DBSession.query(UserInWan).filter_by(papayaId=f).one()
                name = friend.name
                level = friend.level
                fid = friend.uid
            except:
                name = ''
                fid = -1
                level = 0
            friend = UserFriend(uid = uid, papayaId=f, fid=fid, name=name)
            res.append([fid, name, level])
            try:
                exist = DBSession.query(UserFriend).filter_by(uid = uid, papayaId=f).one()
            except:
                DBSession.add(friend)
        return dict(id=1, friends=res)
    
    global FETCH_FRI_NUM
    FETCH_FRI_NUM = 100
    #获取所有的待推荐用户 随机选择100个
    @expose('json')
    def getRecommand(self, uid):
        uid = int(uid)
        allUsers = recommandCollect.find_one()['res']
        userLen = len(allUsers)
        #allUsers = len(AllRecommandUsers)
        begin = randint(0, userLen-1)
        res = range(begin, min(begin+FETCH_FRI_NUM, userLen))
        res += range(0, min(begin, FETCH_FRI_NUM-len(res)))
        retUser = []
        for i in res:
            retUser.append([allUsers[i]['uid'], allUsers[i]['level'], allUsers[i]['name'], allUsers[i]['papayaId']])
        return dict(id=1, retUser=retUser)
            
    
    @expose('json')
    def getNeibors(self, uid):
        uid = int(uid)
        neibors = DBSession.query(UserNeiborRelation).filter_by(uid=uid).all()
        res = []
        for i in neibors:
            mine = DBSession.query(UserCrystalMine).filter_by(uid=i.fid).one()
            try:
                loveTree = DBSession.query(UserBuildings).filter_by(uid=i.fid, kind=datas['PARAMS']['loveTreeId']).one()
                loveLevel = loveTree.level
            except:
                loveTree = None
                loveLevel = 0
            res.append([i.fid, i.papayaId, i.name, i.level, mine.level, i.challengeYet, i.heartYet, loveLevel])
        return dict(id=1, neibors = res)

    #如果已经发送过请求 则 阻止今天继续发送 
    #可能发送的用户不存在
    #可能发送用户的邻居数已经足够则不发送
    #己方已经没有邻居空位则阻止发送
    @expose('json')
    def sendNeiborRequest(self, uid, fid):
        uid = int(uid)
        fid = int(fid)
        friend = getUser(fid)
        neiborNum = DBSession.query(UserNeiborRelation).filter_by(uid=fid).count()
        if neiborNum >= friend.neiborMax:
            return dict(id=0, status=1)
        try:
            rel = DBSession.query(UserNeiborRelation).filter_by(uid=uid, fid=fid).one()
            return dict(id=0, status=2)
        except:
            pass

        try:
            req = DBSession.query(UserNeiborRequest).filter_by(uid=uid, fid=fid).one()
            print "req yet", uid, fid
            return dict(id=0, status=0)
        except:
            req = UserNeiborRequest(uid=uid, fid=fid, time=getTime())
            DBSession.add(req)
        return dict(id=1)
    @expose('json')
    def sendNeiborInviteRequest(self, uid, inviteCode):
        uid = int(uid)
        try:
            inviteCode = int(inviteCode)
        except:
            return dict(id=0, status=0)
        #invite = DBSession.query(UserInWan).filter_by(inviteCode=inviteCode).all()
        invite = DBSession.query(UserInviteRank).filter_by(inviteCode=inviteCode).all()
        if len(invite) == 0:
            return dict(id=0, status=1)

        for i in invite:
            neiborNum = DBSession.query(UserNeiborRelation).filter_by(uid=i.uid).count()
            invFri = getUser(i.uid)
            if neiborNum >= invFri.neiborMax:
                return dict(id=0, status=3)

            try:
                rel = DBSession.query(UserNeiborRelation).filter_by(uid=uid, fid=i.uid).one()
                return dict(id=0, status=2)
            except:
                pass

            try:
                req = DBSession.query(UserNeiborRequest).filter_by(uid=uid, fid=i.uid).one()
                return dict(id=0, status=2)
            except:
                req = UserNeiborRequest(uid=uid, fid=i.uid, time=getTime())
                DBSession.add(req)
        return dict(id=1)


    #发送消息的个体已经被删除
    #发送邻居请求消息
    @expose('json')
    def getMessage(self, uid):
        uid = int(uid)
        res = DBSession.query(UserNeiborRequest).filter_by(fid=uid).all()
        req = []
        for i in res:
            sender = DBSession.query(UserInWan).filter_by(uid=i.uid).one()
            req.append([sender.uid, sender.papayaId, sender.name, sender.level, i.time])
        return dict(id=1, req=req)
    @expose('json')
    def addNeiborMax(self, uid, gold):
        uid = int(uid)
        gold = int(gold)
        cost = {'gold':gold}
        ret = checkCost(uid, cost)
        if not ret:
            return dict(id=0)
        doCost(uid, cost)
        user = getUser(uid)
        user.neiborMax += 1
        return dict(id=1)
    #0 VISIT_PAPAYA
    #1 VISIT_NEIBOR
    #2 VISIT_RECOMMAND
    global VISIT_PAPAYA
    global VISIT_NEIBOR
    global VISIT_RECOMMAND
    VISIT_PAPAYA = 0
    VISIT_NEIBOR = 1
    VISIT_RECOMMAND = 2
    global MAX_PAPAYA
    global MAX_NEIBOR
    global MAX_RECOMMAND
    MAX_PAPAYA = 10
    MAX_NEIBOR = 3
    MAX_RECOMMAND = 15
    @expose('json')
    def helpFriendCry(self, uid, kind, crystal):
        uid = int(uid)
        kind = int(kind)
        crystal = int(crystal)

        user = getUser(uid)

        if kind == VISIT_PAPAYA:
            if user.addPapayaCryNum >= MAX_PAPAYA:
                return dict(id=0)
            user.addPapayaCryNum += 1
        elif kind == VISIT_NEIBOR:
            if user.addNeiborCryNum >= MAX_NEIBOR*user.neiborMax:
                return dict(id=0)
            user.addNeiborCryNum += 1
        elif kind == VISIT_RECOMMAND:
            if user.addFriendCryNum >= MAX_RECOMMAND:
                return dict(id=0)
            user.addFriendCryNum += 1
        user.crystal += crystal
        return dict(id=1)

    #对方接受 添加邻居
    @expose('json')
    def acceptNeibor(self, uid, fid):
        uid = int(uid)
        fid = int(fid)

        try:
            req = DBSession.query(UserNeiborRequest).filter_by(uid=fid, fid=uid).one()
            DBSession.delete(req)
        except:
            return dict(id=0, status=4)
            #print "no request", uid, fid
        try:
            user = getUser(uid)
            friend = getUser(fid)
        except:
            return dict(id=0, reason='no such user', status = 0)
        myNeiNum = DBSession.query(UserNeiborRelation).filter_by(uid=uid).count()
        if myNeiNum >= user.neiborMax:
            return dict(id=0, status = 1)
        friNeiNum = DBSession.query(UserNeiborRelation).filter_by(uid=fid).count()
        if friNeiNum >= friend.neiborMax:
            return dict(id=0, status = 2)

        #等级将在访问邻居之后自动更新

        try:
            neiYet = DBSession.query(UserNeiborRelation).filter_by(uid=uid, fid=fid).one()
            print "neibor yet"
            return dict(id=0, status=3)
        except:
            pass

        neibor = UserNeiborRelation(uid=fid, fid=uid,  name=user.name,  level=user.level)
        neibor.papayaId = user.papayaId
        DBSession.add(neibor)

        neibor = UserNeiborRelation(uid=uid, fid=fid,  name=friend.name, level=friend.level)
        neibor.papayaId = friend.papayaId
        DBSession.add(neibor)


            

        return dict(id=1)
    @expose('json')
    def refuseNeibor(self, uid, fid):
        uid = int(uid)
        fid = int(fid)
        try:
            req = DBSession.query(UserNeiborRequest).filter_by(uid=fid, fid=uid).one()
            DBSession.delete(req)
        except:
            print "no request", uid, fid
        return dict(id=1)

    #解除双方的邻居关系 下次登录更新
    @expose('json')
    def removeNeibor(self, uid, fid):
        uid = int(uid)
        fid = int(fid)
        rel = DBSession.query(UserNeiborRelation).filter_by(uid=uid, fid=fid).one()
        DBSession.delete(rel)
        rel = DBSession.query(UserNeiborRelation).filter_by(uid=fid, fid=uid).one()
        DBSession.delete(rel)
        return dict(id=1)

    #每天第一次用户登录 自动发送清理 挑战记录的请求 getLoginReward 
    @expose('json')
    def challengeNeibor(self, uid, fid):
        uid = int(uid)
        fid = int(fid)
        try:
            rel = DBSession.query(UserNeiborRelation).filter_by(uid=uid, fid=fid).one()
            rel.challengeYet = 1
        except:
            print "neibor relaition broken", uid, fid

        #soldiers = getChallengeSoldiers(fid)
        #equips = getChallengeEquips(fid)
        #other = getUser(fid)
        #skills = DBSession.query(UserSkills).filter_by(uid=fid).all()
        #skills = [[i.soldierId, i.skillId, i.level] for i in skills]
        oData = getOtherData(fid)
        oData.update({'id':1})
        return oData
        #return dict(id=1, soldiers=soldiers, equips=equips, cityDefense=other.cityDefense, skills = skills)
        
    #只有胜利才需要同步数据
    @expose('json')
    def challengeNeiborOver(self, uid, fid, sols, crystal, mid):
        uid = int(uid)
        fid = int(fid)
        sols = json.loads(sols)
        crystal = int(crystal)
        mid = int(mid)

        user = getUser(uid)
        user.crystal += crystal
        for i in sols:
            soldier = DBSession.query(UserSoldiers).filter_by(uid=uid).filter_by(sid=i[0]).one()
            soldier.health = i[1]
            soldier.exp = i[2]
            soldier.dead = i[3]
            soldier.level = i[4]
        msg = UserMessage(uid=uid, fid=fid, kind=datas['PARAMS']['MSG_CHALLENGE'], param=crystal, time=getTime(), mid=mid)
        DBSession.add(msg)

        return dict(id=1)

    #读取之后删除消息
    #消息的接受方是我
    #每种类型消息只能发送一次 uid fid kind 决定
    @expose('json')
    def getUserMessage(self, uid):
        uid = int(uid)
        messages = DBSession.query(UserMessage).filter_by(fid=uid).all()
        ret = []
        for i in messages:
            sender = getUser(i.uid)
            ret.append([i.uid, i.kind, i.param, i.time, sender.name, i.mid])
        return dict(id=1, msg=ret)
    #发送方 fid time
    @expose('json')
    def readMessage(self, uid, fid, mid):
        uid = int(uid)
        fid = int(fid)
        mid = int(mid)
        msg = DBSession.query(UserMessage).filter_by(uid=fid, fid=uid, mid=mid).one()
        DBSession.delete(msg)
        return dict(id=1)

        
            
    #自己的爱心数量由自己修改 
    #其他用户不能修改

    #总的爱心累计数量   其他用户赠送
    #每周的爱心累计数量 服务器每周清空
    #未收获的爱行数量 其他用户赠送 自己清空
    #自己爱心经验 其他用户赠送 自己清空

    #可能自己在清空的时候其他用户还在赠送需要注意
    @expose('json')
    def sendHeart(self, uid, fid, mid):
        uid = int(uid)
        fid = int(fid)
        mid = int(mid)

        nei = DBSession.query(UserNeiborRelation).filter_by(uid=uid, fid=fid).one()
        if nei.heartYet == 1:
            return dict(id=0)
        nei.heartYet = 1

        #sendHeart = DBSession.query(UserHeart).filter_by(uid=uid).one()
        #if sendHeart.heartYet == 1:
        #    return dict(id=1)

        heart = DBSession.query(UserHeart).filter_by(uid=fid).one()
        heart.accNum += 1
        heart.weekNum += 1
        heart.liveNum += 1
        #爱心树 升级经验累计爱心
        #heart.heartExp += 1
        #msg = UserMessage(uid=uid, fid=fid, kind=datas['PARAMS']['MSG_CHALLENGE'], param=crystal, time=getTime())
        msg = UserMessage(uid=uid, fid=fid, kind=datas['PARAMS']['MSG_HEART'], param=0, time=getTime(), mid=mid)
        DBSession.add(msg)
        return dict(id=1)

    
    #每周第一次登录 收集没有收获的爱心数量
    @expose('json')
    def collectHeart(self, uid):
        uid = int(uid)
        heart = DBSession.query(UserHeart).filter_by(uid=uid).one()
        user = getUser(uid)
        user.crystal += heart.liveNum
        heart.liveNum = 0
        return dict(id=1)

    #登录时发现 可以根据当前的等级需要的 升级已有的爱心爱心数量
    #来提升爱心树等级 则 客户端发送等级提升消息 
    #修改爱心树ID

    #不再检测爱心经验只 检测 爱心总量
    @expose('json')
    def upgradeLoveTree(self, uid, bid, level):
        uid = int(uid)
        bid = int(bid)
        level = int(level)
        #lostHeart = int(lostHeart)

        building = DBSession.query(UserBuildings).filter_by(uid=uid, bid=bid).one()
        building.level = level

        #heart = DBSession.query(UserHeart).filter_by(uid=uid).one()
        #heart.heartExp -= lostHeart
        return dict(id=1)
    
    #从mongodb 的中的排行数据中获取数据 按照每周爱心数量
    #清空每周爱心数量
    @expose('json')
    def getHeartRank(self, uid, offset, limit):
        uid = int(uid)
        offset = int(offset)
        limit = int(limit)
        try:
            result = mongoCollect.find_one()['res']  
            ret = result[offset:offset+limit]
            ret = [[i['uid'], i['papayaId'], i['score'], i['rank'], i['name'], i['level']] for i in ret]
        except:
            ret = []
        return dict(id=1, res=ret)
    @expose('json')
    def getInviteRank(self, uid, offset, limit):
        uid = int(uid)
        offset = int(offset)
        limit = int(limit)
        try:
            result = inviteRankCollect.find_one()['res']  
            ret = result[offset:offset+limit]
            ret = [[i['uid'], i['papayaId'], i['score'], i['rank'], i['name'], i['level']] for i in ret]
        except:
            ret = []
        return dict(id=1, res=ret)

    @expose('json')
    def inviteFriend(self, uid, oid):
        uid = int(uid)
        oid = int(oid)
        record = inviteCollect.find_one({'uid':uid, 'oid':oid})
        if record != None:
            return dict(id=0)
        record = {'uid':uid, 'oid':oid}
        inviteCollect.insert(record)
        gain = {'silver': datas['PARAMS']['inviteSilver']}
        doGain(uid, gain)
        return dict(id=1)

    @expose('json')
    def getFriendUpdate(self, uid):#好友更新了数据名字 等级 uid等数据 客户端获取数据后更新
        uid = int(uid)
        allUpdate = DBSession.query(UserFriend).filter_by(uid=uid, updated=True).all()
        ret = []
        for i in allUpdate:
            ret.append([i.papayaId, i.fid, i.lev, i.name])
            i.updated = False
        return dict(id=1, updated=ret)

    #好友模块自动检测第一次登录清理其邻居数据
    @expose('json')
    def clearNeiborData(self, uid):
        uid = int(uid)
        neibors = DBSession.query(UserNeiborRelation).filter_by(uid=uid).all()
        for i in neibors:
            i.challengeYet = 0
            i.heartYet = 0#赠送爱心数据清空
        return dict(id=1)
