#!/usr/bin/env python
#coding=utf-8
__author__ = 'Administrator'
import json
import datetime
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class small_market_value_monitor:
    def __init__(self):
        self.__period = 20

    def get_last_deal_date(self):
        tmp = "../result/small_market_value"
        with open(tmp, 'r') as f:
            lines = f.readlines()
            line = lines[-1]
            deal = json.loads(line)
            date = datetime.datetime.strptime(deal["date"], "%Y-%m-%d")
            return date

    def next_date(self):
        next_date = self.get_last_deal_date()
        for i in range(self.__period):
            next_date += datetime.timedelta(days=1)
            while not self.is_trade_date(next_date):
                next_date += datetime.timedelta(days=1)
        return next_date

    def is_trade_date(self, date):
        if date.weekday() == 5 or date.weekday() == 6:
            return False

        holidays = ["2017-01-27","2017-01-30","2017-01-31","2017-02-02","2017-02-01","2017-04-03","2017-04-04",
                    "2017-05-01","2017-05-29","2017-05-30","2017-10-02","2017-10-03","2017-10-04","2017-10-05",
                    "2017-10-06"]

        if date.strftime("%Y-%m-%d") in holidays:
            return False
        return True

    def format_format_html_result(self):
        detail = ""
        detail += "<p>上次交易日期为：" + str(self.get_last_deal_date()) + "<br/>"
        detail += "建议下次交易日期：" + str(self.next_date()) + "</p>"
        return detail


if __name__ == '__main__':
    smvm = small_market_value_monitor()
    print smvm.next_date()
    # print smvm.get_last_deal_date()