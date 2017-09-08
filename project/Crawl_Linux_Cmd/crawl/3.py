from multiprocessing import Process
import threading
import time


def foo(i):
    print 'say hi', i
    time.sleep(5)

if __name__ == '__main__':
    for i in range(10):
        p = Process(target=foo, args=(i,))
        p.start()
    p.join()
    print 'main process end'

