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

r = '%slogin/%d/ppp' % (base2, random.randint(10, 100))
l = req(r)

uid = l.get('uid')
sid = random.randint(0, 100)
print uid, sid

r = base+'buySoldier/'+str(uid)+'/'+str(sid)+'/0'
soldier = req(r)

r = base+'setName/'+str(uid)+'/'+str(sid)+'/果果'
name = req(r)

r = base+'useDrugInRound/%d/%d' % (uid, 0)
sell = req(r)

r = base+'useDrug/'+str(uid)+'/'+str(sid)+'/'+str(0)
drug = req(r)

r = base+'useDrug/'+str(uid)+'/'+str(sid)+'/'+str(1)
drug = req(r)

#使用药品复活死亡势必功能
r = base+'useDrug/'+str(uid)+'/'+str(sid)+'/'+str(2)
drug = req(r)

r = base+'useDrug/'+str(uid)+'/'+str(sid)+'/'+str(3)
drug = req(r)

r = base+'useDrug/'+str(uid)+'/'+str(sid)+'/'+str(4)
drug = req(r)

r = base+'useEquip/'+str(uid)+'/'+str(sid)+'/'+str(0)
equip = req(r)

r = base+'unloadThing/%d/%d' % (uid, 0)
unload = req(r)

r = base+'useState/'+str(uid)+'/'+str(sid)
state = req(r)

r = base+'challengeOver/%d/%s/%s/%d/%d/%d' %(uid, str([[sid, 10, 100, 1, 20]]), str([[0, 2], [1, 2]]), 2, 0, 0)
over = req(r)

r = base+'inspireMe/'+str(uid)+'/'+str(sid)+'/'+str(100)
exp = req(r)
 
r = base+'doTransfer/'+str(uid)+'/'+str(sid)+'/'+str(2)
trans = req(r)

r = base+'trainDouble/%d/%d' % (uid, 10)
sell = req(r)

r = base+'trainOver/%d/%s' % (uid, json.dumps([[sid, 10, 10, 0, 4]]))
req(r)

r = base+'game1Over/%d/%d/%d/%d/%d' % (uid, sid, 10, 10, 0)
req(r)

r = base+'game2Over/%d/%d/%d/%d' % (uid, 10, 10, 10)
req(r)

r = base+'sellSoldier/%d/%d' % (uid, sid)
sell = req(r)





