import multiprocessing

def out(i):
    print i

def ou():
    manager=multiprocessing.Manager()
    a_dict={'a':'aaa','b':'bbb','c':'ccc','d':'ddd','e':'eee','f':'fff','g':'ggg','h':'hhh','i':'iii'}
    b_dict=manager.dict(a_dict)
    print a_dict
    print b_dict
    pool = multiprocessing.Pool(5)
    for key,value in a_dict.items():
        pool.apply_async(out, args=(value,))

if __name__ == "__main__":
    ou()