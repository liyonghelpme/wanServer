# -*- coding: utf-8 -*-
"""Fallback controller."""
from tg import expose, flash, require, url, lurl, request, redirect
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

__all__ = ['TaskController']


class TaskController(BaseController):
    #增加任务完成数目 num = 0 表示出现新的用户任务 num += num
    @expose('json')
    def doTask(self, uid, tid, num):
        uid = int(uid)
        tid = int(tid)
        num = int(num)
        try:
            task = DBSession.query(UserTask).filter_by(uid=uid).filter_by(tid=tid).one()
        except:
            task = UserTask(uid=uid, tid=tid, number=0, finish=0, stage=0)
            DBSession.add(task)
        task.number += num
        return dict(id=1)

        
    
    #完成任务   finish = 1 获得奖励 累计任务进入下一个阶段
    @expose('json')
    def finishTask(self, uid, tid):
        uid = int(uid)
        tid = int(tid)
        data = getData('task', tid)

        task = DBSession.query(UserTask).filter_by(uid=uid).filter_by(tid=tid).one()

        if task.number < data.get("need") or task.finish == 1:
            return dict(id=0)

        task.finish = 1
        #普通任务
        if data.get('need') > 0:
            gain = getGain('task', tid)
            doGain(uid, gain)
        #在初始化的时候 设定accArray 
        else:
            stage = task.stage
            taskData = getData('task', task.tid)
            accArray = json.loads(taskData.get('accArray'))
            stage = min(len(accArray)-1, stage)
            gain = getGain('task', tid)
            #按照当前的阶段给予奖励
            for g in gain:
                gain[g] *= stage
            doGain(uid, gain)

            task.stage += 1
            task.num = 0
            task.finish = 0
        return dict(id=1)


        

