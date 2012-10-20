# -*- coding: utf-8 -*-
"""The application's model objects"""

from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
from sqlalchemy import Table
#from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base


#从数据库获取当前消耗和增加数据
import MySQLdb
import json
from threading import Thread
import time

import pymongo

mongoCon = pymongo.Connection(host='localhost', port=27017)
mongoDB = mongoCon['Rank']
mongoCollect = mongoDB.heartRank
newRankCollect = mongoDB.UserNewRank
groupRankCollect = mongoDB.UserGroupRank
recommandCollect = mongoDB.UserRecommand
arenaCollect = mongoDB.UserArena
inviteCollect = mongoDB.InviteRecord
inviteCollect.create_index([('uid', pymongo.DESCENDING), ('oid', pymongo.DESCENDING)])
inviteRankCollect = mongoDB.inviteRank

#Arena Collect
attackCollect = mongoDB.UserAttack
defenseCollect = mongoDB.UserDefense

con = MySQLdb.connect(host = 'localhost', user='root', passwd='badperson3', db='Wan2', charset='utf8')
#cur = con.cursor()
"""
EQUIP = 1
DRUG = 2
HERB = 10
TREASURE_STONE = 15
MAGIC_STONE = 16
"""

name = ['building','crystal', 'drug', 'equip',  'gold', 'herb', 'levelExp', 'plant', 'prescription', 'silver', 'soldier', 
'soldierAttBase', 'soldierGrade', 'soldierKind', 'soldierLevel', 'soldierTransfer',
'soldierLevelExp', 'allTasks', 'goodsList', 'magicStone', 'skills', 'loveTreeHeart', 'fightingCost', 'newParam', 'TableMap', 'heroSkill',
'BoxReward']

def getPrescriptionNum():
    sql = 'select * from prescriptionNum'
    con.query(sql)
    res = con.store_result().fetch_row(0, 1)
    nums = {}
    for i in res:
        nums[i['id']] = i
    return nums

prescriptionNum = getPrescriptionNum()

def genArray(possible):
    res = []
    for l in range(0, 13):
        p = l*1.0/12
        t = []
        t.append(int(possible[0]*(1-p) + possible[1]*p))
        t.append(int(possible[2]*(1-p) + possible[3]*p))
        res.append(t)
    return res
#0-59 possible
#0 14 29 44 59
XPOS = [0, 14, 29, 44, 59]
def genMagicArray(pos):
    global XPOS
    res = []
    for l in range(0, 60):
        for i in XPOS:
            if i > l:
                break
        begin = XPOS.index(i)-1
        end = begin+1
        if end >= len(XPOS):
            res.append(pos[end])
        else:
            p = (l-XPOS[begin])*1.0/(XPOS[end]-XPOS[begin])
            t = []
            res.append(int(pos[begin]*(1-p) + pos[end]*p))
    return res
