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

#定义beautiful的查找方法
def has_href_but_no_class(tag):
    return tag.has_attr('href') and not tag.has_attr('class')
#定义beautiful的查找方法
def string_is_nextpage(tag):
    if tag.string == "下一页" and not tag.has_attr('class'):
        return tag

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

#定义多进程下载模块
def MultiProcess_download(b_url,url_file):
    pool=multiprocessing.Pool()#采用进程池
    for url in a_dict:
        pool.apply_async(Muliti_Retry,args=(b_url,url_file))#启动多进程
    pool.close()
    pool.join()

#解決可能出現的网络问题
def Muliti_Retry(b_url,url_file,max_times=10,sleep_time=2,current_excute_time=0):
    try:
        c_request = urllib2.Request(b_url)
        c_response = urllib2.urlopen(c_request)
        c_content = c_response.read()
        c_soup = BeautifulSoup(c_content, 'html.parser')
        c_results = c_soup.find_all('div', class_="down_list")  # 一共有两个，两个内容是一样的
        for c_result in c_results:  # 将链接分别写入到各节目的文件内
            for d_result in c_result.find_all('a'):
                c_download_link = d_result['href']
                url_file.write(c_download_link+'\n')
        url_file.close()
    except urllib2.HTTPError as e:
        current_excute_time= current_excute_time + 1
        print "下载失败，失败原因：%s" % e.reason
        print "HTTP错误代码：%s" % e.code
        if max_times > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                print "进行第%d次重试" % current_excute_time
                time.sleep(sleep_time)
                return Muliti_Retry(b_url,url_file,max_times = max_times - 1)




print "开始"
Base_Url="http://www.meijutt.com/"
#获取大板块名称及链接
a_Request=urllib2.Request(Base_Url)
a_response=urllib2.urlopen(a_Request)
a_content=a_response.read()
print "a"
a_soup=BeautifulSoup(a_content,'html.parser')
a_results=a_soup.select('div[class="menuBox"]')

print chardet.detect(os.getcwd())
print "b"
Base_Dir= os.getcwd().decode('gbk').encode('gbk') + "\\" + "下载".encode('gbk')
if not os.path.exists(Base_Dir):
    os.makedirs(Base_Dir)
print chardet.detect(Base_Dir)
print "c"
a_dict={}
for a_result in a_results:
    # print a_result.prettify()
    for a_link in a_result.find_all('a'):
        if a_link.has_attr('href') and not a_link.has_attr('class'):
            sss=str(a_link.string)
            print type(sss)
            print chardet.detect(sss)
            print sss
            print 'd'
            a_name=str(a_link.string).replace('/','_')
            a_href=a_link['href']
            a_dict[a_name]=a_href
            a_path= Base_Dir + "\\" + a_name.encode('GB2312')
            print type(a_path)
            print chardet.detect(a_path)
            if not os.path.exists(a_path):
                os.makedirs(a_path)

print "e"
TV_dict = {}
# 获取各版块的链接，写入到各自目录下，这里需要使用迭代，必须使用函数了
def Get_Link(start_url,url_file_path):
    print '------------------------------------------------------------------------------------------------------------------------'
    b_link = Base_Url + start_url#获取要爬去的页面的链接
    # print b_link
    # print '------------------------------------------------------------------------------------------------------------------------'
    b_request = urllib2.Request(b_link)
    b_response = urllib2.urlopen(b_request)
    b_content = b_response.read()
    # print b_content.encode("gbk",'ignore')
    # print '------------------------------------------------------------------------------------------------------------------------'
    b_soup = BeautifulSoup(b_content, 'html.parser')
    # print b_soup.prettify()
    # print '------------------------------------------------------------------------------------------------------------------------'
    b_tv_results=b_soup.find_all('div',class_="cn_box2")#将当前页面的电视剧的链接添加到字典中
    for b_tv_result in b_tv_results:
        # print type(b_tv_result)
        # print b_tv_result.prettify()
        b_tv_links=b_tv_result.find_all('a',attrs={"class":"B font_16"})
        # print b_tv_links

        for b_tv_link in b_tv_links:
            b_name=str(b_tv_link["title"])
            b_url=Base_Url+b_tv_link["href"]
            print b_name,b_url
            TV_dict[b_name]=b_url
            print '12f'
            print chardet.detect(url_file_path)
            print chardet.detect(str(b_name).encode('GB2312').replace('/','_'))
            url_file_op=url_file_path+"\\"+b_name.encode('GB2312','ignore').replace('/','_')+".txt"
            print url_file_op
            print type(url_file_op)
            print chardet.detect(url_file_op)
            url_file=open(url_file_op,'ab')
            print 'h'
            print chardet.detect(url_file_op)
            Muliti_Retry(b_url,url_file)

            # url_file.write(b_name + "|" + b_url + "\r")
            # c_request=urllib2.Request(b_url)   #這一段需要獨立出來，因為很有可能會出現網絡問題
            # c_response=urllib2.urlopen(c_request)
            # c_content=c_response.read()
            # c_soup=BeautifulSoup(c_content,'html.parser')
            # c_results = c_soup.find_all('div', class_="down_list")  # 一共有两个，两个内容是一样的
            # for c_result in c_results:  # 将链接分别写入到各节目的文件内
            #     for d_result in c_result.find_all('a', text="迅雷下载"):
            #         c_download_link = d_result['href']
            #         url_file.write(c_download_link)
            # url_file.close()


        print '------------------------------------------------------------------------------------------------------------------------'
    # print TV_dict
    # print len(TV_dict)

    b_result = b_soup.find(string_is_nextpage)#获取下一页的链接
    if b_result == None:
        pass
    else:
        print b_result
        print 'aaaa'
        b_next_page_url=b_result['href']
        print 'bbbb'
        print b_next_page_url
        Get_Link(b_next_page_url,url_file_path)
    print "----"


for key,value in a_dict.items():
    print "##############"
    print key
    print chardet.detect(key)
    print "################"
    b_link=value
    b_file_path=Base_Dir+"\\"+key.encode("gbk")
    print 'f'
    print chardet.detect(b_file_path)
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



print "总耗时%d秒" %(time.time() - begin_time)




