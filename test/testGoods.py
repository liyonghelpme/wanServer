import MySQLdb
import urllib
import json
import sys
import random
from config import *
base = '%sgoodsC/' % (base2)

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

papaid = random.randint(10, 100)
r = '%slogin/%d/ppp' % (base2, papaid)
l = req(r)

uid = l.get('uid')
sid = random.randint(0, 100)
print uid, sid

r = base+'buyDrug/%d/%d' % (uid, 0)
drug = req(r)

r = base+'buyEquip/%d/%d/%d' % (uid, 2, 0)
equip = req(r)



r = base+'makeDrug/%d/%d' % (uid, 0)
res = req(r)

r = base+'makeEquip/%d/%d/%d' % (uid, 5, 20)
res = req(r)


sql = 'insert into UserHerb (uid, kind, num) values (%d, %d, %d)' % (uid, 0, 10)
print sql
con.query(sql)
sql = 'insert into UserHerb (uid, kind, num) values (%d, %d, %d)' % (uid, 1, 10)
con.query(sql)
sql = 'insert into UserHerb (uid, kind, num) values (%d, %d, %d)' % (uid, 100, 10)
con.query(sql)
sql = 'insert into UserHerb (uid, kind, num) values (%d, %d, %d)' % (uid, 107, 10)
con.query(sql)
con.commit()

r = base+'makeDrug/%d/%d' % (uid, 0)
res = req(r)

r = base+'makeEquip/%d/%d/%d' % (uid, 5, 20)
res = req(r)

r = base+'buyTreasureStone/%d/%d' % (uid, 0)
req(r)

r = base+'buyTreasureStone/%d/%d' % (uid, 0)
req(r)



r = '%slogin/%d/ppp' % (base2, papaid)
l = req(r)
print l['treasure']

r = '%supgradeEquip/%d/%d/%d' % (base, uid, 0, 0)
req(r)

r = '%supgradeEquip/%d/%d/%d' % (base, uid, 0, 0)
req(r)

r = '%supgradeEquip/%d/%d/%d' % (base, uid, 0, 0)
req(r)

r = '%supgradeEquip/%d/%d/%d' % (base, uid, 0, 0)
req(r)

r = base+'buyResource/%d/%d/%d' % (uid, 5, 0)
drug = req(r)

con.close()
