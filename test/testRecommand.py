#coding:utf8
import MySQLdb
import urllib
import json
import sys
import random
from config import *
con = MySQLdb.connect(host='localhost', db='Wan2', user='root', passwd='badperson3')
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

r = '%slogin/%d/ppp' % (base2, random.randint(10, 100))
l = req(r)

uid = l.get('uid')
print uid

r = '%sgetRecommand/%d' % (base, uid)
req(r)
