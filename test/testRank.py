#coding:utf8
import MySQLdb
import urllib
import json
import sys
import random
from config import *
con = MySQLdb.connect(host='localhost', db='Wan2', user='root', passwd='badperson3')
base = '%schallengeC/' % (base2)

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

papaya = random.randint(10, 100)
r = '%slogin/%d/ppp' % (base2, papaya)
l = req(r)

uid = l.get('uid')
print uid

r = '%schooseFirstHero/%d/%d/%s' % (base2, uid, 0, 'hero'+str(papaya))
req(r)

oids = []
#other
OTHER_NUM = 5
for i in range(0, OTHER_NUM):
    r = '%slogin/%d/ppp' % (base2, random.randint(110, 30000))
    l = req(r)
    oids.append(l.get('uid')) 
    r = '%sgetLoginReward/%d/%d/%d' % (base2, l['uid'], 10, 10)
    req(r)

r = base+'getRank/%d/%d/%d' % (uid, 0, 10)
soldier = req(r)

r = base+'challengeOther/%d/%d' % (uid, oids[0])
req(r)

#今天已经挑战过
r = base+'challengeOther/%d/%d' % (uid, oids[0])
req(r)

for i in range(1, OTHER_NUM):
    r = base+'challengeOther/%d/%d' % (uid, oids[i])
    req(r)

r = base+'challengeResult/%d/%d/%d/%s' % (uid, 5, 10, json.dumps([[0, 1, 2, 0, 1]]))
req(r)

r = base+'challengeSelf/%d/%d' % (uid, oids[0])
req(r)

r = base+'enableDif/%d/%d/%d' % (uid, 0, 1)
req(r)
