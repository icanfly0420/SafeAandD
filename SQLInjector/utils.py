#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# Author: QianTian
from configparser import ConfigParser
import time


def timer(func, url, cookies):
    if cookies:
        statime = time.time()
        func(url,cookies=cookies)
        endtime = time.time()
        return endtime - statime
    else:
        statime = time.time()
        func(url)
        endtime = time.time()
        return endtime - statime
