#coding:utf8
import MySQLdb
import urllib
import json
import sys
import random
from config import *

base = '%schallengeC/' % (base2)
base1 = '%ssoldierC/' % (base2)


for i in xrange(0, 20):
    papaya = random.randint(9000, 10000)
    r = '%slogin/%d/ppp' % (base2, papaya)
    l = req(r)
    uid = l.get('uid')

    r = '%schooseFirstHero/%d/%d/%s/%d' % (base2, uid, 550, 'hero%d' % papaya, 10)
    req(r)

papaya2 = []
papaya2.append(random.randint(10000, 30000))
r = '%slogin/%d/ppp' % (base2, papaya2[0])
l = req(r)
oid = l['uid']




r = base+'challengeOver/%d/%s/%s/%d/%d/%d/%s/%s' %(uid, json.dumps([1]), json.dumps(dict([["gold", 2], ["silver", 2]])), 2, 0, 0, json.dumps([{'eid':20, 'kind':61}]), json.dumps([10]))
over = req(r)

r = base1+"accReliveHero/%d/%d/%d/%s" % (uid, 10, 20, json.dumps({'gold':10}))
req(r)

r = '%slogin/%d/ppp' % (base2, papaya)
l = req(r)
print l['soldiers']['10']

r = base1+'reliveHero/%d/%d' % (uid, 10)
req(r)

r = '%slogin/%d/ppp' % (base2, papaya)
l = req(r)
print l['soldiers']['10']


#def challengeResult(self, uid, fid, reward, score, sols, mid, win, revenge, hero): 
r = base+'challengeResult/%d/%d/%s/%d/%s/%d/1/0/%s' % (uid, oid, json.dumps([]), 10, json.dumps([]), 5, json.dumps([10]))
req(r)


r = base1+"accReliveHero/%d/%d/%d/%s" % (uid, 10, 20, json.dumps({'gold':10}))
req(r)

r = '%slogin/%d/ppp' % (base2, papaya)
l = req(r)
print l['soldiers']['10']

r = base1+'reliveHero/%d/%d' % (uid, 10)
req(r)

r = '%slogin/%d/ppp' % (base2, papaya)
l = req(r)
print l['soldiers']['10']

