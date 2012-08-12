#coding:utf8
from config import *
import MySQLdb
import json
import time


begin = int(time.mktime((2012, 1, 1, 0, 0, 0, 0, 0, 0)))
now = int(time.mktime(time.localtime())) - begin - 3*24*3600
sql = 'select uid, name, level, papayaId from UserInWan where loginTime > %d' % (now)
con.query(sql)

res = con.store_result().fetch_row(0, 1)

sql = 'delete from UserRecommand'
con.query(sql)

for i in res:
    sql = 'insert into UserRecommand (uid, name, level, papayaId) values (%d, \'%s\', %d, %d)' % (i['uid'], i['name'], i['level'], i['papayaId'])
    con.query(sql)


con.commit()
con.close()

    
    
