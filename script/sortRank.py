import MySQLdb
import json
import time
#mongoDB
con = None

def sortRank(tableName):

    sql = 'select * from %s order by score' % (tableName)
    con.query(sql)
    res = con.store_result()
    res = res.fetch_row(0, 1)
    oid = 0
    for i in res:
        sql = 'update %s set rank = %d' % (tableName, oid)
        con.query(sql)
        con.commit()
        oid += 1

def main():
    while True:
        con = MySQLdb.connect(host='localhost', db='Wan2', user='root', passwd='badperson3')
        sortRank('UserNewRank')
        sortRank('UserGroupRank')
        con.close()
        time.sleep(100)
main()
    
    
