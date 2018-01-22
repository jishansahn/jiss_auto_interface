# -*-coding: utf-8-*-
# @Author = jishanshan
# @Date = 2017/8/2
import xlrd
import os
from db_fixture import mysql_db


def debug():
    try:
        f = xlrd.open_workbook('./test_suites/test_jingji/car_list.xlsx')
        table = f.sheets()[0]
        print(table.nrows)
        for i in range(table.nrows):
            frame_no = table.cell(i, 0).value
            sqlstr = "select owner_name,owner_id_no,owner_mobile, special_car_date,beneficiary from dbzhb.user_car_list where frame_no='" + frame_no + "' limit 1;"
            # print sqlstr
            db = mysql_db.DB()
            rows = db.selectDB(sqlstr=sqlstr)
            if rows != None:
                if len(rows) > 0:
                    print rows[0]
                    # print frame_no + ': ' + rows[0].get('owner_name') + ',' + rows[0].get('owner_id_no') + ',' + rows[0].get('owner_mobile') + ','+rows[0].get('sepcial_car_date') + ',' + rows[0].get('beneficiary')
                else:
                    print frame_no + ': None'
            else:
                print frame_no + ': None'
    except Exception as e:
        print('exception:', e)


if __name__ == "__main__":
    debug()
