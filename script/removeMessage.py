#coding:utf8
from config import *

now = getTime()-7*24*3600
sql = 'delete from UserMessage where time < %d' % (now)
myCon.query(sql)

myCon.commit()
myCon.close()
