# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, request, redirect
from tg.i18n import ugettext as _, lazy_ugettext as l_
from wangguo import model
from repoze.what import predicates
from wangguo.controllers.secure import SecureController

from tgext.admin.tgadminconfig import TGAdminConfig
from tgext.admin.controller import AdminController

from wangguo.lib.base import BaseController
from wangguo.controllers.error import ErrorController
from wangguo.controllers.task import TaskController
from wangguo.controllers.challenge import ChallengeController
from wangguo.controllers.goods import GoodsController
from wangguo.controllers.building import BuildingController
from wangguo.controllers.soldier import SoldierController
from wangguo.controllers.friend import FriendController
from wangguo.controllers.mine import MineController

#from wangguo.model import DBSession, metadata
from wangguo.model import *
from wangguo.controllers.util import *

__all__ = ['RootController']


class RootController(BaseController):
    secc = SecureController()
    admin = AdminController(model, DBSession, config_type=TGAdminConfig)
    taskC = TaskController()
    challengeC = ChallengeController()
    goodsC = GoodsController()
    buildingC = BuildingController()
    soldierC = SoldierController()
    friendC = FriendController()
    mineC = MineController()

    error = ErrorController()

    @expose('wangguo.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')

    @expose('wangguo.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    @expose('wangguo.templates.environ')
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(environment=request.environ)

    @expose('wangguo.templates.data')
    @expose('json')
    def data(self, **kw):
        """This method showcases how you can use the same controller for a data page and a display page"""
        return dict(params=kw)
    @expose('wangguo.templates.authentication')
    def auth(self):
        """Display some information about auth* on this application."""
        return dict(page='auth')

    @expose('wangguo.templates.index')
    @require(predicates.has_permission('manage', msg=l_('Only for managers')))
    def manage_permission_only(self, **kw):
        """Illustrate how a page for managers only works."""
        return dict(page='managers stuff')

    @expose('wangguo.templates.index')
    @require(predicates.is_user('editor', msg=l_('Only for the editor')))
    def editor_user_only(self, **kw):
        """Illustrate how a page exclusive for the editor works."""
        return dict(page='editor stuff')

    """Start the user login."""
    def initUserData(self, user):
        user.silver = 1000
        user.gold = 1000
        user.crystal = 1000
        user.level = 0
        user.people = 5
        user.cityDefense = 831
        user.loginDays = 0
        user.exp = 0
        user.neiborMax = 10
        user.colorCrystal = 5
    #state = 1 Free
    def initBuildings(self, user):
        uid = user.uid
        bid = 0
        buildings = UserBuildings(uid=uid, bid=0, kind=200, px=1504, py=640, state = 1)
        DBSession.add(buildings)
        buildings = UserBuildings(uid=uid, bid=1, kind=202, px=1664, py=656, state = 1)
        DBSession.add(buildings)
        buildings = UserBuildings(uid=uid, bid=2, kind=204, px=1280, py=720, state = 1)
        DBSession.add(buildings)
        buildings = UserBuildings(uid=uid, bid=3, kind=206, px=1728, py=848, state = 1)
        DBSession.add(buildings)
        buildings = UserBuildings(uid=uid, bid=4, kind=0, px=2496, py=624, state= 1)
        DBSession.add(buildings)
        buildings = UserBuildings(uid=uid, bid=5, kind=0, px=2560, py=656, state= 1)
        DBSession.add(buildings)
        buildings = UserBuildings(uid=uid, bid=6, kind=0, px=2432, py=656, state= 1)
        DBSession.add(buildings)
        buildings = UserBuildings(uid=uid, bid=7, kind=0, px=2496, py=688, state= 1)
        DBSession.add(buildings)
        buildings = UserBuildings(uid=uid, bid=8, kind=208, px=1824, py=640, state=1)#MOVE FREE WORK 
        DBSession.add(buildings)

    global ROUND_BIG 
    ROUND_BIG = 5
    global ROUND_SMALL
    ROUND_SMALL = 7
    def initChallenge(self, user):
        uid = user.uid
        for i in range(0, ROUND_BIG):
            for j in range(0, ROUND_SMALL):
                challenge = UserChallenge(uid=uid, big=i, small=j, star=0)
                DBSession.add(challenge)
    def initSoldiers(self, user):
        uid = user.uid
        #sid = 0
        #data = calculateStage(0, 0)[4]
        #soldier = UserSoldiers(uid=uid, sid=0, kind=0, name='剑', health = data)
        #DBSession.add(soldier)
        #编号12 的变身技能 暂时没有英雄变身技能
        #skill = UserSkills(uid=uid, soldierId=sid, skillId=12, level=0)
        #DBSession.add(skill)

    def initDrug(self, user):
        uid = user.uid
        drug = UserDrugs(uid=uid, drugKind=0, num=1)
        DBSession.add(drug)
        drug = UserDrugs(uid=uid, drugKind=1, num=1)
        DBSession.add(drug)
        drug = UserDrugs(uid=uid, drugKind=2, num=1)
        DBSession.add(drug)
        drug = UserDrugs(uid=uid, drugKind=3, num=1)
        DBSession.add(drug)
        drug = UserDrugs(uid=uid, drugKind=4, num=1)
        DBSession.add(drug)

    def initEquip(self, user):
        uid = user.uid
        equip = UserEquips(uid=uid, eid = 0, equipKind=0)
        DBSession.add(equip)

    #保证rank唯一性
    def initRank(self, user):
        num = DBSession.query(UserNewRank).filter("score >= 100").count()
        rank = UserNewRank(uid=user.uid, score=100, rank=num, papayaId = user.papayaId, name=user.name, finish=0)
        DBSession.add(rank)
        """
        num = DBSession.query(UserGroupRank).filter("score >= 100").count()
        rank = UserGroupRank(uid=user.uid, score=100, rank=num, papayaId = user.papayaId, papayaName=user.papayaName)
        DBSession.add(rank)
        """
    def initChallengeFriend(self, user):
        now = getTime()
        challenge = UserChallengeFriend(uid=user.uid, challengeNum=0, challengeTime=now, lastMinusTime = now)
        DBSession.add(challenge)
    def initBuyTask(self, user):
        task = UserBuyTask(uid=user.uid)
        DBSession.add(task)
    #state == 0 Moving
    #1 Free
    #2 Working
    def initCrystalMine(self, user):
        mine = UserCrystalMine(uid=user.uid, px=768, py =352, state = 1, objectTime=getTime(), level=0)
        DBSession.add(mine)

    def initHeart(self, user):
        heart = UserHeart(uid=user.uid, weekNum=0, liveNum = 0, accNum = 0)
        DBSession.add(heart)

    def getHeart(self, uid):
        heart = DBSession.query(UserHeart).filter_by(uid=uid).one()
        return dict(weekNum=heart.weekNum, accNum=heart.accNum, liveNum=heart.liveNum, rank=heart.rank)


    #闯关保存在本地就可以了
    #用户数据保存在服务器上
    #需要用户之间进行沟通的数据才保存在服务器上
    #返回所有的闯关得分数据
    @expose('json')
    def getStars(self, uid):
        challenge = DBSession.query(UserChallenge).filter_by(uid=uid).all()
        res = [ [0 for i in range(0, ROUND_SMALL)] for j in range(0, ROUND_BIG)]

        for i in challenge:#不需要难度
            res[i.big][i.small] = i.star
        #print res
        return dict(id=1, res=res)

    #测试loginTime = 0
    #week = 0
    #
    def getUserData(self, user):
        challenge = DBSession.query(UserChallengeFriend).filter_by(uid=user.uid).one()
        return dict(uid=user.uid, silver=user.silver, gold=user.gold, crystal=user.crystal, level=user.level, people=user.people, cityDefense=user.cityDefense, loginDays=user.loginDays, exp=user.exp, challengeNum=challenge.challengeNum, challengeTime=challenge.challengeTime, loginTime=user.loginTime, neiborMax=user.neiborMax, addFriendCryNum=user.addFriendCryNum, addNeiborCryNum=user.addNeiborCryNum, addPapayaCryNum=user.addPapayaCryNum, colorCrystal=user.colorCrystal) 
    def getBuildings(self, uid):
        buildings = DBSession.query(UserBuildings).filter_by(uid=uid).all()
        res = {}
        for i in buildings:
            res[i.bid] = dict(id=i.kind, px=i.px, py=i.py, state=i.state, dir=i.dir, objectId=i.objectId, objectTime=i.objectTime)
        return res
    def getDrugs(self, uid):
        drugs = DBSession.query(UserDrugs).filter_by(uid=uid).all()
        res = dict()
        for i in drugs:
            res[i.drugKind] = i.num
        return res
    #eid ---> kind level
    def getHerb(self, uid):
        herbs = DBSession.query(UserHerb).filter_by(uid=uid).all()
        res = dict()
        for i in herbs:
            res[i.kind] = i.num
        return res
    def getTask(self, uid):
        tasks = DBSession.query(UserTask).filter_by(uid=uid).all()
        res = dict()
        for i in tasks:
            res[i.tid] = [i.number, i.finish, i.stage]#当前累计任务的阶段
        return res

    def getSkills(self, uid):
        skills = DBSession.query(UserSkills).filter_by(uid=uid).all()
        res = [[k.soldierId, k.skillId, k.level] for k in skills]
        print res
        return res

    #如果用户清空了数据 没有当前最大的礼物ID 则从数据中获取最大的一个
    def getMaxGiftId(self, uid):
        maxId = DBSession.query(UserGift).filter_by(uid=uid).order_by(UserGift.time.desc()).limit(1).all()
        if len(maxId) == 0:
            return 0
        return maxId[0].time+1


    #用户挑战其它用户的记录
    #每天第一次登录清除挑战记录
    #每天第一次登录清除访问记录
    def getChallengeRecord(self, uid):
        res = DBSession.query(UserChallengeRecord).filter_by(uid=uid).all()
        res = [i.oid for i in res]
        return res
    def getRankData(self, uid):
        rank = getRank(uid)
        return [rank.score, rank.rank]

    #buildid 300 crystalMine
    def getCrystalMine(self, uid):
        mine = DBSession.query(UserCrystalMine).filter_by(uid=uid).one()
        return dict(px=mine.px, py=mine.py, state=mine.state, objectTime=mine.objectTime, level=mine.level)
    global GOODS_COFF
    GOODS_COFF = 10000
    def getTreasureStone(self, uid):
        treasure = DBSession.query(UserGoods).filter_by(uid=uid).all()
        res = []
        for t in treasure:
            res.append([t.kind*GOODS_COFF+t.id, t.num])
        return res
            
        
        
    #3天没有挑战 第一天减去5%积分 之后每天减去1%积分
    def minusChallengeScore(self, uid):
        challenge = DBSession.query(UserChallengeFriend).filter_by(uid=uid).one()
        now = getTime()
        today = now/(24*3600)
        lastChaDay = challenge.challengeTime/(24*3600)
        chaDiff = today-lastChaDay

        lastMinusTime = challenge.lastMinusTime
        diff = today-lastMinusTime/(24*3600)

        #三天没有挑战 且 今天没有减去
        if chaDiff >= 3 and diff >= 1:
            rank = getRank(uid)
            rank.score -= rank.score/100*diff
            rank.score = max(0, rank.score)
            challenge.lastMinusTime = now


    #肯能需要客户端主动请求登录奖励保证登录奖励被客户端看到
    #每天第一次登录
    #只在获取登录奖励的时候 更新登录时间 即每天第一次登录时 更新登录时间
    @expose('json')
    def getLoginReward(self, uid, silver, crystal):
        uid = int(uid)
        silver = int(silver)
        crystal = int(crystal)
        user = getUser(uid)

        lastTime = user.loginTime
        lastDay = int(lastTime/(3600*24))
        curTime = getTime()
        today = int(curTime/(3600*24))
        diff = today-lastDay
        user.loginTime = curTime
        if diff == 1:#连续登录
            user.loginDays += 1
        elif diff > 1:#超过1天第一次登录
            user.loginDays = 1
        else:#本天内再次登录
            pass
        user.silver += silver
        user.crystal += crystal
        #奖励都是0 则已经奖励


        #第一次登录清空邻居挑战信息 登录奖励应该在获取邻居信息之前处理
        neibors = DBSession.query(UserNeiborRelation).filter_by(uid=uid).all()
        for i in neibors:
            i.challengeYet = 0
            i.heartYet = 0#赠送爱心数据清空

        #每天剩余的赠送爱心数量
        #heart = DBSession.query(UserHeart).filter_by(uid=uid).one()
        #heart.heartYet = 0

        #每周更新增加1
        #week = time.localtime().tm_wday
        #if week == 0:
        user.updateState += 1

        return dict(id=1, silver=silver, crystal=crystal, loginDays = user.loginDays)

    #用户升级后提升经验等级城堡防御力其它奖励
    @expose('json')
    def levelUp(self, uid, exp, level, rew, cityDefense):
        uid = int(uid)
        exp = int(exp)
        level = int(level)
        cityDefense = int(cityDefense)

        user = getUser(uid)
        user.exp = exp
        user.level = level
        user.cityDefense += cityDefense

        #rew = json.loads(rew)
        #doGain(uid, rew);
        return dict(id=1)

    """
    @expose('json')
    def setName(self, uid, name):
        uid = int(uid)
        sameName = DBSession.query(UserInWan).filter_by(name=name).all()
        #重名且不是自身 则出错
        if len(sameName) > 0 and sameName[0].uid != uid:
            return dict(id=0, status=0, name = sameName[0].name)
        user = getUser(uid)
        user.name = name
        return dict(id=1)
    """

    #更新 缓存数据表中的 用户名称
    #邻居关系 好友关系 
    @expose('json')
    def chooseFirstHero(self, uid, hid, name):
        uid = int(uid)
        user = getUser(uid)
        hid = int(hid)#英雄ID 暂时都用类型0

        sameName = DBSession.query(UserInWan).filter_by(name=name).all()
        if len(sameName) > 0 and sameName[0].uid != uid:
            return dict(id=0, status=0, name = sameName[0].name)

        user.newState = 1
        user.name = name

        #hid  = hid level = 0 第一个士兵
        sid = 0
        hid = 0
        data = calculateStage(hid, 0)[4]
        soldier = UserSoldiers(uid=uid, sid=sid, kind=hid, name=name, health = data)
        DBSession.add(soldier)
        #编号15 凤凰变身技能暂时使用 的变身技能 暂时没有英雄变身技能
        skill = UserSkills(uid=uid, soldierId=sid, skillId=15, level=0)
        DBSession.add(skill)
        return dict(id=1)



    global Keys
    Keys = ['uid', 'silver', 'gold', 'crystal', 'level', 'people', 'cityDefense', 'loginDays', 'exp']
    @expose('json')
    def login(self, papayaId, papayaName):
        print "login", papayaId, papayaName
        papayaId = int(papayaId)
        try:
            user = DBSession.query(UserInWan).filter_by(papayaId=papayaId).one()
        except:
            user = UserInWan(papayaId=papayaId, papayaName=papayaName, name=papayaName)
            DBSession.add(user)
            DBSession.flush()#get Use Id
            user.registerTime = getTime()

            self.initUserData(user)
            self.initChallenge(user)
            self.initBuildings(user)
            self.initSoldiers(user)
            self.initDrug(user)
            self.initEquip(user)
            self.initRank(user)
            self.initChallengeFriend(user)
            self.initBuyTask(user)
            self.initCrystalMine(user)
            self.initHeart(user)
            #self.initSolEquip(user)
        
        #初次登录玩家 需要注册英雄和名称
        if user.newState == 0:
            return dict(id=1, uid=user.uid, newState=0)

        #loginReward = self.getLoginReward(user)
        #在getUserData 获取积分之前 减去积分
        self.minusChallengeScore(user.uid)

        userData = self.getUserData(user)
        #stars = self.getStars(user.uid)
        buildings = self.getBuildings(user.uid)
        soldiers = getSoldiers(user.uid)
        drugs = self.getDrugs(user.uid)
        equips = getEquips(user.uid)
        #solEquip = self.getSolEquip(user.uid)
        herbs = self.getHerb(user.uid)
        tasks = self.getTask(user.uid)
        challengeRecord = self.getChallengeRecord(user.uid)
        rank = self.getRankData(user.uid)
        mine = self.getCrystalMine(user.uid)
        #soldierEquip=solEquip,
        treasure = self.getTreasureStone(user.uid)
        maxGiftId = self.getMaxGiftId(user.uid)

        skills = self.getSkills(user.uid)

        week = time.localtime().tm_wday
        #week = 0

        updateState = user.updateState
        #user.updateState += 1
        lastLoginTime = user.loginTime
        lastWeek = getWeekNum(lastLoginTime)
        now = getTime()
        thisWeek = getWeekNum(now)

        heart = self.getHeart(user.uid)
        #starNum = stars,
        return dict(id=1, uid = user.uid, resource = userData,  buildings = buildings, soldiers = soldiers, drugs=drugs, equips=equips,  herbs=herbs, tasks=tasks, serverTime=now, challengeRecord=challengeRecord, rank=rank, mine=mine, treasure=treasure, maxGiftId=maxGiftId, skills = skills, newState = user.newState, week=week, updateState=updateState, lastWeek = lastWeek, thisWeek=thisWeek, heart=heart, registerTime=user.registerTime) 
    @expose('json')
    def reportError(self, uid, errorDetail):
        uid = int(uid)
        try:
            bug = DBSession.query(UserBug).filter_by(uid=uid).one()
            bug.errorDetail = errorDetail
            bug.time = getTime()
        except:
            bug = UserBug(uid=uid, errorDetail=errorDetail, time=getTime())
            DBSession.add(bug)
        return dict(id=1)


