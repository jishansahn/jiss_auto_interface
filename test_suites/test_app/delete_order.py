# -*-coding: utf-8-*-
# @Author = jishanshan
# @Date = 2018/4/8
import xlrd


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