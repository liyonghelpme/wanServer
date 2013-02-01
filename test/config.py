#coding:utf8
import urllib
import sys
import MySQLdb
import json
con = MySQLdb.connect(host='localhost', db='Wan2', user='root', passwd='badperson3')
base2 = 'http://localhost:8100/'

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
