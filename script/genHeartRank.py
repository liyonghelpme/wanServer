#coding:utf8
import time
import pymongo
import MySQLdb
con = pymongo.Connection(host='localhost', port=27017)
db = con['Rank']
collect = db.heartRank

while True:
    myCon = MySQLdb.connect(host='localhost', user='root', passwd='badperson3', db='Wan2', charset='utf8')
    sql = 'select * from UserHeart where weekNum > 0 order by weekNum desc'
    myCon.query(sql)
    res = myCon.store_result().fetch_row(0, 1)
    
    #删除旧的排序数据

    arr = []
    rank = 0
    for r in res:   
        sql = 'select papayaId, name from UserInWan where uid = %d' % (r['uid'])
        myCon.query(sql)

        try:
            userData = myCon.store_result().fetch_row(0, 1)[0]
            arr.append({'uid':r['uid'], 'score':r['weekNum'], 'rank':rank, 'papayaId':userData['papayaId'], 'name':userData['name']})
            sql = 'update UserHeart set rank = %d where uid = %d' % (rank, r['uid'])
            myCon.query(sql)
            rank += 1
        except:
            pass

    myCon.close()

    db.heartRank.remove()
    db.heartRank.insert({'res':arr})
    time.sleep(100)
