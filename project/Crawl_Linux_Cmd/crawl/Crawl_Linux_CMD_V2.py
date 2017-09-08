#coding=utf-8

"""
相比于版本1的函数式做法，第2版采用了面向对象的方法。
"""

import chardet
import time
import re
import urllib2
import sqlite3
import sys
import os

#定义程序运行起始时间
Process_Begin_Time=time.time()
#设置系统默认字符集
reload(sys)
sys.setdefaultencoding('utf-8')
print "当前IDE环境默认字符集：%s" % sys.getdefaultencoding()

#定义数据库模块
class DB(object):
    def __init__(self,db,sql=None,table=None):
        """
        :param db:要连接的数据库文件的路径
        :param sql: 要执行的sql语句
        :param table: 要处理的数据库表
        """
        self.__db__=db
        self.__sql__=sql
        self.__table__=table

#数据库初始化
    def init_db(self):
        try:
            print "开始初始化数据库"
            print "数据库路径：%s" % self.__db__
            conn=sqlite3.connect(self.__db__)
            cursor=conn.cursor()
            print "开始创建表 Main_Url"
            sql_create_table_Main_Url = 'CREATE TABLE Main_Url \
                                                          (ID INTEGER PRIMARY KEY  autoincrement   NOT NULL,\
                                                           NAME           VARCHAR (20)     NOT NULL,\
                                                           URL            VARCHAR (50)     NOT NULL,\
                                                           PATH           VARCHAR (50)     NOT NULL );'
            cursor.execute(sql_create_table_Main_Url)
            print "创建表 Main_Url 成功"

            print "开始创建表 Second_Url "
            sql_create_table_Second_Url='CREATE TABLE Second_Url \
                                        (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,\
                                         NAME VARCHAR (20) NOT NULL ,\
                                         DES VARCHAR (100),\
                                         PATH VARCHAR (50) NOT NULL );'
            cursor.execute(sql_create_table_Second_Url)
            print "创建表 Second_Url 成功"
        except sqlite3.DatabaseError as e:
            print "数据库初始化失败：%s" % e.message




#定义数据库连接方法
    def connect_db(self):
        try:
            conn=sqlite3.connect(self.__db__)
            print "连接数据库成功：%s" % self.__db__
        except sqlite3.DatabaseError as e:
            print "连接数据库失败：%s" % e.message
        finally:
            conn.close()

#定义数据库操作方法
    def opertaor_db(self):
        try:
            conn=sqlite3.connect(self.__db__)
            cursor=conn.cursor()
            cursor.execute(self.__sql__)
        except sqlite3.DatabaseError as e:
            print "操作数据库失败：%s" % e.message
        finally:
            cursor.close()
            conn.commit()

#定义网页爬取模块
class Crawl_Html(object):
    def __init__(self,url,current_excute_time=0,max_excute_time=10):
        """
        :param url:要爬取的网址链接
        :param current_excute_time: 当前重试次数
        :param max_excute_time: 最大重试次数
        """
        self.__url__=url
        self.__current_excute_time__ = current_excute_time
        self.__max_excute_time__=max_excute_time

    def Get_Html_Content(self):
        try:
            Request=urllib2.Request(self.__url__)
            response=urllib2.urlopen(Request)
            content=response.read()
            return content
        except urllib2.HTTPError as e:
            self.__current_excute_time__=self.__current_excute_time__ + 1
            print "下载失败，失败原因：%s" % e.reason
            print "HTTP错误代码：%s" % e.code
            if self.__max_excute_time__ > 0:
                if hasattr(e,'code') and 500 <= e.code < 600:
                    print "进行第%d次重试" % self.__current_excute_time__
                    self.__max_excute_time__=self.__max_excute_time__ - 1
                    return self.Get_Html_Content()


