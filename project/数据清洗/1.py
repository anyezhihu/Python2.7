#coding=utf-8

"""
用来获取维基百科https://en.wikipedia.org/wiki/Python_(programming_language)中的2-gram列表
"""

import urllib2
from bs4 import BeautifulSoup

def ngrams(in_put,n):
    print 'aaa'
    in_put=str(in_put)#需要将BeautifulSoup转换成string
    print type(in_put)
    #print in_put
    print 'bbb'
    input_list=in_put.split(' ')
    output=[]
    for i in range(len(input_list) - n + 1):
        output.append(input_list[i:i+n])
    return output

html="https://en.wikipedia.org/wiki/Python_(programming_language)"
Request=urllib2.Request(html)
content_a=urllib2.urlopen(Request)
bsObj=BeautifulSoup(content_a,'html.parser')#在python2.7中需要指定解析器
print type(bsObj)
content=bsObj.select('div[id="mw-content-text"]')
print len(content)

#print content[0]
result=ngrams(content[0],2)
print result
print ("2-grams count is: "+str(len(result)))

