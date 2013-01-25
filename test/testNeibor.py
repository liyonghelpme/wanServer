import MySQLdb
import urllib
import json
import sys
import random
from config import *
base = '%sfriendC/' % (base2)

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


papa2 = random.randint(2000, 3000)
r = '%slogin/%d/ppp' % (base2, papa2)
l = req(r)

oid = l.get('uid')
#r = base+'doTask/%d/%d/%d' % (uid, 0, 50)
#task = req(r)

r = base+'sendNeiborRequest/%d/%d' % (oid,  uid)
req(r)

