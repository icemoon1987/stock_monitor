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

        #把今天的数据加入到data_set里
        fetcher = stock_fetcher()
        net = fetcher.get_present_price(code).close_price
        stock = stock_data()
        stock.close_price = net
        # today = datetime.now() - timedelta(days = 2)  #周末测试时使用
        today = datetime.now()
        today = today.strftime("%Y-%m-%d")
        stock.date = today
        data_set.data.append(stock)

        turtle_plan3 = turtle()
        result = turtle_plan3.get_trading_plan3(data_set, today)
        result["code"] = code

        f = open("../result/turtle3_result", "r+")
        line = f.readline()
        f.close()
        if line.startswith("#"):
            return result
        arr = line.strip().split("|")
        print "arr:", arr
        share = arr[5]
        cost = arr[6]
        result["share"] = share
        result["cost"] = cost
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
        detail = "今天: " + result["date"] + "<br/>追踪指数:" + result["code"] + "<br/>最近加入文件的数据对应的交易日:" + result["file_end_date"] + \
                 "<br/>BUY_DAYS:" + result["BUY_DAYS"] + "<br/>SELL_DAYS:" + result["SELL_DAYS"] + \
                 "<br/>start_buy_date:" + result["start_buy_date"] + "<br/>start_sell_date:" + result["start_sell_date"] + \
                 "<br/>现在点位: " + str(result["close_price"]) + "<br/>操作建议: " + result["info"] + \
                 "<br/>仓位：" + str(result["share"]) + "<br/>金额：" + result["cost"] + "<br/>"
        if(result["choise"] >= 0):
            detail += result["BUY_DAYS"] + "个交易日内的最高价:" + str(result["max_date"]) + "<br/>" + result["SELL_DAYS"] + "个交易日内的最低价:" + str(result["min_date"])
        # detail = "today: " + result["date"] + "<br/>code:" + result["code"] + "<br/>file_end_date:" + result["file_end_date"]
        return detail


if __name__ == "__main__":
    tmonitor = turtle_monitor()
    code = "sh000300"  #沪深300
    result = tmonitor.monitor(code)

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
    mail.sendhtmlmail(['sunada2005@163.com'], "轮动模型结果(耐你滴老公~)",detail.encode("utf-8", "ignore"))
    # print detail

