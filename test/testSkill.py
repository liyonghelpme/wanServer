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

for i in range(0, 10):
    papayaId = random.randint(5000, 6000);
    r = '%slogin/%d/ppp' % (base2, papayaId)
    l = req(r)
    uid = l.get('uid')
    #print l.get('soldiers')
    #print l['skills']

    r = '%schooseFirstHero/%d/%d/%s' % (base2, uid, 0, 'hero%d' % papayaId)
    req(r)

    r = base2+'getLoginReward/%d/%d/%d' % (uid, 5, 5)
    reward = req(r)

    for sk in range(0, 12):
        r = base+'buySkill/%d/%d/%d' % (uid, 0, sk)
        req(r)

    r = base2+'goodsC/buyMagicStone/%d/%d' % (uid, 0)
    req(r)

    r = base+'upgradeSkill/%d/%d/%d/%d' % (uid, 0, 0, 0)
    req(r)

    r = '%slogin/%d/ppp' % (base2, papayaId)
    l = req(r)
    print l['skills']

    r = base+'giveupSkill/%d/%d/%d' % (uid, 0, 0)
    req(r)

    r = '%slogin/%d/ppp' % (base2, papayaId)
    l = req(r)
    print l['skills']
