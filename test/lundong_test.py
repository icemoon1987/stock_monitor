#!/usr/bin/env python
#coding=utf-8

import sys
reload(sys)
sys.path.append("..")
sys.setdefaultencoding('utf-8')

from pylab import *
mpl.rcParams["font.sans-serif"] = ["SimHei"]
mpl.rcParams["axes.unicode_minus"] = False

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from model.lundong import lundong
from define import *
from account_simulator import account_simulator
import math
from datetime import datetime, timedelta

import matplotlib.cbook as cbook

def load_data(file_path):
    """
    load stock data from a file
    """
    result = []
    print "loading: " + file_path

    f = open(file_path)

    for line in f:
        line = line.decode("utf-8").strip()
        ary = line.split(",")

        if len(ary) != 6:
            continue
        result.append(ary)

    return result


def pre_process(data1, data2):
    """
    preprocess data, align two dataset based on date_str
    """

    i = 0
    while i < len(data1):
        date_str1 = data1[i][DATE_POS]
        flag = False

        for item2 in data2:
            date_str2 = item2[DATE_POS]
            if date_str1 == date_str2:
                flag = True
                break

        # Delete redundant data in dataset1
        if not flag:
            del data1[i]
        else:
            i = i + 1

    i = 0
    while i < len(data2):
        date_str2 = data2[i][DATE_POS]
        flag = False

        for item1 in data1:
            date_str1 = item1[DATE_POS]
            if date_str2 == date_str1:
                flag = True
                break

        # Delete redundant data in dataset2
        if not flag:
            del data2[i]
        else:
            i = i + 1

    return


def pre_process_2(data1, data2, start_date_str, end_date_str):

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    i = 0
    while i < len(data1):
        date1 = datetime.strptime(data1[i][DATE_POS], "%Y-%m-%d")

        # Delete redundant data in dataset1
        if date1 < start_date or date1 > end_date:
            del data1[i]
        else:
            i = i + 1

    i = 0
    while i < len(data2):
        date2 = datetime.strptime(data2[i][DATE_POS], "%Y-%m-%d")

        # Delete redundant data in dataset1
        if date2 < start_date or date2 > end_date:
            del data2[i]
        else:
            i = i + 1

    return


