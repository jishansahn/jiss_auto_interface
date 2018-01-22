# -*-coding: utf-8-*-
# @Time    : 2017/6/6
# @Author  : Mathilda
import test_suites.test_user_login
import requests
import json
import random

ck = test_suites.test_user_login.test_user_login()
print ck
url = 'https://www.zuihuibao.cn/php2/life_ins_manage/query_order.php'
params_all = {'status': 0, 'order_type': 0, 'index': 0, 'limit': 10, 'action': 'multiple_orders'}
params_unpay = {'status': 1, 'order_type': 0, 'index': 0, 'limit': 10, 'action': 'multiple_orders'}
params_done = {'status': 2, 'order_type': 0, 'index': 0, 'limit': 10, 'action': 'multiple_orders'}



def test_order_list():
    rsp = requests.post(url=url, params=params_all, cookies=ck, verify=False)
    # print rsp.text
    assert rsp.status_code == 200

    res_dict = json.loads(rsp.text)
    assert res_dict['return_code'] == '0'
    lists = res_dict['data']
    if len(lists) > 0:
        lenoflist = len(lists) - 1
        index = random.randint(0, lenoflist)

        item = lists[index]
        assert item['order_type'] == '1'
        assert item['status'] != ''
        assert item['order_id'] != ''
        assert item['car_info']['applicant_id_no'] != ''
        assert item['car_info']['applicant_mobile'] != ''


def test_order_unpay():
    rsp = requests.post(url=url, params=params_unpay, cookies=ck, verify=False)
    # print rsp.text
    assert rsp.status_code == 200

    res_dict = json.loads(rsp.text)
    assert res_dict['return_code'] == '0'
    lists = res_dict['data']
    if len(lists) > 0:
        lenoflist = len(lists) - 1
        index = random.randint(0, lenoflist)

        item = lists[index]
        assert item['order_type'] == '1'
        assert item['status'] == '3'
        assert item['order_id'] != ''
        assert item['car_info']['applicant_id_no'] != ''
        assert item['car_info']['applicant_mobile'] != ''


def test_order_done():
    rsp = requests.post(url=url, params=params_done, cookies=ck, verify=False)
    # print rsp.text
    assert rsp.status_code == 200

    res_dict = json.loads(rsp.text)
    assert res_dict['return_code'] == '0'
    lists = res_dict['data']
    if len(lists) > 0:
        lenoflist = len(lists) - 1
        index = random.randint(0, lenoflist)
        item = lists[index]
    assert item['order_type'] == '1'
    assert item['status'] == '7'
    assert item['order_id'] != ''

