#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append("..")
import matplotlib.pyplot as plt
from model.lundong import lundong
from define import *
from account_simulator import account_simulator
import math

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


def test(data1, data2, data1_name, data2_name, start_money):
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

    plt.figure(1)
    plt.subplot(311)
    plt.plot(data1_close_price, 'b-', data2_close_price, 'r-')
    plt.legend([data1_name, data2_name], loc="upper right")
    plt.grid(True)

    # Initilize a lundong model, and get trading decisions by it
    lundong_model = lundong()

    # the test start with a blank account
    account = account_simulator(start_money)
    money = []

    # record every trading plan
    result = []
    last_valid_trading_plan = {}

    for item in data1:
        trading_plan = lundong_model.get_trading_plan(data1, data2, data1_name, data2_name, item[DATE_POS], 28, last_valid_trading_plan)

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
                choise_0_index.append(i)
            elif item["choise"] == 1:
                choise_1.append(item["data2_up"])
                choise_1_index.append(i)
            elif item["choise"] == 2:
                choise_2.append(0)
                choise_2_index.append(i)

        i = i + 1

    plt.subplot(312)
    plt.plot(range(len(data1_up)), data1_up, 'b-', range(len(data2_up)), data2_up, 'r-',\
        choise_0_index, choise_0, 'bo', choise_1_index, choise_1, 'ro',\
        choise_2_index, choise_2, 'r^')
    #plt.plot(data1_up, 'b-', data2_up, 'r-', choise_0, 'bo', choise_1, 'r^')
    plt.legend([data1_name, data2_name, "switch to:" + data1_name, "switch to:" + data2_name, "sell all"], loc="upper right")
    plt.grid(True)

    plt.subplot(313)
    plt.plot([item / start_money for item in money], 'b-')
    plt.legend(["gain rate"], loc="upper right")
    plt.grid(True)
    plt.show()

    account.dump()

    return

if __name__ == "__main__":

    sh000905_data = load_data("../data/sh000905_day")
    sh000300_data = load_data("../data/sh000300_day")

    #test(sh000905_data[-200:-1], sh000300_data[-200:-1], "sh000905", "sh000300", 100000)
    test(sh000905_data, sh000300_data, "sh000905", "sh000300", 100000)

