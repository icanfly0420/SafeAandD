#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# Author: QianTian
from SqllinjectionTime import TimeInjector
import json

method_dict = {
    "time": TimeInjector
}


class Injector:
    def __init__(self):
        self.method = ''
        self.domain = ''
        self.suffix = ''
        self.cookies = ''
        self.str = ''
        print("## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##\n")
        print("#                       SQLInjector                          #\n")
        print("#                     Author: QianTian                       #\n")
        print("## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##\n")
        while True:
            string = input(">>>>> ")
            if string == 'run':
                if self.method == "" or \
                        self.domain == "":
                    print("Don't have enough options")
                    continue
                else:
                    subject = method_dict[self.method](self.domain,self.cookies,self.str,self.suffix)
            elif string == 'exit':
                break
            else:
                try:
                    strs = string.split(" ", 2)
                    if strs[0] == 'set':
                        self.set_value(strs[1], strs[2])
                    elif strs[0] == 'show' and strs[1] == 'options':
                        self.show_options()
                    else:
                        print("No Command")
                except Exception as ex:
                    print("No Command")

    def show_options(self):
        print("method  : ", f"{self.method}")
        print("domain  : ", f"{self.domain}")
        print("cookies : ", f"{self.cookies}")
        print("str     : ", f"{self.str}")
        print("suffix  : ", f"{self.suffix}")

    def set_value(self, key, value):
        if key == "method":
            self.method = value
        elif key == "domain":
            self.domain = value
        elif key == "str":
            self.str = value
        elif key == "suffix":
            self.suffix = value
        elif key == "cookies":
            self.cookies = json.loads(value)


if __name__ == '__main__':
    a = Injector()
