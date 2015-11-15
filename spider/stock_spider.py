#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append("..")
from datetime import datetime, timedelta
import time 
from data_interface.stock_dataset import stock_dataset
from data_interface.stock_data import stock_data
from data_fetcher.stock_fetcher import stock_fetcher


class stock_spider(object):

    def __init__(self):
        return

    def refresh_his_day_file(self, stockid, days_num, file_name):
        fetcher = stock_fetcher()
        old_dataset = stock_dataset()
        new_data_list = []

        old_dataset.load_from_file(stockid, file_name)
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=days_num)).strftime("%Y%m%d")

        new_dataset = fetcher.get_his_day_k(stockid, start_date, end_date)

        for item in new_dataset.data:
            if old_dataset.get_data(item.date) == None:
                new_data_list.append(item)

        old_dataset.append_to_file(file_name, new_data_list)

        return

if __name__ == "__main__":

    if len(sys.argv) != 4:
        print "Usage: python stock_spider STOCK_ID DAYS_NUM FILE"
    else:

        stock_id = sys.argv[1]
        days_num = int(sys.argv[2])
        file_name = sys.argv[3]

        spider = stock_spider()
        spider.refresh_his_day_file(stock_id, days_num, file_name)

