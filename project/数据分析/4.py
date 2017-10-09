#coding=utf-8

from pandas import DataFrame,Series
import pandas as pd
import numpy as np

data=DataFrame(np.arange(16).reshape((4,4)),index=['Ohio','Colorado','Utah','New York'],columns=['one','two','three','four'])

print data
print '-'*300

print data.drop(['Colorado','Ohio'])

print '-'*300
print data

print '-'*300

print data.drop('two',axis=1)
print '-'*300
print data
print '-'*300
print data.drop(['two','four'],axis=1)
print '-'*300

print data.drop(['Ohio','Utah'],axis=0)