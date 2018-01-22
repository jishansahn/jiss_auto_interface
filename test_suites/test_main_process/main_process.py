# -*-coding: utf-8-*-
# @Author = jishanshan
# @Date = 2017/8/22
import xlrd
import requests
from test_suites import common_func
import json

app_version = 'V3.2.0'
cookies = dict(ZHBSESSID='7c2c99770a304f0a11d5c6a0a76474ba')
s = requests.session()
s.cookies = requests.cookies.cookiejar_from_dict(cookies, cookiejar=None, overwrite=True)


def query_model(frame_no, car_model_no):
    base_url = 'https://www.zuihuibao.cn/yiiapp/car-info/query-model-info'

    model_query = {
        'frame_no': frame_no,
        'car_model_no': car_model_no
    }
    print model_query

    rsp = s.post(url=base_url, data=model_query, verify=False)
    print rsp.text
    if rsp.status_code != 200:
        print rsp.text
        print 'status code not 200'
        return None
    res_dict = json.loads(rsp.text)
    if str(res_dict['return_code']) == '0':
        print('length', len(res_dict['data']))
        if len(res_dict['data']) > 0:
            return res_dict['data'][0]
        else:
            print 'no model data'
            return None
    else:
        print 'query_model fail'
        return None


def replenish_info(req_data):
    base_url = 'https://www.zuihuibao.cn/yiiapp/car-info/replenish-info'
    # req_data['license_no'] = '沪ACZ302'
    # req_data['frame_no'] = 'LSGGA54E2EH263439'
    # req_data['car_model_no'] = '别克SGM7161EAA2轿车'
    # req_data['engine_no'] = '142180221'
    # req_data['reg_date'] = '2014-09-02'
    json_selected_model = query_model(frame_no='', car_model_no=req_data['car_model_no'])
    # json_selected_model = query_model(frame_no=req_data['frame_no'], car_model_no='')
    if json_selected_model is not None:
        req_data['price'] = str(format(float(json_selected_model.get('price')) / float(10000), '.2f'))
        req_data['seat_num'] = str(json_selected_model.get('seat'))
        req_data['selected_car_model_detail'] = json.dumps(json_selected_model, encoding='UTF-8', separators=(',', ':'))
        print req_data
        rsp = s.post(url=base_url, data=req_data, verify=False)
        print rsp.text
        if rsp.status_code != 200:
            print rsp.text
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

def update(req_data):
    base_url='https://www.zuihuibao.cn/yiiapp/car-info/update'

    rsp = s.post(url=base_url, data=req_data, verify=False)
    print rsp.text
    if rsp.status_code != 200:
        print rsp.text
        print 'status code not 200'
        return None
    res_dict = json.loads(rsp.text)
    if str(res_dict['return_code']) == '0':
        return 1

def record_price_info():
    base_url = 'https://www.zuihuibao.cn/yiiapp/car-ins/record-price-info'

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
            'owner_name': '',
            'owner_mobile': '',
            'owner_id_no': '',
        }
        # 'applicant_same_as_owner': '1',
        # 'applicant_name': '',
        # 'applicant_mobile': '',
        # 'applicant_id_no': '',
        # 'insured_same_as_owner': '1',
        # 'insured_name': '',
        # 'insured_mobile': '',
        # 'insured_id_no': '',
        for i in range(table.nrows):
            print '--------------分割线---------------------'
            req_data['owner_name'] = table.cell(i, 0).value
            # req_data['applicant_name'] = req_data['owner_name']
            # req_data['insured_name'] = req_data['owner_name']
            req_data['license_no'] = table.cell(i, 1).value
            if req_data['license_no'] == '':
                req_data['is_new_car'] = '1'
            else:
                req_data['is_new_car'] = '0'
            req_data['car_model_no'] = table.cell(i, 2).value
            req_data['frame_no'] = table.cell(i, 3).value
            req_data['engine_no'] = table.cell(i, 4).value
            req_data['reg_date'] = table.cell(i, 5).value
            req_data['is_special_car'] = table.cell(i, 6).value
            req_data['special_car_date'] = table.cell(i, 7).value
            req_data['is_loaned'] = table.cell(i, 8).value
            req_data['beneficiary'] = table.cell(i, 9).value
            req_data['owner_id_no'] = table.cell(i, 10).value
            # req_data['applicant_id_no'] = req_data['owner_id_no']
            # req_data['insured_id_no'] = req_data['owner_id_no']
            req_data['owner_mobile'] = table.cell(i, 11).value
            # req_data['applicant_mobile'] = req_data['owner_mobile']
            # req_data['insured_mobile'] = req_data['owner_mobile']

            print req_data
            json_order = replenish_info(req_data)
            if json_order is None:
                print req_data['frame_no'] + ': this case fail'
                continue

            req_data3 = {
                'version': app_version,
                'car_id': json_order.get('car_id'),
                'province': table.cell(i, 12).value,
                'city': table.cell(i, 13).value,
                'district': '',
                'force_start_date': table.cell(i, 14).value,
                'force_start_hour': '0',
                'ins_start_date': table.cell(i, 15).value,
                'ins_start_hour': '0',
                'validate_start_date': '0'}
            code=update(req_data3)
            if code is None:
                print req_data['frame_no'] + 'update fail'

            req_data2 = {
                'car_id': json_order.get('car_id'),
                'post_time_stamp': common_func.get_current_time(),
                'insurance_company': 'TAIPINGYANG',
                'force_only': 0,
                'choose_force': 1,
                'car_broken': 1,
                'car_broken_price': 0,
                'non_deduct_car_broken': 1,
                'third_party': 1000000,
                'non_deduct_third_party': 1,
                'driver_seat': 10000,
                'non_deduct_driver_seat': 1,
                'passenger_seat': 10000,
                'non_deduct_passenger_seat': 1,
                'car_rob': 1,
                'non_deduct_car_rob': 1,
                'glass_broken': 0,
                'scratch': 0,
                'non_deduct_scratch': 0,
                'car_burn': 0,
                'non_deduct_car_burn': 0,
                'wade_water': 0,
                'non_deduct_wade_water': 0,
                'find_no_third_party': 0,
                'specify_repair_factory': 0
            }

            # req_data2['post_time_stamp'] = common_func.get_current_time()
            print req_data2
            rsp = s.post(url=base_url, data=req_data2, verify=False)
            print rsp.text
            if rsp.status_code != 200:
                print 'status code not 200'
                print rsp.text
                print req_data['frame_no'] + ': this case fail'
                continue
            # res_dict = json.loads(rsp.text)
            print 'price success' + rsp.text

            # if res_dict
    except Exception as e:
        print('exception:', e)

if __name__ == "__main__":
    record_price_info()