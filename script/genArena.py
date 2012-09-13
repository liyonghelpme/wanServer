#coding:utf8
from config import *
import MySQLdb
import json
import time
import pymongo

monCon = pymongo.Connection(host='localhost', port=27017)
monDb = monCon['Rank']
arenaCollect = monDb.UserArena

sql = 'select * from UserFighting'
con.query(sql)

res = con.store_result().fetch_row(0, 1)

#for i in res:
#    sql = 'select name, level from UserInWan where uid = %d' % (i['uid'])
#    con.query(sql)


key = ['uid', 'name', 'level', 'papayaId']
arr = [ dict([[k,i[k]] for k in key]) for i in res]
recommandCollect.remove()
recommandCollect.insert({'res':arr})

#sql = 'insert into UserRecommand (uid, name, level, papayaId) values (%d, \'%s\', %d, %d)' % (i['uid'], i['name'], i['level'], i['papayaId'])
#con.query(sql)



con.commit()
con.close()

    
    
