#coding=utf-8

import sys
import time
import os
import urllib2
import re
import sqlite3

print "输出当前默认系统编码：%s" % sys.getdefaultencoding()

reload(sys)
sys.setdefaultencoding('utf-8')
print "输出修改之后的默认系统编码：%s" % sys.getdefaultencoding()

#定义通用下载模块
def Get_Url_Results(url,pattern,current_excute_time):
    try:
        Request=urllib2.Request(url)
        response=urllib2.urlopen(Request)
        context=response.read()
        results=re.findall(pattern,context)
        current_excute_time=current_excute_time - 1
    except urllib2.HTTPError as e:
        print "下载错误：%s" % e.reason
        results=None
        if current_excute_time > 0:
            if hasattr(e,'code') and 500 <= e.code < 600:
                print "出现错误，错误代码：%s" % e.code
                print "开始重试，重试次数：%s" % current_excute_time
                return Get_Url_Results(url,pattern,current_excute_time-1)

    return results



print "开始获取主分类信息..."
def Get_First_Layer():
    #Base_Url="http://man.linuxde.net/"
    Base_Url = "http://httpstat.us/500"
    Base_Path=raw_input(r"请输入存储目录：")
    #print Base_Path
    try:
        if not os.path.exists(Base_Path):
            os.makedirs(Base_Path)
            print "已成功创建路径：%s" % Base_Path
        else:
            print "已发现路径：%s" % Base_Path
    except WindowsError as e:
        print "路径不存在，创建路径%s失败。" % Base_Path
        print e
    max_retry_times=10

    try:
        pattern=re.compile(r'<li id="menu-item-[0-9]" class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-[0-9]"><a href="(.*?)</a></li>')
        aaa=Get_Url_Results(Base_Url,pattern,max_retry_times)
    except urllib2.HTTPError as e:
        print "获取网页信息失败"
        print e.reason
    print aaa


#Get_First_Layer()

def sql_exc():
    try:
        import sqlite3

        conn = sqlite3.connect('test.db')
        print "Opened database successfully"
        #exit(1)
        c = conn.cursor()
        c.execute('''CREATE TABLE COMPANY
               (ID INT PRIMARY KEY     NOT NULL,
               NAME           TEXT    NOT NULL,
               URL            CHAR(100)    NOT NULL,
               ADDRESS        CHAR(50),
               SALARY         REAL);''')
        print "Table created successfully"
        conn.commit()
        conn.close()

        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        print "Opened database successfully"

        c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (1, 'Paul', 32, 'California', 20000.00 )")

        c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (2, 'Allen', 25, 'Texas', 15000.00 )")

        c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )")

        c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )")

        conn.commit()
        print "Records created successfully"
        conn.close()



    except sqlite3.Error as e:
        print 'aaa'
        print e.message

    print "连接sqllite3成功"

#sql_exc()
def aaa():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    print "Opened database successfully"
    result=c.execute("select * from COMPANY")
    for a in  result:
        print a

#aaa()

def db_connect():
    #定义数据库文件路径
    current_path=os.getcwd()
    sql_file_name="Linux_CMD.db"
    sql_file_path=current_path+"\\"+sql_file_name

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
                                               NAME           TEXT    NOT NULL,\
                                               URL            CHAR(100)     NOT NULL);'
            cursor.execute(sql_create_table_Main_Url)
            cursor.close()
            print "创建表Main_Url成功"

    except sqlite3.DatabaseError as e:
        print "操作数据库失败：%s" % e.message
    finally:
        cursor.close()
        conn.commit()
    return sql_file_path


def db_insert(sql_file_path,sql):
    #打开数据库连接
    conn=sqlite3.connect(sql_file_path)
    cursor=conn.cursor()
    #插入数据库表Main_Urlk
    try:
        cursor = conn.cursor()
        sql_insert_table_Main_Url = sql
        cursor.execute(sql_insert_table_Main_Url)
        print "插入成功"
    except sqlite3.DatabaseError as e:
        print "连接数据库失败：%s" % e.message
    finally:
        cursor.close()
        conn.commit()

db_connect()