def test(data1, data2, data1_name, data2_name, start_money, gap_days, trading_day, show_pics):
    """
    lundong model test
    """

    print "Dataset1: %s, data_len=%d, start_date=%s, end_date=%s" % (data1_name, len(data1), data1[0][DATE_POS], data1[-1][DATE_POS])
    print "Dataset2: %s, data_len=%d, start_date=%s, end_date=%s" % (data2_name, len(data2), data2[0][DATE_POS], data2[-1][DATE_POS])

    # Preprocess datasets
    print "preprocessing datasets..."
    pre_process(data1, data2)

    print "Dataset1: %s, data_len=%d, start_date=%s, end_date=%s" % (data1_name, len(data1), data1[0][DATE_POS], data1[-1][DATE_POS])
    print "Dataset2: %s, data_len=%d, start_date=%s, end_date=%s" % (data2_name, len(data2), data2[0][DATE_POS], data2[-1][DATE_POS])

    # Get close price of two datasets and plot them
    data1_close_price = [ item[CLOSE_PRICE_POS] for item in data1 ]
    data2_close_price = [ item[CLOSE_PRICE_POS] for item in data2 ]

    dates = [ datetime.strptime(item[DATE_POS], "%Y-%m-%d") for item in data1]

    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    yearsFmt = mdates.DateFormatter("%Y-%m")

    #plt.figure(1)
    #plt.subplot(311)
    if show_pics:
        fig, ax = plt.subplots()
        ax.set_title("股指变化图")
        ax.plot(dates, data1_close_price, 'b-', dates, data2_close_price, 'r-')
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(yearsFmt)
        ax.xaxis.set_minor_locator(months)
        ax.legend([data1_name, data2_name], loc="upper left")
        ax.grid(True)
        ax.set_xlim(dates[0], dates[-1] + timedelta(days=90))
        #plt.xlim(0,len(data1_index)+50)
        plt.show()

    # Initilize a lundong model, and get trading decisions by it
    lundong_model = lundong()

    # the test start with a blank account
    account = account_simulator(start_money)
    money = []

    # record every trading plan
    result = []
    last_valid_trading_plan = {}

    for item in data1:
        trading_plan = lundong_model.get_trading_plan(data1, data2, data1_name, data2_name, item[DATE_POS], gap_days, trading_day, last_valid_trading_plan)

        # if there is a trading plan
        if trading_plan != {}:

            # choise == 0 means buy data1 and sell data2
            if trading_plan["choise"] == 0:

                # if we have data2, sell it
                stock = account.get_stock(data2_name)
                if stock != None and stock.share != 0:
                    account.sell(data2_name, trading_plan["data2_close_price"], stock.share)

                # buy data1 as many as we can
                account.buy(data1_name, trading_plan["data1_close_price"], int(math.floor(account.money / trading_plan["data1_close_price"])))

            # choise == 1 means sell data1 and buy data2
            elif trading_plan["choise"] == 1:

                # if we have data1, sell it
                stock = account.get_stock(data1_name)
                if stock != None and stock.share != 0:
                    account.sell(data1_name, trading_plan["data1_close_price"], stock.share)

                # buy data2 as many as we can
                account.buy(data2_name, trading_plan["data2_close_price"], int(math.floor(account.money / trading_plan["data2_close_price"])))

            # choise == 2 means sell all data2
            elif trading_plan["choise"] == 2:

                # if we have data1, sell it
                stock = account.get_stock(data1_name)
                if stock != None and stock.share != 0:
                    account.sell(data1_name, trading_plan["data1_close_price"], stock.share)

                # if we have data2, sell it
                stock = account.get_stock(data2_name)
                if stock != None and stock.share != 0:
                    account.sell(data2_name, trading_plan["data2_close_price"], stock.share)

            # other choises means do not trade
            else:
                pass
        # if there is no trading plan, do not trade
        else:
            pass

        money.append(account.get_value())
        #money.append(account.money)
        result.append(trading_plan)

        if trading_plan != {} and trading_plan["choise"] != -1:
            last_valid_trading_plan = trading_plan

    # Get rising rates, choises and plot them
    data1_up = []
    data2_up = []
    choise_0 = []
    choise_0_index = []
    choise_1 = []
    choise_1_index = []
    choise_2 = []
    choise_2_index = []

    i = 0
    for item in result:
        if item == {}:
            data1_up.append(0.0)
            data2_up.append(0.0)
        else:
            data1_up.append(item["data1_up"])
            data2_up.append(item["data2_up"])

            if item["choise"] == 0:
                choise_0.append(item["data1_up"])
                choise_0_index.append(dates[i])
            elif item["choise"] == 1:
                choise_1.append(item["data2_up"])
                choise_1_index.append(dates[i])
            elif item["choise"] == 2:
                choise_2.append(0)
                choise_2_index.append(dates[i])

        i = i + 1


    if show_pics:
        fig, ax = plt.subplots()
        ax.set_title("股指涨幅与模型交易方案")
        ax.plot(dates, data1_up, 'b-', dates, data2_up, 'r-',\
            choise_0_index, choise_0, 'bo', choise_1_index, choise_1, 'ro',\
            choise_2_index, choise_2, 'g^')
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(yearsFmt)
        ax.xaxis.set_minor_locator(months)
        ax.legend([data1_name, data2_name, "轮动到:" + data1_name, "轮动到:" + data2_name, "清仓"], loc="upper center")
        ax.grid(True)
        ax.set_xlim(dates[0], dates[-1] + timedelta(days=90))
        #plt.xlim(0,len(data1_index)+50)
        plt.show()

    if show_pics:
        fig, ax = plt.subplots()
        ax.set_title("投资收益对比")
        ax.plot(dates, [item / start_money for item in money], 'g-', \
            dates, [ float(item[CLOSE_PRICE_POS]) / float(data1[0][CLOSE_PRICE_POS]) for item in data1], 'b-', \
            dates, [ float(item[CLOSE_PRICE_POS]) / float(data2[0][CLOSE_PRICE_POS]) for item in data2], 'r-')
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(yearsFmt)
        ax.xaxis.set_minor_locator(months)
        ax.legend(["模型收益率", "单独投资 " + data1_name + " 收益率", "单独投资 " + data2_name + " 收益率"], loc="upper left")
        ax.grid(True)
        ax.set_xlim(dates[0], dates[-1] + timedelta(days=90))
        #plt.xlim(0,len(data1_index)+50)
        plt.show()

    account.dump()

    return account.get_value() / start_money, float(data1[-1][CLOSE_PRICE_POS]) / float(data1[0][CLOSE_PRICE_POS]), float(data2[-1][CLOSE_PRICE_POS]) / float(data2[0][CLOSE_PRICE_POS])


if __name__ == "__main__":

    sh000905_data = load_data("../data/sh000905")
    sh000300_data = load_data("../data/sh000300")

    #test(sh000905_data[-200:-1], sh000300_data[-200:-1], "sh000905", "sh000300", 100000)
    #test(sh000905_data[0:1000], sh000300_data[0:1000], "sh000905", "sh000300", 100000)
    '''
    model_gain_rate, sh000905_gain_rate, sh000300_gain_rate = test(sh000905_data, sh000300_data, u"中证小盘500", u"沪深300", 100000, 28, 4, True)

    print model_gain_rate
    print sh000905_gain_rate
    print sh000300_gain_rate
    '''

    '''
    gain_rates = []

    for i in range(0,5):
        result, tmp, tmp1 = test(sh000905_data, sh000300_data, "sh000905", "sh000300", 100000, 28, i, False)
        print "gap_days:", i, " gain_rates:", result
        gain_rates.append(result)

    print gain_rates

    plt.figure(2)
    plt.title("一周内不同时间轮动的投资收益率")
    plt.plot([1,2,3,4,5], gain_rates, 'r-')
    plt.grid(True)
    plt.show()
    '''

    gain_rates = []

    f = open("./gap_days", "w")

    for i in range(0,60):
        result, tmp, tmp1 = test(sh000905_data, sh000300_data, "sh000905", "sh000300", 100000, i, 4, False)
        print "gap_days:", i, " gain_rates:", result
        gain_rates.append(result)
        f.write(str(result))
        f.write("\n")

    print gain_rates

    plt.figure(2)
    plt.title("不同评估周期的投资收益率")
    plt.plot(range(1,61), gain_rates, 'r-')
    plt.grid(True)
    plt.show()
