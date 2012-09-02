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

__all__ = ['FriendController']


class FriendController(BaseController):
    @expose('json')
    def getFriend(self, uid, papayaId):
        uid = int(uid)
        papayaId = int(papayaId)
        try:
            friend = DBSession.query(UserInWan).filter_by(papayaId=papayaId).one()
            soldiers = getSoldiers(friend.uid)
            return dict(id=1, level=friend.level, soldiers=soldiers, fid = friend.uid, name=friend.name)
        except:
            pass
        #该用户没有在服务器注册，fid 返回-1 更新
        return dict(id=1, level=0, soldiers={}, fid = -1)
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
        allUsers = len(AllRecommandUsers)
        begin = randint(0, allUsers-1)
        res = range(begin, min(begin+FETCH_FRI_NUM, allUsers))
        res += range(0, min(begin, FETCH_FRI_NUM-len(res)))
        retUser = []
        for i in res:
            retUser.append([AllRecommandUsers[i].uid, AllRecommandUsers[i].level, AllRecommandUsers[i].name, AllRecommandUsers[i].papayaId])
        return dict(id=1, retUser=retUser)
            
    
    @expose('json')
    def getNeibors(self, uid):
        uid = int(uid)
        neibors = DBSession.query(UserNeiborRelation).filter_by(uid=uid).all()
        res = []
        for i in neibors:
            mine = DBSession.query(UserCrystalMine).filter_by(uid=i.fid).one()
            res.append([i.fid, i.papayaId, i.name, i.level, mine.level, i.challengeYet, i.heartYet])
        return dict(id=1, neibors = res)

    #如果已经发送过请求 则 阻止今天继续发送 
    #可能发送的用户不存在
    #可能发送用户的邻居数已经足够则不发送
    @expose('json')
    def sendNeiborRequest(self, uid, fid):
        uid = int(uid)
        fid = int(fid)
        friend = getUser(fid)
        neiborNum = DBSession.query(UserNeiborRelation).filter_by(uid=fid).count()
        if neiborNum >= friend.neiborMax:
            return dict(id=0, status=1)
        try:
            req = DBSession.query(UserNeiborRequest).filter_by(uid=uid, fid=fid).one()
            print "req yet", uid, fid
            return dict(id=0, status=0)
        except:
            req = UserNeiborRequest(uid=uid, fid=fid, time=getTime())
            DBSession.add(req)
        return dict(id=1)

    @expose('json')
    def getMessage(self, uid):
        uid = int(uid)
        res = DBSession.query(UserNeiborRequest).filter_by(fid=uid).all()
        req = []
        for i in res:
            sender = DBSession.query(UserInWan).filter_by(uid=i.uid).one()
            req.append([sender.uid, sender.papayaId, sender.name, sender.level])
        return dict(id=1, req=req)
    @expose('json')
    def addNeiborMax(self, uid):
        uid = int(uid)
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


            
        try:
            req = DBSession.query(UserNeiborRequest).filter_by(uid=fid, fid=uid).one()
            DBSession.delete(req)
        except:
            print "no request", uid, fid
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

    @expose('json')
    def challengeNeibor(self, uid, fid):
        uid = int(uid)
        fid = int(fid)
        try:
            rel = DBSession.query(UserNeiborRelation).filter_by(uid=uid, fid=fid).one()
            rel.challengeYet = 1
        except:
            print "neibor relaition broken", uid, fid
        soldiers = getChallengeSoldiers(fid)
        equips = getChallengeEquips(fid)
        other = getUser(fid)
        return dict(id=1, soldiers=soldiers, equips=equips, cityDefense=other.cityDefense)
        
    @expose('json')
    def challengeNeiborOver(self, uid, fid, sols, crystal):
        uid = int(uid)
        fid = int(fid)
        sols = json.loads(sols)
        crystal = int(crystal)

        user = getUser(uid)
        user.crystal += crystal
        for i in sols:
            soldier = DBSession.query(UserSoldiers).filter_by(uid=uid).filter_by(sid=i[0]).one()
            soldier.health = i[1]
            soldier.exp = i[2]
            soldier.dead = i[3]
            soldier.level = i[4]
        msg = UserMessage(uid=uid, fid=fid, kind=MSG_CHALLENGE, param=crystal, time=getTime())
        DBSession.add(msg)

        return dict(id=1)
    @expose('json')
    def sendHeart(self, uid, fid):
        uid = int(uid)
        fid = int(fid)
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
        return dict(id=1)

    
    @expose('json')
    def collectHeart(self, uid):
        uid = int(uid)
        heart = DBSession.query(UserHeart).filter_by(uid=uid).one()
        user = getUser(uid)
        user.crystal += heart.liveNum
        heart.liveNum = 0
        return dict(id=1)

    #登录时发现 可以提升等级 则 客户端发送等级提升消息 
    #修改爱心树ID
    @expose('json')
    def upgradeLoveTree(self, uid, bid, kind):
        uid = int(uid)
        bid = int(bid)
        kind = int(kind)
        building = DBSession.query(UserBuildings).filter_by(uid=uid, bid=bid).one()
        building.kind = kind
        return dict(id=1)
    
    #从mongodb 的中的排行数据中获取数据 按照每周爱心数量
    #清空每周爱心数量
    @expose('json')
    def getHeartRank(self, uid, offset, limit):
        uid = int(uid)
        offset = int(offset)
        limit = int(limit)
        result = mongoCollect.find_one()['res']  
        ret = result[offset:offset+limit]
        ret = [[i['uid'], i['papayaId'], i['score'], i['rank'], i['name']] for i in ret]

        return dict(id=1, res=ret)
