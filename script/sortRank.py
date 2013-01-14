#coding:utf8

#挑战积分榜：
import MySQLdb
import json
import time
import pymongo
from config import *
#mongoDB
#con = None
monDb = db
#monCon = pymongo.Connection(host='localhost', port=27017)
#monDb = monCon['Rank']
newCollect = monDb.UserNewRank
oldCollect = monDb.UserGroupRank

def sortRank(tableName):
    sql = 'select * from %s order by score desc' % (tableName)
    myCon.query(sql)
    res = myCon.store_result()
    res = res.fetch_row(0, 1)

    rank = 0
    arr = []
    for i in res:
        #sql = 'select name from UserInWan where uid = %d' % (i['uid'])
        #con.query(sql)

        sql = 'select papayaId, name, level from UserInWan where uid = %d' % (i['uid'])
        myCon.query(sql)
        try:
            userData = myCon.store_result().fetch_row(0, 1)[0]
            arr.append({'uid':i['uid'], 'score':i['score'], 'rank':rank, 'papayaId':userData['papayaId'], 'name':userData['name'], 'level':userData['level']})
            sql = 'update %s set rank = %d where uid = %d' % (tableName, rank, i['uid'])
            myCon.query(sql)
            rank += 1
        except:
            pass

    print len(arr)
    monDb[tableName].remove()
    monDb[tableName].insert({'res':arr})
    

def main():
    #while True:
    global con
    #myCon = MySQLdb.connect(host='localhost', db='Wan2', user='root', passwd='badperson3')
    sql = 'delete from UserNewRank where finish = 1'
    myCon.query(sql)
    myCon.commit()
    sortRank('UserNewRank')
    sortRank('UserGroupRank')

    myCon.commit()
    myCon.close()
    #time.sleep(1000)
main()
    
    
