#coding:utf8
import time
import MySQLdb
myCon = MySQLdb.connect(host='localhost', user='root', passwd='badperson3', db='Wan2', charset='utf8')
sql = 'select * from building'
res = myCon.store_result().fetch_row(0, 1)
for i in res:
    if res["people"] > 0:
        k = '人口上限'
    elif res["rate"] > 0:
        k = '产量加倍'
    elif res[""]
        sql = "update building set storeWord = ''"
