# -*-coding: utf-8-*-
# @Time    : 2017/4/18
# @Author  : Mathilda
import pymysql
import requests
from bs4 import BeautifulSoup

# db_config = pymysql.connect(
#     host='127.0.0.1',
#     port=3315,
#     user='wanglijun',
#     password='soinLove_13',
#     db='dbzhb',
#     charset='utf8'
# )
#
# connection = pymysql.connect(**db_config)
#
# cur = db_config.cursor()
#
# url = r'https://www.zuihuibao.cn/yiiapp/piazza/article-list'
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87'
# }
# page = requests.post(url, headers=headers)
# # page_info = request.urlopen(page).read().decode('utf-8')
# # soup = BeautifulSoup(page_info, 'html.parser')
# urls = soup.find_all('a', 'title')
#
# try:
#     # 获得数据库游标
#     with connection.cursor() as cursor:
#         # sql = 'insert into titles(title, url) values(%s, %s)'
#         sql = 'select * from piazza_articles limit 10'
#         for u in urls:
#             # 执行sql语句
#             cursor.execute(sql, (u.string, url + u.attrs['href']))
#     # 事务提交
#     connection.commit()
# finally:
#     # 关闭数据库连接
#     connection.close()

import MySQLdb


# def doinsert(cursor, db):
#     # insert
#     # Prepare SQL query to INSERT a record into the database.
#     sql = "UPDATE red_packet SET status = 5 WHERE user_id = '%d'" % 2195818
#     try:
#         cursor.execute(sql)
#         db.commit()
#     except:
#         db.rollback()


# def do_query(cursor, db):
#     sql = "SELECT * FROM red_packet" \
#           " WHERE user_id = '%d'" % 2195818
#     try:
#         # Execute the SQL command
#         cursor.execute(sql)
#         # Fetch all the rows in a list of lists.
#         results = cursor.fetchall()
#         print 'resuts', cursor.rowcount
#         for row in results:
#             id = row[0]
#             user_id = row[1]
#             from_type = row[2]
#             from_serial = row[3]
#             # Now print fetched result
#             print "id=%d,user_id=%d,from_type=%d,from_serial=%d" % \
#                   (id, user_id, from_type, from_serial)
#     except:
#         print "Error: unable to fecth data"


def do_delete(cursor, db):
    sql = "DELETE FROM red_packet WHERE user_id = '%d'" % (2195818)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()


def do_insert(cursor, db, firstname, lastname, age, sex, income):
    sql = "INSERT INTO EMPLOYEE(FIRST_NAME, \
       LAST_NAME, AGE, SEX, INCOME) \
       VALUES ('%s', '%s', '%d', '%c', '%d' )" % \
          (firstname, lastname, age, sex, income)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()


# Open database connection
# change this to your mysql account
# connect(server,username,password,db_name)
db = pymysql.connect(host='localhost', user='wanglijun', password='soinLove_13', database='dbzhb',
                     port=3315, charset='utf8')
# prepare a cursor object using cursor() method
cursor = db.cursor()
# do_query(cursor, db)
# doinsert(cursor, db)
# do_query(cursor, db)
do_delete(cursor, db)
# do_query(cursor, db)
# do_insert(cursor, db, 'hunter', 'xue', 22, 'M', 2000)
# do_insert(cursor, db, 'mary', 'yang', 22, 'f', 5555)
# do_insert(cursor, db, 'zhang', 'xue', 32, 'M', 5000)
# do_insert(cursor, db, 'hunter', 'xue', 22, 'M', 333)
# do_query(cursor, db)
# disconnect from server
db.close()
