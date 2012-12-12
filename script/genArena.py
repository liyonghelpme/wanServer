#coding:utf8
from config import *
import MySQLdb
import json
import time
import pymongo

#monCon = pymongo.Connection(host='localhost', port=27017)
#monDb = monCon['Rank']
monDb = db
arenaCollect = monDb.UserArena

sql = 'select * from UserFighting'
myCon.query(sql)

res = myCon.store_result().fetch_row(0, 1)

#for i in res:
#    sql = 'select name, level from UserInWan where uid = %d' % (i['uid'])
#    con.query(sql)


key = ['uid', 'name', 'level', 'papayaId']
arr = [ dict([[k,i[k]] for k in key]) for i in res]
arenaCollect.remove()
arenaCollect.insert({'res':arr})

#sql = 'insert into UserRecommand (uid, name, level, papayaId) values (%d, \'%s\', %d, %d)' % (i['uid'], i['name'], i['level'], i['papayaId'])
#con.query(sql)



myCon.commit()
myCon.close()

    
    
