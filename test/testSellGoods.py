import MySQLdb
import urllib
import json
import sys
import random
from config import *
base = '%s%s/'% (base2, 'goodsC')

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

r = '%slogin/%d/ppp' % (base2, random.randint(100, 300))
l = req(r)

oid = l.get('uid')

r = '%ssellDrug/%d/%d/%d' % (base, uid, 1, 10)
req(r)


r = '%s/sellEquip/%d/%d/%d' % (base, uid, 0, 10)
req(r)
