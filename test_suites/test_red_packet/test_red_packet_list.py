# -*-coding: utf-8-*-
# @Time    : 2017/4/6
# @Author  : Mathilda

import requests
import json
import random
import test_suites.test_user_login

ck = test_suites.test_user_login.test_user_login()
print ck


url_article = 'https://www.zuihuibao.cn/yiiapp/red-packet/list'
# 待激活（默认）
params1 = {'limit': 10, 'status': 0, 'order_by': 1, 'index': 0}
# 已激活
params2 = {'limit': 10, 'status': 4, 'order_by': 2, 'index': 0}
# 赠送中
params3 = {'limit': 10, 'status': 2, 'order_by': 2, 'index': 0}
# 已赠送
params4 = {'limit': 10, 'status': 3, 'order_by': 1, 'index': 0}
# 已过期
params5 = {'limit': 10, 'status': 5, 'order_by': 2, 'index': 0}


def test_red_packet_list():
    rsp = requests.post(url=url_article, data=params1, cookies=ck, verify=False)
    print rsp.text
    res_dict = json.loads(rsp.text)
    assert res_dict['return_code'] == '0'
    assert rsp.status_code == 200

    lists = res_dict['data']['red_packet_list']
    if len(lists) > 0:
        lenoflist = len(lists) - 1
        index = random.randint(0, lenoflist)

        item = lists[index]
        assert item['red_packet_id'] != ''
        assert item['amount'] != ''
        assert item['red_packet_title'] != ''
        assert item['status'] == 0


def test_red_packet_list_already_active():
    rsp = requests.post(url=url_article, data=params2, cookies=ck, verify=False)
    res_dict = json.loads(rsp.text)
    assert res_dict['return_code'] == '0'
    assert rsp.status_code == 200

    lists = res_dict['data']['red_packet_list']
    if len(lists) > 0:
        lenoflist = len(lists) - 1
        index = random.randint(0, lenoflist)

        item = lists[index]
        assert item['red_packet_id'] != ''
        assert item['amount'] != ''
        assert item['red_packet_title'] != ''
        assert item['status'] == 4


def test_red_packet_list_donating():
    rsp = requests.post(url=url_article, data=params3, cookies=ck, verify=False)
    res_dict = json.loads(rsp.text)
    assert res_dict['return_code'] == '0'
    assert rsp.status_code == 200

    lists = res_dict['data']['red_packet_list']
    if len(lists) > 0:
        lenoflist = len(lists) - 1
        index = random.randint(0, lenoflist)

        item = lists[index]
        assert item['red_packet_id'] != ''
        assert item['amount'] != ''
        assert item['red_packet_title'] != ''
        assert item['status'] == 2


def test_red_packet_list_donated():
    rsp = requests.post(url=url_article, data=params4, cookies=ck, verify=False)
    res_dict = json.loads(rsp.text)
    assert res_dict['return_code'] == '0'
    assert rsp.status_code == 200

    lists = res_dict['data']['red_packet_list']
    if len(lists) > 0:
        lenoflist = len(lists) - 1
        index = random.randint(0, lenoflist)
        item = lists[index]
        assert item['red_packet_id'] != ''
        assert item['amount'] != ''
        assert item['red_packet_title'] != ''
        assert item['status'] == 3


def test_red_packet_list_faded():
    rsp = requests.post(url=url_article, data=params5, cookies=ck, verify=False)
    res_dict = json.loads(rsp.text)
    assert res_dict['return_code'] == '0'
    assert rsp.status_code == 200

    lists = res_dict['data']['red_packet_list']
    if len(lists) > 0:
        lenoflist = len(lists) - 1
        index = random.randint(0, lenoflist)
        item = lists[index]
        assert item['red_packet_id'] != ''
        assert item['amount'] != ''
        assert item['red_packet_title'] != ''
        assert item['status'] == 5

