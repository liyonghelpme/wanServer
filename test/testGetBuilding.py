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


r = '%sgetBuildingData' % (base2)
req(r)

r = '%sgetTaskData' % (base2)
l = req(r)
data = l['taskData']
k = l['taskKey']
com = []
for d in data:
    t = {}
    for i in xrange(0, len(k)):
        t[k[i]] = d[1][i]
    com.append([d[0], t])
for i in com:
    c = i[1]['commandList']
    for j in c:
        if j.get('tip') != None:
            print j
    
