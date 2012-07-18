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

con = MySQLdb.connect(host = 'localhost', user='root', passwd='badperson3', db='Wan2', charset='utf8')
cur = con.cursor()

name = ['building','crystal', 'drug', 'equip',  'gold', 'herb', 'levelExp', 'plant', 'prescription', 'silver', 'soldier', 'soldierLevelExp', 'task']

datas = dict()
for i in name:
    sql = 'select * from '+i;#all Data
    con.query(sql)
    res = con.store_result()
    allData = res.fetch_row(0, 1)
    datas[i] = dict()
    for a in allData:
        if i == 'levelExp':
            datas[i] = json.loads(a['exp'])
        else:
            datas[i][a['id']] = a
        
print datas
con.close()

        


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
    userSolEquipTable = Table("UserSolEquip", metadata, autoload=True, autoload_with=engine)
    mapper(UserSolEquip, userSolEquipTable)
    userHerbTable = Table("UserHerb", metadata, autoload=True, autoload_with=engine)
    mapper(UserHerb, userHerbTable)
    userTaskTable = Table("UserTask", metadata, autoload=True, autoload_with=engine)
    mapper(UserTask, userTaskTable)

# Import your model modules here.
from wangguo.model.auth import User, Group, Permission
from wangguo.model.userInWan import UserInWan
from wangguo.model.userBuildings import UserBuildings
from wangguo.model.userChallenge import UserChallenge
from wangguo.model.userDrugs import UserDrugs
from wangguo.model.userEquips import UserEquips
from wangguo.model.userSoldiers import UserSoldiers
from wangguo.model.userSolEquip import UserSolEquip
from wangguo.model.userHerb import UserHerb
from wangguo.model.userTask import UserTask
