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
import random
from tg import tmpl_context
from tw.jquery import FlotWidget
import tw
import math
import logging

__all__ = ['TaskController']


flot = FlotWidget(id="flotSample", width='640px', height='320px', lable="Simple Flot Example")
class LogController(BaseController):
    def getWeekStartTime(self):
        now = time.localtime()
        week = time.mktime([now.tm_year, now.tm_mon, now.tm_mday-6, 0, 0, 0, 0, 0, 0])
        start = time.mktime(beginTime)
        week -= start
        return week
        
    @expose('wangguo.templates.flot')
    def registerNum(self):
        u"注册人数"
        tmpl_context.flot = flot
        print tmpl_context
        #最近一周的每天打开游戏的人数打开游戏的人数
        #按照天来算
        data = []#x y 
        week = self.getWeekStartTime()

        for i in xrange(0, 7):
            rnum = DBSession.query(UserLog).filter("registerTime >= %d+%d*3600*24 and registerTime < %d+(%d+1)*3600*24" % (week, i, week, i)).count()
            data.append((i, rnum))
        return dict(page="index", data=[data], options={})
    @expose('json')
    def finishNewStage(self, uid, stage):
        uid = int(uid)
        stage = int(stage)
        userLog = DBSession.query(UserLog).filter_by(uid=uid).one()
        userLog.newStage = stage
        return dict(id=1)

    @expose('wangguo.templates.flot')
    def newRoundWin(self):
        u"新手任务完成人数"
        tmpl_context.flot = flot
        week = self.getWeekStartTime()
        data1 = []
        data2 = []
        data3 = []
        for i in xrange(0, 7):
            rnum = DBSession.query(UserLog).filter("newStage = 1 and registerTime >= %d+%d*3600*24 and registerTime < %d+(%d+1)*3600*24" % (week, i, week, i)).count()
            data1.append((i, rnum))

            rnum = DBSession.query(UserLog).filter("newStage = 2 and registerTime >= %d+%d*3600*24 and registerTime < %d+(%d+1)*3600*24" % (week, i, week, i)).count()
            data2.append((i, rnum))

            rnum = DBSession.query(UserLog).filter("newStage = 3 and registerTime >= %d+%d*3600*24 and registerTime < %d+(%d+1)*3600*24" % (week, i, week, i)).count()
            data3.append((i, rnum))
        return dict(data=[data1, data2, data3], options={})
    @expose('wangguo.templates.flot')
    def secondLogin(self):
        u"第二天登录用户数量"
        tmpl_context.flot = flot
        week = self.getWeekStartTime()
        data = []
        for i in xrange(0, 7):
            rnum = DBSession.query(UserLog).filter("secondLoginTime > 0 and registerTime >= %d+%d*3600*24 and registerTime < %d+(%d+1)*3600*24" % (week, i, week, i)).count()
            data.append((i, rnum))
        return dict(data=[data], options={})
    @expose('wangguo.templates.flot')
    def getGoldCost(self):
        u"金币消费"
        tmpl_context.flot = flot
        data = DBSession.execute("select goldLevel, count(*) from UserLog where goldLevel > -1 group by goldLevel").fetchall()
        data = [(int(i[0]), int(i[1])) for i in data]
        options = {"series":{"lines":{"show":False}, "points":{"show":True}}}
        return dict(data=[data], options=options)
    @expose('json')
    def getHalfGoldUserLost(self):
        u"花费掉一半金币的流失用户数量"
        tmpl_context.flot = flot
        now = getTime()-3600*24

        data = DBSession.execute("select count(*) from UserLog where costGold > %d and loginTime < %d" % (getFullGameParam("initGold")/2, now)).fetchall()
        return dict(data=data[0][0])
    @expose('wangguo.templates.flot')
    def chargeUserNum(self):
        u"用户充值记录总数"
        tmpl_context.flot = flot
        week = self.getWeekStartTime()
        data = []
        for i in xrange(0, 7):
            rnum = DBSession.query(UserChargeLog).filter("time >= %d and time < %d" % (week+i*3600*24, week+((i+1)*3600*24))).count()
            data.append((i, rnum))
        return dict(data=[data], options={})

    @expose('wangguo.templates.flot')
    def chargePapayaNum(self):
        u"用户购买木瓜币总数量"
        tmpl_context.flot = flot
        week = self.getWeekStartTime()
        data = []
        for i in xrange(0, 7):
            rnum = DBSession.execute("select sum(papaya) from UserChargeLog where time >= %d and time < %d" % (week+i*3600*24, week+((i+1)*3600*24))).fetchall()
            print rnum
            if len(rnum) > 0 and rnum[0][0] != None:
                data.append((i, int(rnum[0][0])))
            else:
                data.append((i, 0))
        return dict(data=[data], options={})
        

    @expose('wangguo.templates.flot')
    def DAU(self):
        u"DAU 每日活跃用户"
        tmpl_context.flot = flot
        week = self.getWeekStartTime()
        data = []
        for i in xrange(0, 7):
            rnum = DBSession.query(UserLog).filter("loginTime >= %d and loginTime < %d and newStage >= 3" % (week+i*3600*24, week+((i+1)*3600*24))).count()
            data.append((i, rnum))
        return dict(data=[data], options={})
    #income 
    @expose('wangguo.templates.flot')
    def ARPU(self):
        u"ARPU 每用户平均收入"
        tmpl_context.flot = flot
        week = self.getWeekStartTime()
        data = []
        for i in xrange(0, 7):
            papaya = DBSession.execute("select sum(papaya) from UserChargeLog where time >= %d and time < %d" % (week+i*3600*24, week+((i+1)*3600*24))).fetchall()
            dau = DBSession.query(UserLog).filter("loginTime >= %d and loginTime < %d and newStage >= 3" % (week+i*3600*24, week+((i+1)*3600*24))).count()
            if len(papaya) > 0 and papaya[0][0] != None and dau > 0:
                data.append((i, int(papaya[0][0])/dau))
            else:
                data.append((i, 0))
        return dict(data=[data], options={})

    @expose('wangguo.templates.flot')
    def ARPPU(self):
        u"付费用户每人平均付费数"
        tmpl_context.flot = flot
        week = self.getWeekStartTime()
        data = []
        for i in xrange(0, 7):
            papaya = DBSession.execute("select sum(papaya) from UserChargeLog where time >= %d and time < %d" % (week+i*3600*24, week+((i+1)*3600*24))).fetchall()
            payUserNum = DBSession.query(UserChargeLog).filter("time >= %d and time < %d" % (week+i*3600*24, week+((i+1)*3600*24))).count()
            if len(papaya) > 0 and papaya[0][0] != None and payUserNum > 0:
                data.append((i, int(papaya[0][0])/payUserNum))
            else:
                data.append((i, 0))
        return dict(data=[data], options={})

    @expose('json')
    def lostUser(self):
        u"目前为止流失的用户数量"
        now = getTime()-3600*24*3
        lostNum = DBSession.query(UserLog).filter("loginTime < %d" % (now)).count()
        return dict(data=lostNum)

    @expose('wangguo.templates.flot')
    def lostLevelUser(self):
        u"3天没有登录的流失用户的等级分布"
        tmpl_context.flot = flot
        now = getTime()-3600*24*3
        lostNum = DBSession.execute("select level, count(*) from UserInWan where loginTime < %d group by level" % (now)).fetchall()
        data = [(int(i[0]), int(i[1])) for i in lostNum]
        return dict(data=[data], options={})

    @expose('json')
    def tryPay(self, uid, papaya):
        uid = int(uid)
        papaya = int(papaya)
        now = getTime()
        log = logging.getLogger(__name__)
        log.debug("tryPay %d %d %d" % ( uid, papaya, now))
        return dict(id=1)

    @expose('wangguo.templates.flot')
    def solNum(self):
        u"各种类型士兵购买数量"
        tmpl_context.flot = flot
        buySol = DBSession.execute("select kind, count(*) from UserSoldiers group by kind").fetchall()
        buySol = [(int(i[0]), int(i[1]))for i in buySol]
        return dict(data=[buySol], options={})

    @expose('wangguo.templates.logEntry')
    def log(self):
        interfaces = [self.registerNum, self.newRoundWin, self.secondLogin, 
                self.getGoldCost, self.getHalfGoldUserLost, self.chargeUserNum, 
                self.chargePapayaNum, self.DAU, self.ARPU,
                self.ARPPU, self.lostUser, self.lostLevelUser, 
                self.solNum]
        passData = []
        for i in interfaces:
            passData.append([i.__name__, i.__doc__])

        return dict(passData=passData)

     

        
        
        
        

        
            
        
            



        
