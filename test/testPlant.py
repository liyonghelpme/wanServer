import MySQLdb
import urllib
import json
import sys
import random
con = MySQLdb.connect(host='localhost', db='Wan2', user='root', passwd='badperson3')
base = 'http://localhost:8080/'

def exe(sql):
    print sql
    con.query(sql)
    return con.store_result()

def req(r):
    print r
    q = urllib.urlopen(r)
    s = q.read()
    try:
        l = json.loads(s)
        print l
    except:
        print "error\n"
        sys.stderr.write(r+'\n'+s+'\n')
    return l

r = base+'login/234/ppp'
l = req(r)
uid = l.get("uid")
bid = random.randint(1, 100)

r = base+'buildingC/finishBuild/'+str(uid)+'/'+str(bid)+'/'+str(0)+'/10/10/0'
build = req(r)

r = base+'buildingC/beginPlant/'+str(uid)+'/'+str(bid)+'/0'
plant = req(r)

r = base+'buildingC/harvestPlant/'+str(uid)+'/'+str(bid)
fin = req(r)

sql = 'update UserBuildings set objectTime = 0'
exe(sql)
con.commit()

r = base+'buildingC/harvestPlant/'+str(uid)+'/'+str(bid)
fin = req(r)

r = base+'buildingC/finishPlan/'+str(uid)+'/'+str([[bid, 20, 20, 1]])
plan = req(r)

r = base+'buildingC/sellBuilding/'+str(uid)+'/'+str(bid)
sell = req(r)




