#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append("..")
import math
import matplotlib.pyplot as plt
from define import *
from account_simulator import account_simulator
from data_interface.stock_dataset import stock_dataset
from tools.data_analyser import data_analyser
from datetime import datetime
from model.turtle import turtle

def test(dataset, dataset_name, start_money):
    """
    turtle model test
    """

    print "Dataset: %s, data_len=%d, start_date=%s, end_date=%s" % (dataset_name, len(dataset.data), dataset.data[0].date, dataset.data[-1].date)

    # get close price

    close_prices = [ item.close_price for item in dataset.data ]

    # calculate other data
    analyser = data_analyser()
    mean_price_10 = analyser.calcu_mean_line(close_prices, 10)
    mean_price_100 = analyser.calcu_mean_line(close_prices, 100)
    max_price_50 = analyser.calcu_max_line(close_prices, 50)
    min_price_50 = analyser.calcu_min_line(close_prices, 50)
    min_price_25 = analyser.calcu_min_line(close_prices, 25)

    # Initilize a lundong model, and get trading decisions by it
    turtle_model = turtle()

    model_results = []

    for item in dataset.data:
        model_results.append(turtle_model.get_trading_plan(dataset, item.date))

    test_data = [ item["close_price"] for item in model_results ]
    test_data = test_data[99:]

    buy = []
    buy_index = []

    sell_half = []
    sell_half_index = []

    sell_all = []
    sell_all_index = []

    for i in range(len(model_results)):
        if model_results[i]["choise"] == 4:
            buy.append(model_results[i]["close_price"])
            buy_index.append(i)
        elif model_results[i]["choise"] == 0:
            sell_all.append(model_results[i]["close_price"])
            sell_all_index.append(i)
        elif model_results[i]["choise"] == 1:
            sell_half.append(model_results[i]["close_price"])
            sell_half_index.append(i)

    # trunk invalid data
    close_prices = close_prices[99:]
    mean_price_10 = mean_price_10[99:]
    mean_price_100 = mean_price_100[99:]
    max_price_50 = max_price_50[99:]
    min_price_50 = min_price_50[99:]
    min_price_25 = min_price_25[99:]

    buy_index = [ num - 99 for num in buy_index]
    sell_half_index = [ num - 99 for num in sell_half_index]
    sell_all_index = [ num - 99 for num in sell_all_index]

    plt.figure(1)
    #plt.subplot(311)
    #plt.plot(close_prices, 'b-', mean_price_10, 'g-', mean_price_100, 'r-', max_price_50, 'c-', min_price_50, 'm-', min_price_25, 'y-', test_data, 'go')
    #plt.legend([dataset_name, "10 hour mean", "100 hour mean", "50 max price", '50 min price', '25 min price', 'test_data'], loc="upper left")

    plt.plot(close_prices, 'b-', mean_price_10, 'g-', mean_price_100, 'r-', max_price_50, 'c-', min_price_50, 'm-', min_price_25, 'y-', buy_index, buy, 'ro', sell_all_index, sell_all, 'go', sell_half_index, sell_half, 'g^')
    plt.legend([dataset_name, "10 hour mean", "100 hour mean", "50 max price", '50 min price', '25 min price', 'buy', 'sell_all', 'sell_half'], loc="upper left")
    plt.grid(True)

    plt.show()

    return

if __name__ == "__main__":

    sh000300_data = stock_dataset()
    sh000300_data.load_from_file("sh000300", "../data/sh000300_hour")

    test(sh000300_data, "sh000300", 100000)
