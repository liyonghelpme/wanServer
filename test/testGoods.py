import MySQLdb
import urllib
import json
import sys
import random
con = MySQLdb.connect(host='localhost', db='Wan2', user='root', passwd='badperson3')
base = 'http://localhost:8080/goodsC/'

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

r = 'http://localhost:8080/' +'login/%d/ppp' % random.randint(10, 100)
l = req(r)

uid = l.get('uid')
sid = random.randint(0, 100)
print uid, sid

r = base+'buyDrug/%d/%d' % (uid, 0)
drug = req(r)

r = base+'buyEquip/%d/%d' % (uid, 0)
equip = req(r)


