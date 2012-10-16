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

papa = random.randint(5000, 6000)
r = '%slogin/%d/ppp' % (base2, papa)
l = req(r)

uid = l.get('uid')
sid = random.randint(0, 100)
print uid, sid

r = base+'getBuyTask/%d' % (uid)
task = req(r)

r = base+'finishBuyTask/%d/%d/%s' % (uid, 1, json.dumps({'gold':10}))
req(r)

r = base+'getBuyTask/%d' % (uid)
task = req(r)


r = '%slogin/%d/ppp' % (base2, papa)
l = req(r)

r = base+'synCycleTask/%d/%s' % (uid, json.dumps([1, 2, 3]))
req(r)

r = base+'doCycleTask/%d/%d/%d' % (uid, 1, 2)
req(r)

r = base+'finishCycleTask/%d/%d/%s' % (uid, 1, json.dumps({'gold':10}))
req(r)


r = '%slogin/%d/ppp' % (base2, papa)
l = req(r)

r = base+'synCycleTask/%d/%s' % (uid, json.dumps([1, 2, 3]))
req(r)

r = base+'getDayTask/%d' % (uid)
req(r)

r = base+'finishDayTask/%d/%s' % (uid, json.dumps({'gold':10}))
req(r)
