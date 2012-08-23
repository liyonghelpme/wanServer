#coding:utf8
from genSolStage import *

import MySQLdb
import json
con = MySQLdb.connect(host='localhost', user='root', passwd='badperson3', db='Wan2', charset='utf8')

#怪兽出现的 关卡 和等级
#生成每个关卡怪兽 类型 位置 等级 编号

sql = 'select * from monsterAppear'
#关卡对应---> 怪兽列表
con.query(sql)
res = con.store_result()
res = res.fetch_row(0, 1)
roundMons = dict()
for i in res:
    mons = roundMons.get(i['firstNum'], {'mons': [], 'num':0})
    mons['mons'].append(i)
    roundMons[i['firstNum']] = mons

sql = 'select * from monsterNum'
con.query(sql)
#关卡等级
res = con.store_result()
res = res.fetch_row(0, 1)
for i in res:
    roundMons[i['id']]['num'] = i['num']


sql = 'select * from soldier'
con.query(sql)
res = con.store_result()
res = res.fetch_row(0, 1)
allSoldiers = {}
for i in res:
    allSoldiers[i['id']] = i
    
#print roundMons

def genMonster(big, small):
    #本关卡怪兽 等级 id
    #上关卡怪兽  
    #上上关卡怪兽
    allPossibleMon = [] 
    for i in range(small, small-3, -1):
        nb = big
        ns = i
        #print nb, ns
        if i < 0 and big <= 0:
            break
        if i < 0:
            nb = big-1
            ns = i+7

        allPossibleMon += roundMons[nb*10+ns]['mons']
    #print "allPossibleMon", allPossibleMon

    #totalNum 当前已经生成的数量
    totalNum = roundMons[big*10+small]['num']
    res = []
    state = 0#3 个阶段
    #界定每一个怪兽的类型

    findSol = False
    while True:
        if state == 0:
            snum = 4
            #得到第一个 属于本关卡的boss
            findBoss = False
            boss = None
            for i in allPossibleMon:
                if i['isBoss'] == 1 and i['firstNum'] == big*10+small:
                    findBoss = True
                    boss = i
            if findBoss:
                res.append(dict(boss))
                snum -= 1
            
            #本阶段 士兵个数 平分
            #findSol = False 
            sol = []
            for i in allPossibleMon:
                if i['isBoss'] == 0 and i['firstNum'] == big*10+small:
                    findSol = True
                    sol.append(i)

            if findSol:
                solNum = len(sol)
                eachNum = snum/solNum
                for k in range(0, eachNum):
                    res.append(dict(sol[0]))
                
                #2个士兵 第二个数量 
                leftNum = snum-eachNum
                for k in range(0, leftNum):
                    res.append(dict(sol[1]))

            #下一阶段士兵数量
            state = 1
        elif state == 1:
            if totalNum == 4:
                snum = 0
            if totalNum == 9:
                snum = 5
            elif totalNum == 14:
                snum = 5
            elif totalNum == 19:
                snum = 10
            elif totalNum == 25:
                snum = 10

            sol = []
            cb = big
            cs = small - 1
            if cs < 0:
                cb -= 1
                cs += 7
            for i in allPossibleMon:
                if i['isBoss'] == 0 and i['firstNum'] == cb*10+cs:
                    sol.append(i)
            if len(sol) > 0:
                eachNum = snum/len(sol)
                for k in range(0, eachNum):
                    res.append(dict(sol[0]))
                leftNum = snum - eachNum
                for k in range(0, leftNum):
                    res.append(dict(sol[1]))
            state = 2

        elif state == 2:
            snum = totalNum - len(res)
            sol = []
            cb = big
            cs = small - 2
            if cs < 0:
                cb -= 1
                cs += 7
            for i in allPossibleMon:
                if i['isBoss'] == 0 and i['firstNum'] == cb*10+cs:
                    sol.append(i)
            if len(sol) > 0:
                eachNum = snum/len(sol)
                for k in range(0, eachNum):
                    res.append(dict(sol[0]))
                leftNum = snum-eachNum
                for k in range(0, leftNum):
                    res.append(dict(sol[1]))
            break
    #print res
    #print len(res)
    return res

#生成array 所有怪兽可能 等级 id 

#怪兽详细数据 ---》 生成怪兽的能力值--》怪兽模板--》某个等级编号怪兽

#插入怪兽数据
#比较生命值上限

def cmpBasic(x, y):
    if x['basic']['healthBoundary'] > y['basic']['healthBoundary']:
        return 1
    return -1
    
def sortSol(res):   
    sol = []#按照近战 kind = 0 远程 魔法排序
    other = []
    for i in res:
        if allSoldiers[i['id']]['kind'] == 0:
            sol.append(i)
        else:
            other.append(i)
    #按照生命值 攻击力排序
    for i in sol:
        basic = getBasic(i['id'], i['level'])
        i['basic'] = basic
    sol.sort(cmp=cmpBasic)
    for i in other:
        basic = getBasic(i['id'], i['level'])
        i['basic'] = basic
    other.sort(cmp=cmpBasic)
    sol += other
    #print sol
    return sol

def main():
    allSort = {}
    for i in range(0, 5):
        for j in range(0, 7):
            #genMonster(i*10+j)
            #print i*10+j
            #print roundMons[i*10+j]
            res = genMonster(i, j)
            sol = sortSol(res)
            #print "sortedMonster", sol, len(sol)
            allSort[i*10+j] = sol

    #0 - 5
    #0 - 4
    #print "allSort", allSort
    for s in allSort:
        #same Map Soldiers
        map = set()#x*100+y = 1
        print "allSort", s, allSort[s]
        for sol in allSort[s]:
            sdata = allSoldiers[sol['id']]   
            sx = sdata['sx']
            sy = sdata['sy']
            #print sx, sy

            find = False
            beginX = None
            beginY = None
            for x in range(0, 6):
                for y in range(0, 5):
                    col = False
                    if x+sx > 6 or y+sy > 5:
                        continue
                    for i in range(0, sx):
                        for j in range(0, sy):
                            if ((x+i)*100+y+j) in map:
                                col = True
                                break
                        if col:
                            break
                    if not col:
                        find = True
                        break
                if find:
                    beginX = x
                    beginY = y
                    print beginX, beginY
                    break
            if find:                    
                sol['monX'] = beginX
                sol['monY'] = beginY
                for i in range(0, sx):
                    for j in range(0, sy):
                        map.add((beginX+i)*100+beginY+j)
            #print map
        print "setPosition", allSort[s]
        removed = []
        for sol in allSort[s]:
            if sol.get('monX') != None:
                removed.append(sol)

        allSort[s] = removed
        print allSort[s]
        print len(allSort[s]) 

    sql = 'delete from mapMonster'
    con.query(sql)

    for s in allSort:
        sid = 0
        for sol in allSort[s]:
            #big small id monX monY level sid
            sql = 'insert into mapMonster values(%d, %d, %d, %d, %d, %d, %d)' % (s/10, s%10, sol['id'], sol['monX'], sol['monY'], sol['level'], sid)
            con.query(sql)
            sid += 1

        
                        
        
main()

con.commit()
con.close()
