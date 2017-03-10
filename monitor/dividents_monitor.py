#!/usr/bin/env python
#coding=utf-8
__author__ = 'Administrator'
import urllib2
import urllib
import json
import time
import os
import pandas as pd
import tushare as ts
import datetime
import mail

class Dividents_monitor:
    def __init__(self):
        self.cnt = 5
        self.total_value = 10
        self.volume = 1000
        self.npr = 0

    def get_stocks_from_jisilu(self, cnt):
        url = "https://www.jisilu.cn/data/stock/dividend_rate_list/?___t=" + str(int(time.time() * 1000))
        data = urllib.urlopen(url).read()
        json_obj = json.loads(data)
        stocks = json_obj['rows'][0:cnt]
        return stocks

    '''
    流动性要求：20日均量不小于1000万
    流通股本不少于10亿
    利润率：公司的净利润必须为正。
    '''
    def pick_best_stocks(self, cnt):
        stocks = self.get_stocks_from_jisilu(2 * cnt)
        res = ["code,name,pb,pe,eps_growth_ttm,industry,dividend,roe"]

        if not os.path.exists("stock_basics.txt"):
            lc = ts.get_stock_basics()
            lc.to_csv('stock_basics.txt',encoding="utf-8")
        stock_basics = pd.read_csv('stock_basics.txt',dtype=str,encoding='utf-8')

        for stock in stocks:
            stock_id = stock["cell"]['stock_id']
            today = datetime.datetime.today().strftime("%Y-%m-%d")
            df = ts.get_hist_data(stock_id,start=today, end=today)
            #20天平均交易额
            if df.empty or (df.loc[today]['v_ma20'] < self.volume):
                # print "volum:", stock_id
                continue
            #流通股本
            if stock_basics.query("code=='"+stock_id+"'")['outstanding'].iloc[0] < self.total_value:
                # print "total_value:", stock_id
                continue
            #利润率
            if stock_basics.query("code=='"+stock_id+"'")['npr'].iloc[0] < self.npr:
                continue

            obj = stock["cell"]
            tmp = ""
            tmp += obj["stock_id"] + ","
            tmp += obj["stock_nm"] + ","
            tmp += obj["pb"] + ","
            tmp += obj["pe"] + ","
            tmp += obj["eps_growth_ttm"] + ","
            tmp += str(stock_basics.query("code=='"+stock_id+"'")['industry'].iloc[0]) + ","
            tmp += obj["dividend_rate"] + ","
            tmp += obj["roe_ttm"]
            res.append(tmp)
        return res

    def format_format_html_result(self):
        res = self.pick_best_stocks(self.cnt)
        tmp = '<table border="1">'
        for line in res:
            ary = line.split(",")
            tmp += "<tr>"
            tmp += "<td>" + "</td><td>".join(ary) + "</td>"
            tmp += "</tr>"
        tmp += "</table>"
        return tmp

if __name__ == "__main__":
    d = Dividents_monitor()
    res = d.pick_best_stocks(d.cnt)
    # print res
    # for r in res:
    #     print r
    mail_detail = d.format_format_html_result()
    mail.sendhtmlmail(['sunada2005@163.com'], "轮动模型结果(耐你滴老公~)",mail_detail.encode("utf-8", "ignore"))
