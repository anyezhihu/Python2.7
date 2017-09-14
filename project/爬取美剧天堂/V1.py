#coding=utf-8

"""

"""

import urllib2
import re
from bs4 import BeautifulSoup
import chardet

def Crawl_Moudle_Links():
    url="http://m.meijutt.com/"
    Request=urllib2.Request(url)
    response=urllib2.urlopen(Request)
    content=response.read()
    print chardet.detect(content)
    content=content.decode('GB2312')
    return content

soup=BeautifulSoup(Crawl_Moudle_Links(),'html.parser')
print soup.prettify()
print "----------------------------"
dict_module={}
for a in soup.select('div[class="menu"]'):
    # print a.prettify()

    for b in a.find_all('a'):
        print b
        module_name=b.string
        module. b.attrs['href']
        dict_module[]



