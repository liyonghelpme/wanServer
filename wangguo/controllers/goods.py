# -*- coding: utf-8 -*-
"""Fallback controller."""
from tg import expose, flash, require, url, request, redirect
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

__all__ = ['GoodsController']


class GoodsController(BaseController):
    @expose('json')
    def buyResource(self, uid, kind, oid):
        uid = int(uid)
        kind = int(kind)
        oid = int(oid)

        table = datas['TableMap'][kind]['name']
        cost = getCost(table, oid) 
        gain = getGain(table, oid)
        ret = checkCost(uid, cost)
        if not ret:
            return dict(id=0)
        doCost(uid, cost)
        doGain(uid, gain)
        return dict(id=1)
    #购买物品 消耗资源
    @expose('json')
    def buyDrug(self, uid, drugKind):
        uid = int(uid)
        drugKind = int(drugKind)

        cost = getCost('drug', drugKind)
        ret = checkCost(uid, cost)
        if not ret:
            return dict(id=0)

        try:
            drug = DBSession.query(UserDrugs).filter_by(uid=uid).filter_by(drugKind=drugKind).one()
        except:
            drug = UserDrugs(uid=uid, drugKind=drugKind, num = 0)
            DBSession.add(drug)
        drug.num += 1


        doCost(uid, cost)
        return dict(id=1)
        
    @expose('json')
    def buyEquip(self, uid, eid, equipKind):
        uid = int(uid)
        eid = int(eid)
        equipKind = int(equipKind)

        cost = getCost('equip', equipKind)
        ret = checkCost(uid, cost)
        if not ret:
            return dict(id=0)

        equip = UserEquips(uid=uid, eid=eid, equipKind=equipKind)
        DBSession.add(equip)

        doCost(uid, cost)
        return dict(id=1)

    @expose('json')
    def upgradeEquip(self, uid, eid, tid):
        uid = int(uid)
        eid = int(eid)
        tid = int(tid)
        goods = DBSession.query(UserGoods).filter_by(uid=uid, kind = getKindId('goodsList'), id=tid).one()
        if goods.num < 1:
            return dict(id=0, status=0)

        goods.num -= 1
        equip = DBSession.query(UserEquips).filter_by(uid=uid, eid=eid).one()

        gData = getData('goodsList', tid)
        possible = gData.get('possible')

        suc = possible[equip.level][0]
        rd = random.randint(0, 100)
        if rd < suc:
            equip.level += 1
            return dict(id=1, suc=1)

        rd = random.randint(0, 100)
        if rd < possible[equip.level][1]:
            equip.level -= 1
            equip.level = max(equip.level, 0)
            return dict(id=1, suc=0, breakEquip=1)
        return dict(id=1, suc=0, breakEquip=0)

    @expose('json')
    def pickObj(self, uid, silver, crystal, gold):
        uid = int(uid)
        silver = int(silver)
        crystal = int(crystal)
        gold = int(gold)
        user = getUser(uid)
        user.silver += silver
        user.crystal += crystal
        user.gold += gold
        return dict(id=1)

    @expose('json')
    def makeDrug(self, uid, pid):
        uid = int(uid)
        pid = int(pid)
        prescription = getData('prescription', pid)
        needs = prescription['needs']
        kind = prescription['kind']
        tid = prescription['tid']
        #print needs
        print needs

        allHerb = []
        for i in needs:
            try:
                herb = DBSession.query(UserHerb).filter_by(uid=uid, kind=i[0]).one()
                allHerb.append(herb)
                if herb.num < i[1]:
                    return dict(id=0, reason='herb not')
            except:
                return dict(id=0, reason='herb not')

        for i in range(0, len(allHerb)):
            allHerb[i].num -= needs[i][1]

        try:
            drug = DBSession.query(UserDrugs).filter_by(uid=uid, drugKind=kind).one()
        except:
            drug = UserDrugs(uid=uid, drugKind=kind, num=0)
            DBSession.add(drug)
        drug.num += 1
        return dict(id=1)

    @expose('json')
    def makeEquip(self, uid, eid, pid):
        uid = int(uid)
        pid = int(pid)
        prescription = getData('prescription', pid)
        needs = prescription['needs']
        kind = prescription['kind']
        tid = prescription['tid']
        
        print needs

        allHerb = []
        for i in needs:
            try:
                herb = DBSession.query(UserHerb).filter_by(uid=uid, kind=i[0]).one()
                allHerb.append(herb)
                if herb.num < i[1]:
                    return dict(id=0, reason='herb not')
            except:
                return dict(id=0, reason='herb not')
        for i in range(0, len(allHerb)):
            allHerb[i].num -= needs[i][1]
            #print allHerb[i].num

        equip = UserEquips(uid=uid, eid=eid, equipKind=pid)
        DBSession.add(equip)
        return dict(id=1)
    @expose('json')
    def sellDrug(self, uid, kind, silver):
        uid = int(uid)
        kind = int(kind)
        silver = int(silver)

        user = getUser(uid)
        user.silver += silver

        drug = DBSession.query(UserDrugs).filter_by(uid=uid, drugKind=kind).one()
        drug.num = 0
        return dict(id=1)

    @expose('json')
    def sellEquip(self, uid, eid, silver):
        uid = int(uid)
        eid = int(eid)
        silver = int(silver)

        user = getUser(uid)
        user.silver += silver

        equip = DBSession.query(UserEquips).filter_by(uid=uid, eid=eid).one()
        DBSession.delete(equip)

        return dict(id=1)

    @expose('json')
    def buyTreasureStone(self, uid, tid):
        uid = int(uid)
        tid = int(tid)

        tcost = getCost("goodsList", tid)
        doCost(uid, tcost)

        updateGoodsNum(uid, getKindId('goodsList'), tid, 1)
        
        return dict(id=1)
    @expose('json')
    def buyMagicStone(self, uid, tid):
        uid = int(uid)
        tid = int(tid)

        tcost = getCost("magicStone", tid)
        doCost(uid, tcost)

        updateGoodsNum(uid, getKindId('magicStone'), tid, 1)
        return dict(id=1)
        
        
    #ti 主要用于 区分同1秒钟重复赠送相同类型礼物的问题
    @expose('json')
    def sendEquip(self, uid, fid, eid, gid):
        uid = int(uid)
        fid = int(fid)
        eid = int(eid)
        gid = int(gid)

        equip = DBSession.query(UserEquips).filter_by(uid=uid, eid=eid).one()
        #装备取消等级
        gift = UserGift(uid=uid, fid=fid, kind = getKindId('equip'), tid=equip.equipKind, level=0, time=getTime(), gid=gid)
        DBSession.add(gift)
        DBSession.delete(equip)
        return dict(id=1)
    @expose('json')
    def sendDrug(self, uid, fid, did, gid):
        uid = int(uid)
        fid = int(fid)
        did = int(did)
        gid = int(gid)

        drug = DBSession.query(UserDrugs).filter_by(uid=uid, drugKind=did).one()
        if drug.num <= 0:
            return dict(id=0)
        
        drug.num -= 1
        gift = UserGift(uid=uid, fid=fid, kind=getKindId('drug'), tid=did, level=0, time=getTime(), gid=gid)
        DBSession.add(gift)

        return dict(id=1)

    @expose('json')
    def sendHerb(self, uid, fid, tid, gid):
        uid = int(uid)
        fid = int(fid)
        tid = int(tid)
        gid = int(gid)

        material = DBSession.query(UserHerb).filter_by(uid=uid, kind = tid).one()
        if material.num <= 0:
            return dict(id=0)

        material.num -= 1
        gift = UserGift(uid=uid, fid=fid, kind=getKindId('herb'), tid=tid, level=0, time=getTime(), gid=gid)
        DBSession.add(gift)

        return dict(id=1)

    @expose('json')
    def sendTreasureStone(self, uid, fid, tid, gid):
        uid = int(uid)
        fid = int(fid)
        tid = int(tid)
        gid = int(gid)

        stone = DBSession.query(UserGoods).filter_by(uid=uid, kind = getKindId('goodsList'), id=tid).one()
        if stone.num <= 0:
            return dict(id=0)

        stone.num -= 1
        gift = UserGift(uid=uid, fid=fid, kind=getKindId('goodsList'), tid=tid, level=0, time=getTime(), gid=gid)
        DBSession.add(gift)

        return dict(id=1)

    #宝石 和 魔法石 功效 不同 但是 采用统一 编ID 的方式 存储 0-3宝石  4- 魔法石

    #数据类型虽然不同 但是 存储的方式 都是在GOODS 
    #通过 数据ID 来进行 区分
    #数据 形式都是 ID NUM
    @expose('json')
    def sendMagicStone(self, uid, fid, tid, gid):
        uid = int(uid)
        fid = int(fid)
        tid = int(tid)
        gid = int(gid)

        stone = DBSession.query(UserGoods).filter_by(uid=uid, kind=getKindId('magicStone'), id=tid).one()
        if stone.num <= 0:
            return dict(id=0)

        stone.num -= 1
        gift = UserGift(uid=uid, fid=fid, kind=getKindId('magicStone'), tid=tid, level=0, time=getTime(), gid=gid)
        DBSession.add(gift)

        return dict(id=1)

    @expose('json')
    def getGift(self, uid):
        uid = int(uid)
        gifts = DBSession.query(UserGift).filter_by(fid = uid).all()
        res = []
        for g in gifts:
            friend = getUser(g.uid)
            res.append([friend.uid, friend.name, g.kind, g.tid, g.level, g.time, g.gid])
        return dict(id=1, gifts=res)


    #如果是装备 需要客户端提供eid
    @expose('json')
    def receiveGift(self, uid, fid, gid, eid):
        uid = int(uid)
        fid = int(fid)
        gid = int(gid)
        eid = int(eid)
        gift = DBSession.query(UserGift).filter_by(uid=fid, fid=uid, gid=gid).one()
        if gift.kind == getKindId('equip'):
            equip = UserEquips(uid=uid, equipKind=gift.tid, eid=eid)
            equip.level = gift.level
            DBSession.add(equip)
        else:
            updateGoodsNum(uid, gift.kind, gift.tid, 1)

        DBSession.delete(gift)
        return dict(id=1)

            

        
