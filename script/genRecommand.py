#coding:utf8
from config import *
import MySQLdb
import json
import time
import pymongo

monCon = pymongo.Connection(host='localhost', port=27017)
monDb = monCon['Rank']
recommandCollect = monDb.UserRecommand

begin = int(time.mktime((2012, 1, 1, 0, 0, 0, 0, 0, 0)))
now = int(time.mktime(time.localtime())) - begin - 3*24*3600
sql = 'select uid, name, level, papayaId from UserInWan where loginTime > %d' % (now)
con.query(sql)

res = con.store_result().fetch_row(0, 1)

sql = 'delete from UserRecommand'
con.query(sql)

key = ['uid', 'name', 'level', 'papayaId']
arr = [ dict([[k,i[k]] for k in key]) for i in res]
recommandCollect.remove()
recommandCollect.insert({'res':arr})

#sql = 'insert into UserRecommand (uid, name, level, papayaId) values (%d, \'%s\', %d, %d)' % (i['uid'], i['name'], i['level'], i['papayaId'])
#con.query(sql)



con.commit()
con.close()

    
    
