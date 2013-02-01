import MySQLdb
import urllib
import json
import sys
import random
from config import *
base = '%smineC/' % (base2)
buildBase = '%sbuildingC/' % (base2)

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

r = '%slogin/%d/ppp' % (base2, random.randint(3000, 4000))
l = req(r)

uid = l.get('uid')
buildings = l["buildings"]
print buildings
mine = None
for i in buildings:
    if buildings[i]['id'] == 300:
        mine = int(i)
        break


r = base+'upgradeMine/%d/%d/%s' % (uid, mine, json.dumps(dict([["silver", 100]])))
req(r)

r = base+'harvest/%d/%d/%s' % (uid, mine, json.dumps({'crystal':10, 'exp':2}))
req(r)

r = buildBase+'finishBuild/%d/%d/%d/%d/%d/%d/%d/%d/%s' % (uid, 20, 300, 50, 50, 0, 1, 1, json.dumps({'gold':10}))
req(r)

mine = 20

#r = base+'finishPlan/'+str(uid)+'/'+str([[bid, 20, 20, 1]])
r = buildBase+'finishPlan/%d/%s' % (uid, json.dumps([[mine, 20, 20, 1]]))
req(r)

r = buildBase+'sellBuilding/%d/%d/%d' % (uid, mine, 20)
req(r)


