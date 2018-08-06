# -*- coding: utf-8 -*-

import math
import functools
import time

# def log(func):
#     # print('call %s():' % func.__name__)
#     # return func
#     @functools.wraps(func)
#     def wrapper(*args, **kw):
#         print('call %s():' % func.__name__)
#         return func(*args, **kw)
#     return wrapper
# @dec与第一层,第二层在初始化时就运行，第三层在执行被修饰函数时 先执行
def log(text):
    print ("log")
    def decorator(func):
        print "decorator"
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator

def metric(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kw):
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print('%s executed in %s ' % (fn.__name__, time_str))
        return fn(*args,**kw)
    return wrapper


# def quadratic(a, b, c):
#     tmp=math.sqrt(pow(b)-4*a*c)
#     return (-b+tmp)*1.0/(2*a), (-b-tmp)*1.0/(2*a)
#
# print('quadratic(2, 3, 1) =', quadratic(2, 3, 1))
# print('quadratic(1, 3, -4) =', quadratic(1, 3, -4))
#
# if quadratic(2, 3, 1) != (-0.5, -1.0):
#     print('测试失败')
# elif quadratic(1, 3, -4) != (1.0, -4.0):
#     print('测试失败')
# else:
#     print('测试成功')
@log('aa')
def fun_1(b,x):
    print(x,b)

def test_fun_1():
    a=[1,2]
    fun_1(*a)
    print(a)

def product(*args):
    s=1
    for i in args:
        s=s*i
    return s
def test_fun_2():

    print('product(5) =', product(5))
    print('product(5, 6) =', product(5, 6))
    print('product(5, 6, 7) =', product(5, 6, 7))
    print('product(5, 6, 7, 9) =', product(5, 6, 7, 9))
    if product(5) != 5:
        print('测试失败!')
    elif product(5, 6) != 30:
        print('测试失败!')
    elif product(5, 6, 7) != 210:
        print('测试失败!')
    elif product(5, 6, 7, 9) != 1890:
        print('测试失败!')
    else:
        try:
            product()
            print('测试失败!')
        except TypeError:
            print('测试成功!')

def findMinAndMax(L):
    pass

def test_fun_3():
# 测试
    if findMinAndMax([]) != (None, None):
        print('测试失败!')
    elif findMinAndMax([7]) != (7, 7):
        print('测试失败!')
    elif findMinAndMax([7, 1]) != (1, 7):
        print('测试失败!')
    elif findMinAndMax([7, 1, 3, 9, 5]) != (1, 9):
        print('测试失败!')
    else:
        print('测试成功!')

def test_list_gen():
    L1 = ['Hello', 'World', 18, 'Apple', None]
    L2 = [s.lower() for s in L1 if isinstance(s, str)]
    print L2
    # generator
    g = (s.lower() for s in L1 if isinstance(s, str))
    print g

def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        print(id(a),id(b))
        print b
        yield b
        a, b = b, a + b
        n = n + 1
@metric
def triangles():
    x=[1,1]
    i=1
    while True:
        if i==1:
            y=[1]
            yield y
        else:
            y=[1]
            for j in range(1,i-1,1):
                y.append(x[j]+x[j-1])
            y.append(1)
            yield y
            x=y
        i+=1

def test_tri():
    n = 0
    results = []
    for t in triangles():
        print(t)
        results.append(t)
        n = n + 1
        if n == 10:
            break
    if results == [
        [1],
        [1, 1],
        [1, 2, 1],
        [1, 3, 3, 1],
        [1, 4, 6, 4, 1],
        [1, 5, 10, 10, 5, 1],
        [1, 6, 15, 20, 15, 6, 1],
        [1, 7, 21, 35, 35, 21, 7, 1],
        [1, 8, 28, 56, 70, 56, 28, 8, 1],
        [1, 9, 36, 84, 126, 126, 84, 36, 9, 1]
    ]:
        print('测试通过!')
    else:
        print('测试失败!')

if __name__=='__main__':
    test_tri()
    test_fun_1()
    # test_list_gen()

    # generator
    # o=fib(6)
    # for n in o:
    #     next(o)



