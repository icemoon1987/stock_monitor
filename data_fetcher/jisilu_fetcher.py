#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append("..")
import re
import urllib
import myjson
from datetime import datetime
import  time 
from lxml import etree
from data_interface.stock_dataset import stock_dataset
from data_interface.stock_data import stock_data

class jisilu_fetcher(object):

    def __init__(self):
        return

    def get_a_level_fund_list(self):

        result = []

        try:
            url = "http://www.jisilu.cn/data/sfnew/funda_list/?___t=" + str(int(time.time() * 1000))
            data = urllib.urlopen(url).read()

            json_obj = myjson.read(data)
            contents = json_obj["rows"]

            for content in contents:
                try:
                    tmp = {}
                    tmp["id"] = content["id"]
                    tmp["name"] = content["cell"]["funda_name"]
                    tmp["left_year"] = content["cell"]["funda_left_year"]
                    tmp["descr"] = content["cell"]["fund_descr"]
                    tmp["profit_rate"] = content["cell"]["funda_profit_rt_next"]
                    tmp["price"] = content["cell"]["funda_current_price"]

                    result.append(tmp)

                except Exception, ex:
                    print ex.__str__()
                    continue

        except Exception, ex:
            print ex.__str__()
            return None

        return result


if __name__ == "__main__":

    fetcher = jisilu_fetcher()

    result = fetcher.get_a_level_fund_list();

    print result
