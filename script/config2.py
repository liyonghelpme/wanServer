level = [
0, 14, 29, 44, 59, 69, 79
]
#0 1 2  3/ 4
base = [
[33, 20, 20, 13, 0],
[77, 46, 46, 30, 0],
[177, 106, 106, 68, 0],
[409, 245, 245, 158, 0],
[944, 566, 566, 365, 0],
[2178, 1307, 1307, 842, 0],
[5027, 3016, 3016, 1944, 0],
]

kinds = [
]
f = open('kinds.txt', 'r')
line = f.readlines()
id = 0
for l in line:
    l = l.replace('\n', '').split('\t')
    l = [float(k) for k in l]
    #print l
    kinds.append([id, l])
    id += 1
#print kinds
kinds = dict(kinds)
        

grade = dict([
[10, 1.000],
[11, 1.225],
[12, 1.342],
[20, 1.414],
[21, 1.732],
[30, 2.236],
[31, 2.646],
[32, 3.000],
[40, 3.873],
[41, 4.472],
[50, 7.746],
[51, 8.367],
[60, 2.449],
[70, 3.464],
[80, 5.477],
[90, 9.487],
])


