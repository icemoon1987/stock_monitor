#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append("..")

class fix_investment_data(object):
    def __init__(self):
        self.no = 0
        self.date = ""
        self.code = ""
        self.name = ""
        self.net = 0.0
        self.sum_month_money = 0.0
        self.month_share = 0.0
        self.share = 0.0
        self.sum = 0.0
        self.month_money = 0.0
        self.profit = 0.0
        self.profit_rate = 0.0
        return

    def get_last_result(self, file_name, delim="|"):
        f = open(file_name, "r")
        line = f.readline()
        f.close()
        arr = line.strip().split(delim)
        self.no = int(arr[0])
        self.date = arr[1]
        self.code = arr[2]
        self.name = arr[3]
        self.net = arr[4]
        self.month_money = float(arr[5])
        self.sum_month_money = float(arr[6])
        self.month_share = float(arr[7])
        self.share = float(arr[8])
        self.sum = float(arr[9])
        self.profit = float(arr[10])
        self.profit_rate = float(arr[11])
        return




