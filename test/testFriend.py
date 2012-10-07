import MySQLdb
import urllib
import json
import sys
import random
import time
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


papa = random.randint(1000, 1100)
#papa = 978149
r = '%slogin/%d/ppp' % (base2, papa)
l = req(r)
uid = l['uid']
uInCode = l['inviteCode']

r = '%schooseFirstHero/%d/%d/%s' % (base2, uid, 440, 'hero'+str(papa))
req(r)

#uid = l.get('uid')

r = '%slogin/%d/ppp' % (base2, papa)
l = req(r)

print l['heart']

papa2 = random.randint(1200, 1300)
r = '%slogin/%d/ppp' % (base2, papa2)
l = req(r)

oid = l.get('uid')
otherInCode = l['inviteCode']

r = '%schooseFirstHero/%d/%d/%s' % (base2, oid, 440, 'hero'+str(papa2))
req(r)

r = base+'addNeiborMax/%d/%d' % (uid, 10)
req(r)

r = base+'addNeiborMax/%d/%d' % (oid, 10)
req(r)


r = base+'getMyFriend/%d' % (uid)
task = req(r)


r = base+'addFriend/%d/%s' % (uid, json.dumps([12345, 24567]))
t2 = req(r)


r = base+'getMyFriend/%d' % (uid)
t3 = req(r)


r = base+'getFriend/%d/%d' % (uid, 1132)
t4 = req(r)

r = base+'getRecommand/%d' % (uid)
req(r)

r = base+'getNeibors/%d' % (uid)
req(r)

r = base+'sendNeiborRequest/%d/%d' % (uid, oid)
req(r)

r = base+'getMessage/%d' % (oid)
req(r)

r = base+'refuseNeibor/%d/%d' % (oid, uid)
req(r)

r = base+'sendNeiborRequest/%d/%d' % (oid, uid)
req(r)

r = base+'acceptNeibor/%d/%d' % (uid, oid)
req(r)

r = base+'getMessage/%d' % (uid)
req(r)

r = base+'getNeibors/%d' % (uid)
req(r)

r = base+'getNeibors/%d' % (oid)
req(r)


r = base+'sendHeart/%d/%d' % (uid, oid)
req(r)


r = '%slogin/%d/ppp' % (base2, papa2)
l = req(r)

print l['heart']

r = base+'sendHeart/%d/%d' % (uid, oid)
req(r)

r = base+'getNeibors/%d' % (uid)
req(r)

r = base+'collectHeart/%d' % (oid)
req(r)

r = '%slogin/%d/ppp' % (base2, papa2)
l = req(r)

print l['heart']


r = base+'collectHeart/%d' % (oid)
req(r)

r = base+'getNeibors/%d' % (uid)
req(r)

r = base+'upgradeLoveTree/%d/%d/%d' % (uid, 8, 1)
req(r)



r = base+'challengeNeibor/%d/%d' % (uid, oid)
req(r)

r = base+'challengeNeiborOver/%d/%d/%s/%d' % (uid, oid, str([]), 2)
req(r)

r = base+'removeNeibor/%d/%d' % (uid, oid)
req(r)

r = base+'getNeibors/%d' % (uid)
req(r)

r = base+'getNeibors/%d' % (oid)
req(r)

r = base+'getHeartRank/%d/%d/%d' % (uid, 0, 5)
req(r)

r = base+'getHeartRank/%d/%d/%d' % (uid, 5, 10)
req(r)

r= base+'sendNeiborInviteRequest/%d/%d' % (uid, otherInCode)
req(r)

r= base+'sendNeiborInviteRequest/%d/%d' % (uid, otherInCode)
req(r)
time.sleep(2)

r= base+'sendNeiborInviteRequest/%d/%d' % (oid, uInCode)
req(r)

r= base+'inviteFriend/%d/%d' % (uid, 1234)
req(r)

r= base+'inviteFriend/%d/%d' % (uid, 1234)
req(r)

r = base+'getFriendUpdate/%d' % (1613)
req(r)
