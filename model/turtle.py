#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append("..")
import urllib
import myjson
from datetime import *
import time 
from define import *

class turtle(object):
    """
    turtle model
    """

    def get_mean(self, data, end_index, k):
        if end_index < k-1:
            return 0
        else:
            sum = 0
            for num in data[end_index-k+1 : end_index+1]:
                sum += num

        return float(sum / (k * 1.0))


    def get_max(self, data, end_index, k):
        if end_index < k:
            return 0
        else:
            tmp = data[end_index-k : end_index]
            max = tmp[0]

            for num in tmp:
                if num > max:
                    max = num
        return max

    def get_max_date(self, dataset, end_index, k):
        if end_index < k:
            return 0
        else:
            tmp = dataset.data[end_index-k : end_index]
            max = tmp[0].close_price
            date = tmp[0].date

            for num in tmp:
                if num.close_price > max:
                    max = num.close_price
                    date = num.date

            return (max, date)

    def get_min(self, data, end_index, k):
        if end_index < k:
            return 0
        else:
            tmp = data[end_index-k : end_index]
            min = tmp[0]

            for num in tmp:
                if num < min:
                    min = num
        return min

    def get_min_date(self, dataset, end_index, k):
        if end_index < k:
            return 0
        else:
            tmp = dataset.data[end_index-k : end_index]
            min = tmp[0].close_price
            date = tmp[0].date

            for num in tmp:
                if num.close_price < min:
                    min = num.close_price
                    date = num.date
        return (min, date)

    def get_trading_plan(self, dataset, date_str):
        """
        get trading plan of 28 lundong model, return a empty map when no decision can be made

        choise:
            -3:	not enough data, do not trade
            -2:	date_str error
            -1:	unknown problem, do not trade
            0:	sell all
            1:	sell half
            2:	close_price unsatisfy, do not trade
            3:	mean line unsatisfy, do not trade
            4:	buy

        策略：
            1. 我只将此交易模型用于小时图
            2. 一般也只用于趋势性较强的大盘指数，不用于个股
            3. 首先绘制10小时和100小时两根无线，然后绘制50小时最高点和最低点曲线，再加25小时内最低点曲线（如果你使用通达信，可直接复制我下面的指标源代码，记得设为图叠加）。
            4. 买入条件：当且仅当10小时无线大于100小时均线的前提下，小时收盘突破此前50小时的最高点时做多。
            5. 平仓条件：当小时收盘跌破此前25小时的最低点时平仓一半，跌破此前50小时最低点时全部平仓。
        """
        result = {}
        result["choise"] = -1
        # Get stock data by date_str. If not exist, return.
        data = dataset.get_data(date_str)
        if data == None:
            result["choise"] = -2
            return result

        data_index = dataset.get_data_index(date_str)
        close_prices = [ item.close_price for item in dataset.data ]
        result["close_price"] = close_prices[data_index]
        result["10_mean"] = self.get_mean(close_prices, data_index, 10)
        result["100_mean"] = self.get_mean(close_prices, data_index, 100)
        result["50_max"] = self.get_max(close_prices, data_index, 50)
        result["50_min"] = self.get_min(close_prices, data_index, 50)
        result["25_min"] = self.get_min(close_prices, data_index, 25)
        if result["10_mean"] == 0 or result["100_mean"] == 0 or result["50_max"] == 0 or result["50_min"] == 0 or result["25_min"] == 0:
            result["choise"] = -3
        elif result["close_price"] < result["50_min"]:
            result["choise"] = 0
        elif result["close_price"] < result["25_min"]:
            result["choise"] = 1
        elif result["close_price"] > result["50_max"]:
            if result["10_mean"] < result["100_mean"]:
                result["choise"] = 3
            else:
                result["choise"] = 4
        else:
            result["choise"] = 2
        return result

    def get_trading_plan3(self, dataset, date_str):
        """
        策略
            1. 买入条件：收盘价超过60个交易日里面的盘中最高价（不是收盘价中的最高）
            2. 卖出条件：收盘价低于38个交易日里面的盘中最低价
            3. 其他时候维持原状。

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
        # Get stock data by date_str. If not exist, return.
        result = {}
        result["end_date"] = dataset.data[-1].date
        result["start_buy_date"] = dataset.data[0 - BUY_DAYS].date
        result["start_sell_date"] = dataset.data[0 - SELL_DAYS].date
        result["date"] = date_str
        result["choise"] = -1
        result["info"] = "unknown problem, do not trade"
        data = dataset.get_data(date_str)
        if data == None:
            result["choise"] = -2
            result["info"] = "date_str error"
            return result

        data_index = dataset.get_data_index(date_str)

        result["close_price"] = dataset.data[data_index].close_price
        result["max_date"] = self.get_max_date(dataset, data_index, BUY_DAYS)
        result["min_date"] = self.get_min_date(dataset, data_index, SELL_DAYS)
        if result["close_price"] > result["max_date"][0]:
            result["choise"] = 4
            result["info"] = "buy"
        elif result["close_price"] < result["min_date"][0]:
            result["choise"] = 0
            result["info"] = "sell all"
        elif result["close_price"] < result["max_date"][0] or result["close_price"] > result["min_date"][0]:
            result["choise"] = 2
            result["info"] = "hold on"
        return result

if __name__ == '__main__':
    pass

