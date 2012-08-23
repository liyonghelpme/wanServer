#coding:utf8
import MySQLdb
import json
con = MySQLdb.connect(host='localhost', user='root', passwd='badperson3', db='Wan2', charset='utf8')
sql = 'delete from monsterAppear'
con.query(sql)

sql = 'delete from monsterNum'
con.query(sql)

f = open('monsterAppear.txt').readlines()
for l in f:
    l = l.replace('\n', '').split('\t')
    p = {'id':int(l[0]), 'firstNum':int(l[1]), 'level':int(l[4]), 'isBoss':int(l[5])}
    sql = 'insert into monsterAppear values(%d,  %d, %d, %d)' % (p['id'], p['firstNum'], p['level'], p['isBoss'])
    con.query(sql)

f = open('monsterNum.txt').readlines()
for l in f:
    l = l.replace('\n', '').split('\t')
    p = {'id':int(l[0]), 'num':int(l[1])}
    sql = 'insert into monsterNum values(%d,  %d)' % (p['id'], p['num'])
    con.query(sql)

con.commit()
con.close()
