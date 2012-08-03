import MySQLdb
import urllib
import json
import sys
import random
from config import *
base = '%staskC/' % (base2)

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

r = '%slogin/%d/ppp' % (base2, random.randint(5000, 6000))
l = req(r)

uid = l.get('uid')
sid = random.randint(0, 100)
print uid, sid

r = base+'doTask/%d/%d/%d' % (uid, 0, 50)
task = req(r)

r = base+'finishTask/%d/%d' % (uid, 0)
t2 = req(r)

r= base+'doTask/%d/%d/%d' % (uid, 1, 10)
task = req(r)


r = base+'finishTask/%d/%d' % (uid, 1)
t2 = req(r)



r= base+'doTask/%d/%d/%d' % (uid, 1, 20)
task = req(r)


r = base+'finishTask/%d/%d' % (uid, 1)
t2 = req(r)

r = base+'getBuyTask/%d' % (uid)
req(r)

r = base+'finishBuyTask/%d/%d' % (uid, 0)
req(r)
