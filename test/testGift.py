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

r = base+'buyEquip/%d/%d/%d' % (uid, 10, 1)
req(r)

r = base+'buyDrug/%d/%d' % (uid, 1)
req(r)

sql = 'insert into UserHerb (uid, kind, num) values (%d, %d, %d)' % (uid, 0, 10)
print sql
con.query(sql)
con.commit()

r = base+'sendEquip/%d/%d/%d/%d' % (uid, fid, 10, t)
req(r)
t += 1

r = base+'sendDrug/%d/%d/%d/%d' % (uid, fid, 1, t)
req(r)
t += 1

t += 1

t += 1

t += 1

r = base+'getGift/%d' % (fid)
l = req(r)

l = l['gifts']
for g in l:
    r = base+'receiveGift/%d/%d/%d/%d' % (fid, uid, g[6], 10)
    req(r)


r = base+'getGift/%d' % (fid)
l = req(r)


r = '%slogin/%d/ppp' % (base2, papaid)
l = req(r)
print l['treasure']


con.close()
