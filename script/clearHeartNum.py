#coding:utf8
#每周执行一次
from config import *

sql = 'update UserHeart set weekNum = 0'
con.query(sql)

con.commit()
con.close()
