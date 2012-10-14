#coding:utf8

#挑战积分榜：
import MySQLdb
import json
import time
import pymongo
#mongoDB
con = None

monCon = pymongo.Connection(host='localhost', port=27017)
monDb = monCon['Rank']
newCollect = monDb.UserNewRank
oldCollect = monDb.UserGroupRank

def sortRank(tableName):
    sql = 'select * from %s order by score' % (tableName)
    con.query(sql)
    res = con.store_result()
    res = res.fetch_row(0, 1)

    rank = 0
    arr = []
    for i in res:
        #sql = 'select name from UserInWan where uid = %d' % (i['uid'])
        #con.query(sql)

        sql = 'select papayaId, name, level from UserInWan where uid = %d' % (i['uid'])
        con.query(sql)
        try:
            userData = con.store_result().fetch_row(0, 1)[0]
            arr.append({'uid':i['uid'], 'score':i['score'], 'rank':rank, 'papayaId':userData['papayaId'], 'name':userData['name'], 'level':userData['level']})
            sql = 'update %s set rank = %d where uid = %d' % (tableName, rank, i['uid'])
            con.query(sql)
            rank += 1
        except:
            pass

    print len(arr)
    monDb[tableName].remove()
    monDb[tableName].insert({'res':arr})
    

def main():
    #while True:
    global con
    con = MySQLdb.connect(host='localhost', db='Wan2', user='root', passwd='badperson3')
    sql = 'delete from UserNewRank where finish = 1'
    con.query(sql)
    con.commit()
    sortRank('UserNewRank')
    sortRank('UserGroupRank')

    con.commit()
    con.close()
    #time.sleep(1000)
main()
    
    
