# -*-coding: utf-8-*-
# @Time    : 2017/3/16
# @Author  : Mathilda

import re

import mysql

from spongebob.all_configs import all_db_config

mysql.install_as_MySQLdb()
MYSQL_TYPE = 'mysql'


class DBHandler(object):
    def _get_db_client(self, *args, **kwargs):
        pass

    def call(self, db_name, sql):
        pass

    @staticmethod
    def _get_config(db_name):
        db_config = all_db_config.get(db_name)
        if not db_config:
            print '%s has not configured yet' % db_name
            return None
        return db_config

    @staticmethod
    def _get_connect_info(db_config, sql_type):
        if not isinstance(db_config, str) and db_config.startswith(sql_type):
            print 'connect info is wrong, make sure the format is {sql_type}://username:password@host:port/db'. \
                format(sql_type=sql_type)
            return dict()
        pattern = re.compile("{sql_type}.*?//(.*?)/(.*?)$".format(sql_type=sql_type))
        find_result, db = re.findall(pattern, db_config)[0]
        user, password_and_host, port = find_result.split(':')

        # 密码中可能包含多个@
        password_host_list = password_and_host.split('@')
        host = password_host_list[-1]
        passwd = ''
        for x in password_host_list[:-1]:
            passwd = passwd + x + '@'
        passwd = passwd[:-1]

        connect_info = dict()
        connect_info['user'] = user
        connect_info['passwd'] = passwd
        connect_info['host'] = host
        connect_info['port'] = int(port)
        connect_info['db'] = db
        connect_info['charset'] = 'utf8'
        return connect_info


class MySqlHandler(DBHandler):

    def _operator_db_by_mysql(self, db_config, sql):
        db_info = self._get_connect_info(db_config=db_config, sql_type=MYSQL_TYPE)
        if sql.lower().startswith('select'):
            try:
                connection = mysql.connect(**db_info)
            except Exception as e:
                print "Connect to db failed, %s, connect info is %s\n" % (e, db_info)
                return None
            cursor = connection.cursor(mysql.cursors.DictCursor)
            try:
                cursor.execute(sql)
            except Exception as e:
                print "execute sql failed, %s, sql is %s\n" % (e, sql)
                connection.rollback()
                return None
            return cursor.fetchall()
        else:
            with mysql.connect(**db_info) as cursor:
                cursor.execute(sql)
                if sql.lower().startswith('insert'):
                    result = cursor.lastrowid
                    return result
                else:
                    return None

    def call(self, db_name, sql):
        db_config = self._get_config(db_name=db_name)
        if True:
            execute_result = self._operator_db_by_mysql(db_config=db_config, sql=sql)
        return execute_result
