# -*-coding: utf-8-*-
# @Author = jishanshan
# @Date = 2017/7/14
from test_suites import common_func
import xlrd

url = common_func.get_host() + '/yiiapp/car-info/replenish-info'
app_version = common_func.get_app_version()


# try:
#     f = xlrd.open_workbook('./frame_list.xlsx')
#     table=f.sheets()[0]
#     print(table.nrows)
#     for i in range(table.nrows):
#         print(table.cell(i,0).value)
#
# except Exception as e:
#     print('exception:',e)


# is_special_car=0&owner_name=%E5%8F%B6%E5%86%AC&frame_no=LHGVP2681B5467869&owner_id_no=420607197801028722&reg_date=2012-06-14&
# license_no=%E5%B7%9DA9S1V9&seat_num=5&tax_price=0.00&customer_id=888914&charged_matched=0&price=6.78&
# selected_car_model_detail= version=3.3.0&is_new_car=0&car_model_no=DC7146DBA&is_loaned=0&engine_no=8104562&add_only=0
# 客户下新增车辆add_only=1
data = {
    'version': app_version,
    'add_only': 0,
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

car_model_detail = {
    "family_name": "上海通用凯迪拉克ATS-L",
    "seat": "5",
    "engine_desc": "2.0L",
    "gearbox_name": "",
    "description": "上海通用凯迪拉克 凯迪拉克SGM7200AAA1轿车 2.0L  5座 ￥298800",
    "standard_name": "凯迪拉克SGM7200AAA1轿车",  # ---car_model_no
    "brand_name": "上海通用凯迪拉克",
    "parent_veh_name": " 5座",
    "taxprice": "298800",
    "market_date": "2014",
    "price": "298800",
    "codeSet": [
        "KDD3023SHT"
    ]
}

data['selected_car_model_detail']=str(car_model_detail)

def test_add_newcar_success():
    pass

def test_add_oldcar_success():
    pass

def test_update_car():
    pass

# 同一客户下不允许车辆冲突（新车）
def test_newcar_conflict():
    pass

# 同一客户下不允许车辆冲突（未上牌）
def test_oldcar_conflict():
    pass

# {
# 	"return_code": "0",
# 	"return_message": "",
# 	"data": {
# 		"car_id": "535728",
# 		"add_customer_notify": "",
# 		"customer_existence_info": {
# 			"scene": "no_hint"
# 		}
# 	}
# }
