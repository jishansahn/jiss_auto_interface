# -*-coding: utf-8-*-
import ConfigParser
import os
import platform
import random
import requests
import json
import time, datetime


# 获取项目根目录
def get_project_dir():
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print project_dir
    return project_dir


def get_host():
    os.chdir(get_project_dir())
    cf = ConfigParser.ConfigParser()
    cf.read('setup.cfg')
    return cf.get('web_host', 'web_host')


def get_app_version():
    os.chdir(get_project_dir())
    cf = ConfigParser.ConfigParser()
    cf.read('setup.cfg')
    return cf.get('params', 'app_version')


# 当前日期  string
def get_current_date():
    date_str = time.strftime('%Y-%m-%d', time.localtime())
    return date_str


def get_current_time():
    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return time_str

# 当前日期+n天，默认第二天 string
def get_add_days(n=1):
    now_time = datetime.datetime.now()
    new_time = now_time + datetime.timedelta(days=+n)
    new_time_nyr = new_time.strftime('%Y-%m-%d')
    print new_time_nyr
    return new_time_nyr


# 获取当前小时加hours取整，默认=最小可投保时间 string
def get_add_hours(hours=1.5):
    # 时间的加减
    now_time = datetime.datetime.now()
    # 当前时间加半小时
    new_time = now_time + datetime.timedelta(hours=+hours)
    new_time_nyrh = new_time.strftime('%Y-%m-%d %H')
    v_list = new_time_nyrh.split(" ")
    return v_list[0], v_list[1]


# 字符串转time
def str_to_time(str_time):
    t = time.strptime(str_time, '%Y-%m-%d %H:%M:%S')
    y, m, d, H, M, S = t[:6]
    # print(t)
    v_time = datetime.datetime(y, m, d, H, M, S)
    # print v_time
    return v_time


# # 一个月前
# today1 = datetime.datetime.today()
# astmonth = datetime.datetime(today1.year, (today1.month - 1), today1.day, today1.hour, today1.minute, today1.second)


# 获取当前系统路径分隔符
def get_separator():
    if 'Windows' in platform.system():
        separator = '\\'
    else:
        separator = '/'
    return separator


# 获取登录状态
def get_login_status(cookie):
    os.chdir(get_project_dir())
    cf = ConfigParser.ConfigParser()
    cf.read('setup.cfg')
    web_host = cf.get('web_host', 'web_host')
    url = web_host + '/yiiapp/system/query-login-status'
    rsp = requests.post(url, cookies=cookie, verify=False)
    if rsp.status_code == 200 & json.loads(rsp.text)['return_code'] == '0':
        return json.loads(rsp.text)['data']['login_status']


if __name__ == "__main__":
    print get_current_date()
    print get_add_days()
    print get_add_days(20)
    print get_add_hours()
    print get_add_hours(5)
    print get_current_time()
