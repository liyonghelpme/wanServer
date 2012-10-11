#coding:utf8
from config import *

sql = 'delete from UserChallengeRecord'
con.query(sql)

con.commit()
con.close()
