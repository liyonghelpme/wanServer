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

__all__ = ['TaskController']


class TaskController(BaseController):
    #客户端需要用json_dumps 将needSyn 转化成字符串 
    @expose('json')
    def synCycleTask(self, uid, needSyn):
        uid = int(uid)
        needSyn = json.loads(needSyn)
        ret = []
        for i in needSyn:
            try:
                task = DBSession.query(UserTask).filter_by(uid=uid, tid=i).one()
            except:
                task = UserTask(uid=uid, tid=i, number=0, stage=0)
                DBSession.add(task)
            ret.append([task.tid, task.number, task.stage])
        return dict(id=1, ret=ret)
    @expose('json')
    def doCycleTask(self, uid, tid, num):
        uid = int(uid)
        tid = int(tid)
        num = int(num)
        task = DBSession.query(UserTask).filter_by(uid=uid, tid=tid).one()
        task.number += num
        return dict(id=1)
    
    @expose('json')
    def finishCycleTask(self, uid, tid, gain):
        uid = int(uid)
        tid = int(tid)
        gain = json.loads(gain)
        task = DBSession.query(UserTask).filter_by(uid=uid, tid=tid).one()
        task.stage += 1
        task.number = 0
        doGain(uid, gain)
        return dict(id=1)



    @expose('json')
    def getBuyTask(self, uid):
        uid = int(uid)
        task = DBSession.query(UserBuyTaskRecord).filter_by(uid=uid).all()
        tasks = [i.oid for i in task]
        return dict(id=1, tasks=tasks)

    
    @expose('json')
    def finishBuyTask(self, uid, oid, gain):
        print gain
        gain = json.loads(gain)
        task = UserBuyTaskRecord(uid=uid, oid=oid)
        DBSession.add(task)
        doGain(uid, gain)
        return dict(id=1)

    #随机生成一批不同类型的每日任务
    
    #得到所有的每日任务
    #分类每日任务
    #产生3个类
    #从3个类中 去除 3个任务
    @expose('json')
    def getDayTask(self, uid):
        uid = int(uid)
        allTasks = datas['allTasks'].items()
        dayTask = {}#category ---> [a b c]
        for i in allTasks:
            if i[1]["kind"] == getParams("dayTask"):
                cat = dayTask.setdefault(i[1]['dayCategory'], [])
                cat.append(i[1])
        
        allCategory = dayTask.items()
        res = []
        #随机生成3个数
        for i in xrange(0, 3):
            if len(allCategory) > 0:
                pos = random.randint(0, len(allCategory)-1)
                res.append(allCategory[pos])
                allCategory.pop(pos)
        realTid = []
        for i in res:
            pos = random.randint(0, len(i[1])-1)
            realTid.append(i[1][pos]['id'])
        return dict(id=1, dayTid=realTid)
    

    #完成3个每日任务后产生奖励
    @expose('json')
    def finishDayTask(self, uid, gain):
        uid = int(uid)
        gain = json.loads(gain)
        doGain(uid, gain)
        return dict(id=1)
         

            
            
            



