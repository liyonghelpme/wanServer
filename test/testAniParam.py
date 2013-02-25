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



r = '%sfetchAnimate' % (base2)
l = req(r)
ani = dict(l['ani'])
sol = dict(l['sol'])
print ani[10060]
print sol[60]
print ani[sol[60][1]]


print "****************************"
print l['pKey']
print l['pData']

r = '%sgetTaskData' % (base2)
req(r)

r = '%sgetStaticData/%s' % (base2, 'building')
req(r)

r = '%sgetStaticData/%s' % (base2, 'mapBlood')
req(r)

r = '%sgetMapMonster'%(base2)
req(r)

r = '%sgetString' % (base2)
req(r)

r = '%supdateCurrentSoldierId/%d'%(base2, 20)
req(r)

r = '%sgetSkillAnimate' % (base2)
req(r)

papa = random.randint(5000, 6000)
r = '%slogin/%d/ppp' % (base2, papa)
l = req(r)
uid = l['uid']

r = '%scheckData/%d/doAcc/%s' % (base2, uid, json.dumps({'gold':10000}))
req(r)
