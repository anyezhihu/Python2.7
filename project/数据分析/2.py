#coding=utf-8

from pandas import DataFrame,Series
import pandas as pd
import numpy as np

data={'state':['Ohio','Ohio','Ohio','Nevada','Nevada'],
      'year':[2000,2001,2002,2001,2002],
        'pop':[1.5,1.7,3.6,2.4,2.9]}#采用字典方式导入

frame=DataFrame(data)#行从0开始、列随意

print frame
print '-'*300

frame=DataFrame(data=data,columns=['state','year','pop'])#指定列
print frame
print '-'*300

frame=DataFrame(data=data,index=[1,2,3,4,5],columns=['state','year','pop'])#同时指定行、列
print frame
print '-'*300

frame=DataFrame(data=data,columns=['year','state','pop','debt'],index=['one','two','three','four','five'])#没有内容的列会自动填充NaN，不过如果行没有内容的话就会报错了
print frame
print '-'*300

series=frame.columns
print series
print '-'*300

series=frame['state']
print series
series=frame['pop']
print series
series=frame['year']
print series
series=frame['debt']
print series
print '-'*300

print frame.ix
print frame.ix['three']
print '-'*300

frame['debt']='16.5'
print frame
print '-'*300

frame['debt']=np.arange(5)
print frame
print '-'*300

val=Series(data=[-1.2,-1.5,-1.7,-1.9],index=['two','four','five','six'])
frame['debt']=val
print frame
print '-'*300

frame['eastern']=frame.state=='Ohio'
print frame
print '-'*300

print frame.values
print '*'*300

del frame['eastern']
print frame
print '-'*300

data={'Neveda':{2000:2.4,2002:2.9},
      'Ohio':{2000:1.3,2001:1.5,2002:3.6}}

frame=DataFrame(data=data)
print frame
print '-'*300

print frame.T
print '-'*300

# frame=DataFrame(data=data,index=[2002,2003,2004])
# print frame
# print '-'*300

print frame['Ohio'][:-1]
print frame['Ohio'][2000]
print type(frame['Ohio'])
print frame['Neveda'][:-2]
print '-'*300

frame.index.name='year'
frame.columns.name='state'
print frame
print '-'*300
print frame.values
