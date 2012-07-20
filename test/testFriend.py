import MySQLdb
import urllib
import json
import sys
import random
from config import *
"""
con = MySQLdb.connect(host='localhost', db='Wan2', user='root', passwd='badperson3')
base = 'http://localhost:8080/friendC/'
"""
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

r = '%slogin/%d/ppp' % (base2, random.randint(10, 100))
l = req(r)

uid = l.get('uid')
sid = random.randint(0, 100)
print uid, sid

r = base+'getMyFriend/%d' % (uid)
task = req(r)


r = base+'addFriend/%d/%s' % (uid, json.dumps([12345, 24567]))
t2 = req(r)


r = base+'getMyFriend/%d' % (uid)
t3 = req(r)


r = base+'getFriend/%d/%d' % (uid, 1132)
t4 = req(r)
