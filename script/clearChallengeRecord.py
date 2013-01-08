#coding:utf8
from config import *

sql = 'delete from UserChallengeRecord'
myCon.query(sql)

myCon.commit()
myCon.close()
