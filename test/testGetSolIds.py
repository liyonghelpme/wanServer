import MySQLdb
import urllib
import json
import sys
import random
from config import *
#con = MySQLdb.connect(host='localhost', db='Wan2', user='root', passwd='badperson3')
base = '%s'%(base2)

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
        return l
    except:
        print "error\n"
        sys.stderr.write(r+'\n'+s+'\n')


r = '%sgetAllSolIds' % (base2)
req(r)

r = '%ssetTested/%s' % (base2, json.dumps([0, 1, 2]))
req(r)

r = '%sgetAllSolIds' % (base2)
req(r)
