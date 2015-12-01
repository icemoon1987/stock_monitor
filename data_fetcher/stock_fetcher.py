#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append("..")
import urllib
import myjson
from datetime import datetime
import time 
from lxml import etree
from data_interface.stock_dataset import stock_dataset
from data_interface.stock_data import stock_data
import re

class stock_fetcher(object):

    def __init__(self):
        self.repeat_num = 3
        self.wait_gap = 1
        return

    def get_his_day_k(self, stockid, begindate, enddate):

        result = stock_dataset()
        result.name = stockid

        i = 0
        while i < self.repeat_num:
            try:
                url = "http://biz.finance.sina.com.cn/stock/flash_hq/kline_data.php?symbol=%s&begin_date=%s&end_date=%s" % (stockid, begindate, enddate)
                data = urllib.urlopen(url).read()
                tree = etree.HTML(data)

                contents = tree.xpath("//control/content")

                for content in contents:
                    stock = stock_data()
                    stock.date = content.xpath("./@d")[0]
                    stock.open_price = float(content.xpath("./@o")[0])
                    stock.high_price = float(content.xpath("./@h")[0])
                    stock.close_price = float(content.xpath("./@c")[0])
                    stock.low_price = float(content.xpath("./@l")[0])
                    stock.volumn = int(content.xpath("./@v")[0])

                    result.data.append(stock)

                break

            except Exception, ex:
                print ex.__str__()
                time.sleep(self.wait_gap)
                i = i + 1
                if i == self.repeat_num:
                    return None

        return result


    def get_his_hour_k(self, stockid):

        result = stock_dataset()
        result.name = stockid

        i = 0
        while i < self.repeat_num:
            try:
                url = "http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=%s&scale=60&ma=no&datalen=1023" % (stockid)
                data = urllib.urlopen(url).read()
                
                data = data[2:-2]

                ary = data.split("},{")

                print len(ary)

                for item in ary:
                    stock = stock_data()

                    m = re.match(r'.*day:"(.*?)"', item)
                    stock.date = m.group(1)

                    m = re.match(r'.*open:"(.*?)"', item)
                    stock.open_price = float(m.group(1))

                    m = re.match(r'.*high:"(.*?)"', item)
                    stock.high_price = float(m.group(1))

                    m = re.match(r'.*close:"(.*?)"', item)
                    stock.close_price = float(m.group(1))

                    m = re.match(r'.*low:"(.*?)"', item)
                    stock.low_price = float(m.group(1))

                    m = re.match(r'.*volume:"(.*?)"', item)
                    stock.volumn = int(m.group(1))

                    result.data.append(stock)
                break

            except Exception, ex:
                print ex.__str__()
                time.sleep(self.wait_gap)
                i = i + 1
                if i == self.repeat_num:
                    return None

        return result

    def get_present_price(self, stockid):

        stock = stock_data()

        i = 0
        while i < self.repeat_num:
            try:
                url = "http://hq.sinajs.cn/list=%s" % (stockid)
                data = urllib.urlopen(url).read()

                m = re.match(r'.*="(.*)"', data)
                data = m.group(1)

                ary = data.strip().split(",")

                stock.date = ary[30]
                stock.open_price = float(ary[1])
                stock.high_price = float(ary[4]) 
                stock.close_price = float(ary[3])
                stock.low_price = float(ary[5])
                stock.volumn = int(ary[8])

                break
     
            except Exception, ex:
                print ex.__str__()
                time.sleep(self.wait_gap)
                i = i + 1
                if i == self.repeat_num:
                    return None

        return stock


if __name__ == "__main__":
    fetcher = stock_fetcher()
    #result = fetcher.get_his_day_k("sh000300", "20001101", "20151115")
    #result.dump()
    #stock = fetcher.get_present_price("sh000300")
    #print stock

    result = fetcher.get_his_hour_k("sh000300")
    #result.dump()

