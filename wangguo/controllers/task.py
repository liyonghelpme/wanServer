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
    @expose('json')
    def synTask(self, uid, needSyn):
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
        try:
            task = DBSession.query(UserTask).filter_by(uid=uid, tid=tid).one()
        except:
            task = UserTask(uid=uid, tid=tid, number=0, stage=0)
            DBSession.add(task)
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
    def updateNewTaskStage(self, uid, newTaskStage):
        uid = int(uid)
        newTaskStage = int(newTaskStage)
        user = getUser(uid)
        user.newTaskStage = newTaskStage
        return dict(id=1)
         

    @expose('json')
    def finishNewTask(self, uid, tid, gain):
        uid = int(uid)
        tid = int(tid)
        gain = json.loads(gain)
        task = DBSession.query(UserTask).filter_by(uid=uid, tid=tid).one()
        task.stage += 1
        task.number = 0
        doGain(uid, gain)
        return dict(id=1)
            
            
            



