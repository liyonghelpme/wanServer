#coding:utf8
import MySQLdb
import urllib
import json
import sys
import random
con = MySQLdb.connect(host='localhost', db='Wan2', user='root', passwd='badperson3')
base = 'http://localhost:8080/soldierC/'

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

r = 'http://localhost:8080/' +'login/%d/ppp' % random.randint(10, 100)
l = req(r)

uid = l.get('uid')
sid = random.randint(0, 100)
print uid, sid

r = base+'buySoldier/'+str(uid)+'/'+str(sid)+'/0'
soldier = req(r)

r = base+'setName/'+str(uid)+'/'+str(sid)+'/果果'
name = req(r)

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

r = base+'useEquip/'+str(uid)+'/'+str(sid)+'/'+str(0)+'/'+str(2)
equip = req(r)

r = base+'unloadThing/%d/%d' % (uid, 2)
unload = req(r)

r = base+'useState/'+str(uid)+'/'+str(sid)
state = req(r)

r = base+'challengeOver/%d/%s/%s/%d/%d/%d' %(uid, str([[sid, 10, 100, 1, 20]]), str([0, 10]), 2, 0, 0)
over = req(r)

r = base+'inspireMe/'+str(uid)+'/'+str(sid)+'/'+str(100)
exp = req(r)
 
r = base+'doTransfer/'+str(uid)+'/'+str(sid)
trans = req(r)

r = base+'sellSoldier/%d/%d' % (uid, sid)
sell = req(r)




