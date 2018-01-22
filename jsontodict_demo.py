# -*-coding: utf-8-*-
# @Time    : 2017/3/20
# @Author  : Mathilda

import simplejson

user = '{"name" : "jim", "sex" : "male", "age": 18}'

# 使用eval()或exec()函数实现
eval_user_info = eval(user)
print eval_user_info


# json格式，使用simplejson把jason转化为python的内置类型
json_2_dict = simplejson.loads(user)
print json_2_dict

# 字典转换为json格式字符串
dict_2_json = simplejson.dumps(user)
print dict_2_json
