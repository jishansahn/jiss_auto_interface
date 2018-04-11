# -*-coding: utf-8-*-
# @Author = jishanshan
# @Date = 2018/4/8
import xlrd
import xlrd
import requests
from test_suites import common_func
import json
import sys
import time
import traceback
from db_fixture import mysql_db
import os
import ConfigParser

cookies = dict(ZHBSESSID='80e8b347272be7e768ef89e431f2bf55')
s = requests.session()
s.cookies = requests.cookies.cookiejar_from_dict(cookies, cookiejar=None, overwrite=True)

g_debug = 1
g_host = 'https://www.zuihuibao.com'

def delete_order_from_xls():
    base_url = g_host + '/php2/order/delete_order.php'
    req_data = {
        'order_id': '',
        'version':'3.6.0'
    }
    try:
        f = xlrd.open_workbook('./car_list.xlsx')
        table = f.sheets()[1]
        print(table.nrows)
        for i in range(table.nrows):
            req_data['order_id'] = table.cell(i, 0).value
            rsp = s.post(url=base_url, data=req_data, verify=False)
            if rsp.status_code != 200:
                print 'status code not 200'
                print "here is line :",sys._getframe().f_lineno, rsp.text
                print '删除订单请求失败'
            # res_dict = json.loads(rsp.text)
            print "here is line:",  sys._getframe().f_lineno, rsp.text
            time.sleep(2)
    except Exception as e:
        print traceback.format_exc()

def delete_order_from_db():
    base_url = g_host + '/php2/order/delete_order.php'
    req_data = {
        'order_id': '',
        'version':'3.6.0'
    }
    try:
        sqlstr = "select order_id from dbzhb.user_order where user_id='1451682' and create_time>='2018-04-11' and status=3 order by id desc;"
        print sqlstr
        db = mysql_db.DB()
        rows = db.selectDB(sqlstr)
        max_index = len(rows)
        print max_index
        for i in range(max_index):
            req_data['order_id'] = rows[i].get('order_id')
            rsp = s.post(url=base_url, data=req_data, verify=False)
            if rsp.status_code != 200:
                print 'status code not 200'
                print "here is line :",sys._getframe().f_lineno, rsp.text
                print '删除订单请求失败'
            # res_dict = json.loads(rsp.text)
            print "here is line:",  sys._getframe().f_lineno, rsp.text
            time.sleep(2)
    except Exception as e:
        print traceback.format_exc()

if __name__ == "__main__":

    delete_order_from_db()