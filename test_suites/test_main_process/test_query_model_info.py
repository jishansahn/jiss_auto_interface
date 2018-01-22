# -*-coding: utf-8-*-
# @Author = jishanshan
# @Date = 2017/7/14

import json

import requests

from test_suites import common_func

# import xlrd

model_url = common_func.get_host() + '/yiiapp/car-info/query-model-info'
frame_query = {
    'license_no': '',
    'frame_no': ''
}

model_query = {
    'license_no': '',
    'car_model_no': ''
}


# try:
#     f = xlrd.open_workbook('./frame_list.xlsx')
#     table=f.sheets()[0]
#     print(table.nrows)
#     for i in range(table.nrows):
#         print(table.cell(i,0).value)
#
# except Exception as e:
#     print('exception:',e)
# f = open("./db_frame.txt", 'r', encoding='utf-8', errors='ignore')
# frame_list = f.readlines()

# car_model_detail = {
#     "family_name": "上海通用凯迪拉克ATS-L",
#     "seat": "5",
#     "engine_desc": "2.0L",
#     "gearbox_name": "",
#     "description": "上海通用凯迪拉克 凯迪拉克SGM7200AAA1轿车 2.0L  5座 ￥298800",
#     "standard_name": "凯迪拉克SGM7200AAA1轿车",  # ---car_model_no
#     "brand_name": "上海通用凯迪拉克",
#     "parent_veh_name": " 5座",
#     "taxprice": "298800",
#     "market_date": "2014",
#     "price": "298800",
#     "codeSet": [
#         "KDD3023SHT"
#     ]
# }
# frame_list=['LSGXE83L8FD087298','LGWEF4A58EF007053','LZWADAGA9F6118788','LGWEF4A58EF007053','LSVWL2184FN229274','LJDEAA298A0130242']
def test_query_by_frame():
    frame_query['frame_no'] = 'LSGXE83L8FD087298'
    r3 = requests.post(model_url, data=frame_query, verify=False)
    assert r3.status_code == 200
    res_dict = json.loads(r3.text)
    print(res_dict)
    assert str(res_dict['return_code']) == '0'
    print('length', len(res_dict['data']))
    if len(res_dict['data']) > 0:
        print res_dict['data'][0]


def test_query_by_model():
    pass


def query_model_info(frame_no=None, car_model_no=None):
    if frame_no != None:
        frame_query['frame_no'] = frame_no
        r3 = requests.post(model_url, data=frame_query, verify=False)
        if r3.status_code == 200:
            res_dict = json.loads(r3.text)
            if str(res_dict['return_code']) == '0' and len(res_dict['data']) > 0:
                car_model_detail = res_dict['data'][0]
    elif car_model_no != None:
        model_query['car_model_no'] = car_model_no
        rsp = requests.post(model_url, data=model_query, verify=False)
        if rsp.status_code == 200:
            res_dict = json.loads(rsp.text)
            if str(res_dict['return_code']) == '0' and len(res_dict['data']) > 0:
                car_model_detail = res_dict['data'][0]
    else:
        car_model_detail = {}
    return car_model_detail