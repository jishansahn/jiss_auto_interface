# -*-coding: utf-8-*-
# @Author = jishanshan
# @Date = 2017/7/28
import requests
import json
import xlrd
import sys

# https://www.zuihuibao.cn/yiio2o/car-info/query-model-info
# https://www.zuihuibao.cn/yiio2o/o2o-car-ins/price-info
# https://www.zuihuibao.cn/yiio2o/o2o-car-ins/price-policy
# json_cookie={
#     "subscribe":"1",
#     "unionid":"o5k9Ps0SIRZbWdIpzFcTb5VombVs",
#     "user_id":3227,
#     "ZHBSESSID":"3ee278e389a8f5bb7d52b2740009ab51"
# }
cookies = dict(ZHBSESSID='10ab4c4024dfb4eaf9cc28e1fb44766a')
s = requests.session()
s.cookies = requests.cookies.cookiejar_from_dict(cookies, cookiejar=None, overwrite=True)

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

g_province = "广东"
g_city = "广州"
g_district = "代理业务部"
g_insurance_company = "PINGAN"
g_department='代理业务部-ZHBBXJJ-00002'
g_com_id='23010001'

# g_province= "上海"
# g_city="上海"
# g_district= "卢湾支公司直销业务二部"


# g_province = "广东"
# g_city = "广州"
# g_district = "芳村支公司"
# g_insurance_company="RENBAO"




def query_model(frame_no, car_model_no, price=0):
    base_url = 'https://www.zuihuibao.cn/yiio2o/car-info/query-model-info'
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
    print model_query

    rsp = s.post(url=base_url, data=model_query, verify=False)
    print "here is :", __file__, sys._getframe().f_lineno, rsp.text
    if rsp.status_code != 200:
        print "here is :", __file__, sys._getframe().f_lineno, rsp.text
        print 'status code not 200'
        return None
    res_dict = json.loads(rsp.text)
    if str(res_dict['return_code']) == '0':
        print ('length', len(res_dict['data']))
        if len(res_dict['data']) > 0:
            for iter in res_dict['data']:
                this_price = format(float(iter.get('price')) / float(10000), '.2f')

                if this_price == price:
                    return iter
            return res_dict['data'][0]
        else:
            print 'no model data'
            return None
    else:
        print 'query_model fail'
        return None


def price_info(req_data):
    base_url = 'https://www.zuihuibao.cn/yiio2o/o2o-car-ins/price-info'
    # req_data['license_no'] = '沪ACZ302'
    # req_data['frame_no'] = 'LSGGA54E2EH263439'
    # req_data['car_model_no'] = '别克SGM7161EAA2轿车'
    # req_data['engine_no'] = '142180221'
    # req_data['reg_date'] = '2014-09-02'
    price = format(float(req_data['price']), '.2f')
    json_selected_model = query_model(frame_no="", car_model_no=req_data['car_model_no'], price=price)
    # json_selected_model = query_model(frame_no=req_data['frame_no'], car_model_no="")
    if json_selected_model != None:
        req_data['price'] = str(format(float(json_selected_model.get('price')) / float(10000), '.2f'))
        req_data['seat_num'] = str(json_selected_model.get('seat'))
        req_data['selected_car_model_detail'] = json.dumps(json_selected_model, encoding="UTF-8", separators=(',', ':'))
        print req_data
        rsp = s.post(url=base_url, data=req_data, verify=False)
        print "here is :", __file__, sys._getframe().f_lineno, rsp.text
        if rsp.status_code != 200:
            print "here is :", __file__, sys._getframe().f_lineno, rsp.text
            print 'status code not 200'
            return None
        res_dict = json.loads(rsp.text)
        if str(res_dict['return_code']) == '0':
            return res_dict['data']
        else:
            print 'update price info error'
            return None
    else:
        print 'selected model None'
        return None


def price_policy():
    print '--------------分割线---------------------'
    base_url = 'https://www.zuihuibao.cn/yiio2o/o2o-car-ins/price-policy'
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

            print req_data
            json_order = price_info(req_data)
            if json_order == None:
                print req_data['frame_no'] + ': this case fail'
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
                'com_id':g_com_id,
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

            # req_data2["ins_start_date"]=table.cell(i, 13).value
            # req_data2["force_start_date"] = table.cell(i, 14).value
            print req_data2
            rsp = s.post(url=base_url, data=req_data2, verify=False)

            print "here is :", __file__, sys._getframe().f_lineno, rsp.text
            if rsp.status_code != 200:
                print 'status code not 200'
                print "here is :", __file__, sys._getframe().f_lineno, rsp.text
                print req_data['frame_no'] + ': this case fail'
                continue
            res_dict = json.loads(rsp.text)
            # if int(res_dict['data']['status']) == 9:
            #     underwrite_one(res_dict['data']['order_id'])
            # else:
            #     print 'price_policy return status!=9' + rsp.text

                # if res_dict
    except Exception as e:
        print ('exception:', e)


def underwrite_one(order_id):
    base_url = 'https://www.zuihuibao.cn/yiio2o/o2o-car-ins/underwrite'

    insure_addr_url = 'https://www.zuihuibao.cn/yiio2o/order/need-insured-address'
    rsp1 = s.post(url=insure_addr_url, data={'insurance_company': g_insurance_company}, verify=False)
    if rsp1.status_code != 200:
        print "here is :", __file__, sys._getframe().f_lineno, rsp1.text
        print 'status code not 200'
        return None
    res_dict = json.loads(rsp1.text)
    if str(res_dict['return_code']) == '0':
        is_need = res_dict['data']['is_need']
        if is_need:
            req_data = {
                'insurance_company': g_insurance_company,
                'isTwice': '0',
                'order_id': order_id,
                'insured_province': '上海',
                'insured_city': '上海',
                'insured_area': '浦东新区',
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
        rsp = s.post(url=base_url, data=req_data, verify=False)
        if rsp.status_code != 200:
            print 'status code not 200'
            print "here is :", __file__, sys._getframe().f_lineno, rsp.text
            print req_data['frame_no'] + ': this car核保 fail'
        # res_dict = json.loads(rsp.text)
        print "here is :", __file__, sys._getframe().f_lineno, rsp.text
    else:
        print 'insure_addr_url error'
        return None


def underwrite_all():
    base_url = 'https://www.zuihuibao.cn/yiio2o/o2o-car-ins/underwrite'
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
        print ('exception:',e)


if __name__ == "__main__":
    price_policy()
    # underwrite_all()
