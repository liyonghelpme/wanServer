#coding:utf8
import MySQLdb
import urllib
import json
import sys
import random
from config import *
#con = MySQLdb.connect(host='localhost', db='Wan2', user='root', passwd='badperson3')
base = '%sbuildingC/' % (base2)

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

papa = random.randint(3000, 4000)
r = base2+'login/%d/ppp' % (papa)
l = req(r)
uid = l.get("uid")
bid = random.randint(100, 200)
#购买兵营
r = '%schooseFirstHero/%d/%d/%s' % (base2, uid, 440, 'hero'+str(papa))
req(r)


r = base+'finishBuild/'+str(uid)+'/'+str(bid)+'/'+str(0)+'/10/10/0'
build = req(r)

r = base+'beginPlant/'+str(uid)+'/'+str(bid)+'/0'
plant = req(r)

r = base+'harvestPlant/'+str(uid)+'/'+str(bid)
fin = req(r)
 
r = base+'accPlant/'+str(uid)+'/'+str(bid)+'/1'
fin = req(r)

r = base+'harvestPlant/'+str(uid)+'/'+str(bid)
fin = req(r)

r = base+'finishPlan/'+str(uid)+'/'+str([[bid, 20, 20, 1]])
plan = req(r)

r = base+'sellBuilding/'+str(uid)+'/'+str(bid)+'/100'
sell = req(r)

bid = bid+1
r = base+'finishBuild/%d/%d/%d/%d/%d/%d' % (uid, bid, 224, 0, 0, 0)
req(r)

r = base+'beginWork/%d/%d/%d/%d' % (uid, bid, 7, 0)
req(r)

r = base+'accWork/%d/%d/%d/%d' % (uid, bid, 7, 1)
req(r)

r = base+'finishCall/%d/%d/%d' % (uid, bid, 5)
req(r)


r = base2+'login/%d/ppp' % (papa)
l = req(r)
print l['soldiers']
