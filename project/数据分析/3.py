#coding=utf-8

from pandas import DataFrame,Series
import pandas as pd
import numpy as np
obj=Series(data=range(3),index=['a','b','c'])
print obj
print '-'*300
index=obj.index
print index
print '-'*300
# index[0]='d'
index=pd.Index(np.arange(3))
print index
print '-'*300

obj2=Series([1.5,-2.5,0],index=[0,1,2])
print obj2

print index is obj2.index
print '-'*300

obj=Series(data=[4.5,7.2,-5.3,3.6],index=['d','b','a','c'])
print obj
print '-'*300
print obj.reindex(index=['a','b','c','d','e'])
print '-'*300

print obj.reindex(index=['a','b','c','d','e'],fill_value=0)
print '-'*300

obj3=Series(data=['blue','purple','yellow'],index=[0,2,4])
print obj3.reindex(range(6),method='ffill')
print '-'*300
print obj3.reindex(range(6),method='bfill')

print '-'*300
frame=DataFrame(np.arange(9).reshape((3,3)),index=['a','c','d'],columns=['Ohio',"Texas",'California'])
print frame

print DataFrame(data=np.arange(9).reshape((3,3)),index=['a','b','c'],columns=['d','e','f'])




































