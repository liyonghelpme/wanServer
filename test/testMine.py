import MySQLdb
import urllib
import json
import sys
import random
from config import *
base = '%smineC/' % (base2)

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

r = base+'upgradeMine/%d' % (uid)
drug = req(r)

r = base+'harvest/%d/%d' % (uid, 2)
equip = req(r)



