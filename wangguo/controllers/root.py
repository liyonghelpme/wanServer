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
from wangguo.controllers.fight import FightController
from wangguo.controllers.log import LogController

#from wangguo.model import DBSession, metadata
from wangguo.model import *
from wangguo.controllers.util import *
import time
from random import randint
import logging

__all__ = ['RootController']


class RootController(BaseController):
    #secc = SecureController()
    #admin = AdminController(model, DBSession, config_type=TGAdminConfig)
    taskC = TaskController()
    challengeC = ChallengeController()
    goodsC = GoodsController()
    buildingC = BuildingController()
    soldierC = SoldierController()
    friendC = FriendController()
    mineC = MineController()
    fightC = FightController()
    logC = LogController()

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
        user.silver = 1000000
        user.gold = getFullGameParam("initGold")
        user.crystal = 1000000
        user.level = 0
        user.people = getFullGameParam("initPeople")
        user.cityDefense = getFullGameParam('initCityDefense')
        user.loginDays = 0
        user.exp = 0
        user.neiborMax = 5

    """初始化好友的UID"""
    def initFriends(self, user):
        friends = DBSession.query(UserFriend).filter_by(papayaId=user.papayaId).all()
        for i in friends:
            i.fid = user.uid
            i.lev = user.level
            i.name = user.name
            i.updated = True
    #state = 1 Free
    #单向好友关系
    def initNeibor(self, user):
        if getFullGameParam("debugNeibor"):
            twoUid = DBSession.execute("select min(uid) from UserInWan where uid != %d" % (user.uid)).fetchall()
            if len(twoUid) > 0:
                minUid = twoUid[0][0]
                if minUid != None:
                    uid = minUid
                    server = getUser(uid)
                    neibor = UserNeiborRelation(uid=user.uid, fid=uid,  name=server.name,  level=server.level)
                    neibor.papayaId = server.papayaId
                    DBSession.add(neibor)

                    neibor = UserNeiborRelation(uid=uid, fid=user.uid,  name=user.name,  level=user.level)
                    neibor.papayaId = user.papayaId
                    DBSession.add(neibor)


        
    def initBuildings(self, user):
        uid = user.uid
        bid = 0

        con = MySQLdb.connect(host = 'localhost', user='root', passwd='badperson3', db='Wan2', charset='utf8')
        sql = 'select * from initBuildingList'
        con.query(sql)
        rows = con.store_result().fetch_row(0, 1)
        con.close()

        for i in rows:
            buildings = UserBuildings(uid=uid, bid=i['bid'], kind=i['kind'], px=i['px'], py=i['py'], state=i['state'], color=i['color'])
            DBSession.add(buildings)
        
    def initTreasureBox(self, uid):
        box = UserTreasureBox(uid=uid, helperList='[]', has=False)
        DBSession.add(box)

    #global ROUND_BIG 
    #ROUND_BIG = 5
    #global ROUND_SMALL
    #ROUND_SMALL = 7
    def initChallenge(self, user):
        uid = user.uid
        for i in range(0, datas['PARAMS']["bigNum"]):
            for j in range(0, datas['PARAMS']['smallNum']):
                challenge = UserChallenge(uid=uid, big=i, small=j, star=0)
                DBSession.add(challenge)
    
    #编号1的普通士兵 一个
    def initSoldiers(self, user):
        uid = user.uid
        sid = 0
        for i in datas['initSoldierList']:
            k = i
            v = datas['initSoldierList'][i]
            for n in xrange(0, v['num']):
                soldier = UserSoldiers(uid=uid, sid=sid, kind=k, name=datas['soldierName'][randint(0, len(datas['soldierName'])-1)])
                DBSession.add(soldier)
                sid += 1

    def initDrug(self, user):
        uid = user.uid
        drug = UserDrugs(uid=uid, drugKind=1, num=1)
        DBSession.add(drug)
        """
        drug = UserDrugs(uid=uid, drugKind=1, num=1)
        DBSession.add(drug)
        drug = UserDrugs(uid=uid, drugKind=2, num=1)
        DBSession.add(drug)
        drug = UserDrugs(uid=uid, drugKind=3, num=1)
        DBSession.add(drug)
        drug = UserDrugs(uid=uid, drugKind=4, num=1)
        DBSession.add(drug)
        """

    def initEquip(self, user):
        uid = user.uid
        equip = UserEquips(uid=uid, eid = 0, equipKind=1)
        DBSession.add(equip)

    #保证rank唯一性
    def initRank(self, user):
        #num = DBSession.query(UserNewRank).filter("score >= 100").count()
        rank = UserNewRank(uid=user.uid, score=100, rank=0, papayaId = user.papayaId, name=user.name, finish=0)
        DBSession.add(rank)

        attackRank = UserAttack(uid=user.uid, total=0, suc=0, rank=0)
        DBSession.add(attackRank)

        defenseRank = UserDefense(uid=user.uid, total=0, suc=0, rank=0)
        DBSession.add(defenseRank)
        """
        num = DBSession.query(UserGroupRank).filter("score >= 100").count()
        rank = UserGroupRank(uid=user.uid, score=100, rank=num, papayaId = user.papayaId, papayaName=user.papayaName)
        DBSession.add(rank)
        """
    def initChallengeFriend(self, user):
        now = getTime()
        challenge = UserChallengeFriend(uid=user.uid, challengeNum=0, challengeTime=now, lastMinusTime = now)
        DBSession.add(challenge)

        challengeState = UserChallengeState(uid=user.uid, level=user.level, activeScore=getFullGameParam("initActiveScore"), protectTime=0)
        DBSession.add(challengeState)

    #state == 0 Moving
    #1 Free
    #2 Working




    #闯关保存在本地就可以了
    #用户数据保存在服务器上
    #需要用户之间进行沟通的数据才保存在服务器上
    #返回所有的闯关得分数据
    @expose('json')
    def getStars(self, uid):
        challenge = DBSession.query(UserChallenge).filter_by(uid=uid).all()
        res = [ [0 for i in range(0, datas['PARAMS']['smallNum'])] for j in range(0, datas['PARAMS']['bigNum'])]

        for i in challenge:#starNum enable
            res[i.big][i.small] = i.star

        unlockLevel = DBSession.query(UserUnlockLevel).filter_by(uid=uid).all()
        unlockLevel = [i.levelId for i in unlockLevel]
        #print res
        return dict(id=1, res=res, unlockLevel=unlockLevel)

    #测试loginTime = 0
    #week = 0
    #
    def getUserData(self, user):
        challenge = DBSession.query(UserChallengeFriend).filter_by(uid=user.uid).one()
        return dict(uid=user.uid, silver=user.silver, gold=user.gold, crystal=user.crystal, level=user.level, people=user.people, cityDefense=user.cityDefense, loginDays=user.loginDays, exp=user.exp, challengeNum=challenge.challengeNum, challengeTime=challenge.challengeTime, loginTime=user.loginTime, neiborMax=user.neiborMax, addFriendCryNum=user.addFriendCryNum, addNeiborCryNum=user.addNeiborCryNum, addPapayaCryNum=user.addPapayaCryNum, newTaskStage=user.newTaskStage, heroId=user.heroId) 
    def getBuildings(self, uid):
        buildings = DBSession.query(UserBuildings).filter_by(uid=uid).all()
        res = {}
        #res = []
        for i in buildings:
            #res.append([i.bid, i.kind, i.px, i.py, i.state])
            res[i.bid] = dict(id=i.kind, px=i.px, py=i.py, state=i.state, dir=i.dir, objectId=i.objectId, objectTime=i.objectTime, level=i.level, color=i.color, objectList = json.loads(i.objectList), readyList=json.loads(i.readyList))
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

    def getSkills(self, uid):
        skills = DBSession.query(UserSkills).filter_by(uid=uid).all()
        res = [[k.soldierId, k.skillId, k.level] for k in skills]
        print res
        return res

    #如果用户清空了数据 没有当前最大的礼物ID 则从数据中获取最大的一个 用户当前 赠送礼物的time最大值作为gid
    def getMaxGiftId(self, uid):
        maxId = DBSession.query(UserGift).filter_by(uid=uid).order_by(UserGift.gid.desc()).limit(1).all()
        if len(maxId) == 0:
            return 0
        return maxId[0].gid+1
    def getMaxMessageId(self, uid):
        maxId = DBSession.query(UserMessage).filter_by(uid=uid).order_by(UserMessage.mid.desc()).limit(1).all()
        if len(maxId) == 0:
            return 0
        return maxId[0].mid+1


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

    #def initTreasureStone(self, user):
    #    treasure = UserGoods(uid=user.uid, kind=tid=0)
        
    #global GOODS_COFF
    #GOODS_COFF = 10000
    def getTreasureStone(self, uid):
        treasure = DBSession.query(UserGoods).filter_by(uid=uid).all()
        res = []
        for t in treasure:
            res.append([t.kind*getParams("goodsCoff")+t.id, t.num])
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


        user.updateState += 1
        return dict(id=1, silver=silver, crystal=crystal, loginDays = user.loginDays)

    #用户升级后提升经验等级城堡防御力其它奖励
    @expose('json')
    def levelUp(self, uid, exp, level, rew):
        uid = int(uid)
        exp = int(exp)
        level = int(level)

        user = getUser(uid)
        user.exp = exp
        user.level = level
        self.initFriends(user)#升级之后更新好友数据

        return dict(id=1)


    @expose('json')
    def finishNewStory(self, uid):
        uid = int(uid)
        user = getUser(uid)
        user.newState = 1
        return dict(id=1)

    #更新 缓存数据表中的 用户名称
    #邻居关系 好友关系 
    @expose('json')
    def chooseFirstHero(self, uid, hid, name, sid):
        uid = int(uid)
        user = getUser(uid)
        hid = int(hid)#英雄ID 图片暂时使用普通士兵
        #客户端产生sid
        sid = int(sid)

        sameName = DBSession.query(UserInWan).filter_by(name=name).all()
        if len(sameName) > 0 and sameName[0].uid != uid:
            return dict(id=0, status=0, name = sameName[0].name)

        #测试模式不设置完成新手剧情
        if not getFullGameParam("debugStory"):
            user.newState = 1
        user.name = name
        user.heroId = hid

        soldier = UserSoldiers(uid=uid, sid=sid, kind=hid, name=name)
        DBSession.add(soldier)
        #编号15 凤凰变身技能暂时使用 的变身技能 暂时没有英雄变身技能
        
        #取消英雄技能 由装备 药水 获取技能
        #skillId = getData('heroSkill', hid)['skillId']
        #skill = UserSkills(uid=uid, soldierId=sid, skillId=skillId, level=0)
        #DBSession.add(skill)
        return dict(id=1)

    def initInvite(self, user):
        invite = UserInviteRank(uid=user.uid, inviteCode=user.uid+10000, inviteNum=0, rank=0, inputYet=False)
        DBSession.add(invite)
    def getInvite(self, uid):
        invite = DBSession.query(UserInviteRank).filter_by(uid=uid).one()
        return {'inviteCode':invite.inviteCode, 'inviteNum':invite.inviteNum, 'rank':invite.rank, 'inputYet':invite.inputYet}
    def getChallengeState(self, uid):
        challengeState = DBSession.query(UserChallengeState).filter_by(uid=uid).one()
        return dict(protectTime=challengeState.protectTime, activeScore=challengeState.activeScore)


    #生成日志的查询操作比较消耗时间  registerTime  可以加索引
    def initLog(self, user):
        log = UserLog(uid=user.uid, registerTime=getTime())
        DBSession.add(log)
    def setSecondLogin(self, user):
        ulog = DBSession.query(UserLog).filter_by(uid=user.uid).one()
        now = getTime()
        ulog.loginTime = now
        if ulog.newStage == 3:#完成新手任务
            if now - ulog.registerTime < 3600*24:
                ulog.secondLoginTime = now #第二次登录时间

    global Keys
    Keys = ['uid', 'silver', 'gold', 'crystal', 'level', 'people', 'cityDefense', 'loginDays', 'exp']
    #登录时新手依然返回英雄数据 只是英雄 人物 采用临时图片方法
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
            #user.inviteCode = user.uid+10000

            self.initUserData(user)
            self.initChallenge(user)
            self.initBuildings(user)
            self.initSoldiers(user)
            self.initDrug(user)
            self.initEquip(user)
            self.initRank(user)
            self.initChallengeFriend(user)
            #水晶矿 按照正常建筑初始化 经营页面不显示而已 检测类型
            #self.initCrystalMine(user)
            self.initFriends(user)
            self.initNeibor(user)
            self.initTreasureBox(user.uid)
            self.initInvite(user)
            self.initLog(user)
            #self.initSolEquip(user)
        
        #初次登录玩家 需要注册英雄和名称
        #if user.newState == 0:
        #    return dict(id=1, uid=user.uid, newState=0)

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
        #tasks = self.getTask(user.uid)
        challengeRecord = self.getChallengeRecord(user.uid)
        rank = self.getRankData(user.uid)
        #mine = self.getCrystalMine(user.uid)
        #soldierEquip=solEquip,
        treasure = self.getTreasureStone(user.uid)
        maxGiftId = self.getMaxGiftId(user.uid)
        maxMessageId = self.getMaxMessageId(user.uid)

        skills = self.getSkills(user.uid)

        week = time.localtime().tm_wday
        #week = 0

        updateState = user.updateState
        #user.updateState += 1
        lastLoginTime = user.loginTime
        lastWeek = getWeekNum(lastLoginTime)
        now = getTime()
        thisWeek = getWeekNum(now)

        hour = time.localtime().tm_hour
        #hour = 11
        #starNum = stars,

        box = DBSession.query(UserTreasureBox).filter_by(uid=user.uid).one()
        try:
            helperList = json.loads(box.helperList)
        except:
            helperList = []
        #返回帮助者的papayaId name 用于显示 返回好友的宝箱 -1是好友自己  返回自己的宝箱 -1 是自己
        papayaIdName = []
        for i in helperList:
            if i != -1:
                helper = getUser(i)
                papayaIdName.append([helper.papayaId, helper.name])
            else:
                papayaIdName.append([user.papayaId, user.name])
        invite = self.getInvite(user.uid)

        challengeState = self.getChallengeState(user.uid)

        self.setSecondLogin(user)

        ret = dict(id=1, uid = user.uid, name = user.name, resource = userData,  buildings = buildings, soldiers = soldiers, drugs=drugs, equips=equips,  herbs=herbs, serverTime=now, challengeRecord=challengeRecord, rank=rank,  treasure=treasure, maxGiftId=maxGiftId, skills = skills, newState = user.newState, week=week, updateState=updateState, lastWeek = lastWeek, thisWeek=thisWeek, registerTime=user.registerTime, hour = hour, maxMessageId=maxMessageId, hasBox=box.has, helperList=helperList, papayaIdName=papayaIdName, invite=invite, challengeState=challengeState) 
        return ret
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


    @expose('json')
    def fetchParams(self):
        print "fetchParams"
        gameParam = DBSession.query(GameParam).all()
        ret = dict()
        for i in gameParam:
            ret[i.key] = i.value 
        return ret
    #动态获取 士兵数据
    @expose('json')
    def getAllSolIds(self):
        con = MySQLdb.connect(host = 'localhost', user='root', passwd='badperson3', db='Wan2', charset='utf8')
        sql = 'select * from soldier where tested = 0'
        con.query(sql)
        res = con.store_result().fetch_row(0, 1)
        #con.close()

        ids = []
        solDatas = []
        for i in res:
            ids.append(i['id'])
        
        sql = 'select * from soldier'
        con.query(sql)
        res = con.store_result().fetch_row(0, 1)

        solDatas = []
        key = []
        for i in res:
            i = dict(i)
            #i['stage'] = json.loads(i['stage'])
            i['name'] = 'soldier' + str(i['id'])
            i.pop('engName')


            it = list(i.items())
            it = [list(k) for k in it]
            a = [k[1] for k in it]
            key = [k[0] for k in it]
            solDatas.append([i['id'], a])
        return dict(ids=ids, soldierKey=key, soldierData=solDatas)
    @expose('json')
    def setTested(self, sids):
        sids = json.loads(sids)
        con = MySQLdb.connect(host = 'localhost', user='root', passwd='badperson3', db='Wan2', charset='utf8')
        for i in sids:
            sql = 'update soldier set tested = 1 where id = %d' % (i)
            con.query(sql)
        con.commit()
        con.close()

    @expose('json')
    def getBuildingData(self):
        con = MySQLdb.connect(host = 'localhost', user='root', passwd='badperson3', db='Wan2', charset='utf8')
        sql = 'select * from building'
        con.query(sql)
        res = con.store_result().fetch_row(0, 1)

        buildDatas = []
        key = []

        for i in res:
            i = dict(i)
            if i.get('name') != None and i.get('id') != None:
                i['name'] = 'building'+str(i['id'])
            if i.get('engName') != None:
                i.pop('engName')
            it = list(i.items())
            it = [list(k) for k in it]
            key = [k[0] for k in it]
            a = [k[1] for k in it]
            if i.get('id') != None:
                buildDatas.append([i['id'], a])
        return dict(buildingKey=key, buildingData=buildDatas)

    @expose('json')
    def fetchAnimate(self):
        con = MySQLdb.connect(host = 'localhost', user='root', passwd=DB_PASSWORD, db='Wan2', charset='utf8')
        sql = 'select * from AttackEffectAnimate'
        con.query(sql)
        res = con.store_result().fetch_row(0, 1)
        ani = []
        for i in res:
            """
            i = dict()
            it = list(i.items())
            it = [list(k) for k in it]
            key = [k[0] for k in it]
            a = [k[1] for k in it]
            ani.append([i['id'], a])
            """

            ani.append([i['id'], [json.loads(i['animation']), i['time'], [0, 0], i['scale']]])



        sql = 'select * from soldierMagic'
        con.query(sql)
        magic = con.store_result().fetch_row(0, 1)
        mgList = []
        for i in magic:
            mgList.append([i['id'], [i['make'], i['fly'], i['bomb']]])


        sql = 'select * from particleEffectParameter'
        con.query(sql)
        res = con.store_result().fetch_row(0, 1)
        particles = []
        for i in res:
            i = dict(i)
            it = list(i.items())
            it = [list(k) for k in it]
            pkey = [k[0] for k in it]
            a = [k[1] for k in it]
            particles.append([i['id'], a])
        

        con.close()
        return dict(ani=ani, sol=mgList, pData = particles, pKey=pkey)

    @expose('json')
    def getTaskData(self):
        con = MySQLdb.connect(host = 'localhost', user='root', passwd=DB_PASSWORD, db='Wan2', charset='utf8')
        sql = 'select * from allTasks'
        con.query(sql)
        f = con.store_result().fetch_row(0, 1)
        res = []
        for i in f:
            i = dict(i)
            i['title'] = 'title'+str(i['id'])
            i['des'] = 'des'+str(i['id'])


            i['commandList'] = json.loads(i['commandList'])
            for c in i['commandList']:
                if c.get('tip') != None:
                    old = c['tip']
                    c['tip'] = 'taskTip'+str(c['msgId'])

            i['stageArray'] = json.loads(i['stageArray'])
            i['goldArray'] = json.loads(i['goldArray'])
            i['expArray'] = json.loads(i['expArray'])

            it = list(i.items())
            it = [list(k) for k in it]
            key = [k[0] for k in it]
            a = [k[1] for k in it]
            res.append([i['id'], a])

        con.close()
        print 'taskData', len(res)
        return dict(taskData=res, taskKey=key)


    @expose('json')
    def getAllFallGoods(self):
        con = MySQLdb.connect(host = 'localhost', user='root', passwd=DB_PASSWORD, db='Wan2', charset='utf8')
        sql = 'select * from MoneyGameGoods'
        con.query(sql)

        res = con.store_result().fetch_row(0, 1)
        data = []
        for i in res:
            i = dict(i)
            it = list(i.items())
            it = [list(k) for k in it]
            pkey = [k[0] for k in it]
            a = [k[1] for k in it]
            data.append([i['id'], a])

        con.close()
        return dict(MoneyGameGoodsKey=pkey, MoneyGameGoodsData=data)
            
    @expose('json')
    def getStaticData(self, did):
        con = MySQLdb.connect(host = 'localhost', user='root', passwd=DB_PASSWORD, db='Wan2', charset='utf8')
        sql = 'select * from %s' % (did)
        con.query(sql)

        res = con.store_result().fetch_row(0, 1)
        data = []
        pKey = []
        for i in res:
            i = dict(i)
            if i.get('name') != None and i.get('id') != None:
                i['name'] = did+str(i['id'])
            if i.get('engName') != None:
                i.pop('engName')
            if i.get('hasNum') != None:
                if i['hasNum']:
                    i['numCost'] = json.loads(i['numCost'])
                else:
                    i['numCost'] = []

            it = list(i.items())
            it = [list(k) for k in it]
            pKey = [k[0] for k in it]
            a = [k[1] for k in it]
            data.append([i['id'], a])

        con.close()
        return dict(key=pKey, data=data)
        
        
    @expose('json')
    def getMapMonster(self):
        con = MySQLdb.connect(host = 'localhost', user='root', passwd=DB_PASSWORD, db='Wan2', charset='utf8')
        sql = 'select * from mapMonster'
        con.query(sql)
        f = con.store_result().fetch_row(0, 1)
        res = {}
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

        con.close()
        return dict(mapMonsterData=res, mapMonsterKey=key)


        
    @expose('json')
    def getString(self):
        myCon = MySQLdb.connect(host='localhost', user='root', passwd='badperson3', db='Wan2', charset='utf8')
        sql = 'select * from Strings where deleted = 0'
        myCon.query(sql)

        rows = myCon.store_result().fetch_row(0, 1)
        res = []
        for i in rows:
            ch = i['chinese'].replace('\\n', '\n')
            eng = i['english'].replace('\\n', '\n')
            res.append([i['key'], [ch, eng]])

        names = getAllNames() 
        myCon.close()
        return dict(WORDS=res, names=names)
    @expose('json')
    def updateCurrentSoldierId(self, sid):
        sid = int(sid)
        myCon = MySQLdb.connect(host='localhost', user='root', passwd='badperson3', db='Wan2', charset='utf8')
        sql = 'update GameParam set value = %d where `key` = "%s"' % (sid, "currentSoldier")
        myCon.query(sql)
        myCon.commit()
        myCon.close()
        return dict(id=1)
        
    @expose('json')
    def finishPay(self, uid, tid, gain, papaya):
        uid = int(uid)
        tid = int(tid)
        gain = json.loads(gain)
        papaya = int(papaya)
        doGain(uid, gain)
        chargeLog = UserChargeLog(uid=uid, papaya=papaya, time=getTime())
        DBSession.add(chargeLog)
        log = logging.getLogger(__name__)
        log.debug("finishPay %d %d %d %d" % (uid, tid, papaya, getTime()))
        return dict(id=1)
