#!/usr/bin/env python
#coding=utf-8

import matplotlib.pyplot as plt

DATE_POS = 0
OPEN_PRICE_POS = 1
HIGH_PRICE_POS = 2
CLOSE_PRICE_POS = 3
LOW_PRICE_POS = 4
VOLUMN_POS = 5


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
    print data1[-22]
    print data2[-22]

    data1_close_price = [ item[CLOSE_PRICE_POS] for item in data1 ]
    data2_close_price = [ item[CLOSE_PRICE_POS] for item in data2 ]

    print data1_close_price[-1]
    print data2_close_price[-1]

    plt.plot(data1_close_price, 'b-', data2_close_price, 'r-')
    plt.show()

    return

if __name__ == "__main__":

    sh000905_data = load_data("../data/sh000905_day")
    sh000300_data = load_data("../data/sh000300_day")

    test(sh000905_data, sh000300_data)

