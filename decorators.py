# check on properties for login required
from functools import wraps

def check_type(func):
    def func_wrapper():
        func.name = 'huw'
        return func
    return func_wrapper

def pretty_printer(tag):
    def inner_func(func):
        @wraps(func)
        def func_wrapper(s):
            s = "{tag}{name} is fabulous{tag}".format(name=s, tag=tag)
            return func(s)
        return func_wrapper
    return inner_func

@pretty_printer('*************')
def say_name(n):
    print(n)

say_name('huw')
print(say_name.__name__)

@check_type
class Animal(object):
    maintype = 'animal'

    def __init__(self, composure='cool and mellow'):
        self.composure = composure

#cat = Animal()

#print(cat.name)

# if '__name__' == '__main__':

