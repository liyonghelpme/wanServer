
#coding:utf8
from config import *
sql = 'delete from UserChallengeState where uid not in (select uid from UserInWan)'
myCon.query(sql)
sql = 'delete from UserNewRank where uid not in (select uid from UserInWan)'
myCon.query(sql)
sql = 'delete from UserGroupRank where uid not in (select uid from UserInWan)'
myCon.query(sql)

myCon.commit()
myCon.close()
