#coding:utf8
import time
import pymongo
import MySQLdb
con = pymongo.Connection(host='localhost', port=27017)
db = con['Rank']
collect = db.inviteRank

#爱心榜每周清理一次本周爱心数据 如何清理
#while True:
myCon = MySQLdb.connect(host='localhost', user='root', passwd='badperson3', db='Wan2', charset='utf8')
sql = 'select * from UserInviteRank order by inviteNum  desc'#where weekNum > 0  暂时没有爱心也会排名
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
        arr.append({'uid':r['uid'], 'score':r['inviteNum'], 'rank':rank, 'papayaId':userData['papayaId'], 'name':userData['name'], 'level':userData['level']})
        sql = 'update UserInviteRank set rank = %d where uid = %d' % (rank, r['uid'])
        myCon.query(sql)
        rank += 1
    except:
        pass

myCon.close()

collect.remove()
collect.insert({'res':arr})
print len(arr)
 #   time.sleep(100)
