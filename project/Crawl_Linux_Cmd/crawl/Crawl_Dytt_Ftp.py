#coding=utf-8

"""
用于爬取电影天堂网站电影的FTP下载链接，写入到同一个文件中
"""

import sys  #用于修改系统字符集
import os   #用于进行目录操作
import time #用于时间操作
import multiprocessing  #用于多进程操作
import urllib2 #用于HTML操作
import re
from bs4 import BeautifulSoup   #配合正则表达式提取链接
import chardet

"""
分成以下几个模块：
1.获取所有要爬取的链接
"""
print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()

a="中文"
print chardet.detect(a)
def Get_All_Url(Base_Url,Url_File,Max_Retry_Num=10):
    try:
        request=urllib2.Request(Base_Url)
        response=urllib2.urlopen(request)
        content=response.read()
        print type(content)
        print chardet.detect(content)
        #print chardet.detect(content.decode('gbk'))    #chardet.detect()只能侦测str的字符编码
        return content.decode('gb2312').encode('utf-8') #被这里的字符编码搞懵了。
    except urllib2.HTTPError as e:
        print "获取首页信息失败：%s" % e.message
        print "错误代码;%d" % e.code
    finally:
        pass

html=Get_All_Url(Base_Url="http://www.dytt8.net/",Url_File=None)
soup=BeautifulSoup(html,'html.parser')
print soup.prettify()

print '#############################################################################'
for i in soup.find_all('div',id="menu"):
    print type(i)
    print i.prettify()
print '#############################################################################'
for a in i.find_all('a'):
    print a.string









