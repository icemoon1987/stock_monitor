#!/usr/bin/env python
#coding=utf-8
__author__ = 'Administrator'
import json
import datetime
import sys
import pandas as pd
import tushare as ts
import re
import mail

reload(sys)
sys.setdefaultencoding('utf-8')

class small_market_value_monitor:
    def __init__(self):
        self.__period = 20
        self.__amount = 20000
        self.__stock_cnt = 5
        self.__stRegex = re.compile(r"^[^\*ST.*]")
        self.__stocks = pd.DataFrame()

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

    def get_stock_by_mktcap(self):
        lc = ts.get_today_all()
        # lc.to_csv('a.txt',encoding="utf-8")
        # lc = pd.read_csv('a.txt',encoding='utf-8')
        lc_amount = lc.query('amount>10000000')  #交易额大于1kw
        lc_amount_except_ST = lc_amount[(lc_amount['name'].str.contains(self.__stRegex, regex=True))]
        res = lc_amount_except_ST.sort_values(by="mktcap").head(self.__stock_cnt * 3)
        # print res
        res = res[['code','name','trade','amount','mktcap']]
        # print res
        return res

    def get_profit(self, stocks):
        stock_basics = ts.get_stock_basics()
        # stock_basics.to_csv("b.txt", encoding='utf-8')
        # stock_basics = pd.read_csv("b.txt", encoding="utf-8")
        stock_basics.reset_index()
        return pd.merge(stocks, stock_basics, how="left", left_on="code", right_on="code")

    def choose_stocks_by_amount_limit(self, stocks):
        tmp = self.__amount / self.__stock_cnt
        res = stocks.query("trade * 100 + 5 < " + str(tmp))
        # res = stocks
        res = res.sort_values(by="mktcap").head(self.__stock_cnt)
        return res[['code','name_x','trade','pb','pe']]

    def get_target(self):
        res = self.get_stock_by_mktcap()
        result = self.get_profit(res)
        result = result.query('pe>0')
        result = result.sort_values(by="mktcap").head(self.__stock_cnt + 2)[['code','name_x','trade','pb','pe','mktcap']]
        self.__stocks = self.choose_stocks_by_amount_limit(result)
        print self.__stocks

    def format_format_html_result(self):
        self.get_target()
        detail = ""
        detail += "<p>上次交易日期为：" + str(self.get_last_deal_date()) + "<br/>"
        detail += "建议下次交易日期：" + str(self.next_date()) + "</p>"
        detail += "本日调仓建议如下：<br/>"
        detail += self.dataframe_to_html(self.__stocks) + "<br/>"
        return detail

    def dataframe_to_html(self, dataframe):
        dataframe.to_csv("c.txt", encoding="utf-8")
        lines = open("c.txt")
        tmp = '<table border="1">'
        for line in lines:
            ary = line.strip().decode("utf-8").split(",")
            tmp += "<tr>"
            tmp += "<td>" + "</td><td>".join(ary) + "</td>"
            tmp += "</tr>"
        tmp += "</table>"
        return tmp


if __name__ == '__main__':
    smvm = small_market_value_monitor()
    # print smvm.next_date()
    # print smvm.get_last_deal_date()
    # smvm.get_target()
    mail_detail = smvm.format_format_html_result()
    # print mail_detail
    mail.sendhtmlmail(['sunada2005@163.com','516563458@qq.com'], "轮动模型结果(耐你滴老公~)",mail_detail.encode("utf-8", "ignore"))