#coding:utf8
import MySQLdb
import json
sqlName = ['building','crystal', 'challengeReward', 'drug', 'equip', 'fallThing', 'gold', 'herb', 'levelExp', 'plant', 'prescription', 'silver', 'soldier', 'soldierAttBase', 'soldierGrade', 'soldierKind', 'soldierLevel', 'soldierTransfer', 'Strings', 'task', 'mapDefense', 'mapMonster', 'soldierName', 'mapReward', 'levelDefense', 'mineProduction', 'goodsList', 'equipLevel', 'magicStone', 'skills', 'monsterAppear', 'statusPossible', 'loveTreeHeart', 'heroSkill', 'mapBlood']
con = MySQLdb.connect(host='localhost', user='root', passwd='badperson3', db='Wan2', charset='utf8')

sql = 'select * from prescriptionNum'
con.query(sql)
res = con.store_result().fetch_row(0, 1)
nums = {}
for i in res:
    nums[i['id']] = i

def hanData(name, data):
    names = []
    key = []
    res = []
    f = data.fetch_row(0, 1)
    for i in f:
        i = dict(i)
        if i.get('name') != None and i.get('id') != None:
            i['name'] = name+str(i['id'])
        if i.get('engName') != None:
            i.pop('engName')
        it = list(i.items())
        it = [list(k) for k in it]
        #it[4][1] = 'build'+str(i['id'])
        key = [k[0] for k in it]
        a = [k[1] for k in it]
        if i.get('id') != None:
            res.append([i['id'], a])

    #if name == 'mapBlood':
    #    res = []
    #    for i in f:
    #        res.append()
    if name == 'heroSkill':
        res = []
        for i in f:
            res.append([i['hid'], i['skillId']])
        print 'var', name, '=', 'dict(',json.dumps(res), ');'
        return []


    if name == 'loveTreeHeart':
        res = []
        for i in f:
            res = json.loads(i['num'])
        print 'var', name, '=', json.dumps(res), ';'
        return []
    if name == 'statusPossible':
        res = []
        reward = []
        for i in f:
            res.append([i['id'], i['possible']])
            reward.append([i['id'], [i['gainsilver'], i['gaincrystal'], i['gaingold'], [i['sunflower'], i['sun'], i['flower'], i['star'], i['moon']]] ])
        print 'var', name, '=', json.dumps(res), ';'
        key = ['gainsilver', 'gaincrystal', 'gaingold', 'nums']
        print 'var', name+'Key', '=', json.dumps(key), ';'
        print 'var', name+'Data', '=', 'dict(', json.dumps(reward), ');'
        return []


    #bigId--->monsterId
    if name == 'monsterAppear':
        res = dict()
        for i in f:
            r = res.get(i['firstNum']/10, [])
            r.append(i['id'])
            res[i['firstNum']/10] = r
        res = res.items()
        print 'var', name, '=', 'dict(', json.dumps(res), ');'
        return []

    if name == 'mineProduction':
        res = []
        keys = []
        for i in f:
            res = i.items()
        print 'var', name, '=', 'dict(', json.dumps(res), ');'
        return []
    if name == 'equipLevel':
        for i in f:
            res = json.loads(i['levelCoff'])
        print 'var', name, '=', json.dumps(res), ';'
        return []
    if name == 'levelDefense':
        res = []
        for i in f:
            res.append([i['level'], i['defense']])
        print 'var', name, '=', json.dumps(res), ';'
        return []
    
    if name == 'mapReward':
        res = []
        for i in f:
            res.append([i['id'], json.loads(i['reward'])])
        print 'var', name, '=', 'dict(', json.dumps(res), ');'
        return []

            
    if name == 'soldierName':
        res = []
        id = 0
        names = []
        for i in f:
            res.append(['name'+str(id), i['maleOrFemale']])
            names.append(['name'+str(id), [i['name'], i['engName']]])
            id += 1
        #print 'var', name, '=', json.dumps(res), ';'
        #return names
        print 'var', 'SolNames', '=', 'dict(['
        for n in names:
            #n[1][0] = n[1][0].encode('utf8')
            #print json.dumps(n)
            #print '[', json.dumps(n[0]), ',','["'+n[1][0]+'",',  '"'+n[1][1]+'"]','],'
            print '[','"'+n[0]+'"', ',', '['+'"'+ n[1][0].encode('utf8') + '", "'+ n[1][1].encode('utf8')+'"]'+'],'
        print ']);'
        return []
    if name == 'challengeReward':
        for i in f:
            res = json.loads(i['reward'])
        print 'var', name, '=', json.dumps(res), ';'
        return []

    if name == 'soldierTransfer':
        res = []
        for i in f:
            res = json.loads(i['level'])
        print 'var', name, '=', json.dumps(res), ';'
        return []
    if name == 'soldierAttBase':
        res = []
        for i in f:
            res = json.loads(i['base'])
        print 'var', name, '=', json.dumps(res), ';'
        return []
    if name == 'soldierGrade':
        res = []
        for i in f:
            res.append([i['id'], int(i['level']*100)])
        print 'var', name, '=', 'dict(', json.dumps(res), ');'
        return []
    if name == 'soldierKind':
        res = []
        for i in f:
            i['attribute'] = [int(at*100) for at in json.loads(i['attribute'])]
            res.append([i['id'], i['attribute']])

        print 'var', name, '=', 'dict(', json.dumps(res), ');'
        return []
    if name == 'soldierLevel':
        res = []
        for i in f:
            res = json.loads(i['levelData'])
        print 'var', name, '=', json.dumps(res), ';'
        return []
        

    if name == 'mapDefense':
        res = []
        for i in f:
            res.append([i['id'], i['defense']])
        print 'var', name, '=', 'dict(', json.dumps(res), ');'
        return []
            

    if name == 'levelExp':
        res = []
        for i in f:
            res = json.loads(i['exp'])
        print 'var', name, '=', json.dumps(res), ';'
        return [] 
     
    if name == 'mapMonster':#大地图 小关的怪兽位置 类型 等级
        res = {}
        key = []
        for i in f:
            k = i['big']*10+i['small']
            mons = res.get(k, [])
            i.pop('big')
            i.pop('small')
            key = i.keys()
            it = i.values()
            mons.append(it)
            res[k] = mons
        res = res.items()
        print 'var', name+'Key', '=', json.dumps(key), ';'
        print 'var', name+'Data', '=', 'dict(', json.dumps(res), ');'
        return []
    if name == 'soldierLevelExp':
        res = []
        for i in f:
            i = dict(i)
            res.append([i['id'], json.loads(i['exp'])])
        print 'var', name, '=', 'dict(', json.dumps(res), ');'
        return []

    #名字 描述desc
    if name == 'drug' or name == 'equip' or name == 'skills':
        res = []
        keys = []
        names = []
        for i in f:
            i = dict(i)
            i['name'] = name+str(i['id'])
            i['des'] = name+'Des'+str(i['id'])
            i.pop('engName')
            it = list(i.items())
            it = [list(k) for k in it]
            key = [k[0] for k in it]
            a = [k[1] for k in it]
            res.append([i['id'], a])

        names = [[name+str(i['id']), [i['name'], i['engName']]] for i in f]
        names += [[name+'Des'+str(i['id']), i['des']] for i in f ]
        print 'var', name+'Key', '=', json.dumps(key), ';'
        print 'var', name+'Data', '=', 'dict(', json.dumps(res), ');'
        return names

    #if name == 'skills':
         
    if name == 'magicStone':
        res = []
        keys = []
        names = []
        for i in f:
            i = dict(i)
            i['name'] = name+str(i['id'])
            i['des'] = name+'Des'+str(i['id'])
            i.pop('engName')
            i.pop('pos0')
            i.pop('pos14')
            i.pop('pos29')
            i.pop('pos44')
            i.pop('pos59')
            i['possible'] = json.loads(i['possible'])
            it = list(i.items())
            it = [list(k) for k in it]
            key = [k[0] for k in it]
            a = [k[1] for k in it]
            res.append([i['id'], a])

        names = [[name+str(i['id']), [i['name'], i['engName']]] for i in f]
        names += [[name+'Des'+str(i['id']), i['des']] for i in f ]
        print 'var', name+'Key', '=', json.dumps(key), ';'
        print 'var', name+'Data', '=', 'dict(', json.dumps(res), ');'
        return names

    if name == 'goodsList':
        res = []
        keys = []
        names = []
        for i in f:
            i = dict(i)
            i['name'] = name+str(i['id'])
            i['des'] = name+'Des'+str(i['id'])
            i.pop('engName')
            i.pop('maxFail')
            i.pop('minFail')
            i.pop('maxBreak')
            i.pop('minBreak')
            i['possible'] = json.loads(i['possible'])

            it = list(i.items())
            it = [list(k) for k in it]
            key = [k[0] for k in it]
            a = [k[1] for k in it]
            res.append([i['id'], a])

        names = [[name+str(i['id']), [i['name'], i['engName']]] for i in f]
        names += [[name+'Des'+str(i['id']), i['des']] for i in f ]
        print 'var', name+'Key', '=', json.dumps(key), ';'
        print 'var', name+'Data', '=', 'dict(', json.dumps(res), ');'
        return names
        
        
    if name == 'herb':#药材中 描述
        res = []
        key = []
        for i in f:
            i = dict(i)
            i['name'] = 'herb'+str(i['id'])
            i['des'] = 'herbDes'+str(i['id'])
            i.pop('engName')
            it = list(i.items())
            it = [list(k) for k in it]
            #it[4][1] = 'build'+str(i['id'])
            key = [k[0] for k in it]
            a = [k[1] for k in it]
            res.append([i['id'], a])
        names = [['herb'+str(i['id']), [i['name'], i['engName']]] for i in f]
        names += [ ['herbDes'+str(i['id']), i['des']] for i in f]
        print 'var', name+'Key', '=', json.dumps(key), ';'
        print 'var', name+'Data', '=', 'dict(', json.dumps(res), ');'
        return names
            

    if name == 'prescription':
        drugId = []
        equipId = []
        res = []
        key = ['id', 'kind', 'level', 'tid', 'needs']
        for i in f:
            i = dict(i)
            needs = []
            numId = i['numId']
            r = nums[numId]
            i['num1'] = r['xNum']
            i['num2'] = r['yNum']
            i['num3'] = r['zNum']
            if i['num1'] != 0:
                needs.append([i['id1'], i['num1']])
            if i['num2'] != 0:
                needs.append([i['id2'], i['num2']])
            if i['num3'] != 0:
                needs.append([i['id3'], i['num3']])
            res.append([i['id'], [i['id'], i['kind'], i['level'], i['tid'], needs]])
            if i['kind'] == 2:
                drugId.append(i['id'])
            else:
                equipId.append(i['id'])
        print 'var', 'PRE_DRUG_ID', '=', json.dumps(drugId), ';'
        print 'var', 'PRE_EQUIP_ID', '=', json.dumps(equipId), ';'

    if name == 'smallMapInfo':
        res = []
        key = ['rewards']
        for i in f:
            i = dict(i)
            rewards = []
            if i['reward0Pos'] > 0:
                rewards.append([i['reward0'], i['reward0Pos']])
            if i['reward1Pos'] > 0:
                rewards.append([i['reward1'], i['reward1Pos']])
            res.append([i['id'], rewards])

    if name == 'Strings':
        res = []

        names = []
        for i in f:
            i = dict(i)
            res.append([i['key'], [i['chinese'], i['english']]])
            names.append([i['key'], [i['chinese'], i['english']]])

        return names

    
    #name list [name, [chinese, english]]
    #res key key = [k[0] for k in it]
    #res data data = [ [id, [k[1] for k in it]] ]
    if name == 'soldier':
        res = []
        key = []
        for i in f:
            i = dict(i)
            #i['stage'] = json.loads(i['stage'])
            i['name'] = 'soldier' + str(i['id'])
            i.pop('engName')
            it = list(i.items())
            it = [list(k) for k in it]
            a = [k[1] for k in it]
            key = [k[0] for k in it]
            res.append([i['id'], a])

        names = [['soldier'+str(i['id']), [i['name'], i['engName']]] for i in f]
        print 'var', name+'Key', '=', json.dumps(key), ';'
        print 'var', name+'Data', '=', 'dict(', json.dumps(res), ');'
        return names 

    if name == 'task':#任务的title 和desc 引用字符串中的titleid desid
        for i in f:
            i = dict(i)
            i['title'] = 'title'+str(i['id'])
            i['des'] = 'des'+str(i['id'])
            i['accArray'] = json.loads(i['accArray'])
            it = list(i.items())
            it = [list(k) for k in it]
            key = [k[0] for k in it]
            a = [k[1] for k in it]
            res.append([i['id'], a])
        names = [['title'+str(i['id']), i['title']] for i in f]
        names += [ ['des'+str(i['id']), i['des']] for i in f]
        print 'var', name+'Key', '=', json.dumps(key), ';'
        print 'var', name+'Data', '=', 'dict(', json.dumps(res), ');'
        return names

            
            

    if f[0].get('name', None) != None:
        if f[0].get('engName') != None:
            names = [ [name+str(i['id']), [i['name'], i.get('engName')]] for i in f]
        else:
            names = [ [name+str(i['id']), i['name']] for i in f]
            
    else:
        names = []


    #print json.dumps(names)
    #for n in names:
    #    print '[','"'+n[0]+'"', ',','"'+ n[1]+'"','],'

    print 'var', name+'Key', '=', json.dumps(key), ';'
    print 'var', name+'Data', '=', 'dict(', json.dumps(res), ');'
    return names
        
