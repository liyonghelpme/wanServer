#coding:utf8
from config import *

sql = 'update UserInWan set addPapayaCryNum = 0, addFriendCryNum = 0, addNeiborCryNum = 0'
myCon.query(sql)

myCon.commit()
myCon.close()
