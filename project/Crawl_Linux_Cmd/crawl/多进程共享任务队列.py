#coding=utf-8

"""
该程序用于演示windows多进程运行
"""

# import time
# import multiprocessing
#
# begin_time=time.time()
#
# """
# 每次只发起一个进程
# """
#
# def a(i):
#     print "现在输出的是%s" % i
#     time.sleep(2)
#
# def b(c):
#     for i in range(len(c)):
#         print "当前输出的是%d" % c[i]
#         time.sleep(2)
#         c[i] = -c[i]
#
# def f(d,l):
#     d[1]='1'
#     d['2']=2
#     d[0.25]=None
#     l.reverse()
#
# # if __name__ == "__main__":#必须有这句话，否则无法启动子进程。这是 Windows 上多进程的实现问题。在 Windows 上，子进程会自动 import 启动它的这个文件，
# # 而在 import 的时候是会执行这些语句的。如果你这么写的话就会无限递归创建子进程报错。所以必须把创建子进程的部分用那个 if 判断保护起来，
# # import 的时候 __name__ 不是 __main__ ，就不会递归运行了。
# #     process_list=[]
# #     for b in range(10):
# #         p=multiprocessing.Process(target=a,args=(b,))
# #         # p.daemon=True
# #         process_list.append(p)
# #
# #     for c in process_list:
# #         c.start()
# #         print c.name    #输出进程名称，默认情况下是Process-数字序号
# #         print c.pid #输出进程PID
# #         print c.daemon  #输出进程是否是后台运行，如果前面没有设置daemon=True则返回False
# #         print c.authkey #不知道是啥
# #         print c.exitcode    #输出退出代码，正常情况下是None，输出其他数字这表示进程异常退出
# #         #c.join() #等待当前进程结束后，再退出主进程。放在这里其实相当于顺序执行的效果
# #     c.join()    #放的位置不一样，效果也不一样，放在这是等所有的子进程结束后再退出主进程
#
#
# """采用进程池，一次发起多个进程"""
#
#
#
# # if __name__ == "__main__":
# #     pool = multiprocessing.Pool(6)
# #     for b in range(12):
# #         # pool.apply(func=a,args=(b,))    #同步进程
# #         pool.apply_async(func=a,args=(b,))  #异步进程
# #     pool.close()
# #     pool.join() #使用Pool类的时候，在pool.join()之前，一定要有pool.close()或者pool.terminate()
# #     # pool.terminate()  #这里有没有都一样，因为前面已经pool.close()了
# #     print "执行完毕"
# #     print "总执行时间：%d"  %(time.time() - begin_time)
# #
#
# """
# 进程间共享数据
# 使用：
# multiprocessing.Queue()
# multiprocessing.Manager()
# multiprocessing.Array()
# """
#
# # #array
# # if __name__ == "__main__":
# #     array=multiprocessing.Array('i',range(10))
# #     p = multiprocessing.Process(target=b,args=(array,))
# #     p.start()
# #     p.join()
# #     print (array[:])
#
# # #manager
# # if __name__ == "__main__":
# #     with multiprocessing.Manager() as manager:
# #         d=manager.dict()
# #         l=manager.list(range(10))
# #
# #         p=multiprocessing.Process(target=f,args=(d,l))
# #         p.start()
# #         p.join()
# #
# #         print d
# #         print l

#实战
#coding=utf-8
import time
import multiprocessing
import urllib2

begin_time=time.time()
#url_list=["https://www.hao123.com","https://www.baidu.com/","https://www.360.cn/","http://www.qq.com/"]
url_dict={"好123":"https://www.hao123.com","百度":"https://www.baidu.com/","流氓":"https://www.360.cn/","妇科王":"http://www.qq.com/"}

def out(name,url):
    print "当前正在爬取的是:%s" % url
    try:
        request=urllib2.Request(url)
        response=urllib2.urlopen(request)
        content=response.read()
        f=open(name,'w')
        f.write(content)
        f.close()
    except Exception as e:
        print e.message
    finally:
        print "爬取完毕"
        time.sleep(5)

if __name__ == "__main__":
    Poll=multiprocessing.Pool(2)
    for name,url in url_dict.items():
        name=name.decode('utf-8').encode('gbk')
        Process=multiprocessing.Process(target=out,args=(name,url))
        Process.start()
    Poll.close()
    Process.join()
    print "运行结束，运行时间：%d" %(time.time() - begin_time)

