#coding:utf8
#清理 缓存在 monggodb 中的数据
#重新生成 排名数据  推荐好友数据
import os
#挑战好友记录
print "clearChallengeRecord"
os.system('python clearChallengeRecord.py')
#帮助好友清理士兵状态
print "clearEliminate"
os.system('python clearEliminate.py')
#清理 生成新的推荐好友
print 'genRecommand'
os.system('python genRecommand.py')
#清理 1周的用户信息 可以调整参数
print 'removeMessage'
os.system('python removeMessage.py')
#排序 挑战好友记录
print 'sortRank'
os.system('python sortRank.py')

