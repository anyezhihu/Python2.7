#coding=utf-8

"""
用于爬取电影天堂网站电影的FTP下载链接，写入到同一个文件中
"""

import sys  #用于修改系统字符集
import os   #用于进行目录操作
import time #用于时间操作
import multiprocessing  #用于多进程操作
import urllib2 #用于HTML操作
import re   #用于正则表达式，这里不好使用正则表达式呢
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

#print Get_All_Url(Base_Url="http://www.dytt8.net/",Url_File=None)



from lxml import etree
text = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a>
     </ul>
 </div>
'''
html = etree.HTML(text)
result = etree.tostring(html)
print(result)


