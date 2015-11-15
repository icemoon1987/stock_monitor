#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append("..")
from define import *

class stock_data(object):

    def __init__(self):
        self.date = ""
        self.open_price = 0.0
        self.close_price = 0.0
        self.high_price = 0.0
        self.low_price = 0.0
        self.volumn = 0

        return

    def parse_from_str(self, str_in, delim=","):
        ary = str_in.strip().split(delim)

        self.date = ary[DATE_POS]
        self.open_price = float(ary[OPEN_PRICE_POS])
        self.close_price = float(ary[CLOSE_PRICE_POS])
        self.high_price = float(ary[HIGH_PRICE_POS])
        self.low_price = float(ary[LOW_PRICE_POS])
        self.volumn = int(ary[VOLUMN_POS])

    def __str__(self):

        result = "%s,%s,%s,%s,%s,%s\n" % \
                (str(self.date), str(self.open_price), str(self.high_price), str(self.close_price),\
                str(self.low_price), str(self.volumn)) 

        return result

if __name__ == "__main__":

    stock = stock_data()
    print stock

    stock.parse_from_str("date1,0.1,0.2,0.3,0.4,5")
    print stock

