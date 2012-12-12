#coding:utf8
import time
beginTime = (2012, 1, 1, 0, 0, 0, 0, 0, 0)
bTime = time.mktime(beginTime)
def getTime():
    return int(time.mktime(time.localtime()) - bTime)
import MySQLdb
myCon = MySQLdb.connect(host='localhost', passwd='badperson3', db='Wan2', user='root', charset='utf8')
import pymongo
con = pymongo.Connection(host='localhost', port=27017)
db = con['WanRank']
