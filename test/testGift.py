#coding:utf8
import MySQLdb
import urllib
import json
import sys
import random
from config import *
import time
base = '%sgoodsC/' % (base2)

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

papaid = random.randint(300, 400)
r = '%slogin/%d/ppp' % (base2, papaid)
l = req(r)
uid = l.get('uid')
t = l.get('maxGiftId')

papaid = random.randint(100, 200)
r = '%slogin/%d/ppp' % (base2, papaid)
l = req(r)
fid = l.get('uid')

beginTime = [2012, 1, 1, 0, 0, 0, 0, 0, 0]
#t = int(time.mktime(time.localtime())-time.mktime(beginTime))

r = base+'buyEquip/%d/%d/%d' % (uid, 10, 0)
req(r)

r = base+'buyDrug/%d/%d' % (uid, 0)
req(r)

sql = 'insert into UserHerb (uid, kind, num) values (%d, %d, %d)' % (uid, 0, 10)
print sql
con.query(sql)
con.commit()

r = base+'buyTreasureStone/%d/%d' % (uid, 0)
req(r)
#登录返回最大的礼物ID
r = base+'buyMagicStone/%d/%d' % (uid, 0)
req(r)

r = base+'sendEquip/%d/%d/%d/%d' % (uid, fid, 10, t)
req(r)
t += 1

r = base+'sendDrug/%d/%d/%d/%d' % (uid, fid, 0, t)
req(r)
t += 1

r = base+'sendHerb/%d/%d/%d/%d' % (uid, fid, 0, t)
req(r)
t += 1

r = base+'sendTreasureStone/%d/%d/%d/%d' % (uid, fid, 0, t)
req(r)
t += 1

r = base+'sendMagicStone/%d/%d/%d/%d' % (uid, fid, 0, t)
req(r)
t += 1

r = base+'getGift/%d' % (fid)
l = req(r)

l = l['gifts']
for g in l:
    r = base+'receiveGift/%d/%d/%d/%d' % (fid, uid, g[5], 10)
    req(r)


r = base+'getGift/%d' % (fid)
l = req(r)


r = '%slogin/%d/ppp' % (base2, papaid)
l = req(r)
print l['treasure']


con.close()
