# -*-coding: utf-8-*-
# @Author = jishanshan
# @Date = 2017/8/22
import xlrd
import requests
from test_suites import common_func
import json
import sys
import time
import traceback
import os
import ConfigParser

cookies = dict(ZHBSESSID='80e8b347272be7e768ef89e431f2bf55')
s = requests.session()
s.cookies = requests.cookies.cookiejar_from_dict(cookies, cookiejar=None, overwrite=True)

app_version='3.6.0'
g_provider = 'official'
g_province = "吉林"
g_city = "吉林"
g_district=''
g_area = "丰满区"
g_insurance_company = 'TAIPINGYANG'
g_department = ''
g_com_id = ''
g_debug = 1
g_host = 'https://www.zuihuibao.com'

# os.chdir(common_func.get_project_dir())
# cf = ConfigParser.ConfigParser()
# cf.read('setup.cfg')
# app_version = cf.get('params', 'app_version')
# g_provider = cf.get('params', 'provider')
# g_province = cf.get('params', 'province')
# g_city = cf.get('params', 'city')
# g_district = cf.get('params', 'district')
# g_insurance_company = cf.get('params', 'insurance_company')
# g_department = cf.get('params', 'department')
# g_com_id = cf.get('params', 'com_id')
# g_env = cf.get('params', 'env')
# if g_env == 'dev':
#     g_host = 'https://www.zuihuibao.cn'
# else:
#     g_host = 'https://www.zuihuibao.com'


def main_proc():
    print '--------------test start----------'
    try:
        f = xlrd.open_workbook('./car_list.xlsx')
        table = f.sheets()[0]
        print(table.nrows)
        req_data = {
            'version': app_version,
            'add_only': 0,
            'customer_id': '',
            'is_new_car': '0',
            'license_no': '',
            'frame_no': '',
            'car_model_no': '',
            'selected_car_model_detail': '',
            'seat_num': '',
            'price': '',
            'engine_no': '',
            'reg_date': '',
            'is_special_car': '0',
            'special_car_date': '1900-01-01',
            'is_loaned': '0',
            'beneficiary': '',
            'driving_key': '',
            'owner_name': '',
            'owner_mobile': '',
            'owner_id_no': '',
            'applicant_same_as_owner': '1',
            'applicant_name': '',
            'applicant_mobile': '',
            'applicant_id_no': '',
            'insured_same_as_owner': '1',
            'insured_name': '',
            'insured_mobile': '',
            'insured_id_no': '',
            'insured_province': g_province,
            'insured_city': g_city,
            'insured_district': g_area,
            'insured_detail': '陆家嘴软件园',
            'provider': g_provider,
            'province': g_province,
            'city': g_city,
            'district': g_district,
            'department': g_department,
            'insurance_company': g_insurance_company,
            'com_id': 0,
        }

        for i in range(table.nrows):
            print '--------------分割线---------------------'
            req_data['owner_name'] = table.cell(i, 0).value
            req_data['applicant_name'] = req_data['owner_name']
            req_data['insured_name'] = req_data['owner_name']
            req_data['license_no'] = table.cell(i, 1).value
            if req_data['license_no'] == '':
                req_data['is_new_car'] = '1'
            else:
                req_data['is_new_car'] = '0'
            req_data['car_model_no'] = table.cell(i, 2).value
            req_data['frame_no'] = table.cell(i, 3).value
            req_data['engine_no'] = table.cell(i, 4).value
            req_data['reg_date'] = table.cell(i, 5).value
            req_data['is_special_car'] = table.cell(i, 7).value
            req_data['special_car_date'] = table.cell(i, 8).value
            req_data['is_loaned'] = table.cell(i, 9).value
            req_data['beneficiary'] = table.cell(i, 10).value
            req_data['owner_id_no'] = table.cell(i, 11).value
            req_data['applicant_id_no'] = req_data['owner_id_no']
            req_data['insured_id_no'] = req_data['owner_id_no']
            req_data['owner_mobile'] = table.cell(i, 12).value
            req_data['applicant_mobile'] = req_data['owner_mobile']
            req_data['insured_mobile'] = req_data['owner_mobile']
            req_data['price'] = table.cell(i, 6).value

            if g_debug: print req_data
            price = format(float(req_data['price']), '.2f')
            # 查询车型
            json_selected_model = query_model(frame_no="", car_model_no=req_data['car_model_no'], price=price)
            if json_selected_model == None:
                print '未获取到车型'
                continue
            req_data['price'] = str(format(float(json_selected_model.get('price')) / float(10000), '.2f'))
            req_data['seat_num'] = str(json_selected_model.get('seat'))
            req_data['selected_car_model_detail'] = json.dumps(json_selected_model, encoding="UTF-8",
                                                               separators=(',', ':'))
            if g_debug: print req_data

            json_order = replenish_info(req_data)
            if json_order is None:
                print req_data['owner_name'] + ': 保存车辆信息失败'
                continue
            car_id = json_order.get('car_id')
            req_data3 = {
                'version': app_version,
                'car_id': car_id,
                'provider': g_provider,
                'province': g_province,
                'city': g_city,
                'district': g_district,
                'department': '',
                'choose_force': 1,
                'force_only': 0,
                'user_force_start_date_change': 0,
                'user_ins_start_date_change': 0,
                'force_start_date': '',
                'force_start_hour': '0',
                'ins_start_date': '',
                'ins_start_hour': '0',
                'validate_start_date': '1'
            }

            req_data3['user_ins_start_date_change'] = 1
            req_data3['ins_start_date'] = table.cell(i, 13).value
            req_data3["user_force_start_date_change"] = 1
            req_data3["force_start_date"] = table.cell(i, 14).value
            if g_debug: print 'line', sys._getframe().f_lineno, req_data3

            code = update(req_data3)
            if code is None:
                print req_data['owner_name'] + 'update fail'
                continue

            req_data2 = {
                'car_id': car_id,
                'post_time_stamp': common_func.get_current_time(),
                'insurance_company': g_insurance_company,
                'force_only': 0,
                'choose_force': 1,
                'car_broken': 0,
                'car_broken_price': 0,
                'non_deduct_car_broken': 0,
                'third_party': 500000,
                'non_deduct_third_party': 0,
                'driver_seat': 10000,
                'non_deduct_driver_seat': 0,
                'passenger_seat': 10000,
                'non_deduct_passenger_seat': 0,
                'car_rob': 0,
                'non_deduct_car_rob': 0,
                'glass_broken': 0,
                'scratch': 0,
                'non_deduct_scratch': 0,
                'car_burn': 0,
                'non_deduct_car_burn': 0,
                'wade_water': 0,
                'non_deduct_wade_water': 0,
                'find_no_third_party': 0,
                'specify_repair_factory': 0,
                'pay_tax': 1,
                'product_source': 'app',
                'provider': g_provider,
            }
            if g_debug: print 'line', sys._getframe().f_lineno, req_data2
            # 请求报价
            price_order = record_price_info(req_data2)
            if price_order == None:
                continue
            # 请求核保
            place_order(price_order['data']['order_id'], addressee_mobile=req_data['owner_mobile'],
                        addressee_name=req_data['owner_name'])
    except Exception as e:
        print traceback.format_exc()


