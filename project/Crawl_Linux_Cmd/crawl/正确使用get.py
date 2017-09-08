# coding:utf-8
from  multiprocessing import Pool
import time


def Foo(i):
    time.sleep(2)
    return i + 100

def Bar(arg):
    return arg

if __name__ == '__main__':
    res_list=[]
    t_start=time.time()
    pool = Pool(5)

    for i in range(10):
        res = pool.apply_async(func=Foo, args=(i,), callback=Bar)
        res_list.append(res)    #添加到列表中

    pool.close()
    pool.join()
    for res in res_list:
        print res.get()
    t_end=time.time()
    t=t_end-t_start
    print 'the program time is :%s' %t
