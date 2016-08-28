#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append("..")
from data_fetcher.stock_fetcher import stock_fetcher
from data_interface.stock_dataset import stock_dataset
from data_interface.stock_data import stock_data
from model.turtle import turtle
from datetime import datetime,timedelta
import mail
from define import *

reload(sys)
sys.setdefaultencoding('utf-8')

class turtle_monitor:
    def __init__(self):
        return

    # def monitor(self, code, filename, delim):
    def monitor(self, code):
        data_set = stock_dataset()
        data_set.load_from_file(code, "../data/" + code)

        # fetcher = stock_fetcher()
        # net = fetcher.get_present_price(code).close_price


        # stock = stock_data()
        # stock.close_price = net
        # today = datetime.now().strftime("%Y-%m-%d")

        # today = datetime.now() - timedelta(days = 2)  #周末测试时使用
        today = datetime.now()
        today = today.strftime("%Y-%m-%d")

        # stock.date = today
        # data_set.data.append(stock)

        turtle_plan3 = turtle()
        result = turtle_plan3.get_trading_plan3(data_set, today)
        result["code"] = code

        # f = open(filename, "r+")
        # line = f.readline()
        # arr = line.strip().split(delim)
        # print "arr:", arr
        # share = arr[2]
        # money = arr[3]
        # profit = arr[4]
        # if(result["choise"] == 4):  #buy
        #     result["share"] = round((money * (1 - DEAL_RATE) / result["close_price"]), 3)
        #     result["money"] = round(money * (1 - DEAL_RATE), 3)
        #     result["profit"] = profit
        #     self.append_result_to_file(filename, result, delim)
        # elif(result["choise"] == 2): #sell
        #     result["share"] = share
        #     result["money"] = round(result["close_price"] * share * (1 - DEAL_RATE), 3)
        #     result["profit"] = result["money"] - money
        #     self.append_result_to_file(filename, result, delim)
        return result


    def append_result_to_file(self, filename, result, delim):
        # 交易时间|交易价格|交易份额|交易金额|利润|操作方向
        line = result["date"] + delim + result["close_price"] + delim + result["share"] + delim + result["money"] + delim + \
            result["profit"] + delim + result["info"] + "\n"
        print line
        f = open(filename, "r+")
        content = f.read()
        f.seek(0)
        f.write(line + content)
        f.close()

    def format_format_result(self, result):
        detail = "today: " + result["date"] + "<br/>code:" + result["code"] + "<br/>file_end_date:" + result["end_date"] + \
                 "<br/>BUY_DAYS:" + result["BUY_DAYS"] + "<br/>SELL_DAYS:" + result["SELL_DAYS"] + \
                 "<br/>start_buy_date:" + result["start_buy_date"] + "<br/>start_sell_date:" + result["start_sell_date"] + \
                 "<br/>close_price: " + str(result["close_price"]) + "<br/>choise:" + result["info"] + "<br/>"
        if(result["choise"] >= 0):
            detail += "max_date: " + str(result["max_date"]) + "<br/>min_date:" + str(result["min_date"])
        return detail


if __name__ == "__main__":
    tmonitor = turtle_monitor()
    code = "sh000300"  #沪深300
    result = tmonitor.monitor(code, "../result/turtle3_result", "|")

    """
    choise:
        -3:	not enough data, do not trade
        -2:	date_str error
        -1:	unknown problem, do not trade
        0:	sell all
        1:	sell half
        2:	close_price unsatisfy, do not trade
        3:	mean line unsatisfy, do not trade
        4:	buy
     """
    detail = tmonitor.format_format_result(result)
    #
    # mail.sendmail(['sunada2005@163.com'], "轮动模型结果(耐你滴老公~)",detail.encode("utf-8", "ignore"))
    print detail