datas = dict()
def getDataFromDB():
    #需要保证TableMap 比 BoxReward 先初始化 Str2IntKind 存储从表名 到 整数类型的映射
    datas['Str2IntKind'] = dict()
    for i in name:
        sql = 'select * from '+i;#all Data
        con.query(sql)
        res = con.store_result()
        allData = res.fetch_row(0, 1)
        datas[i] = dict()
        if i == 'BoxReward':
            dic = {}
            for a in allData:
                a['id'] = datas['Str2IntKind'][a['kind']]['id'] 
                dic[a['kind']] = a
            datas[i] = dic 
        elif i == 'newParam':
            dic = {}
            for a in allData:
                dic[a['key']] = a['value']
            datas['PARAMS'] = dic
        elif i == 'PARAMS':
            for a in allData:
                datas[i] = a
        elif i == 'loveTreeHeart':
            for a in allData:
                datas[i] = json.loads(a['num'])
        elif i == 'prescription':
            for a in allData:
                needs = []
                numId = a['numId']
                r = prescriptionNum[numId]
                a['num1'] = r['xNum']
                a['num2'] = r['yNum']
                a['num3'] = r['zNum']

                if a['num1'] != 0:
                    needs.append([a['id1'], a['num1']])
                if a['num2'] != 0:
                    needs.append([a['id2'], a['num2']])
                if a['num3'] != 0:
                    needs.append([a['id3'], a['num3']])
                        
                #res.append([i['id'], [i['id'], i['kind'], i['level'], i['tid'], needs]])
                a.update({'needs':needs})
                datas[i][a['id']] = a
                
        elif i == 'mapMonster':
            for a in allData:
                k = a['big']*10+a['small']
                mons = datas[i].get(k, [])
                mons.append(a)
                datas[i][k] = mons
        else:
            for a in allData:
                if i == 'levelExp':
                    datas[i] = json.loads(a['exp'])
                elif i == 'soldierAttBase':
                    datas[i] = json.loads(a['base'])
                elif i == 'soldierGrade':
                    datas[i][a['id']] = a['level']
                elif i == 'soldierKind':
                    datas[i][a['id']] = json.loads(a['attribute'])
                elif i == 'soldierLevel':
                    datas[i] = json.loads(a['levelData'])
                elif i == 'soldierTransfer':
                    datas[i] = json.loads(a['level'])
                elif i == 'goodsList':
                    possible = [a['maxFail'], a['minFail'], a['minBreak'], a['maxBreak']]
                    a['possible'] = genArray(possible)
                    sql = 'update goodsList set possible = \'%s\' where id = %d' % (str(a['possible']), a['id'])
                    con.query(sql)
                    datas[i][a['id']] = a
                elif i == 'magicStone':
                    possible = [a['pos0'], a['pos14'], a['pos29'], a['pos44'], a['pos59']]
                    a['possible'] = genMagicArray(possible)
                    sql = 'update magicStone set possible = \'%s\' where id = %d' % (str(a['possible']), a['id'])
                    con.query(sql)
                    datas[i][a['id']] = a
                elif i == 'heroSkill':
                    datas[i][a['hid']] = a
                elif i == 'TableMap':
                    datas[i][a['id']] = a
                    datas['Str2IntKind'][a['name']] = a
                else:
                    datas[i][a['id']] = a
getDataFromDB()
        
#print datas['prescription']
#print datas

#每种士兵类型和层级对应的各个等级的属性系数
stagePool = {}
def getStage(id):
    soldiers = datas.get("soldier")
    data = soldiers.get(id)
    soldierLevel = datas.get("soldierLevel")
    soldierAttBase = datas.get("soldierAttBase")
    soldierGrade = datas.get("soldierGrade")
    soldierKind = datas.get("soldierKind")

    category = soldierKind[data.get("category")]
    grade = soldierGrade[data.get("grade")]
    magic = data.get("kind") == 2
    res = []
    for i in range(0, len(soldierLevel)):
        r = []
        r.append(soldierAttBase[i][0]*category[0]*grade)
        r.append(soldierAttBase[i][1]*category[1]*grade)
        r.append(soldierAttBase[i][2]*category[2]*grade)
        if magic == False:
            r.append(soldierAttBase[i][3]*category[3]*grade)
        else:
            r.append(0)
        if magic == True:
            r.append(soldierAttBase[i][3]*category[3]*grade)
        else:
            r.append(0)
        r = [soldierLevel[i], r]
        res.append(r)
    stagePool[id] = res

#计算所有士兵的stage
def initStage():
    sql = 'select id from soldier'
    con.query(sql)
    res = con.store_result()
    rows = res.fetch_row(0, 1)
    for r in rows:
        getStage(r['id'])
        
initStage()
#print "getStagePool", stagePool

con.close()

#TREASURE_STONE = 15
        


# Global session manager: DBSession() returns the Thread-local
# session object appropriate for the current web request.
maker = sessionmaker(autoflush=True, autocommit=False,
                     extension=ZopeTransactionExtension())
DBSession = scoped_session(maker)

# Base class for all of our model classes: By default, the data model is
# defined with SQLAlchemy's declarative extension, but if you need more
# control, you can switch to the traditional method.
DeclarativeBase = declarative_base()

# There are two convenient ways for you to spare some typing.
# You can have a query property on all your model classes by doing this:
# DeclarativeBase.query = DBSession.query_property()
# Or you can use a session-aware mapper as it was used in TurboGears 1:
# DeclarativeBase = declarative_base(mapper=DBSession.mapper)

# Global metadata.
# The default metadata is the one from the declarative base.
metadata = DeclarativeBase.metadata

# If you have multiple databases with overlapping table names, you'll need a
# metadata for each database. Feel free to rename 'metadata2'.
#metadata2 = MetaData()