allNames = []
for i in sqlName:
    sql = 'select * from '+i
    con.query(sql)
    res = con.store_result()
    allNames += hanData(i, res)
        

SOL = 7
EQUIP = 1
BUILD = 0

levels = {}
sql = 'select * from soldier'
con.query(sql)
res = con.store_result().fetch_row(0, 1)

for i in res:
    if i['id']%10 == 0:
        l = levels.get(i['level'], [])
        l.append([SOL, i])
        levels[i['level']] = l

sql = 'select * from equip'
con.query(sql)
res = con.store_result().fetch_row(0, 1)

for i in res:
    l = levels.get(i['level'], [])
    l.append([EQUIP, i])
    levels[i['level']] = l

sql = 'select * from building'
con.query(sql)
res = con.store_result().fetch_row(0, 1)

for i in res:
    if i['funcs'] == 2:
        l = levels.get(i['level'], [])
        l.append([BUILD, i])
        levels[i['level']] = l
#old = levels
res = []

levels = levels.items()
levels.sort()
maxLevel = levels[-1][0]
for l in levels:
    #print l[0]
    #for i in l[1]:
    #    print i[1]['name'].encode('utf8')

    res.append([l[0], [[i[0], i[1]['id']] for i in l[1]]])

import json
print 'var', 'levelUpdate', '=', 'dict(' ,json.dumps(res), ');'
print 'const', 'MAX_LEVEL', '=', maxLevel, ';'


#商店士兵 类型只有 初级士兵 和 怪兽
sql = 'select * from soldier order by level'
con.query(sql)
res = con.store_result().fetch_row(0, 1)
showId = []
for r in res:
    if r['id'] % 10 == 0 and r['isHero'] == 0:
        showId.append(r['id'])

print 'var', 'storeSoldier', '=', json.dumps(showId), ';'
    




print 'var', 'strings = dict(['
for n in allNames:
    if type(n[1]) == type([]):
        print '[','"'+n[0]+'"', ',', '['+'"'+ n[1][0].encode('utf8') + '", "'+ n[1][1].encode('utf8')+'"]'+'],'
    else:
        print '[','"'+n[0]+'"', ',','"'+ n[1].encode('utf8')+'"','],'
print ']);'


