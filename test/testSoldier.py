#coding:utf8
import MySQLdb
import urllib
import json
import sys
import random
from config import *
con = MySQLdb.connect(host='localhost', db='Wan2', user='root', passwd='badperson3')
base = '%ssoldierC/' % (base2)

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

r = '%slogin/%d/ppp' % (base2, random.randint(6000, 8000))
l = req(r)

uid = l.get('uid')
#sid = random.randint(0, 100)
sid = 0
print uid, sid

#r = base+'buySoldier/'+str(uid)+'/'+str(sid)+'/0'
#soldier = req(r)

#r = base+'setName/'+str(uid)+'/'+str(sid)+'/果果'
#name = req(r)

r = base+'useDrugInRound/%d/%d' % (uid, 1)
sell = req(r)


r = base+'useEquip/'+str(uid)+'/'+str(sid)+'/'+str(0)
equip = req(r)

r = base+'unloadThing/%d/%d' % (uid, 0)
unload = req(r)




 
r = base+'doTransfer/'+str(uid)+'/'+str(sid)+'/%s' % (json.dumps({'gold':2}))
trans = req(r)

r = base+'doAcc/%d/%d/%d/%d' % (uid, sid, 10, 1)
req(r)

r = base+'finishTransfer/'+str(uid)+'/'+str(sid)
req(r)


r = base+'game1Over/%d/%d/%d/%d/%d' % (uid, sid, 10, 10, 0)
req(r)

r = base+'game2Over/%d/%d/%d/%d' % (uid, 10, 10, 10)
req(r)

#r = base+'sellSoldier/%d/%d' % (uid, sid)
#sell = req(r)

r = base+'game4Over/%d/%s' % (uid, json.dumps([[0, 100, 10, 1]]))
req(r)

r = base+'playGame4/%d/%s' % (uid, json.dumps({'gold':10}))
req(r)


r = base+'useEquip/'+str(uid)+'/'+str(sid)+'/'+str(0)
equip = req(r)



sid = 10
sid += 1

sid += 1