#####
# Generally you will not want to define your table's mappers, and data objects
# here in __init__ but will want to create modules them in the model directory
# and import them at the bottom of this file.
#
######

#allCost Data
"""
AllRecommandUsers = None


class RecommandThread(Thread):
    finish = False
    def run(self):
        while not self.finish:
            global AllRecommandUsers
            AllRecommandUsers = DBSession.query(UserRecommand).all()
            time.sleep(24*3600)

thr = RecommandThread()
"""

def init_model(engine):
    """Call me before using any of the tables or classes in the model."""
    DBSession.configure(bind=engine)

    # If you are using reflection to introspect your database and create
    # table objects for you, your tables must be defined and mapped inside
    # the init_model function, so that the engine is available if you
    # use the model outside tg2, you need to make sure this is called before
    # you use the model.

    #
    # See the following example:

    #global t_reflected

    #t_reflected = Table("Reflected", metadata,
    #    autoload=True, autoload_with=engine)

    #mapper(Reflected, t_reflected)
    userInWanTable = Table("UserInWan", metadata, autoload=True, autoload_with=engine)
    mapper(UserInWan, userInWanTable)
    userBuildingsTable = Table("UserBuildings", metadata, autoload=True, autoload_with=engine)
    mapper(UserBuildings, userBuildingsTable)
    userChallengeTable = Table("UserChallenge", metadata, autoload=True, autoload_with=engine)
    mapper(UserChallenge, userChallengeTable)
    userDrugsTable = Table("UserDrugs", metadata, autoload=True, autoload_with=engine)
    mapper(UserDrugs, userDrugsTable)
    userEquipsTable = Table("UserEquips", metadata, autoload=True, autoload_with=engine)
    mapper(UserEquips, userEquipsTable)
    userSoldiersTable = Table("UserSoldiers", metadata, autoload=True, autoload_with=engine)
    mapper(UserSoldiers, userSoldiersTable)

    #userSolEquipTable = Table("UserSolEquip", metadata, autoload=True, autoload_with=engine)
    #mapper(UserSolEquip, userSolEquipTable)
    userHerbTable = Table("UserHerb", metadata, autoload=True, autoload_with=engine)
    mapper(UserHerb, userHerbTable)
    userTaskTable = Table("UserTask", metadata, autoload=True, autoload_with=engine)
    mapper(UserTask, userTaskTable)
    userFriendTable = Table("UserFriend", metadata, autoload=True, autoload_with=engine)
    mapper(UserFriend, userFriendTable)
    userGoodsTable = Table("UserGoods", metadata, autoload=True, autoload_with=engine)
    mapper(UserGoods, userGoodsTable)
    userChallengeRecordTable = Table("UserChallengeRecord", metadata, autoload=True, autoload_with=engine)
    mapper(UserChallengeRecord, userChallengeRecordTable)
    userNewRankTable = Table("UserNewRank", metadata, autoload=True, autoload_with=engine)
    mapper(UserNewRank, userNewRankTable)
    userGroupRankTable = Table("UserGroupRank", metadata, autoload=True, autoload_with=engine)
    mapper(UserGroupRank, userGroupRankTable)
    userChallengeFriendTable = Table("UserChallengeFriend", metadata, autoload=True, autoload_with=engine)
    mapper(UserChallengeFriend, userChallengeFriendTable)
    #userBuyTaskTable = Table("UserBuyTask", metadata, autoload=True, autoload_with=engine)
    #mapper(UserBuyTask, userBuyTaskTable)
    userNeiborTable = Table("UserNeibor", metadata, autoload=True, autoload_with=engine)
    mapper(UserNeibor, userNeiborTable)
    userNeiborRelationTable = Table("UserNeiborRelation", metadata, autoload=True, autoload_with=engine)
    mapper(UserNeiborRelation, userNeiborRelationTable)
    userRecommandTable = Table("UserRecommand", metadata, autoload=True, autoload_with=engine)
    mapper(UserRecommand, userRecommandTable)
    userNeiborRequestTable = Table("UserNeiborRequest", metadata, autoload=True, autoload_with=engine)
    mapper(UserNeiborRequest, userNeiborRequestTable)
    userCrystalMineTable = Table("UserCrystalMine", metadata, autoload=True, autoload_with=engine)
    mapper(UserCrystalMine, userCrystalMineTable)
    userMessageTable = Table("UserMessage", metadata, autoload=True, autoload_with=engine)
    mapper(UserMessage, userMessageTable)
    #one User one Bug at most
    userBugTable = Table("UserBug", metadata, autoload=True, autoload_with=engine)
    mapper(UserBug, userBugTable)

    userGiftTable = Table("UserGift", metadata, autoload=True, autoload_with=engine)
    mapper(UserGift, userGiftTable)
    userSkillsTable = Table("UserSkills", metadata, autoload=True, autoload_with=engine)
    mapper(UserSkills, userSkillsTable)
    userHeartTable = Table("UserHeart", metadata, autoload=True, autoload_with=engine)
    mapper(UserHeart, userHeartTable)
    userFightingTable = Table("UserFighting", metadata, autoload=True, autoload_with=engine)
    mapper(UserFighting, userFightingTable)
    userFightRecordTable = Table("UserFightRecord", metadata, autoload=True, autoload_with=engine)
    mapper(UserFightRecord, userFightRecordTable)
    userAttackTable = Table("UserAttack", metadata, autoload=True, autoload_with=engine)
    mapper(UserAttack, userAttackTable)
    userDefenseTable = Table("UserDefense", metadata, autoload=True, autoload_with=engine)
    mapper(UserDefense, userDefenseTable)

    userUnlockLevelTable = Table("UserUnlockLevel", metadata, autoload=True, autoload_with=engine)
    mapper(UserUnlockLevel, userUnlockLevelTable)

    userTreasureBoxTable = Table("UserTreasureBox", metadata, autoload=True, autoload_with=engine)
    mapper(UserTreasureBox, userTreasureBoxTable)
    userInviteRankTable = Table("UserInviteRank", metadata, autoload=True, autoload_with=engine)
    mapper(UserInviteRank, userInviteRankTable)
    userBuyTaskRecordTable = Table("UserBuyTaskRecord", metadata, autoload=True, autoload_with=engine)
    mapper(UserBuyTaskRecord, userBuyTaskRecordTable)
    GameParamTable = Table("GameParam", metadata, autoload=True, autoload_with=engine)
    mapper(GameParam, GameParamTable)

    #userHeartRankTable = Table("UserHeartRank", metadata, autoload=True, autoload_with=engine)
    #mapper(UserHeartRank, userHeartRankTable)

    #每天更新数据 需要服务器内存数据更新
    #thr.start()


