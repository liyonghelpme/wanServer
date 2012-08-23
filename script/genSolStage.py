#coding:utf8
import MySQLdb
import json
from config2 import *
#根据数据库的怪兽 的 种类 和 层次 计算 怪兽的stage 并写入到数据库中
#monster的 solOMon
#生命值 魔法防御 物理防御 物理攻击 魔法攻击
#根据士兵类型决定 采用物理攻击还是魔法攻击


#kind solIds
con = MySQLdb.connect(host='localhost', user='root', passwd='badperson3', db='Wan2', charset='utf8')
sql = 'select * from soldier'
con.query(sql)
res = con.store_result()
res = res.fetch_row(0, 1)
#category 种类
#grade 档次

#stage 每个级别
#[[lev, []]]
#更新所有的怪兽的 stage数据
stagePool = {}
#{id:[[lev, [health,  ] ]] }
soldiers = {}
for i in res:
    #if i['solOrMon'] == 0:#士兵
    soldiers[i['id']] = i
    cat = kinds[i['category']]
    gra = grade[i['grade']]
    #kind == 2 魔法攻击
    mag = i['kind'] == 2 
    data = []
    for k in range(0, len(level)):
        d = []
        d.append(int(base[k][0]*cat[0]*gra))
        d.append(int(base[k][1]*cat[1]*gra))
        d.append(int(base[k][2]*cat[2]*gra))
        if mag == False:
            d.append(int(base[k][3]*cat[0]*gra))
        else:
            d.append(0)
        if mag == True:
            d.append(int(base[k][3]*cat[0]*gra))
        else:
            d.append(0)

        d = [level[k], d]
        data.append(d)
    #sql = "update soldier set stage = '"+str(data)+"' where id = "+str(i['id'])
    #print sql
    #con.query(sql)
    stagePool[i['id']] = data

#print stagePool
#print soldiers

#basic ability
def getBasic(id, lev):
    data = soldiers[id] 
    stage = stagePool[id]
    for i in range(1, len(stage)):
        if lev < level[i]:
            break
    begin = stage[i-1]
    end = stage[i]
    levelDiff = end[0]-begin[0]
    
    addHealth = end[1][0]-begin[1][0];
    addMagicDefense = end[1][1]-begin[1][1];
    addPhysicDefense = end[1][2]-begin[1][2];
    addPhysicAttack = end[1][3]-begin[1][3];
    addMagicAttack = end[1][4]-begin[1][4];

    physicAttack = begin[1][3]+(lev-begin[0])*addPhysicAttack/levelDiff; 
    physicDefense = begin[1][2]+(lev-begin[0])*addPhysicDefense/levelDiff; 

    magicAttack = begin[1][4]+(lev-begin[0])*addMagicAttack/levelDiff; 
    magicDefense = begin[1][1]+(lev-begin[0])*addMagicDefense/levelDiff; 

    healthBoundary = begin[1][0]+(lev-begin[0])*addHealth/levelDiff;
    return {'physicAttack':physicAttack, 'physicDefense':physicDefense, 'magicAttack':magicAttack, 'magicDefense':magicDefense, 'healthBoundary':healthBoundary}

def getPhyHurt(cat):
    return kinds[cat][4]
def getMagHurt(cat):
    return kinds[cat][5]
#allId  allLevel ---> basic
count = 0

minExp = 1000000000
maxExp = 0

#0 300 ---> sqrt
allExp = {}

sql = 'delete from allSoldierData'
con.query(sql)

import math
for i in soldiers:
    for j in range(0, 79):
        data = soldiers[i]
        cat = data['category']
        basic = getBasic(data['id'], j)
        pcoff = getPhyHurt(cat)
        mcoff = getMagHurt(cat)
        #pb = basic[4]*basic[0]/pcoff
        #mb = basic[4]*basic[2]/mcoff
        #ab = max(pb, mb)
        #if count % 30 == 0:
        #    print 'id', 'name', 'level', 'phyAtt phyDef magAtt magDef health', 'phyHurt', 'magHurt', 'phyBasic', 'magBasic', 'maxBasic'
        #print data['id'], data['name'].encode('utf8'), j, str(basic).replace('[', '').replace(']', '').replace(',', ''), pcoff, mcoff,  int(pb), int(mb), int(ab)
        #print data, basic, pcoff, mcoff 
        
        sql = 'insert into allSoldierData (id, name, level, physicAttack, physicDefense, magicAttack, magicDefense, healthBoundary, physicHurt, magicHurt) values(%d, \'%s\', %d, %d, %d, %d, %d, %d, %d, %d)' % (data['id'], data['name'].encode('utf8'), j, basic['physicAttack'], basic['physicDefense'], basic['magicAttack'], basic['magicDefense'], basic['healthBoundary'], int(pcoff*100), int(mcoff*100))
        con.query(sql)
        """
        if int(ab) > maxExp:
            maxExp = int(ab)
        if int(ab) < minExp:
            minExp = int(ab)
        count += 1
        exp = int(ab)
        exp = math.sqrt(exp)
        item = int(exp/100*100)
        v = allExp.get(item, 0)
        allExp[item] = v+1
        """

#print maxExp
#print minExp
#print allExp

#val = allExp.items()
#val.sort()
#for i in val:
#    print i[0], i[1] 


            

            

con.commit()
con.close()
