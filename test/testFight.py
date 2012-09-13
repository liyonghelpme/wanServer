#coding:utf8
import MySQLdb
import urllib
import json
import sys
import random
from config import *
con = MySQLdb.connect(host='localhost', db='Wan2', user='root', passwd='badperson3')
base = '%sfightC/' % (base2)

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

papaya = random.randint(11000, 12000)
r = '%slogin/%d/ppp' % (base2, papaya)
l = req(r)
uid = l['uid']

r = '%schooseFirstHero/%d/%d/%s' % (base2, uid, 0, 'liyong'+str(papaya))
req(r)

op = random.randint(11000, 12000)
r = '%slogin/%d/ppp' % (base2, op)
l = req(r)
oid = l['uid']

r = '%smakeFighting/%d/%d/%d/%d' % (base, uid, 0, 1, 1)
req(r)

r = '%sgetMyArena/%d' % (base, uid)
req(r)

r= '%sgetArenaNum/%d' % (base, oid)
req(r)

r = '%sgetRandArena/%d/%d/%d' % (base, oid, 0, 1)
req(r)

r = '%sgetArenaRecord/%d' % (base, oid)
req(r)

r = '%sattackArena/%d/%d/%d/%d' % (base, oid, uid, 1, 1)
req(r)

r = '%sattackOver/%d/%d/%s/%d/%d/%d' % (base, oid, uid, "[]", 1, 1, 1)
req(r)

r = '%sgetArenaRecord/%d' % (base, oid)
req(r)

r = '%sgetMyArena/%d' % (base, uid)
req(r)

r= '%sdefenseOther/%d/%d' % (base, uid, oid)
req(r)

r= '%sdefenseOver/%d/%d/%s/%d/%d/%d' % (base, uid, oid, '[]', 1, 1, 1)
req(r)


r = '%sgetMyArena/%d' % (base, uid)
req(r)

r = '%sattackArena/%d/%d/%d/%d' % (base, oid, uid, 1, 1)
req(r)

r = '%sgetMyArena/%d' % (base, uid)
req(r)

r = '%sdefenseTimeOut/%d' % (base, uid)
req(r)

r = '%sgetMyArena/%d' % (base, uid)
req(r)

r = '%sgetAttackRank/%d/%d/%d' % (base, uid, 0, 10)
req(r)

r = '%sgetDefenseRank/%d/%d/%d' % (base, uid, 0, 10)
req(r)

r = '%smakeFighting/%d/%d/%d/%d' % (base, uid, 0, 1, 1)
req(r)
