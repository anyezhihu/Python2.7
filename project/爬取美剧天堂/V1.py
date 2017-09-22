#coding=utf-8

"""
编码问题，一直没解决。在家里可以正常运行，在办公室就不行。
No handlers could be found for logger "bs4.dammit"--无关紧要的报错不用管
需要优化一下代码结构和变量命名
需要添加缓存及缓存检测
使用QT做个简单的展示和触发迅雷的页面
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


def Get_Module():
    print "开始"
    global Base_Url
    Base_Url = "http://www.meijutt.com/"
    # 获取大板块名称及链接
    a_Request = urllib2.Request(Base_Url)
    a_response = urllib2.urlopen(a_Request)
    a_content = a_response.read()
    print "a"
    a_soup = BeautifulSoup(a_content, 'html.parser')
    a_results = a_soup.select('div[class="menuBox"]')

    print chardet.detect(os.getcwd())
    global Base_Dir
    Base_Dir = os.getcwd().decode('gbk').encode('gbk') + "\\" + "下载".encode('gbk')

    if not os.path.exists(Base_Dir):
        os.makedirs(Base_Dir)
    print chardet.detect(Base_Dir)

    global a_dict
    a_dict = {}
    for a_result in a_results:
        # print a_result.prettify()
        for a_link in a_result.find_all('a'):
            if a_link.has_attr('href') and not a_link.has_attr('class'):
                a_name = str(a_link.string).replace('/', '_')
                a_href = a_link['href']
                a_dict[a_name] = a_href
                a_path = Base_Dir + "\\" + a_name.encode('GB2312')
                print type(a_path)
                print chardet.detect(a_path)
                if not os.path.exists(a_path):
                    os.makedirs(a_path)

# 获取各版块的链接，写入到各自目录下，这里需要使用迭代，必须使用函数了
def Get_Link(start_url,url_file_path):
    print '------------------------------------------------------------------------------------------------------------------------'
    b_link = Base_Url + start_url#获取要爬去的页面的链接
    b_request = urllib2.Request(b_link)
    b_response = urllib2.urlopen(b_request)
    b_content = b_response.read()
    b_soup = BeautifulSoup(b_content, 'html.parser')
    b_tv_results=b_soup.find_all('div',class_="cn_box2")#将当前页面的电视剧的链接添加到字典中
    for b_tv_result in b_tv_results:
        b_tv_links=b_tv_result.find_all('a',attrs={"class":"B font_16"})
        for b_tv_link in b_tv_links:
            b_name=str(b_tv_link["title"])
            b_url=Base_Url+b_tv_link["href"]
            print b_name,b_url
            TV_dict[b_name]=str(b_url)

        print '------------------------------------------------------------------------------------------------------------------------'
    b_result = b_soup.find(string_is_nextpage)#获取下一页的链接
    if b_result == None:
        pass
    else:
        print b_result
        b_next_page_url=b_result['href']
        print b_next_page_url
        Get_Link(b_next_page_url,url_file_path)
    print "----"

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
        for d_result in c_result.find_all('a'):
            c_download_link=d_result['href']
            c_file.write(c_download_link)

#定义多进程下载模块
#多进程采用的是进程池，针对的是模块级别的，获取到该模块下所有的节目链接后，再使用多进程下载
def MultiProcess_download(b_file_path):
    pool=multiprocessing.Pool()#采用进程池
    for key,value in TV_dict.items():
        print '12f'
        b_name=key
        b_url=value
        pool.apply_async(Muliti_Retry,args=(b_file_path,b_name,b_url,))#启动多进程
    pool.close()
    pool.join()

#解決可能出現的网络问题
def Muliti_Retry(b_file_path,b_name,b_url,max_times=10,sleep_time=2,current_excute_time=0):
    try:
        # print chardet.detect(str(b_name).encode('GB2312').replace('/', '_'))
        try:
            url_file_op = b_file_path + "\\" + b_name.encode('GB2312', 'ignore').replace('/', '_') + ".txt"
            url_file = open(url_file_op, 'ab')
            c_request = urllib2.Request(b_url)
            c_response = urllib2.urlopen(c_request)
            c_content = c_response.read()
            c_soup = BeautifulSoup(c_content, 'html.parser')
            c_results = c_soup.find_all('div', class_="down_list")  # 一共有两个，两个内容是一样的
            for c_result in c_results:  # 将链接分别写入到各节目的文件内
                for d_result in c_result.find_all('a'):
                    c_download_link = d_result['href']
                    url_file.write(c_download_link + '\n')  # 有一些链接内是没有下载链接的，这样会生成一个空白文件
            url_file.close()
        except:
            pass
    except urllib2.HTTPError as e:
        current_excute_time= current_excute_time + 1
        print "下载失败，失败原因：%s" % e.reason
        print "HTTP错误代码：%s" % e.code
        if max_times > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                print "进行第%d次重试" % current_excute_time
                time.sleep(sleep_time)
                return Muliti_Retry(b_url,url_file,max_times = max_times - 1)

if __name__ == "__main__":
    Get_Module()
    for key, value in a_dict.items():
        print key
        print chardet.detect(key)
        b_link = value
        b_file_path = Base_Dir + "\\" + key.encode("gbk")
        print chardet.detect(b_file_path)
        print b_file_path
        TV_dict = {}
        Get_Link(b_link, b_file_path)#获取各模块下的链接字典
        MultiProcess_download(b_file_path)#多进程爬取链接字典

    print "总耗时%d秒" % (time.time() - begin_time)





