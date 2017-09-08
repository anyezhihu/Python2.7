class Animal(object):
    def __init__(self, name):
        self.name = name

    def greet(self):
        print 'Hello, I am %s.' % self.name


class Dog(Animal):
    def greet(self):
        super(Dog, self).greet()
        print 'WangWang...'

dog = Dog('dog')

dog.greet()
