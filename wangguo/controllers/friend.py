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

__all__ = ['FriendController']


class FriendController(BaseController):
    @expose('json')
    def getFriend(self, uid, papayaId):
        uid = int(uid)
        papayaId = int(papayaId)
        try:
            friend = DBSession.query(UserInWan).filter_by(papayaId=papayaId).one()
            soldiers = getSoldiers(friend.uid)
            return dict(id=1, level=friend.level, soldiers=soldiers, fid = friend.uid)
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
            res.append([i.papayaId, i.fid, i.lev])
        return dict(id=1, res=res) 
    @expose('json')
    def addFriend(self, uid, flist):
        uid = int(uid)
        flist = json.loads(flist)#[papayaId,]
        for f in flist:
            try:
                fid = DBSession.query(UserInWan).filter_by(papayaId=f).one()
                fid = fid.uid
            except:
                fid = -1
            friend = UserFriend(uid = uid, papayaId=f, fid=fid)
            try:
                exist = DBSession.query(UserFriend).filter_by(uid = uid, papayaId=f).one()
            except:
                DBSession.add(friend)
        return dict(id=1)
            
        
