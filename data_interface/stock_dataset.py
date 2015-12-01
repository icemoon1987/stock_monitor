#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append("..")
from define import *
from stock_data import stock_data

class stock_dataset(object):

    def __init__(self):
        self.name = ""
        self.data = []

        return

    def load_from_file(self, data_name, file_name, delim=","):

        self.name = data_name
        f = open(file_name, "r")

        for line in f:
            stock = stock_data()
            stock.parse_from_str(line, delim)
            self.data.append(stock)

        f.close()

        return

    def get_data(self, date_str):
        for item in self.data:
            if item.date == date_str:
                return item
        return None

    def get_data_index(self, date_str):
        for i in range(len(self.data)):
            if self.data[i].date == date_str:
                return i
        return None

    def store_to_file(self, file_name):

        f = open(file_name, "w")
        for item in self.data:
            f.write(str(item))
        f.close()
        return

    def append_to_file(self, file_name, data_list):

        f = open(file_name, "a")
        for item in data_list:
            f.write(str(item))
        f.close()
        return

    def dump(self):

        print "name = " + self.name + "\n"

        for item in self.data:
            print str(item),

        return

if __name__ == "__main__":

    stock_set = stock_dataset()

    stock_set.load_from_file("sh000300", "../data/sh000300")
    #stock_set.dump()

    print stock_set.get_data("2015-10-20")
    print stock_set.get_data("2015-10-19")
    print stock_set.get_data("2000-10-19")

    print stock_set.get_data_index("2015-10-20")
    print stock_set.get_data_index("2015-10-19")
    print stock_set.get_data_index("2000-10-19")

    #stock_set.store_to_file("./tmp")
    #stock_set.append_to_file("./tmp", stock_set.data)

