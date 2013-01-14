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
#保护时间
print 'protectTime', l['challengeState']

uid = l.get('uid')
print uid

#r = '%schooseFirstHero/%d/%d/%s' % (base2, uid, 0, 'hero'+str(papaya))
#req(r)

oids = []
#other
OTHER_NUM = 5
papaya2 = []
for i in range(0, OTHER_NUM):
    papaya2.append(random.randint(10000, 30000))
    r = '%slogin/%d/ppp' % (base2, papaya2[i])
    l = req(r)
    oids.append(l.get('uid')) 
    r = '%sgetLoginReward/%d/%d/%d' % (base2, l['uid'], 10, 10)
    req(r)

r = base+'getRank/%d/%d/%d' % (uid, 0, 10)
soldier = req(r)

r = base+'challengeOther/%d/%d' % (uid, oids[0])
req(r)
print 'protectTime', l['challengeState']

r = base+'clearProtectTime/%d' % (oids[0])
req(r)

r = base+'realChallenge/%d/%d' % (uid, oids[0])
req(r)

r = base+'getRevenge/%d/%d' % (uid, oids[0])
req(r)

r = base+'getRandChallenge/%d' % (uid)
req(r)


#今天已经挑战过20次查看保护状态
mid = 5
for i in xrange(0, 20):
    r = base+'challengeOther/%d/%d' % (uid, oids[0])
    req(r)
    r = base+'challengeResult/%d/%d/%s/%d/%s/%d/1/0' % (uid, oids[0], json.dumps([]), 10, json.dumps([]), mid)
    req(r)

    r = base+'realChallenge/%d/%d' % (uid, oids[0])
    req(r)
    mid += 1

r = '%slogin/%d/ppp' % (base2, papaya2[0])
l = req(r)
#保护时间
print 'now in protect protectTime', l['challengeState']

r = '%sfriendC/getUserMessage/%d' % (base2, oids[0])
msg = req(r)
msg = msg['msg']

r = base+'readChallengeMsg/%d/%s/%s' % (oids[0], json.dumps([[uid, msg[0][5]]]), json.dumps({'silver':10}))
req(r)


r = '%slogin/%d/ppp' % (base2, papaya)
l = req(r)
#保护时间
print 'protectTime', l['challengeState']

r = '%slogin/%d/ppp' % (base2, papaya2[0])
l = req(r)

#保护时间
print 'protectTime', l['challengeState']

for i in range(1, OTHER_NUM):
    r = base+'challengeOther/%d/%d' % (uid, oids[i])
    req(r)

r = base+'challengeResult/%d/%d/%s/%d/%s/%d/1/1' % (uid, oids[1], json.dumps([]), 10, json.dumps([0]), 5)
req(r)
r = '%slogin/%d/ppp' % (base2, papaya2[1])
l = req(r)
#保护时间
print 'fail ones protectTime', l['challengeState']


r = base+'enableDif/%d/%d/%d' % (uid, 0, 1)
req(r)

