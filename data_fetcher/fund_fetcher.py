#!/usr/bin/env python
#coding=utf-8

import sys
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

            url = "http://biz.finance.sina.com.cn/fund/flash_hq/kline_data.php?symbol=%s&begin_date=%s&end_date=%s" % (fundid, begindate, enddate)
            data = urllib.urlopen(url).read()
            tree = etree.HTML(data)

            contents = tree.xpath("//control/content")

            for content in contents:
                tmp = {}
                date = content.xpath("./@d")[0]
                open_price = content.xpath("./@o")[0]
                high_price = content.xpath("./@h")[0]
                close_price = content.xpath("./@c")[0]
                low_price = content.xpath("./@l")[0]
                volumn = content.xpath("./@v")[0]

                tmp["date"] = date
                tmp["open_price"] = open_price
                tmp["high_price"] = high_price
                tmp["close_price"] = close_price
                tmp["low_price"] = low_price
                tmp["volumn"] = volumn

                result.append(tmp)

        except Exception, ex:
            print ex.__str__()
            return {}

        return result


    def store_to_file(self, result, file_path):

        try:
            f = open(file_path, 'w')

            for item in result:
                f.write("%s,%s,%s,%s,%s,%s\n" % \
                    (str(item["date"]), str(item["open_price"]), str(item["high_price"]), str(item["close_price"]),\
                    str(item["low_price"]), str(item["volumn"])) )

            f.close()

        except Exception, ex:
            print ex.__str__()

        return

if __name__ == "__main__":

    """
    if len(sys.argv) >= 4:
        fetcher = fund_fetcher()
        result = fetcher.get_his_day_k(sys.argv[1], sys.argv[2], sys.argv[3])
        print result

    if len(sys.argv) == 5:
        fetcher.store_to_file(result, sys.argv[4])
        print "store to file: " + sys.argv[1]
    """
    
