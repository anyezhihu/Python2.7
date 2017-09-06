#coding=utf-8
#filename='a/b/c'
#filename='／'.join(segment[:255] for segment in filename.split('／'))
#filename='／'.join(segment[:255] for segment in filename.split('／'))
#print filename

"""
import pickle
import pprint
a={'a':'a1','b':'b2','c':'c3'}
file=open(r"C:\Users\Administrator\Desktop\a\1.txt",'wb')
pickle.dump(a,file)
file.close()

b=open(r"C:\Users\Administrator\Desktop\a\1.txt")
c=pickle.load(b)
pprint.pprint(c)
"""

import pymongo
pymongo.MongoClient('localhost',27017)

