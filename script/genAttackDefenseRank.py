#coding:utf8
import time
import pymongo
import MySQLdb
con = pymongo.Connection(host='localhost', port=27017)
db = con['Rank']
attackCollect = db.UserAttack
defenseCollect = db.UserDefense

myCon = MySQLdb.connect(host='localhost', user='root', passwd='badperson3', db='Wan2', charset='utf8')

#uid total suc rank
def sortRank(name):
    sql = 'select * from %s order by suc desc' % (name)
    myCon.query(sql)
    res = myCon.store_result().fetch_row(0, 1)

    #删除旧的排序数据
    arr = []
    rank = 0
    for r in res:   
        sql = 'select papayaId, name, level from UserInWan where uid = %d' % (r['uid'])
        myCon.query(sql)
        try:
            userData = myCon.store_result().fetch_row(0, 1)[0]
            arr.append({'uid':r['uid'], 'suc':r['suc'], 'total':r['total'], 'rank':rank, 'papayaId':userData['papayaId'], 'name':userData['name'], 'level':userData['level']})
            sql = 'update %s set rank = %d where uid = %d' % (name, rank, r['uid'])
            myCon.query(sql)
            rank += 1
        except:
            pass

    db[name].remove()
    db[name].insert({'res':arr})

sortRank('UserAttack')
sortRank('UserDefense')

myCon.commit()
myCon.close()


