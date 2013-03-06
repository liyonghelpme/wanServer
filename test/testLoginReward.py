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
    except:
        print "error\n"
        sys.stderr.write(r+'\n'+s+'\n')
    return l

papaya = random.randint(10000, 20000)
r = '%slogin/%d/ppp' % (base2, papaya)
l = req(r)



uid = l.get('uid')
#sid = random.randint(0, 100)
print uid

#r = '%schooseFirstHero/%d/%d/%s' % (base2, uid, 0, 'test11')
#req(r)

r = '%sfinishNewStory/%d' % (base2, uid)
req(r)

#r = '%schooseFirstHero/%d/%d/%s/%d' % (base2, uid, 440, 'hero'+str(papaya), 2)
#req(r)


r = '%slogin/%d/ppp' % (base2, papaya)
l = req(r)


r = base+'getLoginReward/%d/%s' % (uid, json.dumps({'gold':10}))
reward = req(r)


r = base+'getStars/%d' % (uid)
req(r)


r = '%slogin/%d/ppp' % (base2, papaya)
print l['lastWeek'], l['thisWeek']

r = '%slevelUp/%d/%d/%d/%s' % (base2, uid, 0, 2, '{}')
req(r)

r = '%sfinishPay/%d/%d/%s/%d' % (base2, uid, 0, json.dumps({'gold':10}), 1)
req(r)

r = '%sdownloadFinish/%d/%s' % (base2, uid, json.dumps({'gold':10}))
req(r)


r = '%slogin/%d/ppp' % (base2, papaya)
l = req(r)
