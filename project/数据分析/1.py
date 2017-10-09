#coding=utf-8

from pandas import Series,DataFrame
import pandas as pd
from collections import Iterable

objs=Series([0,1,2,3,4,5])
print type(objs)
print objs

print type(objs.values)
print objs.values

print type(objs.index)
print objs.index

print objs[3]

print "-"*20

print objs[objs > 3]

print "-"*50

print objs * 2

print '-'*100
print objs *objs

if 2 in objs:
    print "Find 2"

for i in objs.values:
    print i


objs=Series(data=[0,'a','b',2],index=[1,2,3,4])

print objs[3]

print "-"*120

a=['a','b','c','d','e']

objs=Series(a)

print objs

b={1:'a','a':'b'}

objs=Series(b)

print objs

print isinstance(objs,Iterable)

print "-"*200
a={'a':'a','b':'b','c':'c','d':'d'}
b=['a','b','c','d','e']
objs=Series(data=a,index=b)
print objs
print pd.isnull(objs)
print pd.notnull(objs)
print '-'*200
print objs.isnull()
print objs.notnull()

print '-'*500

data_a={'a':'a','b':'b','c':'c','d':'d'}
list_a=['a','b','c','d','e']

objs_a=Series(data=data_a,index=list_a)
print objs_a

data_b={'b':'1b','c':'1c','d':'1d','e':'1e'}
list_b=['a','b','c','d','e']
objs_b=Series(data=data_b,index=list_b)
print objs_b

objs_c=objs_a + objs_b
print objs_c

print "-"*200
print objs_c.name

objs_c.name="xxx"
print objs_c.name
