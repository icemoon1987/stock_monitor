#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append("..")
import matplotlib.pyplot as plt
from model.lundong import lundong
from define import *

def load_data(file_path):
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

    i = 0
    while i < len(data1):
        date_str1 = data1[i][0]
        flag = False

        for item2 in data2:
            date_str2 = item2[0]
            if date_str1 == date_str2:
                flag = True
                break

        if not flag:
            del data1[i]
        else:
            i = i + 1

    i = 0
    while i < len(data2):
        date_str2 = data2[i][0]
        flag = False

        for item1 in data1:
            date_str1 = item1[0]
            if date_str2 == date_str1:
                flag = True
                break

        if not flag:
            del data2[i]
        else:
            i = i + 1

    return


def test(data1, data2):

    pre_process(data1, data2)

    print len(data1), len(data2)
    print data1[0]
    print data2[0]
    print data1[-1]
    print data2[-1]

    data1_close_price = [ item[CLOSE_PRICE_POS] for item in data1 ]
    data2_close_price = [ item[CLOSE_PRICE_POS] for item in data2 ]

    print data1_close_price[-1]
    print data2_close_price[-1]

    plt.figure(1)
    plt.subplot(311)
    plt.plot(data1_close_price, 'b-', data2_close_price, 'r-')
    plt.legend(["sh000905", "sh000300"], "upper right")
    #plt.show()

    lundong_model = lundong()

    result = []
    trading_status = {  "data1": { "price": 0.0, "amount": 0},
                        "data2": { "price": 0.0, "amount": 0}
    }

    costs = []
    gains = []

    for item in data1:
        tmp = lundong_model.get_result(data1, data2, item[DATE_POS], trading_status)
        if tmp != {}:
            if tmp["choise"] == 0:
                costs.append(tmp["data1_close_price"] + costs[-1])

                if trading_status["data2"]["amount"] == 1:
                    gains.append(tmp["data2_close_price"] + gains[-1])
                else:
                    gains.append(gains[-1])

                trading_status["data1"]["price"] = tmp["data1_close_price"]
                trading_status["data1"]["amount"] = trading_status["data1"]["amount"] + 1
                trading_status["data2"]["price"] = 0
                if trading_status["data2"]["amount"] == 1:
                    trading_status["data2"]["amount"] = trading_status["data2"]["amount"] - 1

            elif tmp["choise"] == 1:
                costs.append(tmp["data2_close_price"] + costs[-1])
                if trading_status["data1"]["amount"] == 1:
                    gains.append(tmp["data1_close_price"] + gains[-1])
                else:
                    gains.append(gains[-1])

                trading_status["data1"]["price"] = 0
                if trading_status["data1"]["amount"] == 1:
                    trading_status["data1"]["amount"] = trading_status["data1"]["amount"] - 1
                trading_status["data2"]["price"] = tmp["data2_close_price"]
                trading_status["data2"]["amount"] = trading_status["data2"]["amount"] + 1
            else:
                costs.append(costs[-1])
                gains.append(gains[-1])

        else:
            if len(costs) == 0:
                costs.append(0)
                continue
            if len(gains) == 0:
                gains.append(0)
                continue
            costs.append(costs[-1])
            gains.append(gains[-1])

        result.append(tmp)

    data1_up = []
    data2_up = []
    data1_choise = []
    data2_choise = []

    for item in result:
        if item == {}:
            data1_up.append(0.0)
            data2_up.append(0.0)
            data1_choise.append(0)
            data2_choise.append(0)
        else:
            data1_up.append(item["data1_up"])
            data2_up.append(item["data2_up"])

            if item["choise"] == 0:
                data1_choise.append(item["data1_up"])
                data2_choise.append(0)
            elif item["choise"] == 1:
                data1_choise.append(0)
                data2_choise.append(item["data2_up"])
            else:
                data1_choise.append(0)
                data2_choise.append(0)

    plt.subplot(312)
    plt.plot(data1_up, 'b-', data2_up, 'r-', data1_choise, 'bo', data2_choise, 'ro')
    plt.legend(["sh000905", "sh000300", "sh000905", "sh000300"], "upper right")

    plt.subplot(313)
    plt.plot(costs, 'b-', gains, 'r-')
    plt.legend(["costs", "gains",], "upper right")
    plt.show()

    print costs[-1]
    print gains[-1]

    return

if __name__ == "__main__":

    sh000905_data = load_data("../data/sh000905_day")
    sh000300_data = load_data("../data/sh000300_day")

    test(sh000905_data, sh000300_data)

