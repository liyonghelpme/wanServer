#coding:utf8
import os
import sys
import re
#查找字符串
s = sys.argv[1]
print s
pat = re.compile(s)

from os import path
def walkThrough(cur):
    f = os.listdir(cur)
    for i in f:
        n = path.join(cur, i)
        if path.isdir(n):
            walkThrough(n)
        elif n.find('py') != -1 and n.find('swp') == -1 and n.find('pyc') == -1:
            li = open(n).readlines()
            for p in li:
                #if p.find(s) != -1:
                if pat.search(p) != None:
                    print n
                    print p

walkThrough('.')

