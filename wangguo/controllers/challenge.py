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

#from wangguo.model import DBSession, metadata
from wangguo.model import *

__all__ = ['ChallengeController']


class ChallengeController(BaseController):
    pass
    """
    The fallback controller for wangGuo.
    
    By default, the final controller tried to fulfill the request
    when no other routes match. It may be used to display a template
    when all else fails, e.g.::
    
        def view(self, url):
            return render('/%s' % url)
    
    Or if you're using Mako and want to explicitly send a 404 (Not
    Found) response code when the requested template doesn't exist::
    
        import mako.exceptions
        
        def view(self, url):
            try:
                return render('/%s' % url)
            except mako.exceptions.TopLevelLookupException:
                abort(404)
    
    """
    #def finishChallenge(self, uid, big, small, star, reward):

    """
    def updateChallenge(self, uid, big, small, star):
        uid = int(uid)
        big = int(big)
        small = int(small)
        star = int(star)
        #没有拿到任务数据    
        challenge = DBSession.query(UserChallenge).filter_by(uid=uid).filter_by(big=big).filter_by(small=small).one()
        challenge.star = star
        return dict(id=1)
    """
        

