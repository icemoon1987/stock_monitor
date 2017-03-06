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
        json_obj = json.loads(data)
        stocks = json_obj['rows'][0:cnt]
        return stocks

    '''
    Step1:市值与流动性考察
    （1）市值要求：指数调整参考日的自由流通市值不低于10亿人民币；
    （2）流动性要求：过去6个月的平均日交易额不低于1千万人民币；(此处使用20日均量替换）

         Step 2：盈利稳定性考察
    （1）利润率：公司过去12个月的净利润必须为正。
    （2）盈利增长：考察期的过去十二个月的每股盈利，即EPS（TTM）必须大于三年前的数据。

          Step 3:股息率排名，确定成分股。
    将前两步筛选出的股票池中的股票，按年度股息率排序，筛选股息率排名前100 的股票。构成成份股。

         Step 4:权重调整，指数诞生
    以股息率加权，每只股票的权重不得超过3%，单个行业的权重不超过33%。
    （1）个股权重：超过3%的部分需向权重低于3%的股票中权重最大的那一只移动，如果该股票也超过了3%，则重复该运作，使得没有股票的权重超过3%为止。
    （2）行业权重：若权重超过33%，则将多余部分移动到其他行业中权重低于3%的股票中，移动顺序根据与个股的调整法相同。
    '''
    def pick_best_stocks(self, cnt):
        stocks = self.get_stocks_from_jisilu(2 * cnt)
        res = []

        if not os.path.exists("stock_basics.txt"):
            lc = ts.get_stock_basics()
            lc.to_csv('stock_basics.txt',encoding="utf-8")
        stock_basics = pd.read_csv('stock_basics.txt',encoding='utf-8')

        for stock in stocks:
            stock_id = stock["cell"]['stock_id']
            today = datetime.datetime.today().strftime("%Y-%m-%d")
            df = ts.get_hist_data(stock_id,start=today, end=today)
            if df.loc[today]['v_ma20'] < self.volume:
                continue
            if stock_basics.query("code="+stock_id)['outstanding'] < self.total_value:
                continue
            if stock_basics[stock_id]['esp'] < self.eps_year:
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
        print r["cell"]