def query_model(frame_no, car_model_no, price=0):
    base_url = g_host + '/yiiapp/car-info/get-car-model-no-info'

    model_query = {
        'province': g_province,
        'city': g_city,
        'district': g_district,
        'department': g_department,
        'insurance_company': g_insurance_company,
        'license_no': '',
        'frame_no': frame_no,
        'car_model_no': car_model_no,
        'provider': g_provider,
        'version': app_version
    }
    if g_debug: print model_query

    rsp = s.post(url=base_url, data=model_query, verify=False)
    if g_debug: print "here is line:", sys._getframe().f_lineno, rsp.text
    if rsp.status_code != 200:
        print base_url + ':status code not 200'
        if g_debug: print "here is line:", sys._getframe().f_lineno, rsp.text
        return None
    res_dict = json.loads(rsp.text)
    if str(res_dict['return_code']) != '0':
        print 'query_model fail'
        return None
    if len(res_dict['data']) <= 0:
        print 'no model data'
        return None

    for iter in res_dict['data']:
        this_price = format(float(iter.get('price')) / float(10000), '.2f')
        if this_price == price:
            return iter
    return res_dict['data'][0]


def replenish_info(req_data):
    base_url = g_host + '/yiiapp/car-info/replenish-info-merge'

    rsp = s.post(url=base_url, data=req_data, verify=False)
    if g_debug: print "here is line :", sys._getframe().f_lineno, rsp.text
    if rsp.status_code != 200:
        print "here is line :", sys._getframe().f_lineno, rsp.text
        print base_url + ':status code not 200'
        return None
    res_dict = json.loads(rsp.text)
    if str(res_dict['return_code']) != '0':
        print 'update price info error'
        return None
    return res_dict['data']


def update(req_data):
    base_url = g_host + '/yiiapp/car-info/update'

    rsp = s.post(url=base_url, data=req_data, verify=False)
    print rsp.text
    if rsp.status_code != 200:
        print rsp.text
        print 'status code not 200'
        return None
    res_dict = json.loads(rsp.text)
    if str(res_dict['return_code']) == '0':
        return 1


def record_price_info(req_data2):
    base_url = g_host + '/yiiapp/car-ins/record-price-info-merge'

    rsp = s.post(url=base_url, data=req_data2, verify=False)

    if g_debug: print "here is line :", sys._getframe().f_lineno, rsp.text
    if rsp.status_code != 200:
        print base_url + '：status code not 200'
        print "here is line :", sys._getframe().f_lineno, rsp.text
        return None
    res_dict = json.loads(rsp.text)
    if str(res_dict['return_code']) == '0':
        if int(res_dict['data']['status']) == 9:
            print '报价成功'
            return res_dict
        else:
            print '报价完成，非成功状态'
    else:
        print '报价请求返回错误：', rsp.text


def place_order(order_id, addressee_mobile='13895274545', addressee_name='吉祥'):
    base_url = g_host + '/yiiapp/car-ins/place-order/1.1'
    req_data = {
        'addressee_mobile': addressee_mobile,
        'addressee_name': '测试单',
        'addressee_province': g_province,
        'addressee_city': g_city,
        'addressee_area': g_area,
        'addressee_detail': '人民大道1122号',
        'has_addressee_info': 1,
        'is_self_fetch': 0,
        'order_id': order_id,
        'version': app_version
    }
    rsp = s.post(url=base_url, data=req_data, verify=False)
    if g_debug: print "here is line:", sys._getframe().f_lineno, rsp.text
    if rsp.status_code != 200:
        print 'status code not 200'
        print "here is line :", sys._getframe().f_lineno, rsp.text
    res_dict = json.loads(rsp.text)
    if str(res_dict['return_code']) == '0':
        if int(res_dict['data']['status']) == 3:
            print '核保成功'
        else:
            print '核保完成，非成功状态'
    else:
        print '核保请求返回错误：', rsp.text

def delete_order():
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

if __name__ == "__main__":
    # main_proc()
    # place_order(31522034177000910)
    delete_order()
