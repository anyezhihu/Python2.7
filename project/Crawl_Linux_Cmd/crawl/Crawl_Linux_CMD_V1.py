#coding=utf-8

import urllib2
import re
import os
import sys
import chardet
import time
import sqlite3

begin_time=time.time()

#设置系统默认编码
reload(sys)
sys.setdefaultencoding('utf-8')

# 定义数据库文件路径
current_path = os.getcwd()
sql_file_name = "Linux_CMD.db"
sql_file_path = current_path + "\\sql\\" + sql_file_name

Main_URL_Dict={}
Base_Url = "http://man.linuxde.net/"
Base_Path = "E:\\python\\"

#定义连接数据库及建表操作
def db_connect():

    #连接数据库（如果数据库文件不存在则创建）
    try:
        conn=sqlite3.connect("%s" % sql_file_path)
        print "成功连接数据库"
    except sqlite3.DatabaseError as e:
        print "连接数据库失败：%s" % e.message

    #若表不存在则创建表Main_Url
    try:
        cursor = conn.cursor()
        try:
            print "查看数据库Main_Url是否存在"
            cursor.execute("select * from Main_Url")
        except sqlite3.DatabaseError as e:
            print "操作数据库失败：%s" % e.message
            sql_create_table_Main_Url = 'CREATE TABLE Main_Url \
                                              (ID INTEGER PRIMARY KEY  autoincrement   NOT NULL,\
                                               NAME           VARCHAR (20)     NOT NULL,\
                                               URL            VARCHAR (50)     NOT NULL,\
                                               PATH           VARCHAR (50)     NOT NULL );'
            cursor.execute(sql_create_table_Main_Url)
            cursor.close()
            print "创建表Main_Url成功"

    except sqlite3.DatabaseError as e:
        print "操作数据库失败：%s" % e.message
    finally:
        cursor.close()
        conn.commit()

    # 若表不存在则创建表Second_Url
    try:
        cursor = conn.cursor()
        try:
            print "查看数据库Main_Url是否存在"
            cursor.execute("select * from Second_Url")
        except sqlite3.DatabaseError as e:
            print "操作数据库失败：%s" % e.message
            sql_create_table_Main_Url = 'CREATE TABLE Second_Url \
                                                (ID INTEGER PRIMARY KEY  autoincrement   NOT NULL,\
                                                 NAME           VARCHAR (20)     NOT NULL,\
                                                 URL            VARCHAR (50)     NOT NULL,\
                                                 DES            VARCHAR (100) ,\
                                                 PATH           VARCHAR (50)     NOT NULL );'
            cursor.execute(sql_create_table_Main_Url)
            cursor.close()
            print "创建表Main_Url成功"

    except sqlite3.DatabaseError as e:
        print "操作数据库失败：%s" % e.message
    finally:
        cursor.close()
        conn.commit()

#定义出入操作
def db_insert(sql_file_path,sql):
    #打开数据库连接
    conn=sqlite3.connect(sql_file_path)
    cursor=conn.cursor()
    #插入数据库表
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        print "插入成功"
    except sqlite3.DatabaseError as e:
        print "连接数据库失败：%s" % e.message
    finally:
        cursor.close()
        conn.commit()

#从首页获取大分类信息，并创建对应的目录
def Get_Base_Directory():

    Request = urllib2.Request(Base_Url)
    response = urllib2.urlopen(Request)
    context = response.read()
    pattern = re.compile(r'<li id="menu-item-[0-9]" class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-[0-9]"><a href="(.*?)</a></li>')
    results=re.findall(pattern, context)

    for line in results:
        result=line.split("\">")
        Main_URL_Dict[result[0]]=result[1]
        url=result[0]
        name=result[1]
        path=Base_Path+result[1]
        #print url,name,path
        if os.path.exists(Base_Path+result[1].decode('utf-8').encode('gbk')):
            pass
        else:
            os.makedirs(Base_Path+result[1].decode('utf-8').encode('gbk'))
        sql="INSERT INTO Main_Url (NAME,URL,PATH) VALUES ('%s','%s','%s')" % (name,url,path)
        #print sql
        db_insert(sql_file_path,sql)

#进入到对应的分类下，获取二级网页链接，进入对应的目录下创建以命令名命名的文件，将对应网页的内容写入到文件中
def Get_URL():
    for key,value in Main_URL_Dict.items():
        time.sleep(1)
        print "开始获取%s下的命令链接" % key
        Request=urllib2.Request(key)
        response=urllib2.urlopen(key)

        context=response.read()
        #print context
        pattern_4 = re.compile('<div class=\'paging\'>.*class=\'inactive\' >(.*?)</a>.*</div>')
        Page_Num=re.findall(pattern_4,context)
        print Page_Num[0]
        Num=1
        #print type(Page_Num[0])
        Name_List=[]
        URL_List=[]
        Des_List=[]
        while Num <= int(Page_Num[0]):
            print "当前爬取链接：%s" % key+"/page/%s" % Num
            Request_1=urllib2.Request(key+"page/%s" % Num)
            response_1=urllib2.urlopen(Request_1)

            pattern_1 = re.compile('<div class="name"><a href="http://man.linuxde.net/.*" title=".*">(.*?)</a></div>')
            pattern_2 = re.compile(' <div class="name"><a href="(.*?)" title=".*">.*</a></div>')
            pattern_3 = re.compile('<div class="des">(.*?)</div>')

            Name_List+=re.findall(pattern_1, context)
            URL_List+=re.findall(pattern_2, context)
            Des_List+=re.findall(pattern_3, context)

            Num+=1
            print "爬取链接信息完毕，包含命令名称、介绍链接、命令描述"
        #print Name_List
        #print URL_List
        #print Des_List

        for a in Name_List:
            try:
                time.sleep(1)
                Absolute_Path=Base_Path+value+"\\"+a.replace("/", "-",)
                #print Absolute_Path
                file=open(Absolute_Path.encode('gbk'),'wb')
                Request_2=urllib2.Request(URL_List[Name_List.index(a)])
                response_2=urllib2.urlopen(Request_2)
                context_1=response_2.read()
                file.write(context_1)
                file.close()
                NAME=a.replace("/","-")
                URL=URL_List[Name_List.index(a)]
                DES=Des_List[Name_List.index(a)]
                PATH=Absolute_Path
                sql="INSERT INTO Second_Url (NAME,URL,DES,PATH) VALUES ('%s','%s','%s','%s')" %(NAME,URL,DES,PATH)
                #print sql
                db_insert(sql_file_path,sql)
            except urllib2.HTTPError as e:
                print e.code
                print e.reason


        print '-------------------------------------------------------------------------------------------'



#写入数据库，跳过已写入的
#添加错误重试

if __name__ == "__main__":
    db_connect()
    Get_Base_Directory()
    Get_URL()
    excute_time = time.time() - begin_time
    print "执行耗时:%d" % excute_time