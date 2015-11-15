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

class fund_fetcher(object):

    def __init__(self):
        return

    def get_his_day_k(self, fundid, begindate, enddate):

        raw_result = []

        try:
            begindate_str = datetime.strptime(begindate, "%Y%m%d").strftime("%Y-%m-%d")
            enddate_str = datetime.strptime(enddate, "%Y%m%d").strftime("%Y-%m-%d")

            url = "http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=%s&page=1&per=5000&sdate=%s&edate=%s&rt=0.7955276783627965"\
                % (fundid, begindate_str, enddate_str)

            data = urllib.urlopen(url).read()
            m = re.match(r'.*content:"(.*)"', data)
            html_data = m.group(1)
            tree = etree.HTML(html_data)
            contents = tree.xpath("//tbody/tr")

            for content in contents:
                try:
                    tmp = {}
                    date = content.xpath("./td/text()")[0]
                    close_price = float(content.xpath("./td/text()")[1])
                    acc_close_price = float(content.xpath("./td/text()")[2])
                    rise_rate = float(content.xpath("./td/text()")[3][:-1]) / 100
                    buy_status = content.xpath("./td/text()")[4]
                    sell_status = content.xpath("./td/text()")[5]
                    #meta = content.xpath("./td/text()")[6]

                    tmp["date"] = date
                    tmp["close_price"] = close_price
                    tmp["acc_close_price"] = acc_close_price
                    tmp["rise_rate"] = rise_rate
                    tmp["buy_status"] = buy_status
                    tmp["sell_status"] = sell_status
                    #tmp["meta"] = meta

                    raw_result.append(tmp)
                except Exception, ex:
                    continue

        except Exception, ex:
            print ex.__str__()
            return None

        raw_result.reverse()
        for i in range(len(raw_result)):
            if i != 0:
                raw_result[i]["acc_close_price"] = raw_result[i-1]["acc_close_price"] * (1 + raw_result[i]["rise_rate"])

        dataset = stock_dataset()
        dataset.name = fundid

        for item in raw_result:
            stock = stock_data()
            stock.date = item["date"]
            stock.close_price = item["acc_close_price"]

            dataset.data.append(stock)

        return dataset


if __name__ == "__main__":

    fetcher = fund_fetcher()

    result = fetcher.get_his_day_k("270026", "20001101", "20151115")

    result.dump()


    
