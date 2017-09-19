#coding=utf-8

"""
第一版
不采用模块方式
采用流水账方式
"""

import urllib2
import re
from bs4 import BeautifulSoup
import chardet
import sys
import os
import time
import multiprocessing

begin_time=time.time()

reload(sys)
sys.setdefaultencoding('utf-8')

def has_href_but_no_class(tag):
    return tag.has_attr('href') and not tag.has_attr('class')

Base_Url="http://www.meijutt.com/"
#获取大板块名称及链接
a_Request=urllib2.Request(Base_Url)
a_response=urllib2.urlopen(a_Request)
a_content=a_response.read()
#print chardet.detect(a_content)
#a_content=a_content.decode('GB2312')    #被编码问题搞懵了，上午一直不行，下午就行了
# print a_content
a_soup=BeautifulSoup(a_content,'html.parser')
a_results=a_soup.select('div[class="menuBox"]')

Base_Dir= os.getcwd() + "\\" + "下载".encode('gbk')
if not os.path.exists(Base_Dir):
    os.makedirs(Base_Dir)

a_dict={}
for a_result in a_results:
    # print a_result.prettify()
    for a_link in a_result.find_all('a'):
        if a_link.has_attr('href') and not a_link.has_attr('calss'):
            a_name=str(a_link.string).decode('GB18030').encode('GB18030').replace('/','_')
            a_href=a_link['href']
            a_dict[a_name]=a_href
            a_path= Base_Dir + "\\" + a_name
            if not os.path.exists(a_path):
                os.makedirs(a_path)

def string_is_nextpage(tag):
    if tag.string == "下一页" and not tag.has_attr('class'):
        return tag

TV_dict = {}
# 获取各版块的链接，写入到各自目录下，这里需要使用迭代，必须使用函数了
def Get_Link(start_url,url_file_path):
    print '------------------------------------------------------------------------------------------------------------------------'
    b_link = Base_Url + start_url#获取要爬去的页面的链接
    print b_link
    print '------------------------------------------------------------------------------------------------------------------------'
    b_request = urllib2.Request(b_link)
    b_response = urllib2.urlopen(b_request)
    b_content = b_response.read()
    print b_content.decode("GB18030",'ignore')
    print '------------------------------------------------------------------------------------------------------------------------'
    b_soup = BeautifulSoup(b_content, 'html.parser')
    print b_soup.prettify()
    print '------------------------------------------------------------------------------------------------------------------------'
    b_tv_results=b_soup.find_all('div',class_="cn_box2")#将当前页面的电视剧的链接添加到字典中
    for b_tv_result in b_tv_results:
        # print type(b_tv_result)
        # print b_tv_result.prettify()
        b_tv_links=b_tv_result.find_all('a',attrs={"class":"B font_16"})
        print b_tv_links
        for b_tv_link in b_tv_links:
            b_name=b_tv_link["title"]
            b_url=Base_Url+b_tv_link["href"]
            print b_name,b_url
            TV_dict[b_name]=b_url
            print chardet.detect(str(b_name))
            url_file=open((url_file_path+"\\"+b_name+".txt"),'ab')
            # url_file.write(b_name + "|" + b_url + "\r")
            c_request=urllib2.Request(b_url)
            c_response=urllib2.urlopen(c_request)
            c_content=c_response.read()
            c_soup=BeautifulSoup(c_content,'html.parser')
            c_results = c_soup.find_all('div', class_="down_list")  # 一共有两个，两个内容是一样的
            for c_result in c_results:  # 将链接分别写入到各节目的文件内
                for d_result in c_result.find_all('a', text="迅雷下载"):
                    c_download_link = d_result['href']
                    url_file.write(c_download_link)
            url_file.close()

        print '------------------------------------------------------------------------------------------------------------------------'
    print TV_dict
    print len(TV_dict)

    b_result = b_soup.find(string_is_nextpage)#获取下一页的链接
    if b_result == None:
        pass
    else:
        print b_result
        print 'aaaa'
        b_next_page_url=b_result['href']
        print 'bbbb'
        print b_next_page_url
        Get_Link(b_next_page_url,url_file)
    print "----"




for key,value in a_dict.items():
    print "##############"
    print key
    print chardet.detect(key)
    print "################"
    b_link=value
    b_file_path=Base_Dir+"\\"+key.decode("GB18030").encode("GB18030")
    print b_file_path
    # b_file=open(b_file_path,'ab')
    Get_Link(b_link,b_file_path)
    # b_file.close()
    # break
#     #print b_link
#     b_request=urllib2.Request(b_link)
#     b_response=urllib2.urlopen(b_request)
#     b_content=b_response.read()
#     # print b_content.decode("GB2312")
#     b_soup=BeautifulSoup(b_content,'html.parser')
#     print b_soup.prettify()
#     b_results=b_soup.find_all('div',class_="cn_box2")
#     print "----"
#     print b_results.
#
#     break

#采用多进程进行操作
def Get_TV_link(c_link,c_file):
    c_request=urllib2.Request(c_link)
    c_response=urllib2.urlopen(c_request)
    c_content=c_response.read()

    c_soup=BeautifulSoup(c_content,'html.parser')
    c_results=c_soup.find_all('div',class_="down_list")#一共有两个，两个内容是一样的
    for c_result in c_results:#将链接分别写入到各节目的文件内
        for d_result in c_result.find_all('a',text="迅雷下载"):
            c_download_link=d_result['href']
            c_file.write(c_download_link)

def MultiProcess_download():
    pool=multiprocessing.Pool()#采用进程池
    for url in a_dict:
        pool.apply_async(Get_TV_link,args=(url,))#启动多进程

    pool.close()
    pool.join()

print "总耗时%d秒" %(time.time() - begin_time)




