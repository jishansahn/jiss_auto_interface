# -*-coding: utf-8-*-
# @Time    : 2017/4/18
# @Author  : Mathilda
import test_user_login
import requests
import json
import random

default_first_page = {
    'license_no': '川A9S1V9',
    'owner_name': '叶冬',
    'version': '3.1.0'
}
url_first_page = 'https://www.zuihuibao.cn/yiiapp/car-info/record-common-car-info'

default_car_info = {
    'add_only': '0',
    'tax_price': '0.00',
    'selected_car_model_detail': {
        'description': '北京现代BH6440LAY轻型客车 手自一体舒适型两驱国Ⅳ 5座 ￥148800',
        'codeSet': '[XDABED0023]',
        'market_date': '',
        'brand_name': '',
        'engine_desc': '',
        'seat': '5',
        'gearbox_name': '',
        'vehicle_fgw_code': 'BJXD-BH6440LAY',
        'price': '148800',
        'standard_name': '北京现代BH6440LAY轻型客车',
        'vehicle_id': '',
        'taxprice': '0',
        'extendInfo': {
            'com': 'renbao',
            'guid': '31491020798194968',
            'code': ''
        },
        'family_name': '北京现代BH6440LAY轻型客车',
        'parent_veh_name': '手自一体舒适型两驱国Ⅳ 5座'
    },
    'seat_num': 5,
    'is_loaned': 0,
    'owner_id_no': '330302198809027155',
    'price': '14.88',
    'is_special_car': 0,
    'car_model_no': 'BH6440LAY',
    'reg_date': '2015-07-25',
    'engine_no': '8104562',
    'owner_name': '叶冬',
    'is_new_car': 0,
    'customer_id': 1116991,
    'license_no': '川A9S1V9',
    'frame_no': 'LBELMBKB2FY596702',
    'charged_matched': 0
}
url_car_info = 'https://www.zuihuibao.cn/yiiapp/car-info/replenish-info'

default_update_info = {
    'district': '武侯区',
    'car_id': '1235222225',
    'ins_start_date': '2017-07-06',
    'city': '成都',
    'force_start_date': '2017-07-06',
    'choose_force': 1,
    'force_only': 0,
    'validate_start_date': 1,
    'province': '四川'
}
url_update_info = 'https://www.zuihuibao.cn/yiiapp/car-info/update'

default_price_configuration = {
    'district': '武侯区',
    'frame_no': 'LBELMBKB2FY596702',
    'city': '成都',
    'id': 1235222225,
    'immediate_effect': 0,
    'version': '3.1.0',
    'license_no': '川A9S1V9',
    'province': '四川'
}
url_price_configuration = 'https://www.zuihuibao.cn/yiiapp/car-ins/price-configuration'

default_record_price_info = {
    'insurance_company': 'RENBAO',
    'district': '武侯区',
    'specify_repair_factory': 0,
    'car_id': 1235222225,
    'non_deduct_third_party': 1,
    'passenger_seat': 10000,
    'frame_no': 'LBELMBKB2FY596702',
    'non_deduct_car_broken': 1,
    'post_time_stamp': '2017-05-22 16:04:47',
    'glass_broken': 0,
    'non_deduct_driver_seat': 1,
    'car_burn': 0,
    'choose_force': 1,
    'third_party': 500000,
    'license_no': '川A9S1V9',
    'scratch': 0,
    'ins_start_date': '2017-07-06',
    'force_start_date': '2017-07-06',
    'non_deduct_car_rob': 0,
    'driver_seat': 10000,
    'wade_water': 0,
    'car_rob': 0,
    'non_deduct_passenger_seat': 1,
    'car_broken': 1
}
url_record_price_info = 'https://www.zuihuibao.cn/yiiapp/car-ins/record-price-info'

ck = test_user_login.test_user_login()


def test_first_page():
    rsp = requests.post(url=url_first_page, params=default_first_page, cookies=ck, verify=False)
    print rsp.text
    assert rsp.status_code == 200

    res_dict = json.loads(rsp.text)
    print type(res_dict)
    # print res_dict
    assert res_dict['return_code'] == '0'
    assert res_dict['data']['customer_id'] == 1116991


def test_car_info():
    rsp = requests.post(url=url_car_info, params=default_car_info, cookies=ck, verify=False)
    assert rsp.status_code == 200

    res_dict = json.loads(rsp.text)
    assert res_dict['return_code'] == '0'
    assert res_dict['data']['car_id'] == '1235222225'
    assert res_dict['data']['customer_existence_info']['scene'] == 'no_hint'


def test_update_info():
    rsp = requests.post(url=url_update_info, params=default_update_info, cookies=ck, verify=False)
    assert rsp.status_code == 200

    res_dict = json.loads(rsp.text)
    assert res_dict['return_code'] == '0'
    assert res_dict['data']['effected_num'] == '1'
    assert res_dict['data']['post_time_stamp'] != ''
    assert res_dict['data']['car_info_complete_rate'] == '100'


def test_price_configuration():
    rsp = requests.post(url=url_price_configuration, params=default_price_configuration, cookies=ck, verify=False)
    assert rsp.status_code == 200

    res_dict = json.loads(rsp.text)
    assert res_dict['return_code'] == '0'
    assert res_dict['data']['embed'] == []
    lists = res_dict['data']['ins_companies']
    if len(lists) > 0:
        lenoflist = len(lists) - 1
        index = random.randint(0, lenoflist)
        item = lists[index]
    assert item['company'] != ''
    assert item['is_open'] != ''
    assert item['biz_only'] != ''
    assert item['force_only'] != ''
    assert item['activities'] == []
    assert item['auto_select'] != ''


def test_record_price_info():
    rsp = requests.post(url=url_record_price_info, params=default_record_price_info, cookies=ck, verify=False)
    assert rsp.status_code == 200

    res_dict = json.loads(rsp.text)
    print type(res_dict)
    print rsp.text
    assert res_dict['data']['license_no'] != ''
    assert res_dict['data']['owner_name'] != ''
    assert res_dict['data']['owner_id_no'] != ''
    assert res_dict['return_code'] == 0
