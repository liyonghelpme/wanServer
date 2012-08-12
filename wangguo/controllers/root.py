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
    """
    @expose('wangguo.templates.login')
    def login(self, came_from=lurl('/')):

        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')
        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from)
    """
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


    def initChallenge(self, user):
        uid = user.uid
        for i in range(0, 5):
            for j in range(0, 6):
                challenge = UserChallenge(uid=uid, big=i, small=j, star=0)
                DBSession.add(challenge)
    def initSoldiers(self, user):
        uid = user.uid
        sid = 0
        data = calculateStage(0, 0)[4]
        soldier = UserSoldiers(uid=uid, sid=0, kind=0, name='剑', health = data)
        DBSession.add(soldier)
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


    #闯关保存在本地就可以了
    #用户数据保存在服务器上
    #需要用户之间进行沟通的数据才保存在服务器上
    def getStars(self, uid):
        challenge = DBSession.query(UserChallenge).filter_by(uid=uid).all()
        res = [ [[0] for i in range(0, 6)] for j in range(0, 5)]

        for i in challenge:
            res[i.big][i.small][0] = i.star
        #print res
        return res
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


        #第一次登录清空邻居挑战信息
        neibors = DBSession.query(UserNeiborRelation).filter_by(uid=uid).all()
        for i in neibors:
            i.challengeYet = 0

        return dict(id=1, silver=silver, crystal=crystal, loginDays = user.loginDays)


    @expose('json')
    def levelUp(self, uid, level, rew):
        uid = int(uid)
        level = int(level)
        rew = json.loads(rew)
        doGain(uid, rew);
        return dict(id=1)

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
            #self.initSolEquip(user)

        #loginReward = self.getLoginReward(user)
        #在getUserData 获取积分之前 减去积分
        self.minusChallengeScore(user.uid)

        userData = self.getUserData(user)
        stars = self.getStars(user.uid)
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


        return dict(id=1, uid = user.uid, resource = userData, starNum = stars, buildings = buildings, soldiers = soldiers, drugs=drugs, equips=equips,  herbs=herbs, tasks=tasks, serverTime=getTime(), challengeRecord=challengeRecord, rank=rank, mine=mine) 
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


