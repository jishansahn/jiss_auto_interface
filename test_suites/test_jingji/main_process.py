# -*-coding: utf-8-*-
# @Author = jishanshan
# @Date = 2017/7/28
import requests
import json
import xlrd
import sys
import traceback

# https://www.zuihuibao.cn/yiio2o/car-info/query-model-info
# https://www.zuihuibao.cn/yiio2o/o2o-car-ins/price-info
# https://www.zuihuibao.cn/yiio2o/o2o-car-ins/price-policy
# json_cookie={
#     "subscribe":"1",
#     "unionid":"o5k9Ps0SIRZbWdIpzFcTb5VombVs",
#     "user_id":3227,
#     "ZHBSESSID":"3ee278e389a8f5bb7d52b2740009ab51"
# }
cookies = dict(ZHBSESSID='381677bda23eb4-e058-45bb-b03a-03c1bfd3a6de')
s = requests.session()
s.cookies = requests.cookies.cookiejar_from_dict(cookies, cookiejar=None, overwrite=True)
g_host = 'https://www.zhbbroker.cn'

# g_provider = 'ahuasheng'
g_provider = 'agent'
# g_department = ''
# g_source='huasheng'
g_source = 'new'

# g_province = "江苏"
# g_city = "无锡"
# g_district = "惠山支公司"
# g_insurance_company="TAIPINGYANG"

# g_province = "广东"
# g_city = "广州"
# g_district = "广州市直属支公司"
# g_insurance_company="RENBAO"

# g_province = "安徽"
# g_city = "合肥"
# g_district = "营业部"
# g_insurance_company="RENBAO"

# g_province = "广东"
# g_city = "广州"
# g_district = "代理业务部"
# g_insurance_company = "PINGAN"
# g_department='代理业务部-ZHBBXJJ-00002'
# g_com_id='23010001'

# g_province= "上海"
# g_city="上海"
# g_district= "卢湾支公司直销业务二部"


# g_province = "广东"
# g_city = "广州"
# g_district = "芳村支公司"
# g_insurance_company="RENBAO"

# g_province = "湖南"
# g_city = "长沙"
# g_district = "天心区支公司"
# g_department = ''
# g_insurance_company = "ZHONGHUA"
# g_com_id = '12100104'
g_debug = 1

#
# g_province = "四川"
# g_city = "攀枝花"
# g_district = "陶家渡支公司"
# g_department = ''
# g_insurance_company = "RENBAO"
# g_com_id = '10061401'

g_province = "湖北"
g_city = "宜昌"
g_district = "中支营业部"
g_department = ''
g_insurance_company = "DINGHE"
g_com_id = '25000000'

def main_proc():
    print '--------------分割线---------------------'

    try:
        f = xlrd.open_workbook('./car_list.xlsx')
        table = f.sheets()[0]
        print(table.nrows)
        req_data = {
            'is_new_car': '0',
            'ex_order': '',
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
            'image_info': '',
            'provider': g_provider,
            'source': g_source
        }
        for i in range(table.nrows):
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
            req_data['reg_date'] = xlrd.xldate_as_datetime(table.cell(i, 5).value,0).strftime("%Y-%m-%d")
            req_data['is_special_car'] = table.cell(i, 7).value
            req_data['special_car_date'] = xlrd.xldate_as_datetime(table.cell(i, 8).value,0).strftime("%Y-%m-%d")
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
            # 保存车辆信息
            json_order = price_info(req_data)
            if json_order == None:
                print req_data['owner_name'] + ': 保存车辆信息失败'
                continue

            req_data2 = {
                "order_id": json_order.get('order_id'),
                "is_repost": json_order.get('is_repost'),
                'provider': g_provider,
                "insurance_company": g_insurance_company,
                "province": g_province,
                "city": g_city,
                "district": g_district,
                'department': g_department,
                'com_id': g_com_id,
                "force_only": 0,
                "choose_force": 1,
                "ins_start_date": "",
                "ins_start_hour": 0,
                "force_start_date": "",
                "force_start_hour": 0,
                "car_broken": 1,
                "car_broken_price": 0,
                "non_deduct_car_broken": 1,
                "third_party": 1000000,
                "non_deduct_third_party": 1,
                "driver_seat": 10000,
                "non_deduct_driver_seat": 1,
                "passenger_seat": 10000,
                "non_deduct_passenger_seat": 1,
                "car_rob": 0,
                "non_deduct_car_rob": 0,
                "glass_broken": 0,
                "scratch": 0,
                "non_deduct_scratch": 0,
                "car_burn": 0,
                "non_deduct_car_burn": 0,
                "wade_water": 0,
                "non_deduct_wade_water": 0,
                "find_no_third_party": 0,
                "specify_repair_factory": 0,
                "has_toast": 0
            }

            # req_data2["ins_start_date"] = table.cell(i, 13).value
            # req_data2["force_start_date"] = table.cell(i, 14).value
            if g_debug: print 'line', sys._getframe().f_lineno, req_data2
            # 请求报价
            price_order = price_policy(req_data2)
            if price_order == None:
                continue
            hebao_data = need_insured_address(price_order['data']['order_id'])
            if hebao_data == None:
                continue
            # 请求核保
            underwrite_one(hebao_data)
    except Exception as e:
        print traceback.format_exc()


