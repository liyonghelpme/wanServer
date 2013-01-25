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

papa = random.randint(6000, 7000)
r = '%slogin/%d/ppp' % (base2, papa)
l = req(r)
uid = int(l['uid'])
print l['invite']
inviteCode = int(l['invite']['inviteCode'])

papa = random.randint(7000, 8000)
r = '%slogin/%d/ppp' % (base2, papa)
l = req(r)
oid = int(l['uid'])
oInvite = int(l['invite']['inviteCode'])


r = base+'finishInvite/%d/%d' % (uid, inviteCode)
req(r)

r = base+'finishInvite/%d/%d' % (uid, oInvite)
req(r)

r = base+'finishInvite/%d/%d' % (uid, oInvite)
req(r)

r = '%slevelUp/%d/%d/%d/%s' % (base2, oid, 0, 3, '{}')
req(r)

r = base+'finishInvite/%d/%d' % (oid, inviteCode)
req(r)

r = base+'getInviteRank/%d/%d/%d' % (uid, 0, 10)
req(r)

