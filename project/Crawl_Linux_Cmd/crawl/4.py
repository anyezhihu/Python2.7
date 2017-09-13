class A:
    def __init__(self):
        print "enter A"
        print "leave A"

class C(object):
    def __init__(self):
        print "enter C"
        print "leave C"

class B(C):
    def __init__(self):
        print "enter B"
        #C.__init__(self)
        super(B,self).__init__()
        print "leave B"

b = B()