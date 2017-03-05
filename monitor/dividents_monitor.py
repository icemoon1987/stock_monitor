#!/usr/bin/env python
#coding=utf-8
__author__ = 'Administrator'
import urllib2
import urllib
import myjson
import time

class Dividents_monitor:
    def __init__(self):
        self.cnt = 4
        self.total_value = 10
        self.volume = 1000
        self.pe = 0
        self.eps_year = 3

    def get_stocks_from_jisilu(self, cnt):
        url = "https://www.jisilu.cn/data/stock/dividend_rate_list/?___t=" + str(int(time.time() * 1000))
        data = urllib.urlopen(url).read()
        json_obj = myjson.read(data)
        stocks = json_obj['rows'][0:cnt]
        return stocks

    def pick_best_stocks(self, cnt):
        stocks = self.get_stocks_from_jisilu(2 * cnt)
        res = []
        for stock in stocks:
            cell = stock["cell"]
            if float(cell["total_value"]) <= self.total_value:
                continue
            if float(cell["volume"]) <= self.volume:
                continue
            if float(cell["pe"]) <= self.pe:
                continue
            res.append(stock)
        return res

    def res_to_html(self):
        res = self.pick_best_stocks(self.cnt)
        lines = []
        tmp = '<table border="1">'
        for line in res:
            ary = line.decode("utf-8").split(",")
            tmp += "<tr>"
            tmp += "<td>" + "</td><td>".join(ary) + "</td>"
            tmp += "</tr>"
        tmp += "</table>"
        return tmp

if __name__ == "__main__":
    d = Dividents_monitor()
    res = d.pick_best_stocks(d.cnt)
    # print res
    for r in res:
        print r["cell"]["stock_id"]
