#coding:utf8
import MySQLdb
import urllib
import json
import sys
import random
from config import *

base = '%slogC/'%(base2)


for i in xrange(0, 5):
    papa = random.randint(19000, 60000)
    r = '%slogin/%d/ppp' % (base2, papa)
    l = req(r)
    uid = l['uid']

    r = '%sfinishNewStage/%d/%d' % (base, uid, random.randint(1, 3))
    req(r)

    r = '%slevelUp/%d/%d/%d/%s' % (base2, uid, 0, random.randint(0, 100), '{}')
    req(r)
    bid = 100
    r = base2+'buildingC/'+'finishBuild/'+str(uid)+'/'+str(bid)+'/'+str(0)+'/10/10/0/1/1/%s' % (json.dumps({"gold":20}))
    build = req(r)


papa = random.randint(19000, 60000)
r = '%slogin/%d/ppp' % (base2, papa)
l = req(r)
uid = l['uid']

r = '%sfinishNewStage/%d/%d' % (base, uid, 3)
req(r)

#设定第二次登录时间
r = '%slogin/%d/ppp' % (base2, papa)
req(r)

r = '%sgetHalfGoldUserLost' % (base)
req(r)

r = "%slostUser" % (base)
req(r)

r = '%stryPay/%d/%d' % (base, uid, 10)
req(r)
r = '%sfinishPay/%d/%d/%s/%d' % (base2, uid, 100, json.dumps({'gold':10}), 10)
req(r)