# Import your model modules here.
from wangguo.model.auth import User, Group, Permission
from wangguo.model.userInWan import UserInWan
from wangguo.model.userBuildings import UserBuildings
from wangguo.model.userChallenge import UserChallenge
from wangguo.model.userDrugs import UserDrugs
from wangguo.model.userEquips import UserEquips
from wangguo.model.userSoldiers import UserSoldiers
#from wangguo.model.userSolEquip import UserSolEquip
from wangguo.model.userHerb import UserHerb
from wangguo.model.userTask import UserTask
from wangguo.model.userFriend import UserFriend
from wangguo.model.userGoods import UserGoods
from wangguo.model.userChallengeRecord import UserChallengeRecord
from wangguo.model.userNewRank import UserNewRank
from wangguo.model.userGroupRank import UserGroupRank
from wangguo.model.userChallengeFriend import UserChallengeFriend
#from wangguo.model.userBuyTask import UserBuyTask
from wangguo.model.userNeibor import UserNeibor
from wangguo.model.userNeiborRelation import UserNeiborRelation
from wangguo.model.userRecommand import UserRecommand
from wangguo.model.userNeiborRequest import UserNeiborRequest
from wangguo.model.userCrystalMine import UserCrystalMine
from wangguo.model.userMessage import UserMessage
from wangguo.model.userBug import UserBug
from wangguo.model.userGift import UserGift
from wangguo.model.userSkills import UserSkills
from wangguo.model.userHeart import UserHeart
from wangguo.model.userFighting import UserFighting
from wangguo.model.userFightRecord import UserFightRecord
from wangguo.model.userAttack import UserAttack
from wangguo.model.userDefense import UserDefense
from wangguo.model.userUnlockLevel import UserUnlockLevel
from wangguo.model.userTreasureBox import UserTreasureBox
from wangguo.model.userInviteRank import UserInviteRank
from wangguo.model.userBuyTaskRecord import UserBuyTaskRecord
from wangguo.model.gameParam import GameParam
