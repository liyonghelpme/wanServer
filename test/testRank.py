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

r = '%slogin/%d/ppp' % (base2, random.randint(10, 100))
l = req(r)

uid = l.get('uid')
print uid

oids = []
#other
for i in range(0, 11):
    r = '%slogin/%d/ppp' % (base2, random.randint(10, 100))
    l = req(r)
    oids.append(l.get('uid')) 

r = base+'getRank/%d/%d/%d' % (uid, 0, 10)
soldier = req(r)

r = base+'challengeOther/%d/%d' % (uid, oids[0])
req(r)

#今天已经挑战过
r = base+'challengeOther/%d/%d' % (uid, oids[0])
req(r)

for i in range(1, 10):
    r = base+'challengeOther/%d/%d' % (uid, oids[i])
    req(r)

r = base+'challengeResult/%d/%d/%d/%s' % (uid, 5, 10, json.dumps([[0, 1, 2, 0, 1]]))
req(r)

