#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append("..")
import urllib
import myjson
from  datetime  import  *  
import  time 
from define import *

class lundong(object):
	"""
	28lundong model
	"""

	def get_data(self, dataset, date_str):
		"""
		get stock data by date_str, return a empty list if not exist
		"""
		for item in dataset:
			if item[DATE_POS] == date_str:
				return item
		return []


	def get_trading_plan(self, dataset1, dataset2, dataset1_name, dataset2_name, date_str, days_gap, trading_day, last_valid_trading_plan):
		"""
		get trading plan of 28 lundong model, return a empty map when no decision can be made

		choise:  
			0:	buy data1, sell data2
			1:	sell data1, buy data2
			2:	sell all
			-1:	do not trade
		"""

		result = {}

		# Get stock data by date_str. If not exist, return.
		data1 = self.get_data(dataset1, date_str)
		if data1 == []:
			return {}

		data2 = self.get_data(dataset2, date_str)
		if data2 == []:
			return {}

		# Get the last trading date, at least days_gap days before. If not exist, return.
		date_last = datetime.strptime(date_str, "%Y-%m-%d") - timedelta(days=days_gap)
		last_valid_date = datetime.strptime(dataset1[0][DATE_POS], "%Y-%m-%d")
		data1_last = []
		data2_last = []

		while True:
			date_str_last = date_last.strftime("%Y-%m-%d")
			data1_last = self.get_data(dataset1, date_str_last)
			data2_last = self.get_data(dataset2, date_str_last)

			if data1_last != [] and data2_last != []:
				break
			else:
				date_last = date_last - timedelta(days=1)
				if date_last < last_valid_date:
					return {}

		# Now we have four valid data, get close prices and calculate the rising rate
		data1_close_price = float(data1[CLOSE_PRICE_POS]) 
		data1_close_price_last = float(data1_last[CLOSE_PRICE_POS]) 
		data2_close_price = float(data2[CLOSE_PRICE_POS]) 
		data2_close_price_last = float(data2_last[CLOSE_PRICE_POS]) 

		data1_up = (data1_close_price - data1_close_price_last) / data1_close_price_last
		data2_up = (data2_close_price - data2_close_price_last) / data2_close_price_last

		# Give a initial trading plan according to rising rate
		if data1_up > data2_up:
			if data1_up > 0:
				choise = 0
			else:
				choise = 2
		elif data1_up < data2_up:
			if data2_up > 0:
				choise = 1
			else:
				choise = 2
		else:
			choise = -1

		# if it is not friday, don't trade
		if trading_day < 5:
			if datetime.strptime(date_str, "%Y-%m-%d").weekday() != trading_day:
				choise = -1

		# if the same decision as last time, do not trade
		if last_valid_trading_plan != {} and choise == last_valid_trading_plan["choise"]:
			choise = -1

		# if losing money now, don't trade
		# choise == 0 means buy data1 and sell data2, should decide whether sell data2 will lose money
		"""
		if choise == 0 and account_data2 != None and account_data2.share > 0:
			if data2_close_price < account_data2.mean_price:
				choise = -1
		elif choise == 1 and account_data1 != None and account_data1.share > 0:
			if data1_close_price < account_data1.mean_price:
				choise = -1
		"""

		result["date_str"] = date_str
		result["date_str_last"] = date_str_last
		result["data1_close_price"] = data1_close_price
		result["data1_close_price_last"] = data1_close_price_last
		result["data1_up"] = data1_up
		result["data2_close_price"] = data2_close_price
		result["data2_close_price_last"] = data2_close_price_last
		result["data2_up"] = data2_up
		result["choise"] = choise

		return result


if __name__ == '__main__':
	"""
	#etf500_sohu = 'cn_510500'
	#etf300_sohu = 'cn_510300'
	"""
	etf500_sohu = 'zs_000905'
	etf300_sohu = 'zs_000300'
	
	etf300_sina = 'sh000300'
	etf500_sina = 'sh000905'
	up500, up300 = get_ups(etf500_sina, etf300_sina,etf500_sohu, etf300_sohu)

	if up500 > up300:
		print "Buy 500etf (510500)"
	elif up500 < up300:
		print "Buy 300etf (510300)"
	else:
		print "up500 == up300"


