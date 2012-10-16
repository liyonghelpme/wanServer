import MySQLdb
import urllib
import json
import sys
import random
import time
from config import *

base = '%s%s/'% (base2, 'friendC')

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
uid = l['uid']

print l['hasBox'], l['helperList']

r = base+'genNewBox/%d' % (uid)
req(r)

r = base+'getFriend/%d/%d' % (uid, papa)
l = req(r)
print l['hasBox'], l['helperList']

r = base+'helpOpen/%d/%d' % (uid, uid)
req(r)

r = base+'helpOpen/%d/%d' % (uid, uid)
req(r)

r = base+'selfOpen/%d' % (uid)
req(r)

r = '%slogin/%d/ppp' % (base2, papa)
l = req(r)
print l['hasBox'], l['helperList']

r = base+'openBox/%d' %(uid)
req(r)

r = base+'getFriend/%d/%d' % (uid, papa)
l = req(r)
print l['hasBox'], l['helperList']

for i in xrange(0, 9):
    r = base+'selfOpen/%d' % (uid)
    req(r)

r = base+'getFriend/%d/%d' % (uid, papa)
l = req(r)
print l['hasBox'], l['helperList']

r = base+'openBox/%d' %(uid)
req(r)
