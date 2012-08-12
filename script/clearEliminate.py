#coding:utf8
from config import *

sql = 'update UserInWan set addFriendCryNum = 0, addNeiborCryNum = 0'
con.query(sql)

con.commit()
con.close()
