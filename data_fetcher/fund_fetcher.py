#!/usr/bin/env python
#coding=utf-8

import sys
import re
import urllib
import myjson
from datetime import datetime
import  time 
from lxml import etree

class fund_fetcher(object):

    def __init__(self):
        return

    def get_his_day_k(self, fundid, begindate, enddate):

        result = []

        try:
            begindate_str = datetime.strptime(begindate, "%Y%m%d").strftime("%Y-%m-%d")
            enddate_str = datetime.strptime(enddate, "%Y%m%d").strftime("%Y-%m-%d")

            url = "http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=%s&page=1&per=5000&sdate=%s&edate=%s&rt=0.7955276783627965"\
                % (fundid, begindate_str, enddate_str)

            print url

            data = urllib.urlopen(url).read()

            m = re.match(r'.*content:"(.*)"', data)
            #m = re.match(r'.*', data)

            html_data = m.group(1)

            tree = etree.HTML(html_data)

            contents = tree.xpath("//tbody/tr")

            for content in contents:

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

                result.append(tmp)

        except Exception, ex:
            print ex.__str__()
            return {}

        return result


    def post_process(self, data_list):
        data_list.reverse()

        for i in range(len(data_list)):
            if i != 0:
                data_list[i]["acc_close_price"] = data_list[i-1]["acc_close_price"] * (1 + data_list[i]["rise_rate"])

        return result


    def store_to_file(self, result, file_path):

        try:
            f = open(file_path, 'w')

            for item in result:
                f.write("%s,%s,%s,%s,%s,%s\n" % \
                    (str(item["date"]), "0", "0", str(item["acc_close_price"]),\
                    "0", "0")) 

            f.close()

        except Exception, ex:
            print ex.__str__()

        return

if __name__ == "__main__":

    if len(sys.argv) >= 4:
        fetcher = fund_fetcher()
        result = fetcher.get_his_day_k(sys.argv[1], sys.argv[2], sys.argv[3])

        print result

        fetcher.post_process(result)

        print result

    if len(sys.argv) == 5:
        fetcher.store_to_file(result, sys.argv[4])
        print "store to file: " + sys.argv[1]
    