def query_model(frame_no, car_model_no, price=0):
    base_url = g_host + '/yiio2o/car-info/query-model-info'
    model_query = {
        'frame_no': frame_no,
        'car_model_no': car_model_no,
        "province": g_province,
        "city": g_city,
        "district": g_district,
        "insurance_company": g_insurance_company,
        'provider': g_provider,
        'department': g_department
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


def price_info(req_data):
    base_url = g_host + '/yiio2o/o2o-car-ins/price-info'

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


def price_policy(req_data2):
    base_url = g_host + '/yiio2o/o2o-car-ins/price-policy'
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


def need_insured_address(order_id):
    insure_addr_url = 'https://www.zuihuibao.cn/yiio2o/order/need-insured-address'
    rsp1 = s.post(url=insure_addr_url, data={'insurance_company': g_insurance_company}, verify=False)
    if rsp1.status_code != 200:
        print 'status code not 200'
        print "here is line :", sys._getframe().f_lineno, rsp1.text
        return None
    res_dict1 = json.loads(rsp1.text)
    if str(res_dict1['return_code']) == '0':
        is_need = res_dict1['data']['is_need']
        if is_need:
            req_data = {
                'insurance_company': g_insurance_company,
                'isTwice': '0',
                'order_id': order_id,
                'insured_province': '四川',
                'insured_city': '攀枝花',
                'insured_area': '东区',
                'insured_detail': '陆家嘴软件园',
                'image_info': ''
            }
        else:
            req_data = {
                'insurance_company': g_insurance_company,
                'isTwice': '0',
                'order_id': order_id,
                'insured_province': '',
                'insured_city': '',
                'insured_area': '',
                'insured_detail': '',
                'image_info': ''
            }
        return req_data
    else:
        print 'insure_addr_url error'
        return None


def underwrite_one(req_data):
    base_url = g_host + '/yiio2o/o2o-car-ins/underwrite'

    rsp = s.post(url=base_url, data=req_data, verify=False)
    print "here is line:", sys._getframe().f_lineno, rsp.text
    if rsp.status_code != 200:
        print 'status code not 200'
        print "here is line :", sys._getframe().f_lineno, rsp.text
        return None
    res_dict = json.loads(rsp.text)
    if str(res_dict['return_code']) == '0':
        if int(res_dict['data']['status']) == 3:
            print '核保成功'
        else:
            print '核保完成，非成功状态'
    else:
        print '核保请求返回错误：', rsp.text


def underwrite_all():
    base_url = g_host + '/yiio2o/o2o-car-ins/underwrite'
    req_data = {
        'insurance_company': g_insurance_company,
        'isTwice': '0',
        'order_id': '',
        'insured_province': '上海',
        'insured_city': '上海',
        'insured_area': '浦东新区',
        'insured_detail': '陆家嘴软件园',
        'image_info': ''
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
                print "here is :", __file__, sys._getframe().f_lineno, rsp.text
                print req_data['frame_no'] + ': this car核保 fail'
            # res_dict = json.loads(rsp.text)
            print "here is :", __file__, sys._getframe().f_lineno, rsp.text
    except Exception as e:
        print ('exception:', e)


if __name__ == "__main__":
    main_proc()
    # underwrite_all()
