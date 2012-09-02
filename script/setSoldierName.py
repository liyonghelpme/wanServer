#coding:utf8

from config import *
import MySQLdb
import json
import time


begin = int(time.mktime((2012, 1, 1, 0, 0, 0, 0, 0, 0)))
now = int(time.mktime(time.localtime())) - begin - 3*24*3600
n = ["初级", "中级", "高级", "圣级"]

for i in range(400, 600, 10):
    for j in range(0, 4):
        sql = 'select * from soldier where id = %d' % (i+j)
        con.query(sql)
        res = con.store_result().fetch_row(0, 1)
        sql = 'update soldier set name = \'%s\' where id = %d' % (n[j]+res[0]['name'].encode('utf8'), i+j)
        con.query(sql)

con.commit()
con.close()

    
    