#定义正则表达式处理模块
class Re_Get_Results(object):
    def __init__(self,str,content):
        """
        :param str: 用来生成表达式对象的字符串
        :param content: 进行查找的目标字符串
        """
        self.__str__=str
        self.__content__=content

    def Get_Results(self):
        try:
            pattern=re.compile('%s' % self.__str__)
            results=re.findall(pattern,self.__content__)
            if results == "[]":
                print "获取的是一个空列表，正则表达式命中失败"
                raise "获取的是一个空列表，正则表达式命中失败"
            else:
                return results
        except BaseException as e:
            print "正则表达式匹配失败：%s" % e.message

class Operator_File(object):
    def __init__(self,file,content):
        """
        :param file:要写入的文件路径
        :param content: 要写入的内容
        """
        self.__file__=file
        self.__content__=content

    #写入文件
    def Write_File(self):
        try:
            file=open(self.__file__,'wb')
            file.write(self.__content__)
            file.close()
        except BaseException as e:
            print "文件操作失败：%s" % e.message

#定义入口函数
def main():
    BaseUrl="http://man.linuxde.net/"
    BasePath=os.path.split(os.getcwd())[0]
    db_path=BasePath+"\\sql\\"+"Linux_CMD.db"
    a=DB(db=db_path)
#初始化数据库只有在第一次执行时才需要
    a.init_db()

    Main_Url_Pattern='<li id="menu-item-[0-9]" class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-[0-9]"><a href="(.*?)</a></li>'
    b=Crawl_Html(BaseUrl)
    c=Re_Get_Results(Main_Url_Pattern,b.Get_Html_Content())
    for line in c.Get_Results():
        #解决部分命令名中存在\导致路径创建失败的问题
        result=line.split("\">")
        Path_GBK=BasePath+"\\Download\\"+result[1].encode('gbk')
        Path_Utf=BasePath+"\\Download\\"+result[1]
        print Path_Utf
        if not os.path.exists(Path_GBK):
            os.makedirs(Path_GBK)
        sql="INSERT INTO Main_Url (NAME,URL,PATH) VALUES ('%s','%s','%s')" %(result[1],result[0],Path_Utf)
        d = DB(db=db_path, sql=sql)
        d.opertaor_db()
        print result[0]
        e=Crawl_Html(result[0])
        #e.Get_Html_Content()
        Page_Num_Url_Pattern='<div class=\'paging\'>.*class=\'inactive\' >(.*?)</a>.*</div>'
        Page_Num=Re_Get_Results(Page_Num_Url_Pattern,e.Get_Html_Content()).Get_Results()
        Num=1
        while Num <= int(Page_Num[0]):
            time.sleep(1)
            url=result[0] + "/page/%s" % Num
            print "当前爬取链接：%s" % url
            f=Crawl_Html(url)
            #f.Get_Html_Content()

            Second_Name = '<div class="name"><a href="http://man.linuxde.net/.*" title=".*">(.*?)</a></div>'
            Second_Url = ' <div class="name"><a href="(.*?)" title=".*">.*</a></div>'
            Second_Des ='<div class="des">(.*?)</div>'

            g=Re_Get_Results(Second_Name,f.Get_Html_Content()).Get_Results()
            h=Re_Get_Results(Second_Url,f.Get_Html_Content()).Get_Results()
            i=Re_Get_Results(Second_Des,f.Get_Html_Content()).Get_Results()


            Num += 1
            print "爬取链接信息完毕，包含命令名称、介绍链接、命令描述"
            for abc in h:
                k=g[h.index(abc)]
                l=i[h.index(abc)]
                print Path_Utf+k
                m=Path_Utf+"\\"+k
                j = Operator_File(Path_GBK + "\\" + k, Crawl_Html(abc).Get_Html_Content()).Write_File()
                sql = "INSERT INTO Second_Url (NAME,DES,PATH) VALUES ('%s','%s','%s')" % (k, l, m)
                n = DB(db=db_path, sql=sql)
                n.opertaor_db()






if __name__ == "__main__":
    main()
    print "运行总耗时：%d" %(time.time() - Process_Begin_Time)

