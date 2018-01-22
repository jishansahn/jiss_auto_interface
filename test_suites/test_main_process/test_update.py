# -*-coding: utf-8-*-
# @Author=jishanshan

import requests

from db_fixture import mysql_db, common_main_proc_db
from test_suites import common_func,user_login

# pytestmark = pytest.mark.usefixtures("getCookies")
url = common_func.get_host() + '/yiiapp/car-info/update'
app_version = common_func.get_app_version()

# 方案页update


# 次日日期
tomorrow_date = common_func.get_add_days(1)
get_cookies=user_login.get_cookies()
# ins_start_hour=16&version=3.2.0&province=%E5%AE%89%E5%BE%BD&force_start_date=2017-07-13&car_id=1235222764&force_start_hour=16
# &validate_start_date=1&force_only=0&ins_start_date=2017-07-13&city=%E5%90%88%E8%82%A5&district=&choose_force=1
data = {'version': app_version,
        'car_id': '',
        'province': '四川',
        'city': '成都',
        'district': '',
        'force_start_date': tomorrow_date,
        'force_start_hour': '0',
        'ins_start_date': tomorrow_date,
        'ins_start_hour': '0',
        'choose_force': '1',
        'force_only': '0',
        'validate_start_date': '1'}

car_data = {
    'customer_id': '',
    'is_new_car': '0',
    'license_no': '',
    'frame_no': '',
    'car_model_no': '',
    'selected_car_model_detail': '',
    'seat_num': '',
    'charged_matched': '',
    'price': '',
    'tax_price': '',
    'engine_no': '',
    'reg_date': '',
    'is_special_car': '0',
    'special_car_date': '',
    'is_loaned': '0',
    'beneficiary': '',
    'owner_name': '',
    'owner_id_no': '330302198809027155',
}

# 确认更新后数据一致
def test_plan_update_succes():
    data['province'] = ''
    data['city'] = ''
    data['district'] = ''

    user_id = get_cookies.get('user_id')
    effect_rows = common_main_proc_db.exec_dict_insert('dbzhb.user_car_list', car_data)
    if effect_rows == 1:
        sqlstr = "select id from dbzhb.user_car_list where user_id=" + user_id + " and license_no='" + car_data[
            'license_no'] + "'"
        db = mysql_db.DB()
        rows = db.insertDB(sqlstr)
        if len(rows) > 0:
            car_id = rows[0].get('id')



def setup_function(test_plan_illegal_date):
    print "setup" +test_plan_illegal_date.__name__

def test_plan_illegal_date():
    user_id = get_cookies.get('user_id')
    car_info = common_main_proc_db.get_index_carinfo(user_id, index=0)
    car_id = car_info.get('id')

    # 设置保险起期在90天以外
    illegal_date = common_func.get_add_days(91)
    data['car_id'] = car_id
    data['ins_start_date'] = illegal_date
    data['force_only'] = 0

    rsp = requests.post(url, data=data, cookies=get_cookies, verify=False)
    assert rsp.status_code == 200
    rsp_dict = rsp.json()
    print rsp_dict
    # 找不到车辆信息 也是-1004 ？？
    # 起期不合法 也是-1004 ？？
    assert rsp_dict['return_code'] == '-1004'


def test_plan_legal_date():
    user_id = get_cookies.get('user_id')
    car_info = common_main_proc_db.get_index_carinfo(user_id, index=0)
    car_id = car_info.get('id')
    # 设置保险起期在90天内
    legal_date = common_func.get_add_days(90)
    data['car_id'] = car_id
    data['force_start_date'] = legal_date
    data['ins_start_date'] = legal_date
    data['choose_force'] = 1
    data['force_only'] = 0
    print data
    rsp = requests.post(url, data=data, cookies=get_cookies, verify=False)
    assert rsp.status_code == 200
    rsp_dict = rsp.json()
    print rsp_dict
    assert rsp_dict['return_code'] == '0'
